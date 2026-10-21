"""Regenerate every report figure from results/REGISTRY.csv. Owner: M1 · Task: T501 (stub from T001).

Writes PNG + PDF (each < 2 MB) to figures/. Figures are GENERATED - never edit by hand.
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
    p.add_argument("--registry", default="results/REGISTRY.csv")
    p.add_argument("--out", default="figures")
    return p


def main(argv=None) -> int:
    build_parser().parse_args(argv)
    return not_implemented("scripts/make_figures.py", "T501", "M1")


if __name__ == "__main__":
    raise SystemExit(main())
