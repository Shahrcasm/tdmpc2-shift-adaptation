"""Bridge to the vendored upstream TD-MPC2 code (owner: M1, created in T001).

Upstream modules import each other as top-level packages (``from common import ...``,
``from envs import ...``), so ``third_party/tdmpc2/tdmpc2`` must be on ``sys.path``.
This module is the single place that

* puts the vendored upstream package on ``sys.path`` (:func:`ensure_upstream_on_path`),
* decides the MuJoCo rendering backend before ``mujoco``/``dm_control`` are imported
  (:func:`configure_rendering`), and
* builds small randomly initialised world models for CPU smoke tests and CI
  (:func:`make_tiny_cfg`, :func:`build_world_model`).

Never edit files under ``third_party/``; extend upstream behaviour by subclassing or
wrapping from ``src/datdmpc/``.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_ROOT = REPO_ROOT / "third_party" / "tdmpc2"
UPSTREAM_PKG_DIR = UPSTREAM_ROOT / "tdmpc2"
UPSTREAM_COMMIT = "e9f59321933cbc8e11a002b842adc7d4ffae8ff1"

# Values of MUJOCO_GL that turn rendering off in both `mujoco` and `dm_control`.
RENDERING_OFF = "disable"


def ensure_upstream_on_path() -> Path:
    """Prepend the vendored upstream package directory to ``sys.path`` (idempotent)."""
    if not UPSTREAM_PKG_DIR.is_dir():
        raise FileNotFoundError(
            f"Vendored upstream not found at {UPSTREAM_PKG_DIR}. "
            "See third_party/tdmpc2/UPSTREAM_COMMIT.txt."
        )
    path = str(UPSTREAM_PKG_DIR)
    if path not in sys.path:
        sys.path.insert(0, path)
    return UPSTREAM_PKG_DIR


def configure_rendering(render: bool = False) -> str:
    """Choose the MuJoCo GL backend. Must run before ``mujoco``/``dm_control`` are imported.

    * If the user already set ``MUJOCO_GL``, it is respected unchanged.
    * ``render=False`` (laptops, CI, all evaluation runs): rendering is disabled. Physics
      stepping never needs an OpenGL context.
    * ``render=True`` on Linux (Colab GPU runtime, for videos only): ``egl``.
      On Windows the default backend is used (``egl``/``osmesa`` are Linux-only).

    Returns the value in effect ("" means: library default).
    """
    if "MUJOCO_GL" in os.environ:
        return os.environ["MUJOCO_GL"]
    if not render:
        os.environ["MUJOCO_GL"] = RENDERING_OFF
    elif sys.platform.startswith("linux"):
        os.environ["MUJOCO_GL"] = "egl"
    return os.environ.get("MUJOCO_GL", "")


def mt30_tasks() -> list[str]:
    """The 30 mt30 task names in upstream index order (index = task embedding row)."""
    ensure_upstream_on_path()
    from common import TASK_SET  # upstream: tdmpc2/common/__init__.py

    return list(TASK_SET["mt30"])


class UpstreamCfg(SimpleNamespace):
    """Attribute container with the ``.get`` method that upstream code expects from its config."""

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


def make_tiny_cfg(
    obs_dim: int,
    action_dim: int,
    tasks: Sequence[str] = ("tiny-task-a", "tiny-task-b"),
    action_dims: Sequence[int] | None = None,
    task_dim: int = 8,
) -> UpstreamCfg:
    """Config for a *tiny* multitask world model (random weights; smoke tests and CI only).

    Field names follow upstream ``tdmpc2/config.yaml``; widths are deliberately tiny so the
    model builds in milliseconds on any CPU. Planning settings are irrelevant here — the
    tiny model is never used to report results.
    """
    tasks = list(tasks)
    if action_dims is None:
        action_dims = [action_dim] * len(tasks)
    num_bins, vmin, vmax = 101, -10.0, 10.0
    return UpstreamCfg(
        # task / observation
        task="tiny",
        tasks=tasks,
        multitask=True,
        obs="state",
        obs_shape={"state": (obs_dim,)},
        action_dim=action_dim,
        action_dims=list(action_dims),
        episodic=False,
        # architecture (tiny)
        task_dim=task_dim,
        num_enc_layers=2,
        enc_dim=32,
        mlp_dim=32,
        latent_dim=32,  # must be divisible by simnorm_dim
        simnorm_dim=8,
        num_channels=8,
        num_q=2,  # upstream Q(return_type='min'/'avg') subsamples 2 heads
        dropout=0.01,
        # actor / critic (upstream defaults)
        log_std_min=-10,
        log_std_max=2,
        num_bins=num_bins,
        vmin=vmin,
        vmax=vmax,
        bin_size=(vmax - vmin) / (num_bins - 1),
        tau=0.01,
    )


def build_world_model(cfg: UpstreamCfg, device: str = "cpu"):
    """Instantiate upstream ``WorldModel`` on ``device`` (no CUDA assumption)."""
    ensure_upstream_on_path()
    from common.world_model import WorldModel  # upstream: tdmpc2/common/world_model.py

    model = WorldModel(cfg).to(device)
    model.eval()
    return model


def unwrap_dm_env(env):
    """Return the innermost dm_control environment (the object that has ``.physics``)."""
    seen = 0
    while not hasattr(env, "physics"):
        if seen > 20:
            raise AttributeError("Could not find a dm_control environment with `.physics`.")
        nxt = getattr(env, "unwrapped", None)
        if nxt is None or nxt is env:
            nxt = getattr(env, "env", None)
        if nxt is None:
            raise AttributeError("Could not find a dm_control environment with `.physics`.")
        env = nxt
        seen += 1
    return env
