"""Evaluate the frozen model (method B0) on one or all mt30 tasks, nominal or shifted.
Owner: M1 · Task: T006. Used by T007 (nominal) and T103 (degradation).

Writes results/<phase>_<exp>/<run_id>/{config.yaml, episodes.csv, summary.json, env.txt, git_sha.txt}.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

try:
    import datdmpc  # noqa: F401
except ImportError:  # package not installed with `pip install -e .` yet
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from datdmpc.eval.harness import (
    MT30_TASKS,
    build_mt30_cfg,
    evaluate,
    infer_model_size,
    load_agent,
)
from datdmpc.eval.logging import RunLogger, make_run_id


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ckpt", required=True, help="e.g. checkpoints/mt30-19M.pt")
    p.add_argument(
        "--model-size",
        type=int,
        choices=[5, 19],
        default=None,
        help="inferred from the checkpoint filename if omitted",
    )
    p.add_argument("--task", required=True, help="mt30 task name, or 'all' for all 30 tasks")
    shift = p.add_mutually_exclusive_group()
    shift.add_argument("--shift", default="none", help="'none' or <type>:<level>, e.g. mass:1.5")
    shift.add_argument("--shifts-from", default=None, help="configs/shifts.yaml")
    p.add_argument("--split", choices=["dev", "test", "all"], default=None, help="with --shifts-from")
    p.add_argument("--episodes", type=int, required=True)
    seeds = p.add_mutually_exclusive_group(required=True)
    seeds.add_argument("--seed", type=int)
    seeds.add_argument("--seeds", type=int, nargs="+")
    p.add_argument("--out", required=True, help="phase folder, e.g. results/P0_nominal/ or outputs/debug/")
    p.add_argument("--resume", action="store_true", help="skip episodes already in episodes.csv")
    p.add_argument("--shard", default=None, help="i/N (1-based), e.g. 2/3")
    p.add_argument("--tier", choices=["T0", "T1", "T1b"], default="T0")
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    p.add_argument("--max-steps", type=int, default=None, help="limit steps per episode (for laptop CPU debugging)")
    return p


def partition_shards(items: Sequence[str], shard_spec: str | None) -> list[str]:
    """Filter items using 1-based i/N shard specification."""
    if not shard_spec:
        return list(items)

    i_str, separator, n_str = shard_spec.partition("/")
    i = int(i_str)
    n = int(n_str)
    if not (1 <= i <= n):
        raise ValueError(f"Invalid shard {shard_spec!r}; must satisfy 1 <= i <= N")

    selected = []
    for index, item in enumerate(items):
        if index % n == (i - 1):
            selected.append(item)
    return selected


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    model_size = infer_model_size(args.ckpt, args.model_size)

    if args.seed is not None:
        seeds = [args.seed]
    else:
        seeds = list(args.seeds)

    if args.task == "all":
        tasks = list(MT30_TASKS)
    else:
        if args.task not in MT30_TASKS:
            raise ValueError(f"Unknown task {args.task!r}. Valid mt30 tasks: {MT30_TASKS}")
        tasks = [args.task]

    # Apply sharding
    tasks = partition_shards(tasks, args.shard)
    if not tasks:
        print(f"[eval] No tasks assigned to shard {args.shard}.")
        return 0

    # Resolve shifts
    if args.shifts_from:
        import yaml
        with open(args.shifts_from, "r", encoding="utf-8") as f:
            shifts_cfg = yaml.safe_load(f)
        # T102 format: shifts list or dict
        shifts = shifts_cfg.get("shifts", ["none"])
    else:
        shifts = [args.shift]

    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)

    print(f"[eval] Loading agent from {args.ckpt} (size={model_size}M, device={args.device})...")
    agent = load_agent(args.ckpt, model_size=model_size, device=args.device)

    for task in tasks:
        for shift in shifts:
            for seed in seeds:
                run_id = make_run_id(
                    ckpt=args.ckpt,
                    task=task,
                    shift=shift,
                    method="B0",
                    seed=seed,
                )
                resolved_cfg = vars(args).copy()
                resolved_cfg["resolved_task"] = task
                resolved_cfg["resolved_shift"] = shift
                resolved_cfg["resolved_seed"] = seed

                logger = RunLogger(
                    out_dir=out_root,
                    run_id=run_id,
                    config=resolved_cfg,
                    tier=args.tier,
                    device=args.device,
                    shard=args.shard,
                    resume=args.resume,
                )

                if len(logger.completed_episodes) >= args.episodes:
                    print(f"[eval] {run_id}: already has {len(logger.completed_episodes)}/{args.episodes} episodes. Skipping.")
                    continue

                print(f"[eval] Starting {run_id} ({args.episodes} episodes, tier={args.tier})...")
                res = evaluate(
                    agent=agent,
                    task=task,
                    episodes=args.episodes,
                    seed=seed,
                    shift=shift,
                    logger=logger,
                    tier=args.tier,
                    shard=args.shard,
                    max_steps=args.max_steps,
                )

                summary = logger.finish()
                print(f"[eval] Finished {run_id}: mean return = {summary['mean_return']:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
