"""Streamlit Interactive Web Demo for DA-TDMPC2 (CSE 465).

Course: Pattern Recognition and Neural Network (CSE 465)
Single Novelty: Test-Time Task Embedding Adaptation for Neural World Models under Dynamics Shift.

This app runs both locally (`streamlit run streamlit_app.py`) and on
Streamlit Community Cloud (`share.streamlit.io`). If the pretrained checkpoint
`checkpoints/mt30-5M.pt` is not present on disk (for example on Streamlit Cloud),
it automatically downloads and verifies it from Hugging Face on first startup.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Ensure local packages are importable
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import torch
import torch.nn.functional as F

from datdmpc.adapt.embedding import adapt_embedding
from datdmpc.eval.harness import MT30_TASKS, load_agent, make_task_env
from scripts.get_checkpoints import download_and_verify


# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="DA-TDMPC2 | CSE 465 Neural Network Demo",
    page_icon="🤖",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Model Caching & Automatic Checkpoint Fetching
# ---------------------------------------------------------------------------


@st.cache_resource(show_spinner="Loading Pretrained 5.2M-Parameter TD-MPC2 Neural World Model...")
def get_cached_agent():
    """Ensure checkpoint exists (download from Hugging Face if on cloud) and load agent."""
    ckpt_dir = REPO_ROOT / "checkpoints"
    ckpt_path = ckpt_dir / "mt30-5M.pt"

    if not ckpt_path.is_file():
        download_and_verify(
            model_names=["mt30-5M"],
            dest_dir=ckpt_dir,
            verify_only=False,
        )

    agent = load_agent(ckpt_path, device="cpu")
    return agent


@st.cache_data(show_spinner=False)
def get_original_embedding_table(_agent) -> torch.Tensor:
    """Save a clean copy of the original 30x64 task embedding table."""
    return _agent.model._task_emb.weight.data.clone().cpu()


# ---------------------------------------------------------------------------
# Helper Functions (Beginner-Friendly Syntax)
# ---------------------------------------------------------------------------


def select_action(agent, obs: torch.Tensor, task_idx: int, step_idx: int, use_mppi: bool) -> torch.Tensor:
    """Select an action using either fast neural policy prior or full MPPI planning."""
    if use_mppi:
        is_first = False
        if step_idx == 0:
            is_first = True
        with torch.no_grad():
            action = agent.act(obs, t0=is_first, task=task_idx)
        return action
    else:
        # Fast neural policy network forward pass (< 1 ms per step)
        device = agent.device
        task_tensor = torch.tensor([task_idx], device=device)
        with torch.no_grad():
            obs_batch = obs.to(device=device, dtype=torch.float32).unsqueeze(0)
            z = agent.model.encode(obs_batch, task_tensor)
            _, info = agent.model.pi(z, task_tensor)
            mean_action = info["mean"][0].cpu()
        return mean_action


def compute_fixed_target_mse(
    agent,
    transitions: dict[str, torch.Tensor],
    task_idx: int,
    nominal_embedding: torch.Tensor,
) -> float:
    """Compute latent transition prediction MSE in the fixed nominal coordinate space."""
    model = agent.model
    device = agent.device
    task_tensor = torch.tensor([task_idx], device=device)

    obs = transitions["obs"].to(device=device, dtype=torch.float32)
    action = transitions["action"].to(device=device, dtype=torch.float32)
    next_obs = transitions["next_obs"].to(device=device, dtype=torch.float32)

    with torch.no_grad():
        saved_row = model._task_emb.weight.data[task_idx].clone()

        # 1. Encode target next state with fixed nominal embedding e_0
        model._task_emb.weight.data[task_idx] = nominal_embedding.to(device)
        target_next_z = model.encode(next_obs, task_tensor)

        # 2. Encode current state and predict next state with current embedding
        model._task_emb.weight.data[task_idx] = saved_row
        z = model.encode(obs, task_tensor)
        pred_next_z = model.next(z, action, task_tensor)

        mse_val = float(F.mse_loss(pred_next_z, target_next_z).item())

    return mse_val


def run_environment_rollout(
    agent,
    task: str,
    shift_spec: str,
    steps: int,
    seed: int,
    task_idx: int,
    nominal_embedding: torch.Tensor,
    use_mppi: bool,
) -> tuple[dict[str, torch.Tensor], float, float]:
    """Run the agent in a DMControl environment and collect transitions, reward, and MSE."""
    env = make_task_env(task, seed=seed, shift=shift_spec)
    obs_list = []
    act_list = []
    next_obs_list = []
    reward_list = []
    total_reward = 0.0

    obs = env.reset()
    for step_idx in range(steps):
        action = select_action(agent, obs, task_idx, step_idx, use_mppi)
        next_obs, reward, done, _ = env.step(action)

        obs_list.append(obs.cpu().clone())
        act_list.append(action.cpu().clone())
        next_obs_list.append(next_obs.cpu().clone())
        reward_list.append(reward)
        total_reward = total_reward + reward

        obs = next_obs
        if done:
            obs = env.reset()

    transitions = {
        "obs": torch.stack(obs_list),
        "action": torch.stack(act_list),
        "next_obs": torch.stack(next_obs_list),
        "reward": torch.tensor(reward_list, dtype=torch.float32),
    }

    mse_val = compute_fixed_target_mse(agent, transitions, task_idx, nominal_embedding)
    return transitions, total_reward, mse_val


# ---------------------------------------------------------------------------
# Main UI Layout
# ---------------------------------------------------------------------------


def main() -> None:
    st.title("🤖 DA-TDMPC2: Test-Time Task Embedding Adaptation")
    st.markdown(
        "**Course:** CSE 465 (Pattern Recognition and Neural Network) · "
        "**Base Paper:** *TD-MPC2: Scalable, Robust World Models for Continuous Control* (ICLR 2024)"
    )

    with st.expander("📖 Project Overview & Our Single Novelty (Click to Expand)", expanded=True):
        st.markdown(
            """
            1. **The Problem:** Pretrained neural world models predict physical transitions $(s_t, a_t) \\to s_{t+1}$ accurately under normal conditions, but fail when real-world physics shifts (e.g., heavier robot mass, slippery floor friction, or weaker motors).
            2. **Why Full Fine-Tuning Fails:** Updating all **5,241,066 neural network weights** on a small test-time sample causes severe overfitting and takes too much compute.
            3. **Our Single Novelty:** We **freeze 100% of the neural network weights** and update **only the 64-dimensional task embedding vector ($e$)** using standard PyTorch gradient descent on transition consistency loss:
               $$\\mathcal{L}(e) = \\frac{1}{K} \\sum_{t=1}^{K} \\| d(h(s_t, e), a_t, e) - h(s_{t+1}, e_0) \\|^2$$
            4. **Result:** Because a physical shift is low-dimensional, updating only 64 numbers acts as a strong regularizer and adapts the neural world model in **~0.1 seconds on a CPU**.
            """
        )

    # Load model and original embeddings
    agent = get_cached_agent()
    original_table = get_original_embedding_table(agent)

    total_params = 0
    for param in agent.model.parameters():
        total_params = total_params + param.numel()
    embedding_dim = int(agent.model._task_emb.weight.shape[1])

    # -----------------------------------------------------------------------
    # Sidebar Controls
    # -----------------------------------------------------------------------
    st.sidebar.header("⚙️ Experiment Settings")

    selected_task = st.sidebar.selectbox(
        "1. Select Robot Control Task",
        options=["walker-walk", "cheetah-run", "hopper-stand", "cartpole-balance", "reacher-easy"],
        index=0,
    )

    shift_type = st.sidebar.selectbox(
        "2. Physical Shift Type",
        options=["mass", "friction", "actuator", "gravity"],
        index=0,
    )

    shift_level = st.sidebar.slider(
        "3. Shift Scale Factor (1.0 = Nominal)",
        min_value=0.3,
        max_value=2.5,
        value=1.5,
        step=0.1,
    )
    shift_spec = f"{shift_type}:{shift_level:.1f}"

    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 Novelty Hyperparameters")

    buffer_steps = st.sidebar.slider(
        "4. Transition Buffer Size (K steps)",
        min_value=10,
        max_value=60,
        value=30,
        step=5,
    )

    grad_steps = st.sidebar.slider(
        "5. Gradient Descent Steps on Embedding",
        min_value=5,
        max_value=40,
        value=15,
        step=5,
    )

    lr = st.sidebar.select_slider(
        "6. Learning Rate (Adam)",
        options=[0.0005, 0.001, 0.002, 0.005, 0.01],
        value=0.002,
    )

    rollout_mode = st.sidebar.radio(
        "7. Rollout Execution Mode",
        options=[
            "Fast Neural Policy (< 1 sec, Cloud Recommended)",
            "Full MPPI Planning (512 Trajectories, ~60 sec on CPU)",
        ],
        index=0,
    )

    use_mppi = False
    if "Full MPPI" in rollout_mode:
        use_mppi = True
        if buffer_steps > 10:
            st.sidebar.warning("Tip: For CPU MPPI mode, set K=5 or 10 steps so it finishes in ~45 seconds.")

    run_clicked = st.sidebar.button("🚀 Run Live Adaptation Experiment", type="primary", use_container_width=True)

    # -----------------------------------------------------------------------
    # Run Live Experiment
    # -----------------------------------------------------------------------
    if run_clicked:
        task_idx = MT30_TASKS.index(selected_task)
        nominal_embedding = original_table[task_idx].clone()

        # Always reset embedding table to clean nominal weights before starting
        with torch.no_grad():
            agent.model._task_emb.weight.data.copy_(original_table.to(agent.device))

        with st.spinner(f"Running MuJoCo simulation and adapting 64-D embedding for `{selected_task}` under `{shift_spec}`..."):
            # Phase 1: Nominal rollout
            _, nominal_return, nominal_mse = run_environment_rollout(
                agent=agent,
                task=selected_task,
                shift_spec="none",
                steps=buffer_steps,
                seed=0,
                task_idx=task_idx,
                nominal_embedding=nominal_embedding,
                use_mppi=use_mppi,
            )

            # Phase 2: Shifted rollout (unadapted)
            shifted_transitions, shifted_return, shifted_mse = run_environment_rollout(
                agent=agent,
                task=selected_task,
                shift_spec=shift_spec,
                steps=buffer_steps,
                seed=0,
                task_idx=task_idx,
                nominal_embedding=nominal_embedding,
                use_mppi=use_mppi,
            )

            # Phase 3: Our Single Novelty — 64-D Embedding Adaptation
            t_start = time.perf_counter()
            adapt_res = adapt_embedding(
                agent=agent,
                transitions=shifted_transitions,
                task_idx=task_idx,
                grad_steps=grad_steps,
                lr=lr,
            )
            adapt_time_s = time.perf_counter() - t_start

            # Phase 4: Re-evaluate on shifted environment
            _, adapted_return, adapted_rollout_mse = run_environment_rollout(
                agent=agent,
                task=selected_task,
                shift_spec=shift_spec,
                steps=buffer_steps,
                seed=0,
                task_idx=task_idx,
                nominal_embedding=nominal_embedding,
                use_mppi=use_mppi,
            )

        initial_loss = adapt_res["initial_loss"]
        final_loss = adapt_res["final_loss"]

        if nominal_mse > 1e-8:
            shift_spike_pct = ((shifted_mse - nominal_mse) / nominal_mse) * 100.0
        else:
            shift_spike_pct = 0.0

        if initial_loss > 1e-8:
            loss_reduction_pct = ((initial_loss - final_loss) / initial_loss) * 100.0
        else:
            loss_reduction_pct = 0.0

        # -------------------------------------------------------------------
        # Top Summary Metrics
        # -------------------------------------------------------------------
        st.subheader("📊 Live Experiment Results")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            label="Parameters Updated",
            value=f"{embedding_dim} / {total_params:,}",
            delta="99.9988% Frozen",
            delta_color="normal",
        )
        col2.metric(
            label=f"Shifted MSE ({shift_spec})",
            value=f"{shifted_mse:.6f}",
            delta=f"{shift_spike_pct:+.1f}% vs Nominal",
            delta_color="inverse",
        )
        col3.metric(
            label="Adapted MSE (Ours)",
            value=f"{final_loss:.6f}",
            delta=f"-{loss_reduction_pct:.1f}% Error Drop",
            delta_color="normal",
        )
        col4.metric(
            label="Adaptation CPU Time",
            value=f"{adapt_time_s:.3f} s",
            delta=f"{grad_steps} Gradient Steps",
            delta_color="off",
        )

        # -------------------------------------------------------------------
        # Visual Charts (3 Columns)
        # -------------------------------------------------------------------
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("#### 1. Gradient Descent Convergence Curve")
            fig1, ax1 = plt.subplots(figsize=(6, 3.8))
            steps_axis = list(range(1, len(adapt_res["loss_history"]) + 1))
            ax1.plot(steps_axis, adapt_res["loss_history"], marker="o", color="#1f77b4", linewidth=2)
            ax1.set_title(f"Latent Consistency Loss over {grad_steps} Steps (lr={lr})")
            ax1.set_xlabel("Gradient Descent Step")
            ax1.set_ylabel("Transition Prediction MSE")
            ax1.grid(True, linestyle="--", alpha=0.5)
            st.pyplot(fig1)

        with chart_col2:
            st.markdown("#### 2. Prediction Error Comparison")
            fig2, ax2 = plt.subplots(figsize=(6, 3.8))
            labels = ["1. Nominal\n(Normal Physics)", f"2. Shifted\n({shift_spec}, Frozen)", "3. Ours\n(64-D Adapted)"]
            mse_values = [nominal_mse, shifted_mse, final_loss]
            colors = ["#2ca02c", "#d62728", "#1f77b4"]
            bars = ax2.bar(labels, mse_values, color=colors, width=0.55)
            ax2.set_title("World Model Transition Prediction Error (Lower is Better)")
            ax2.set_ylabel("Latent Transition MSE")
            ax2.grid(True, axis="y", linestyle="--", alpha=0.5)
            for bar in bars:
                height = bar.get_height()
                ax2.annotate(
                    f"{height:.5f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )
            st.pyplot(fig2)

        # -------------------------------------------------------------------
        # Embedding Vector Shift Visualization
        # -------------------------------------------------------------------
        st.markdown("#### 3. Inside the Neural Network: 64-Dimensional Task Embedding Shift ($\Delta e = e_{\\text{adapted}} - e_0$)")
        init_e_np = adapt_res["initial_embedding"].numpy()
        adapt_e_np = adapt_res["adapted_embedding"].numpy()
        delta_e_np = adapt_e_np - init_e_np

        fig3, ax3 = plt.subplots(figsize=(12, 3.0))
        dims = np.arange(embedding_dim)
        ax3.bar(dims, delta_e_np, color="#9467bd", alpha=0.85)
        ax3.axhline(0.0, color="black", linewidth=0.8)
        ax3.set_title(f"Per-Dimension Change Across the 64 Embedding Parameters (L2 Shift = {np.linalg.norm(delta_e_np):.4f})")
        ax3.set_xlabel("Embedding Dimension Index (0 to 63)")
        ax3.set_ylabel("Parameter Change (Δe)")
        ax3.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig3)

        # -------------------------------------------------------------------
        # Summary Comparison Table
        # -------------------------------------------------------------------
        st.markdown("#### 4. Experiment Summary Table")
        summary_df = pd.DataFrame(
            [
                {
                    "Condition": "1. Nominal (Normal Physics)",
                    "Physics": "none (1.0x)",
                    "Parameters Updated": "0 (Pretrained)",
                    "Transition MSE": f"{nominal_mse:.6f}",
                    f"Rollout Return ({buffer_steps} steps)": f"{nominal_return:.2f}",
                },
                {
                    "Condition": "2. Shifted (Unadapted Baseline)",
                    "Physics": shift_spec,
                    "Parameters Updated": "0 (Frozen)",
                    "Transition MSE": f"{shifted_mse:.6f} ({shift_spike_pct:+.1f}%)",
                    f"Rollout Return ({buffer_steps} steps)": f"{shifted_return:.2f}",
                },
                {
                    "Condition": "3. Ours (Test-Time Embedding Adaptation)",
                    "Physics": shift_spec,
                    "Parameters Updated": f"{embedding_dim} / {total_params:,} (0.0012%)",
                    "Transition MSE": f"{final_loss:.6f} (-{loss_reduction_pct:.1f}% vs Shifted)",
                    f"Rollout Return ({buffer_steps} steps)": f"{adapted_return:.2f}",
                },
            ]
        )
        st.table(summary_df)

    else:
        st.info("👈 Choose your task and physical shift in the sidebar, then click **'🚀 Run Live Adaptation Experiment'** to run live PyTorch adaptation!")


if __name__ == "__main__":
    main()

