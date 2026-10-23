"""Tests for single-task multitask evaluation harness (Owner: M1 · Task: T006)."""

from pathlib import Path
import pytest
import torch

from datdmpc.eval.harness import (
    build_mt30_cfg,
    infer_model_size,
    load_agent,
    make_task_env,
    MT30_TASKS,
    MT30_MAX_OBS_DIM,
    MT30_MAX_ACTION_DIM,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CKPT_5M = REPO_ROOT / "checkpoints" / "mt30-5M.pt"
CKPT_19M = REPO_ROOT / "checkpoints" / "mt30-19M.pt"


def test_infer_model_size():
    assert infer_model_size("checkpoints/mt30-5M.pt") == 5
    assert infer_model_size("checkpoints/mt30-19M.pt") == 19
    assert infer_model_size("custom.pt", model_size=5) == 5
    assert infer_model_size("custom.pt", model_size=19) == 19
    with pytest.raises(ValueError):
        infer_model_size("unknown.pt")


def test_mppi_config_settings_match_upstream():
    """Guards rule §4.4: MPPI settings are never changed in reported results."""
    cfg = build_mt30_cfg(model_size=5, device="cpu")
    assert cfg.iterations == 6
    assert cfg.num_samples == 512
    assert cfg.num_elites == 64
    assert cfg.num_pi_trajs == 24
    assert cfg.horizon == 3
    assert cfg.min_std == 0.05
    assert cfg.max_std == 2
    assert cfg.temperature == 0.5
    assert cfg.compile is False
    assert cfg.task_dim == 64
    assert len(cfg.tasks) == 30


@pytest.mark.skipif(not CKPT_5M.is_file(), reason="mt30-5M.pt not present locally")
def test_load_agent_5M_cpu():
    """Load mt30-5M on CPU and verify task embedding dimension is strictly (30, 64)."""
    agent = load_agent(CKPT_5M, device="cpu")
    assert str(agent.device) == "cpu"
    emb = agent.model._task_emb.weight
    assert emb.shape == (30, 64), f"Task embedding shape must be (30, 64), got {emb.shape}"
    assert emb.device.type == "cpu"
    assert not agent.model.training


@pytest.mark.skipif(not CKPT_19M.is_file(), reason="mt30-19M.pt not present locally")
def test_load_agent_19M_cpu():
    """Load mt30-19M on CPU and verify task embedding dimension is strictly (30, 64) and latent_dim=512."""
    agent = load_agent(CKPT_19M, device="cpu")
    assert str(agent.device) == "cpu"
    emb = agent.model._task_emb.weight
    assert emb.shape == (30, 64), f"Task embedding shape must be (30, 64), got {emb.shape}"
    assert agent.cfg.latent_dim == 512


def test_single_task_env_padding_and_truncation():
    """Test pendulum-spin (obs_dim=3, act_dim=1) is padded to 24 and truncates 6-dim actions."""
    env = make_task_env("pendulum-spin", seed=42)
    obs = env.reset()
    assert isinstance(obs, torch.Tensor)
    assert obs.shape == (MT30_MAX_OBS_DIM,), f"Observation should be padded to 24, got {obs.shape}"
    # The first 3 are real state; trailing 21 must be 0
    assert torch.all(obs[3:] == 0.0)

    # Step with a 6-dimensional model action vector
    dummy_action = torch.tensor([0.5, 0.9, -0.4, 0.1, -0.8, 0.2], dtype=torch.float32)
    next_obs, reward, done, info = env.step(dummy_action)
    assert next_obs.shape == (MT30_MAX_OBS_DIM,)
    assert torch.all(next_obs[3:] == 0.0)
    assert isinstance(reward, float)
    assert isinstance(done, bool)


def test_shard_partitioning_disjoint_and_complete():
    """Test that sharding splits an arbitrary list into disjoint parts whose union is the whole list."""
    def shard_list(items, shard_spec):
        # i/N (1-based)
        i_str, separator, n_str = shard_spec.partition("/")
        i = int(i_str)
        n = int(n_str)
        assert 1 <= i <= n

        selected = []
        for index, item in enumerate(items):
            if index % n == (i - 1):
                selected.append(item)
        return selected

    tasks = list(MT30_TASKS)
    shards = [shard_list(tasks, f"{i}/3") for i in (1, 2, 3)]

    # Disjoint
    assert len(set(shards[0]) & set(shards[1])) == 0
    assert len(set(shards[1]) & set(shards[2])) == 0
    assert len(set(shards[0]) & set(shards[2])) == 0

    # Complete union
    union = set(shards[0]) | set(shards[1]) | set(shards[2])
    assert union == set(tasks)
