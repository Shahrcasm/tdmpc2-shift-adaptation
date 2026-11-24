"""Test-Time Task Embedding Adaptation (Our Single Novelty).

Under physical dynamics shift (e.g. mass, friction, or gravity changes),
we completely freeze all neural network weights (5M+ parameters) and adapt
ONLY the 64-dimensional task embedding vector `e` using standard gradient descent
on observed transition prediction errors.

Why this works:
1. Physical shifts are low-dimensional changes (scalar multipliers).
2. Fine-tuning all 5M weights on 50 steps causes severe overfitting and forgetting.
3. Updating only 64 embedding parameters acts as a powerful regularizer,
   adapting the model in under a second on a laptop CPU.
"""

from __future__ import annotations

from typing import Any
import torch
import torch.nn.functional as F


def adapt_embedding(
    agent,
    transitions: dict[str, torch.Tensor],
    task_idx: int,
    grad_steps: int = 15,
    lr: float = 0.002,
) -> dict[str, Any]:
    """Adapt only the task embedding row for `task_idx` using transition prediction loss.

    Args:
        agent: The DeviceAwareTDMPC2 agent holding the neural world model.
        transitions: Dictionary containing:
            - 'obs': (K, obs_dim) observed states from the shifted environment
            - 'action': (K, act_dim) actions taken
            - 'next_obs': (K, obs_dim) next states reached
        task_idx: Integer index of the current task (0..29 for MT30).
        grad_steps: Number of gradient descent steps (default 15).
        lr: Learning rate for Adam optimizer (default 0.002).

    Returns:
        Dictionary containing:
            - 'initial_loss': Loss before adaptation
            - 'final_loss': Loss after adaptation
            - 'loss_history': List of loss values per step
            - 'initial_embedding': Original 64-dimensional tensor before adaptation
            - 'adapted_embedding': Adapted 64-dimensional tensor after adaptation
    """
    model = agent.model
    device = agent.device

    # 1. Prepare transition data on the target device
    obs = transitions["obs"].to(device=device, dtype=torch.float32)
    action = transitions["action"].to(device=device, dtype=torch.float32)
    next_obs = transitions["next_obs"].to(device=device, dtype=torch.float32)

    # Save a copy of the original embedding before adaptation
    initial_e = model._task_emb.weight.data[task_idx].clone().cpu()

    # 2. Freeze all neural network parameters
    for param in model.parameters():
        param.requires_grad = False

    # 3. Unfreeze ONLY the embedding table
    model._task_emb.weight.requires_grad = True

    # 4. Standard PyTorch Adam optimizer on the embedding weights
    optimizer = torch.optim.Adam([model._task_emb.weight], lr=lr)

    task_tensor = torch.tensor([task_idx], device=device)
    loss_history: list[float] = []

    # Pre-encode target next-states using the fixed nominal embedding to prevent moving-target drift
    with torch.no_grad():
        target_next_z = model.encode(next_obs, task_tensor).detach()

    # 5. Gradient descent adaptation loop
    for step in range(grad_steps):
        optimizer.zero_grad()

        # Step A: Encode current states into latent features z
        z = model.encode(obs, task_tensor)

        # Step B: Predict next latent states using the dynamics network
        pred_next_z = model.next(z, action, task_tensor)

        # Step C: Compute Mean Squared Error (MSE) transition consistency loss
        loss = F.mse_loss(pred_next_z, target_next_z)
        loss_history.append(float(loss.item()))

        # Step D: Compute gradients via standard backpropagation
        loss.backward()

        # Step E: Safety mask — ensure non-zero gradients ONLY touch row `task_idx`
        with torch.no_grad():
            grad = model._task_emb.weight.grad
            if grad is not None:
                mask = torch.zeros_like(grad)
                mask[task_idx] = 1.0
                grad.mul_(mask)

        # Step F: Apply optimizer step
        optimizer.step()

        # Step G: Enforce unit ball constraint (norm <= 1.0) per upstream architecture
        with torch.no_grad():
            norm = model._task_emb.weight.data[task_idx].norm()
            if norm > 1.0:
                model._task_emb.weight.data[task_idx].div_(norm)

    # 6. Extract adapted embedding
    adapted_e = model._task_emb.weight.data[task_idx].clone().cpu()

    if len(loss_history) > 0:
        initial_loss = loss_history[0]
        final_loss = loss_history[-1]
    else:
        initial_loss = 0.0
        final_loss = 0.0

    return {
        "initial_loss": initial_loss,
        "final_loss": final_loss,
        "loss_history": loss_history,
        "initial_embedding": initial_e,
        "adapted_embedding": adapted_e,
    }
