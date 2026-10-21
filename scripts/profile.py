"""Measure planning sec/decision and adaptation sec/gradient-step. Owner: M3 · Task: T008 (stub from T001).

Run on each tier (T0 laptop CPU, Colab CPU, Colab GPU) -> results/P0_profile/. These measurements
set every compute budget in the task cards.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# NOTE: this file shares its name with the standard-library module `profile` (the layout
# requires the name). Importing `datdmpc` FIRST removes scripts/ from sys.path (see
# src/datdmpc/__init__.py), so `import torch` -> cProfile -> `import profile` finds the stdlib
# module. Keep `import datdmpc` above every other heavy import in this file.
try:
    import datdmpc  # noqa: F401
except ImportError:  # package not installed with `pip install -e .` yet
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from datdmpc import not_implemented


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ckpt", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--what", choices=["plan", "adapt", "all"], default="all")
    p.add_argument("--steps", type=int, required=True, help="timed decisions / gradient steps")
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    p.add_argument("--tier", choices=["T0", "T1", "T1b"], default="T0")
    p.add_argument("--out", required=True, help="results/P0_profile/")
    return p


def main(argv=None) -> int:
    build_parser().parse_args(argv)
    return not_implemented("scripts/profile.py", "T008", "M3")


if __name__ == "__main__":
    raise SystemExit(main())
