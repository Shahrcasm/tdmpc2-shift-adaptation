"""Unit tests for Test-Time Task Embedding Adaptation (Our Single Novelty).

Verifies:
1. Adaptation reduces transition prediction error (final_loss < initial_loss).
2. ONLY the target task's embedding row changes; all other rows are bit-identical.
3. All other neural network parameters (encoder, dynamics, reward, Q-functions) remain frozen.
4. The adapted embedding respects the unit-norm constraint (norm <= 1.0).
"""

import numpy as np
import pytest
import torch

from datdmpc import _upstream
from datdmpc.adapt.embedding import adapt_embedding


class MockAgent:
    """Lightweight mock agent wrapping an upstream tiny WorldModel for fast CPU testing."""

    def __init__(self, task_idx: int = 1, obs_dim: int = 24, act_dim: int = 6):
        self.device = torch.device("cpu")
        self.task_idx = task_idx

        _upstream.ensure_upstream_on_path()
        cfg = _upstream.make_tiny_cfg(
            obs_dim=obs_dim,
            action_dim=act_dim,
            tasks=["task_0", "task_1", "task_2"],
            task_dim=8,
        )
        self.model = _upstream.build_world_model(cfg, device="cpu")


def _generate_synthetic_transitions(n_steps=30, obs_dim=24, act_dim=6):
    """Generate dummy transitions for testing the gradient adaptation loop."""
    torch.manual_seed(42)
    return {
        "obs": torch.randn(n_steps, obs_dim),
        "action": torch.randn(n_steps, act_dim),
        "next_obs": torch.randn(n_steps, obs_dim),
    }


def test_adapt_embedding_reduces_loss():
    """Verify that gradient descent on the embedding decreases prediction loss."""
    agent = MockAgent(task_idx=1)
    transitions = _generate_synthetic_transitions(n_steps=30)

    result = adapt_embedding(agent, transitions, task_idx=1, grad_steps=15, lr=0.1)

    assert result["final_loss"] < result["initial_loss"], (
        f"Expected final loss ({result['final_loss']}) to be lower than initial loss ({result['initial_loss']})"
    )
    assert len(result["loss_history"]) == 15


def test_adapt_embedding_modifies_only_target_row():
    """Verify that only the target task's embedding row is updated."""
    agent = MockAgent(task_idx=1)
    target_task = 1

    # Snapshot all embedding rows before adaptation
    original_weights = agent.model._task_emb.weight.data.clone()

    transitions = _generate_synthetic_transitions(n_steps=30)
    adapt_embedding(agent, transitions, task_idx=target_task, grad_steps=10, lr=0.1)

    updated_weights = agent.model._task_emb.weight.data

    # Target row MUST have changed
    target_diff = (updated_weights[target_task] - original_weights[target_task]).abs().max().item()
    assert target_diff > 1e-4, "Target task embedding row was not updated!"

    # All OTHER rows MUST remain 100% bit-identical
    for idx in range(original_weights.shape[0]):
        if idx != target_task:
            diff = (updated_weights[idx] - original_weights[idx]).abs().max().item()
            assert diff == 0.0, f"Embedding row {idx} was modified, but only row {target_task} should change!"


def test_adapt_embedding_freezes_all_other_parameters():
    """Verify that all neural network weights outside the embedding table stay completely frozen."""
    agent = MockAgent(task_idx=1)

    # Snapshot every parameter in the model except the task embedding
    saved_params = {}
    for name, param in agent.model.named_parameters():
        if "_task_emb" not in name:
            saved_params[name] = param.data.clone()

    transitions = _generate_synthetic_transitions(n_steps=30)
    adapt_embedding(agent, transitions, task_idx=1, grad_steps=10, lr=0.1)

    # Assert exact bitwise identity for every single parameter
    for name, original_tensor in saved_params.items():
        current_tensor = agent.model.get_parameter(name).data
        assert torch.equal(current_tensor, original_tensor), f"Parameter '{name}' was modified during adaptation!"


def test_adapt_embedding_respects_norm_constraint():
    """Verify that the adapted embedding vector stays within the unit ball (norm <= 1.0)."""
    agent = MockAgent(task_idx=1)
    transitions = _generate_synthetic_transitions(n_steps=30)

    # Use a large learning rate to push the vector outwards
    result = adapt_embedding(agent, transitions, task_idx=1, grad_steps=20, lr=1.0)
    adapted_e = result["adapted_embedding"]

    norm = adapted_e.norm().item()
    assert norm <= 1.0 + 1e-5, f"Adapted embedding norm {norm:.4f} exceeded 1.0!"
