"""Evaluate the frozen model (method B0) on one or all mt30 tasks, nominal or shifted.
Owner: M1 · Task: T006 (stub created in T001). Used by T007 (nominal) and T103 (degradation).

Writes results/<phase>_<exp>/<run_id>/{config.yaml, episodes.csv, summary.json, env.txt, git_sha.txt}.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import datdmpc  # noqa: F401
except ImportError:  # package not installed with `pip install -e .` yet
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from datdmpc import not_implemented


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ckpt", required=True, help="e.g. checkpoints/mt30-19M.pt")
    p.add_argument("--model-size", type=int, choices=[5, 19], default=None,
                   help="inferred from the checkpoint filename if omitted")
    p.add_argument("--task", required=True, help="mt30 task name, or 'all' for all 30 tasks")
    shift = p.add_mutually_exclusive_group()
    shift.add_argument("--shift", default="none", help="'none' or <type>:<level>, e.g. mass:1.5")
    shift.add_argument("--shifts-from", default=None, help="configs/shifts.yaml")
    p.add_argument("--split", choices=["dev", "test", "all"], default=None, help="with --shifts-from")
    p.add_argument("--episodes", type=int, required=True)
    seeds = p.add_mutually_exclusive_group(required=True)
    seeds.add_argument("--seed", type=int)
    seeds.add_argument("--seeds", type=int, nargs="+")
    p.add_argument("--out", required=True, help="phase folder, e.g. results/P1_degradation/")
    p.add_argument("--resume", action="store_true", help="skip episodes already in episodes.csv")
    p.add_argument("--shard", default=None, help="i/N (1-based), e.g. 2/3")
    p.add_argument("--tier", choices=["T0", "T1", "T1b"], default="T0")
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    return p


def main(argv=None) -> int:
    build_parser().parse_args(argv)
    return not_implemented("scripts/eval.py", "T006", "M1")


if __name__ == "__main__":
    raise SystemExit(main())
