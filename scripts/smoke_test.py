"""Smoke test for DA-TDMPC2. Owner: M1 · tiny mode: T001 · full mode: T006 + T101.

Modes
-----
tiny  Random *tiny* multitask TD-MPC2 world model (upstream ``WorldModel`` class) on CPU +
      a real DMControl env (upstream ``envs.make_env``). Runs ``--steps`` nominal steps, then
      scales the body masses by the ``--shift mass:<k>`` factor, asserts the MuJoCo parameter
      actually changed, runs ``--steps`` more steps, and prints sec/step. No checkpoint needed;
      this is what CI runs.
full  Loads the checkpoint through the T006 harness and runs a nominal and a perturbed
      ``--steps``-step rollout with MPPI (available once T006 and T101 are merged).
auto  (default) full if the checkpoint exists and the harness is implemented, else tiny with
      a printed notice.

Numbers printed here are for debugging only - never cite them in docs or the report.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

try:
    import datdmpc  # noqa: F401
except ImportError:  # package not installed with `pip install -e .` yet
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from datdmpc import _upstream


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mode", choices=["auto", "tiny", "full"], default="auto")
    p.add_argument("--ckpt", default="checkpoints/mt30-5M.pt", help="checkpoint for full mode")
    p.add_argument("--task", default="walker-walk", help="DMControl task (mt30 name)")
    p.add_argument("--steps", type=int, default=50, help="agent steps per rollout")
    p.add_argument("--shift", default="mass:1.5", help="tiny mode supports mass:<k> only")
    p.add_argument("--seed", type=int, default=0)
    return p


def _parse_mass_shift(spec: str) -> float:
    kind, _, level = spec.partition(":")
    if kind != "mass" or not level:
        raise SystemExit(f"tiny mode only supports --shift mass:<k>, got {spec!r}")
    return float(level)


def run_tiny(task: str, steps: int, shift: str, seed: int) -> dict:
    """Tiny-model smoke test. Returns timing figures (debug only)."""
    factor = _parse_mass_shift(shift)
    _upstream.configure_rendering(render=False)
    _upstream.ensure_upstream_on_path()

    import numpy as np
    import torch

    torch.manual_seed(seed)
    np.random.seed(seed)
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))

    from envs import make_env  # upstream: tdmpc2/envs/__init__.py

    env_cfg = _upstream.UpstreamCfg(task=task, obs="state", seed=seed, multitask=False)
    env = make_env(env_cfg)
    obs_dim = int(env.observation_space.shape[0])
    act_dim = int(env.action_space.shape[0])

    cfg = _upstream.make_tiny_cfg(obs_dim=obs_dim, action_dim=act_dim, tasks=(task, "tiny-placeholder"))
    model = _upstream.build_world_model(cfg, device="cpu")
    task_idx = torch.tensor([0])

    from common.math import two_hot_inv  # upstream: tdmpc2/common/math.py

    def rollout(n: int, expected_mass=None) -> float:
        obs = env.reset()
        if expected_mass is not None:  # dm_control's reset must not undo a physics edit
            assert np.allclose(physics.model.body_mass, expected_mass), "reset reverted the mass edit"
        t0 = time.perf_counter()
        for _ in range(n):
            with torch.no_grad():
                z = model.encode(obs.unsqueeze(0), task_idx)
                action, _ = model.pi(z, task_idx)
                z_next = model.next(z, action, task_idx)
                r_hat = two_hot_inv(model.reward(z, action, task_idx), cfg)
                q_all = model.Q(z, action, task_idx, return_type="all")
            assert z.shape == (1, cfg.latent_dim) and z_next.shape == z.shape
            assert r_hat.shape == (1, 1) and q_all.shape[0] == cfg.num_q
            obs, _, done, _ = env.step(action[0])
            if done:
                obs = env.reset()
        return (time.perf_counter() - t0) / n

    physics = _upstream.unwrap_dm_env(env).physics

    # Nominal rollout.
    sec_nominal = rollout(steps)

    # Perturbed rollout: scale all body masses (body 0 is the static world body).
    original = physics.model.body_mass.copy()
    physics.model.body_mass[1:] = original[1:] * factor
    changed = physics.model.body_mass.copy()
    assert np.allclose(changed[1:], original[1:] * factor), "body_mass was not scaled"
    assert factor == 1.0 or not np.allclose(changed[1:], original[1:]), "body_mass did not change"
    sec_perturbed = rollout(steps, expected_mass=changed)
    physics.model.body_mass[:] = original

    # Embedding norm constraint (nn.Embedding(max_norm=1)) holds after lookup.
    emb_norm = float(model._task_emb(task_idx).norm())
    assert emb_norm <= 1.0 + 1e-5, f"task embedding norm {emb_norm} > 1"

    return {
        "mode": "tiny",
        "task": task,
        "obs_dim": obs_dim,
        "action_dim": act_dim,
        "tiny_model_params": int(model.total_params),
        "mass_factor": factor,
        "sec_per_step_nominal": sec_nominal,
        "sec_per_step_perturbed": sec_perturbed,
        "mujoco_gl": os.environ.get("MUJOCO_GL", ""),
    }


def run_full(ckpt: str, task: str, steps: int, shift: str, seed: int) -> dict:
    from datdmpc.eval import harness

    return harness.run_smoke(ckpt=ckpt, task=task, steps=steps, shift=shift, seed=seed)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    t_start = time.perf_counter()
    mode = args.mode
    if mode in ("auto", "full"):
        reason = None
        if not Path(args.ckpt).is_file():
            reason = f"checkpoint {args.ckpt} not found (run scripts/get_checkpoints.py, task T005)"
        else:
            try:
                result = run_full(args.ckpt, args.task, args.steps, args.shift, args.seed)
            except NotImplementedError as exc:
                reason = f"full mode not implemented yet ({exc})"
        if reason is not None:
            if mode == "full":
                print(f"[smoke] FAILED: {reason}", file=sys.stderr)
                return 1
            print(f"[smoke] full mode unavailable: {reason} -> running tiny mode instead")
            mode = "tiny"
    if mode == "tiny":
        result = run_tiny(args.task, args.steps, args.shift, args.seed)
    for key, value in result.items():
        print(f"[smoke] {key}: {value}")
    print(f"[smoke] total wall time: {time.perf_counter() - t_start:.1f} s")
    print("[smoke] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
