"""Adaptation baselines. Owner: M2 · Task: T203 (stub created in T001).

* B1 ``full_ft``     - finetune every world-model parameter on the same K transitions.
* B2 ``partial_ft``  - finetune only the reward and Q heads.
* B3 ``rand_e``      - re-initialise ``e`` randomly, then run the C2 ``e``-only adaptation.
(B0 = frozen model, evaluated by ``scripts/eval.py``.) All methods see identical transitions.
"""

from __future__ import annotations


def full_finetune(agent, transitions, task_idx, grad_steps, lr, **kwargs):
    raise NotImplementedError("datdmpc.adapt.baselines.full_finetune - task T203 (owner M2)")


def partial_finetune(agent, transitions, task_idx, grad_steps, lr, **kwargs):
    raise NotImplementedError("datdmpc.adapt.baselines.partial_finetune - task T203 (owner M2)")


def random_embedding_then_adapt(agent, transitions, task_idx, grad_steps, lr, **kwargs):
    raise NotImplementedError("datdmpc.adapt.baselines.random_embedding_then_adapt - task T203 (owner M2)")
