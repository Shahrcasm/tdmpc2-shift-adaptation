"""Test-time adaptation runner for DA-TDMPC2 (Single Novelty: e_only).

Under physical dynamics shift, adapts the 64-dimensional task embedding
using K transitions from the shifted environment and evaluates the adapted agent.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Bridge to src
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root / "src"))

import torch

from datdmpc.adapt.embedding import adapt_embedding
from datdmpc.eval.harness import MT30_TASKS, load_agent, make_task_env, evaluate
from datdmpc.eval.logging import RunLogger, make_run_id


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ckpt", default="checkpoints/mt30-5M.pt", help="Path to checkpoint")
    p.add_argument("--task", default="walker-walk", help="MT30 task name")
    p.add_argument("--shift", default="mass:1.5", help="<type>:<level>, e.g. mass:1.5 or friction:0.5")
    p.add_argument("--method", choices=["e_only"], default="e_only", help="Our single novelty: e_only adaptation")
    p.add_argument("--K", type=int, default=50, help="Number of recent transitions used for adaptation")
    p.add_argument("--grad-steps", type=int, default=15, help="Gradient steps on embedding")
    p.add_argument("--lr", type=float, default=0.002, help="Learning rate for Adam")
    seeds = p.add_mutually_exclusive_group(required=False)
    seeds.add_argument("--seed", type=int, default=0)
    seeds.add_argument("--seeds", type=int, nargs="+")
    p.add_argument("--episodes", type=int, default=1, help="Evaluation episodes after adaptation")
    p.add_argument("--out", default="results/P2_adapt/", help="Output directory")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--shard", default=None, help="i/N (1-based)")
    p.add_argument("--tier", choices=["T0", "T1", "T1b"], default="T0")
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    return p


def collect_k_transitions(agent, task: str, shift: str, K: int, seed: int, task_idx: int):
    """Collect K transition steps in the shifted environment."""
    env = make_task_env(task, seed=seed, shift=shift)
    obs_list = []
    act_list = []
    next_obs_list = []
    r_list = []

    obs = env.reset()
    for step_idx in range(K):
        is_first_step = False
        if step_idx == 0:
            is_first_step = True

        with torch.no_grad():
            action = agent.act(obs, t0=is_first_step, task=task_idx)
        next_obs, reward, done, _ = env.step(action)

        obs_list.append(obs.cpu().clone())
        act_list.append(action.cpu().clone())
        next_obs_list.append(next_obs.cpu().clone())
        r_list.append(reward)

        obs = next_obs
        if done:
            obs = env.reset()

    return {
        "obs": torch.stack(obs_list),
        "action": torch.stack(act_list),
        "next_obs": torch.stack(next_obs_list),
        "reward": torch.tensor(r_list, dtype=torch.float32),
    }


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.seeds is not None:
        seed_list = args.seeds
    else:
        seed_list = [args.seed]

    task_idx = MT30_TASKS.index(args.task)

    print(f"[adapt] Loading agent from {args.ckpt} on {args.device}...")
    agent = load_agent(args.ckpt, device=args.device)

    for seed in seed_list:
        run_id = make_run_id(
            ckpt_path=args.ckpt,
            task=args.task,
            shift_spec=args.shift,
            method="e_only",
            seed=seed,
        )
        run_dir = Path(args.out) / run_id
        logger = RunLogger(out_dir=run_dir, run_id=run_id, config=vars(args), resume=args.resume)

        if logger.is_complete(args.episodes):
            print(f"[adapt] Run {run_id} already complete. Skipping.")
            continue

        print(f"[adapt] Step 1: Collecting {args.K} transitions under {args.shift} (seed={seed})...")
        transitions = collect_k_transitions(agent, args.task, args.shift, args.K, seed, task_idx)

        print(f"[adapt] Step 2: Optimizing 64-dim embedding via {args.grad_steps} gradient steps...")
        adapt_res = adapt_embedding(
            agent=agent,
            transitions=transitions,
            task_idx=task_idx,
            grad_steps=args.grad_steps,
            lr=args.lr,
        )
        print(f"[adapt] Loss: {adapt_res['initial_loss']:.6f} -> {adapt_res['final_loss']:.6f}")

        # Save adapted embedding
        adapted_path = run_dir / "adapted_embedding.json"
        with open(adapted_path, "w", encoding="utf-8") as f:
            json.dump(adapt_res["adapted_embedding"].tolist(), f)

        print(f"[adapt] Step 3: Evaluating adapted agent for {args.episodes} episodes...")
        eval_res = evaluate(
            agent=agent,
            task=args.task,
            episodes=args.episodes,
            seed=seed,
            shift=args.shift,
            logger=logger,
            tier=args.tier,
        )
        print(f"[adapt] Mean return after adaptation: {eval_res['mean_return']:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
