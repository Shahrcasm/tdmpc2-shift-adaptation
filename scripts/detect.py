"""Shift detection: signal extraction, calibration, evaluation. Owner: M3 · Tasks: T301-T303 (stub from T001).

Subcommands
  signals    dump per-step signals (consistency error, reward error, Q-ensemble std) -> outputs/signals/
  calibrate  fit detector thresholds on nominal calibration seeds (1000-1099) -> results/P3_detect/
  evaluate   mid-episode shift injection; AUROC, delay, false alarms -> results/P3_detect/
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


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--ckpt", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--tier", choices=["T0", "T1", "T1b"], default="T0")
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("signals", help="T301: extract per-step signals")
    _common(s)
    s.add_argument("--shift", default="none")
    s.add_argument("--episodes", type=int, required=True)
    s.add_argument("--seed", type=int, required=True)
    s.add_argument("--out", default="outputs/signals/")

    c = sub.add_parser("calibrate", help="T302: calibrate on nominal seeds")
    _common(c)
    c.add_argument("--seeds", type=int, nargs="+", required=True)
    c.add_argument("--episodes", type=int, required=True)
    c.add_argument("--out", required=True, help="results/P3_detect/")

    e = sub.add_parser("evaluate", help="T303: mid-episode injection evaluation")
    _common(e)
    e.add_argument("--shift", required=True)
    e.add_argument("--inject-at", type=int, required=True, help="agent step at which the shift starts")
    e.add_argument("--detector-config", required=True, help="configs/experiments/M3_detector.yaml")
    e.add_argument("--seeds", type=int, nargs="+", required=True)
    e.add_argument("--out", required=True, help="results/P3_detect/")
    e.add_argument("--resume", action="store_true")
    e.add_argument("--shard", default=None, help="i/N (1-based)")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    task = {"signals": "T301", "calibrate": "T302", "evaluate": "T303"}[args.command]
    return not_implemented(f"scripts/detect.py {args.command}", task, "M3")


if __name__ == "__main__":
    raise SystemExit(main())
