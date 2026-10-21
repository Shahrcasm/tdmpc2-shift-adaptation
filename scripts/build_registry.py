"""Build results/REGISTRY.csv from every results/*/*/summary.json + config.yaml. Owner: M1 · Task: T501 (stub from T001).

Reads results/ only; never edits run folders. REGISTRY.csv is GENERATED - do not edit by hand.
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
    p.add_argument("--results", default="results")
    p.add_argument("--out", default="results/REGISTRY.csv")
    return p


def main(argv=None) -> int:
    build_parser().parse_args(argv)
    return not_implemented("scripts/build_registry.py", "T501", "M1")


if __name__ == "__main__":
    raise SystemExit(main())
