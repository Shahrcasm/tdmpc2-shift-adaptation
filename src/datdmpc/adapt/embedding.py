"""C2: adapt only the task embedding ``e`` of a frozen TD-MPC2 model. Owner: M2 · Task: T202 (stub from T001).

Facts to respect (see docs/PROJECT_PLAN.md and docs/design/C2_embedding_adaptation.md):

* For mt30-5M/19M the embedding table is ``model._task_emb`` = ``nn.Embedding(30, 64,
  max_norm=1)`` (upstream ``common/world_model.py`` + ``common/parser.py``), so one task's
  ``e`` has 64 numbers. ``max_norm`` renormalises the looked-up row in place.
* Loss terms and default coefficients come from upstream ``TDMPC2._update`` /
  ``config.yaml`` (consistency 20, reward 0.1, value 0.1, rho 0.5); the final choice is
  fixed in the T201 design note before any T204 run.
* ``tests/test_embedding.py`` must prove that only the chosen embedding row changes and every
  other parameter stays bit-identical.
"""

from __future__ import annotations


def adapt_embedding(agent, transitions, task_idx, grad_steps, lr, **kwargs):
    raise NotImplementedError("datdmpc.adapt.embedding.adapt_embedding - task T202 (owner M2)")
