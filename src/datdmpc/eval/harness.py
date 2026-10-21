"""Single-task evaluation of a multitask TD-MPC2 checkpoint. Owner: M1 · Task: T006 (stub from T001).

Why this exists: upstream ``evaluate.py`` cannot evaluate one task of a multitask checkpoint,
asserts CUDA, and upstream ``TDMPC2`` hard-codes ``torch.device('cuda:0')``
(``third_party/tdmpc2/tdmpc2/tdmpc2.py``). The harness therefore builds the 30-task model on a
configurable device by subclassing/wrapping (never by editing ``third_party/``).

Contract (to implement in T006):

* ``load_agent(ckpt, model_size=None, device='cpu')`` - build the mt30 config (task list and
  per-task obs/action dims from upstream), instantiate the model on ``device`` with
  ``compile=False``, load the checkpoint, and assert the task embedding has shape (30, 64)
  for mt30-5M/19M (``common/parser.py`` sets task_dim=64 for these).
* ``make_task_env(task, seed, shift='none')`` - one DMControl task, observations zero-padded
  to the multitask width, actions truncated to the task's dims, optional shift (T101).
* ``evaluate(agent, task, episodes, seed, shift, logger)`` - MPPI with upstream settings
  (never changed), one CSV row per finished episode via ``datdmpc.eval.logging``.
* ``run_smoke(ckpt, task, steps, shift, seed) -> dict`` - used by ``scripts/smoke_test.py
  --mode full``: a ``steps``-step nominal and perturbed rollout; returns sec/step figures.
"""

from __future__ import annotations


def load_agent(ckpt, model_size=None, device="cpu"):
    raise NotImplementedError("datdmpc.eval.harness.load_agent - task T006 (owner M1)")


def make_task_env(task, seed, shift="none"):
    raise NotImplementedError("datdmpc.eval.harness.make_task_env - task T006 (owner M1)")


def evaluate(agent, task, episodes, seed, shift="none", logger=None):
    raise NotImplementedError("datdmpc.eval.harness.evaluate - task T006 (owner M1)")


def run_smoke(ckpt, task, steps, shift, seed):
    raise NotImplementedError("datdmpc.eval.harness.run_smoke - tasks T006 + T101 (owner M1)")
