"""Download released TD-MPC2 multitask checkpoints and verify them. Owner: M1 · Task: T005 (stub from T001).

Source: https://huggingface.co/nicklashansen/tdmpc2/resolve/main/multitask/<name>.pt
Writes/updates checkpoints/MANIFEST.csv with columns name,size_bytes,sha256,url and verifies
every file's sha256 against the value published by Hugging Face (see docs/RUNS.md).
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
    p.add_argument("--models", nargs="+", required=True, help="e.g. mt30-5M mt30-19M")
    p.add_argument("--dest", default="checkpoints", help="download folder (gitignored)")
    p.add_argument("--verify-only", action="store_true", help="only re-check sha256 of existing files")
    return p


def main(argv=None) -> int:
    build_parser().parse_args(argv)
    return not_implemented("scripts/get_checkpoints.py", "T005", "M1")


if __name__ == "__main__":
    raise SystemExit(main())
