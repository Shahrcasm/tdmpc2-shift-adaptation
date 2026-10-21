"""Test-time adaptation runs: Ours-C2 (e_only) and baselines B1-B3. Owner: M2 · Tasks: T202-T204 (stub from T001).

Methods: e_only = Ours-C2 (adapt only the 64-d task embedding), e_ln = G2 fallback (embedding
+ LayerNorm affine parameters), rand_e = B3 (random e, then adapt), full_ft = B1 (all
parameters), partial_ft = B2 (reward + Q heads). All methods see the same K transitions.
Saves adapted_embedding.json in each run folder for e-based methods.
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
    p.add_argument("--ckpt", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--shift", required=True, help="<type>:<level>, e.g. friction:0.5")
    p.add_argument("--method", choices=["e_only", "e_ln", "rand_e", "full_ft", "partial_ft"], required=True)
    p.add_argument("--K", type=int, required=True, help="number of recent transitions used for adaptation")
    p.add_argument("--grad-steps", type=int, required=True)
    p.add_argument("--lr", type=float, required=True)
    seeds = p.add_mutually_exclusive_group(required=True)
    seeds.add_argument("--seed", type=int)
    seeds.add_argument("--seeds", type=int, nargs="+")
    p.add_argument("--episodes", type=int, required=True, help="evaluation episodes after adaptation")
    p.add_argument("--out", required=True, help="e.g. results/P2_adapt/")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--shard", default=None, help="i/N (1-based)")
    p.add_argument("--tier", choices=["T0", "T1", "T1b"], default="T0")
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    return p


def main(argv=None) -> int:
    build_parser().parse_args(argv)
    return not_implemented("scripts/adapt.py", "T202-T204", "M2")


if __name__ == "__main__":
    raise SystemExit(main())
