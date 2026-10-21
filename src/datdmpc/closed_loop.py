"""Closed-loop detect -> adapt evaluation (Ours-C2+C3). Owner: M1 · Task: T304 (stub from T001).

Run as ``python -m datdmpc.closed_loop ...``. Combines the C3 detector
(``datdmpc.detect``) with C2 embedding adaptation (``datdmpc.adapt.embedding``): a shift is
injected mid-episode at ``--inject-at``; when the detector fires, ``e``-only adaptation runs
on the most recent K transitions and planning continues with the adapted embedding.
Results go to ``results/P3_closedloop/``.
"""

from __future__ import annotations

import argparse

from datdmpc import not_implemented


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m datdmpc.closed_loop", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ckpt", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--shift", required=True, help="shift SPEC, e.g. mass:1.5")
    p.add_argument("--inject-at", type=int, required=True, help="agent step at which the shift starts")
    p.add_argument("--detector-config", required=True, help="e.g. configs/experiments/M3_detector.yaml")
    p.add_argument("--adapt-config", required=True, help="e.g. configs/experiments/M2_adapt.yaml")
    p.add_argument("--seeds", type=int, nargs="+", required=True)
    p.add_argument("--episodes", type=int, required=True)
    p.add_argument("--out", required=True, help="e.g. results/P3_closedloop/")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--shard", default=None, help="i/N, 1-based")
    p.add_argument("--tier", choices=["T0", "T1", "T1b"], default="T0")
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    return p


def main(argv=None) -> int:
    build_parser().parse_args(argv)
    return not_implemented("datdmpc.closed_loop", "T304", "M1")


if __name__ == "__main__":
    raise SystemExit(main())
