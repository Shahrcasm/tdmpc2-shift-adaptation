"""Ranking-fidelity diagnostic. Owner: M1 · Tasks: T104, T205 (stub created in T001).

Run as ``python -m datdmpc.diagnostics.ranking_fidelity ...``. For N sampled states, save the
simulator state (``physics.get_state()``), roll out M candidate action sequences of length H in
the real simulator (restoring with ``physics.set_state()`` between candidates) and compare their
true short-horizon returns with the model's predicted returns (discounted predicted rewards plus
discounted Q bootstrap, as in upstream ``TDMPC2._estimate_value``). Reports Kendall tau and
top-1 agreement, nominal vs shifted, and (T205) with an adapted embedding.
"""

from __future__ import annotations

import argparse

from datdmpc import not_implemented


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m datdmpc.diagnostics.ranking_fidelity",
                                description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ckpt", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--shift", default="none", help="shift SPEC, e.g. mass:1.5 (default: none)")
    p.add_argument("--states", type=int, required=True, help="number of start states N")
    p.add_argument("--candidates", type=int, required=True, help="candidate action sequences M per state")
    p.add_argument("--horizon", type=int, required=True, help="rollout horizon H (agent steps)")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--embedding", default=None, help="adapted_embedding.json from scripts/adapt.py (T205)")
    p.add_argument("--out", required=True, help="e.g. results/P1_ranking/")
    p.add_argument("--tier", choices=["T0", "T1", "T1b"], default="T0")
    p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    return p


def main(argv=None) -> int:
    build_parser().parse_args(argv)
    return not_implemented("datdmpc.diagnostics.ranking_fidelity", "T104", "M1")


if __name__ == "__main__":
    raise SystemExit(main())
