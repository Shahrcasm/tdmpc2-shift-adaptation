"""Per-step shift-detection signals. Owner: M3 · Task: T301 (stub created in T001).

* latent consistency error ``||d(z_t, a_t, e) - h(s_{t+1}, e)||^2`` (``model.next`` vs ``model.encode``)
* reward prediction error (``two_hot_inv(model.reward(...))`` vs observed reward)
* Q-ensemble disagreement: ``model.Q(z, a, task, return_type='all')`` gives every member's
  logits; convert each with upstream ``common.math.two_hot_inv`` and take the std.
"""

from __future__ import annotations


def compute_signals(agent, obs, action, reward, next_obs, task_idx):
    raise NotImplementedError("datdmpc.detect.signals.compute_signals - task T301 (owner M3)")
