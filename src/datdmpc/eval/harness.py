"""Single-task evaluation of a multitask TD-MPC2 checkpoint. Owner: M1 · Task: T006.

Why this exists: upstream evaluate.py cannot evaluate one task of a multitask checkpoint,
asserts CUDA, and upstream TDMPC2 and RunningScale hard-code torch.device('cuda:0').
The harness builds the model on a configurable device by subclassing/wrapping
(never by editing third_party/).
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Sequence

import gymnasium as gym
import numpy as np
import torch

from datdmpc import _upstream
from datdmpc.eval.logging import RunLogger

# Ground truth metadata for the 30 mt30 tasks (verified from upstream envs)
MT30_TASKS = [
    "walker-stand", "walker-walk", "walker-run", "cheetah-run", "reacher-easy",
    "reacher-hard", "acrobot-swingup", "pendulum-swingup", "cartpole-balance",
    "cartpole-balance-sparse", "cartpole-swingup", "cartpole-swingup-sparse",
    "cup-catch", "finger-spin", "finger-turn-easy", "finger-turn-hard",
    "fish-swim", "hopper-stand", "hopper-hop", "walker-walk-backwards",
    "walker-run-backwards", "cheetah-run-backwards", "cheetah-run-front",
    "cheetah-run-back", "cheetah-jump", "hopper-hop-backwards",
    "reacher-three-easy", "reacher-three-hard", "cup-spin", "pendulum-spin",
]

MT30_OBS_DIMS = [
    24, 24, 24, 17, 6, 6, 6, 3, 5, 5, 5, 5, 8, 9, 12, 12,
    24, 15, 15, 24, 24, 17, 17, 17, 17, 15, 8, 8, 8, 3,
]

MT30_ACTION_DIMS = [
    6, 6, 6, 6, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
    5, 4, 4, 6, 6, 6, 6, 6, 6, 4, 3, 3, 2, 1,
]

MT30_EPISODE_LENGTHS = [500] * 30
MT30_MAX_OBS_DIM = 24
MT30_MAX_ACTION_DIM = 6


def infer_model_size(ckpt_path: str | Path, model_size: int | None = None) -> int:
    """Infer model size (5 or 19) from path or argument."""
    if model_size is not None:
        if model_size not in (5, 19):
            raise ValueError(f"model_size must be 5 or 19, got {model_size}")
        return model_size

    path_str = str(ckpt_path)
    if "19M" in path_str:
        return 19
    elif "5M" in path_str:
        return 5
    else:
        raise ValueError(
            f"Could not infer model size (5 or 19) from {ckpt_path}. Specify --model-size."
        )


def build_mt30_cfg(model_size: int = 5, device: str = "cpu") -> _upstream.UpstreamCfg:
    """Build full resolved configuration for mt30 agent inference on `device`."""
    _upstream.ensure_upstream_on_path()
    from common import MODEL_SIZE

    size_params = MODEL_SIZE[model_size]

    # For mt30 multitask models at sizes 5M and 19M, latent dimension is 512
    if model_size in (5, 19):
        latent_dim = 512
    else:
        latent_dim = size_params["latent_dim"]

    enc_dim = size_params["enc_dim"]
    num_enc_layers = size_params["num_enc_layers"]
    mlp_dim = size_params["mlp_dim"]
    # Upstream config.yaml sets default num_q to 5 if not specified in MODEL_SIZE
    num_q = size_params.get("num_q", 5)

    num_bins = 101
    vmin = -10.0
    vmax = 10.0
    bin_size = (vmax - vmin) / (num_bins - 1)

    return _upstream.UpstreamCfg(
        task="mt30",
        tasks=list(MT30_TASKS),
        multitask=True,
        obs="state",
        obs_shape={"state": (MT30_MAX_OBS_DIM,)},
        obs_shapes=list(MT30_OBS_DIMS),
        action_dim=MT30_MAX_ACTION_DIM,
        action_dims=list(MT30_ACTION_DIMS),
        episode_length=500,
        episode_lengths=list(MT30_EPISODE_LENGTHS),
        episodic=False,
        # Model architecture
        model_size=model_size,
        task_dim=64,  # Exactly 64 for mt30-5M and mt30-19M
        latent_dim=latent_dim,
        enc_dim=enc_dim,
        num_enc_layers=num_enc_layers,
        mlp_dim=mlp_dim,
        num_q=num_q,
        simnorm_dim=8,
        num_channels=32,
        dropout=0.01,
        # Action space & planning
        log_std_min=-10,
        log_std_max=2,
        num_bins=num_bins,
        vmin=vmin,
        vmax=vmax,
        bin_size=bin_size,
        lr=3e-4,
        enc_lr_scale=0.1,
        tau=0.01,
        discount_denom=5,
        discount_min=0.95,
        discount_max=0.995,
        iterations=6,
        num_samples=512,
        num_elites=64,
        num_pi_trajs=24,
        horizon=3,
        min_std=0.05,
        max_std=2,
        temperature=0.5,
        mpc=True,
        compile=False,
        device=str(device),
    )


class DeviceAwareRunningScale(torch.nn.Module):
    """Running trimmed scale estimator that respects a target device (no hardcoded cuda:0)."""

    def __init__(self, cfg, device: torch.device):
        super().__init__()
        self.cfg = cfg
        self.device = device
        self.value = torch.nn.Buffer(torch.ones(1, dtype=torch.float32, device=device))
        self._percentiles = torch.nn.Buffer(torch.tensor([5, 95], dtype=torch.float32, device=device))

    def state_dict(self):
        return dict(value=self.value, percentiles=self._percentiles)

    def load_state_dict(self, state_dict):
        self.value.copy_(state_dict["value"])
        self._percentiles.copy_(state_dict["percentiles"])

    def _positions(self, x_shape):
        positions = self._percentiles * (x_shape - 1) / 100
        floored = torch.floor(positions)
        ceiled = floored + 1
        ceiled = torch.where(ceiled > x_shape - 1, x_shape - 1, ceiled)
        weight_ceiled = positions - floored
        weight_floored = 1.0 - weight_ceiled
        return floored.long(), ceiled.long(), weight_floored.unsqueeze(1), weight_ceiled.unsqueeze(1)

    def _percentile(self, x):
        x_dtype, x_shape = x.dtype, x.shape
        x = x.flatten(1, x.ndim - 1)
        in_sorted = torch.sort(x, dim=0).values
        floored, ceiled, weight_floored, weight_ceiled = self._positions(x.shape[0])
        d0 = in_sorted[floored] * weight_floored
        d1 = in_sorted[ceiled] * weight_ceiled
        return (d0 + d1).reshape(-1, *x_shape[1:]).to(x_dtype)

    def update(self, x):
        percentiles = self._percentile(x.detach())
        value = torch.clamp(percentiles[1] - percentiles[0], min=1.0)
        self.value.copy_(self.cfg.tau * value + (1 - self.cfg.tau) * self.value)
        return self.value

    def __call__(self, x, update=False):
        if update:
            self.update(x)
        return (x / self.value).clamp(-1e4, 1e4)


_upstream.ensure_upstream_on_path()
from tdmpc2 import TDMPC2


class DeviceAwareTDMPC2(TDMPC2):
    """Subclass of upstream TDMPC2 that supports CPU and arbitrary devices."""

    def __init__(self, cfg, device: str = "cpu"):
        super(TDMPC2, self).__init__()
        _upstream.ensure_upstream_on_path()
        from common.world_model import WorldModel

        self.cfg = cfg
        self.device = torch.device(device)
        self.model = WorldModel(cfg).to(self.device)
        self.model.eval()

        self.scale = DeviceAwareRunningScale(cfg, self.device)
        self.cfg.iterations += 2 * int(cfg.action_dim >= 20)

        # Compute discount factors for each task on target device
        def get_discount(ep_len: int) -> float:
            frac = ep_len / self.cfg.discount_denom
            scaled = (frac - 1.0) / frac
            bounded = max(scaled, self.cfg.discount_min)
            return min(bounded, self.cfg.discount_max)

        if self.cfg.multitask:
            discount_list = []
            for ep_len in cfg.episode_lengths:
                discount_list.append(get_discount(ep_len))
            self.discount = torch.tensor(discount_list, device=self.device)
        else:
            self.discount = get_discount(cfg.episode_length)

        self._prev_mean = torch.nn.Buffer(
            torch.zeros(self.cfg.horizon, self.cfg.action_dim, device=self.device)
        )

    def load(self, fp: str | Path | dict) -> None:
        """Load state dict onto agent device with cross-platform PosixPath compatibility."""
        import pathlib

        # Workaround for Linux checkpoints containing PosixPath when unpickled on Windows
        if os.name == "nt":
            pathlib.PosixPath = pathlib.WindowsPath

        if isinstance(fp, dict):
            state_dict = fp
        else:
            state_dict = torch.load(fp, map_location=self.device, weights_only=False)

        # Some checkpoints store weights under a top-level 'model' key
        if "model" in state_dict:
            state_dict = state_dict["model"]

        _upstream.ensure_upstream_on_path()
        from common.layers import api_model_conversion

        state_dict = api_model_conversion(self.model.state_dict(), state_dict)
        self.model.load_state_dict(state_dict)


def load_agent(ckpt: str | Path, model_size: int | None = None, device: str = "cpu") -> DeviceAwareTDMPC2:
    """Load a pretrained TD-MPC2 multitask agent on `device`."""
    ckpt_path = Path(ckpt)
    if not ckpt_path.is_file():
        raise FileNotFoundError(f"Checkpoint not found at {ckpt_path}")

    size = infer_model_size(ckpt_path, model_size)
    cfg = build_mt30_cfg(model_size=size, device=device)
    agent = DeviceAwareTDMPC2(cfg, device=device)

    # Load weights
    agent.load(str(ckpt_path))
    agent.model.eval()

    # Verify task embedding dimensions
    emb_shape = tuple(agent.model._task_emb.weight.shape)
    assert emb_shape == (30, 64), f"Expected task embedding (30, 64), got {emb_shape}"

    return agent


class SingleTaskMultitaskEnv(gym.Wrapper):
    """Wraps a single DMControl task to match multitask model input/output dimensions."""

    def __init__(self, task: str, env: gym.Env, max_obs_dim: int = MT30_MAX_OBS_DIM, max_action_dim: int = MT30_MAX_ACTION_DIM):
        super().__init__(env)
        self.task_name = task
        self.task_idx = MT30_TASKS.index(task)
        self.max_obs_dim = max_obs_dim
        self.max_action_dim = max_action_dim

        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(self.max_obs_dim,), dtype=np.float32
        )
        self.action_space = gym.spaces.Box(
            low=-1.0, high=1.0, shape=(self.max_action_dim,), dtype=np.float32
        )

    def _pad_obs(self, obs: torch.Tensor) -> torch.Tensor:
        if obs.shape[-1] < self.max_obs_dim:
            pad_len = self.max_obs_dim - obs.shape[-1]
            pad = torch.zeros(*obs.shape[:-1], pad_len, dtype=obs.dtype, device=obs.device)
            return torch.cat((obs, pad), dim=-1)
        return obs

    def reset(self, **kwargs):
        obs = self.env.reset(**kwargs)
        if isinstance(obs, tuple):
            obs = obs[0]
        return self._pad_obs(obs)

    def step(self, action: torch.Tensor):
        task_act_dim = self.env.action_space.shape[0]
        sub_action = action[:task_act_dim]
        obs, reward, done, info = self.env.step(sub_action)
        if torch.is_tensor(reward):
            reward = float(reward.item())
        else:
            reward = float(reward)
        return self._pad_obs(obs), reward, done, info


def make_task_env(task: str, seed: int, shift: str = "none") -> SingleTaskMultitaskEnv:
    """Create a single DMControl task wrapped for multitask inference."""
    if task not in MT30_TASKS:
        raise ValueError(f"Unknown mt30 task {task!r}. Valid tasks: {MT30_TASKS}")

    _upstream.configure_rendering(render=False)
    _upstream.ensure_upstream_on_path()
    from envs import make_env

    cfg = _upstream.UpstreamCfg(task=task, obs="state", seed=seed, multitask=False)
    raw_env = make_env(cfg)

    # Optional shift wrapper hook (T101 will supply full shifts)
    if shift != "none":
        from datdmpc.envs.perturb import apply_perturbation
        raw_env = apply_perturbation(raw_env, shift)

    return SingleTaskMultitaskEnv(task, raw_env)


def evaluate(
    agent: DeviceAwareTDMPC2,
    task: str,
    episodes: int,
    seed: int,
    shift: str = "none",
    logger: RunLogger | None = None,
    tier: str = "T0",
    shard: str | None = None,
    max_steps: int | None = None,
) -> dict[str, Any]:
    """Evaluate frozen agent on a single task, logging each finished episode."""
    env = make_task_env(task, seed=seed, shift=shift)
    task_idx = MT30_TASKS.index(task)

    shift_type, _, shift_level = shift.partition(":")
    if not shift_level:
        shift_level = "0"

    ep_returns = []

    for ep_num in range(episodes):
        if logger is not None and logger.has_episode(ep_num):
            continue

        obs = env.reset()
        done = False
        ep_reward = 0.0
        step_count = 0
        t0_time = time.perf_counter()

        while not done:
            with torch.no_grad():
                action = agent.act(obs, t0=(step_count == 0), task=task_idx)
            obs, reward, done, info = env.step(action)
            ep_reward += float(reward)
            step_count += 1

            if max_steps is not None and step_count >= max_steps:
                done = True

        wall_time_s = time.perf_counter() - t0_time
        ep_returns.append(ep_reward)

        if logger is not None:
            logger.log_episode(
                episode=ep_num,
                ep_return=ep_reward,
                length=step_count,
                wall_time_s=wall_time_s,
                task=task,
                task_idx=task_idx,
                shift_type=shift_type,
                shift_level=shift_level,
                method="B0",
                seed=seed,
            )

    if logger is not None and len(logger.returns) > 0:
        all_returns = logger.returns
    else:
        all_returns = ep_returns

    if len(all_returns) > 0:
        mean_ret = float(np.mean(all_returns))
    else:
        mean_ret = 0.0

    return {
        "task": task,
        "n_episodes": len(all_returns),
        "mean_return": mean_ret,
    }


def run_smoke(ckpt: str | Path, task: str, steps: int, shift: str, seed: int) -> dict[str, float]:
    """Run full-mode smoke test: nominal and shifted rollouts with sec/step timing."""
    agent = load_agent(ckpt, device="cpu")
    env = make_task_env(task, seed=seed, shift="none")
    task_idx = MT30_TASKS.index(task)

    # Nominal steps
    obs = env.reset()
    t0 = time.perf_counter()
    for s in range(steps):
        with torch.no_grad():
            action = agent.act(obs, t0=(s == 0), task=task_idx)
        obs, _, done, _ = env.step(action)
        if done:
            obs = env.reset()
    sec_nominal = (time.perf_counter() - t0) / steps

    # Shifted steps
    env_shift = make_task_env(task, seed=seed, shift=shift)
    obs = env_shift.reset()
    t1 = time.perf_counter()
    for s in range(steps):
        with torch.no_grad():
            action = agent.act(obs, t0=(s == 0), task=task_idx)
        obs, _, done, _ = env_shift.step(action)
        if done:
            obs = env_shift.reset()
    sec_shifted = (time.perf_counter() - t1) / steps

    return {"sec_step_nominal": sec_nominal, "sec_step_shifted": sec_shifted}
