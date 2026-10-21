"""Tests for the bridge to vendored upstream TD-MPC2 (owner: M1, T001)."""

import re

import pytest
import torch

from datdmpc import _upstream


def test_vendored_upstream_is_pinned():
    text = (_upstream.UPSTREAM_ROOT / "UPSTREAM_COMMIT.txt").read_text(encoding="utf-8")
    assert _upstream.UPSTREAM_COMMIT in text
    assert (_upstream.UPSTREAM_ROOT / "LICENSE").is_file()
    assert (_upstream.UPSTREAM_PKG_DIR / "common" / "world_model.py").is_file()


def test_mt30_task_order():
    tasks = _upstream.mt30_tasks()
    assert len(tasks) == 30 and len(set(tasks)) == 30
    assert tasks[0] == "walker-stand" and tasks[1] == "walker-walk"


def test_mt30_task_dim_is_64_for_5M_and_19M():
    # Guards the documented fact dim(e) = 64 for mt30-5M/19M (docs/PROJECT_PLAN.md).
    parser_src = (_upstream.UPSTREAM_PKG_DIR / "common" / "parser.py").read_text(encoding="utf-8")
    assert re.search(
        r"cfg\.task_dim = 96 if cfg\.task == 'mt80' or cfg\.get\('model_size', 5\) in \{1, 317\} else 64",
        parser_src,
    ), "upstream task_dim rule changed - re-check every doc that states dim(e) = 64"


def test_tiny_world_model_forward_on_cpu():
    obs_dim, act_dim = 24, 6
    cfg = _upstream.make_tiny_cfg(obs_dim=obs_dim, action_dim=act_dim)
    model = _upstream.build_world_model(cfg, device="cpu")
    task = torch.tensor([1])
    obs = torch.randn(4, obs_dim)
    with torch.no_grad():
        z = model.encode(obs, task)
        a, info = model.pi(z, task)
        z_next = model.next(z, a, task)
        r_logits = model.reward(z, a, task)
        q_all = model.Q(z, a, task, return_type="all")
        q_avg = model.Q(z, a, task, return_type="avg")
    assert z.shape == (4, cfg.latent_dim) and z_next.shape == z.shape
    assert a.shape == (4, act_dim) and torch.all(a.abs() <= 1)
    assert r_logits.shape == (4, cfg.num_bins)
    assert q_all.shape == (cfg.num_q, 4, cfg.num_bins)
    assert q_avg.shape == (4, 1)
    # SimNorm: each group of simnorm_dim latent entries sums to 1.
    groups = z.view(4, -1, cfg.simnorm_dim).sum(-1)
    assert torch.allclose(groups, torch.ones_like(groups), atol=1e-5)


def test_task_embedding_norm_is_bounded():
    cfg = _upstream.make_tiny_cfg(obs_dim=5, action_dim=1)
    model = _upstream.build_world_model(cfg)
    with torch.no_grad():
        model._task_emb.weight.mul_(1000.0)  # far outside the unit ball
        emb = model._task_emb(torch.tensor([0, 1]))
    assert torch.all(emb.norm(dim=-1) <= 1.0 + 1e-5)


def test_unwrap_dm_env_rejects_non_env():
    with pytest.raises(AttributeError):
        _upstream.unwrap_dm_env(object())
