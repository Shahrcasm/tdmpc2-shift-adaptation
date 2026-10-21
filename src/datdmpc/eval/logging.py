"""Resume-safe per-episode result logging. Owner: M1 · Task: T006 (stub created in T001).

Contract (to implement in T006) - results schema, see AGENTS.md / docs/RUNS.md:

``results/<phase>_<exp>/<run_id>/`` containing ``config.yaml``, ``episodes.csv``,
``summary.json``, ``env.txt``, ``git_sha.txt``.

* ``run_id = <ckpt-stem>__<task>__<shift>__<method>__seed<seed>`` with ':' replaced by '-'.
* ``episodes.csv`` columns: ``run_id,task,task_idx,shift_type,shift_level,method,seed,episode,
  return,length,wall_time_s,tier,shard,timestamp`` - one row appended and flushed per finished
  episode, so an interrupted Colab session loses at most one episode.
* ``--resume``: episodes already present in ``episodes.csv`` are skipped.
* ``summary.json``: at least ``run_id, n_episodes, mean_return, ci95_low, ci95_high``.
* ``env.txt``: python / torch / mujoco / dm_control / numpy versions, OS, CPU, device, tier.
"""

from __future__ import annotations


class RunLogger:
    def __init__(self, out_dir, run_id, config, tier="T0", shard=None, resume=False):
        raise NotImplementedError("datdmpc.eval.logging.RunLogger - task T006 (owner M1)")


def make_run_id(ckpt, task, shift, method, seed) -> str:
    raise NotImplementedError("datdmpc.eval.logging.make_run_id - task T006 (owner M1)")
