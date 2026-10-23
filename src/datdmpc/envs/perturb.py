"""Dynamics-shift wrappers for DMControl tasks. Owner: M1 · Task: T101.

This module provides wrappers and utilities to perturb the dynamics, observations,
or action timing of DMControl environments for TD-MPC2.

Shift Grammar:
    "none"          -> No shift applied (nominal environment).
    "<type>:<level>" -> Perturbation specified by type and level.

Allowed Types:
    - "mass": Multiplicative scaling of body masses (physics.model.body_mass).
    - "friction": Multiplicative scaling of surface friction (physics.model.geom_friction).
    - "actuator": Multiplicative scaling of actuator gear ratios (physics.model.actuator_gear).
    - "gravity": Multiplicative scaling of gravitational acceleration (physics.model.opt.gravity).
    - "obs_noise": Standard deviation of additive Gaussian noise on observations.
    - "action_delay": Integer number of agent decision steps to delay actions.
"""

from __future__ import annotations

from typing import Any
import collections
import gymnasium as gym
import numpy as np
import torch

from datdmpc import _upstream

# List of valid shift types
SHIFT_TYPES = ("mass", "friction", "actuator", "gravity", "obs_noise", "action_delay")
PHYSICAL_SHIFT_TYPES = ("mass", "friction", "actuator", "gravity")


def parse_shift(spec: str) -> tuple[str, float | int] | None:
    """Parse a shift specification string into a validated tuple.

    Args:
        spec: Shift string such as 'none', 'mass:1.5', or 'action_delay:2'.

    Returns:
        None if spec is 'none', or a tuple (shift_type, shift_level).

    Raises:
        ValueError: If spec has an invalid format, unknown type, or invalid level.
    """
    if spec == "none":
        return None

    if ":" not in spec:
        raise ValueError(
            f"Invalid shift specification {spec!r}. Format must be 'none' or '<type>:<level>'."
        )

    parts = spec.split(":")
    if len(parts) != 2:
        raise ValueError(
            f"Invalid shift specification {spec!r}. Exactly one colon ':' is expected."
        )

    shift_type = parts[0].strip()
    level_str = parts[1].strip()

    if shift_type not in SHIFT_TYPES:
        raise ValueError(
            f"Unknown shift type {shift_type!r}. Allowed types are: {SHIFT_TYPES}."
        )

    if shift_type == "action_delay":
        try:
            delay_steps = int(level_str)
        except ValueError:
            raise ValueError(
                f"Shift level for 'action_delay' must be an integer, got {level_str!r}."
            )
        if delay_steps < 0:
            raise ValueError(
                f"Shift level for 'action_delay' must be non-negative (>= 0), got {delay_steps}."
            )
        return (shift_type, delay_steps)

    elif shift_type == "obs_noise":
        try:
            noise_std = float(level_str)
        except ValueError:
            raise ValueError(
                f"Shift level for 'obs_noise' must be a float, got {level_str!r}."
            )
        if noise_std < 0.0:
            raise ValueError(
                f"Shift level for 'obs_noise' must be non-negative (>= 0.0), got {noise_std}."
            )
        return (shift_type, noise_std)

    else:
        # Physical shifts: mass, friction, actuator, gravity
        try:
            scale_factor = float(level_str)
        except ValueError:
            raise ValueError(
                f"Shift level for {shift_type!r} must be a float, got {level_str!r}."
            )
        if scale_factor <= 0.0:
            raise ValueError(
                f"Shift level for physical shift {shift_type!r} must be positive (> 0.0), got {scale_factor}."
            )
        return (shift_type, scale_factor)


class ShiftedEnv(gym.Wrapper):
    """Gym wrapper that applies dynamics, observation, or action shifts to an environment.

    Supports both episode-start perturbation and mid-episode injection at step `inject_at`.
    """

    def __init__(
        self,
        env: gym.Env,
        spec: str,
        inject_at: int | None = None,
        seed: int | None = None,
    ) -> None:
        super().__init__(env)
        self.shift_spec = spec
        self.parsed = parse_shift(spec)
        self.inject_at = inject_at
        self.seed = seed

        if self.parsed is None:
            self.shift_type = None
            self.shift_level = None
        else:
            self.shift_type = self.parsed[0]
            self.shift_level = self.parsed[1]

        # Find innermost dm_control environment to access MuJoCo physics model
        self.dm_env = _upstream.unwrap_dm_env(env)
        self.physics = self.dm_env.physics

        # Save copies of nominal physics arrays so we can restore or compare them
        self.nominal_body_mass = self.physics.model.body_mass.copy()
        self.nominal_geom_friction = self.physics.model.geom_friction.copy()
        self.nominal_actuator_gear = self.physics.model.actuator_gear.copy()
        self.nominal_gravity = self.physics.model.opt.gravity.copy()

        # Step counter within the current episode
        self.step_count = 0
        self.physical_shift_applied = False

        # Queue for action delays
        self.delay_queue: collections.deque = collections.deque()

        # Random generator for observation noise
        self.rng = np.random.default_rng(seed)

        # If shift is immediate (inject_at is None or <= 0), apply physical shift now
        if self._should_apply_at_start():
            if self.shift_type in PHYSICAL_SHIFT_TYPES:
                self._apply_physical_shift()

    def _should_apply_at_start(self) -> bool:
        """Return True if shift should be active right from the start of the episode."""
        if self.shift_type is None:
            return False
        if self.inject_at is None:
            return True
        if self.inject_at <= 0:
            return True
        return False

    def _is_shift_active(self) -> bool:
        """Return True if the shift is currently active at this step."""
        if self.shift_type is None:
            return False
        if self._should_apply_at_start():
            return True
        return self.step_count >= self.inject_at

    def _apply_physical_shift(self) -> None:
        """Scale the targeted MuJoCo parameter by the shift level."""
        factor = float(self.shift_level)
        if self.shift_type == "mass":
            self.physics.model.body_mass[:] = self.nominal_body_mass * factor
        elif self.shift_type == "friction":
            self.physics.model.geom_friction[:] = self.nominal_geom_friction * factor
        elif self.shift_type == "actuator":
            self.physics.model.actuator_gear[:] = self.nominal_actuator_gear * factor
        elif self.shift_type == "gravity":
            self.physics.model.opt.gravity[:] = self.nominal_gravity * factor
        self.physical_shift_applied = True

    def _restore_nominal_physics(self) -> None:
        """Restore all MuJoCo parameters to their original nominal values."""
        self.physics.model.body_mass[:] = self.nominal_body_mass
        self.physics.model.geom_friction[:] = self.nominal_geom_friction
        self.physics.model.actuator_gear[:] = self.nominal_actuator_gear
        self.physics.model.opt.gravity[:] = self.nominal_gravity
        self.physical_shift_applied = False

    def reset(self, **kwargs) -> Any:
        """Reset the environment, step counter, and shift state."""
        self.step_count = 0

        # Reset delay queue
        self.delay_queue.clear()
        if self.shift_type == "action_delay":
            delay_steps = int(self.shift_level)
            for _ in range(delay_steps):
                self.delay_queue.append(None)

        # Handle physical parameter reset
        if self._should_apply_at_start():
            if self.shift_type in PHYSICAL_SHIFT_TYPES:
                # Re-apply physical shift so it persists across resets
                self._apply_physical_shift()
        else:
            # Mid-episode injection: start episode in nominal state
            self._restore_nominal_physics()

        obs = self.env.reset(**kwargs)

        # If observation noise is active at reset, add noise to initial observation
        if self._is_shift_active() and self.shift_type == "obs_noise":
            obs = self._add_obs_noise(obs)

        return obs

    def step(self, action: Any) -> tuple[Any, float, bool, dict[str, Any]]:
        """Take a step, handling mid-episode injection, action delays, and noise."""
        # Mid-episode injection check
        if self.inject_at is not None and self.step_count == self.inject_at:
            if self.shift_type in PHYSICAL_SHIFT_TYPES:
                self._apply_physical_shift()

        # Handle action delay
        if self._is_shift_active() and self.shift_type == "action_delay":
            delay_steps = int(self.shift_level)
            if delay_steps == 0:
                action_to_apply = action
            else:
                self.delay_queue.append(action)
                delayed_action = self.delay_queue.popleft()
                if delayed_action is None:
                    # Before buffer has real actions, apply zero action
                    if torch.is_tensor(action):
                        action_to_apply = torch.zeros_like(action)
                    else:
                        action_to_apply = np.zeros_like(action)
                else:
                    action_to_apply = delayed_action
        else:
            action_to_apply = action

        obs, reward, done, info = self.env.step(action_to_apply)

        # Handle observation noise
        if self._is_shift_active() and self.shift_type == "obs_noise":
            obs = self._add_obs_noise(obs)

        self.step_count += 1
        return obs, reward, done, info

    def _add_obs_noise(self, obs: Any) -> Any:
        """Add zero-mean Gaussian noise to observation with std = shift_level."""
        std = float(self.shift_level)
        if std == 0.0:
            return obs

        if torch.is_tensor(obs):
            noise_np = self.rng.normal(loc=0.0, scale=std, size=obs.shape).astype(np.float32)
            noise_tensor = torch.from_numpy(noise_np).to(device=obs.device, dtype=obs.dtype)
            return obs + noise_tensor
        else:
            noise_np = self.rng.normal(loc=0.0, scale=std, size=obs.shape).astype(obs.dtype)
            return obs + noise_np


def apply_shift(
    env: gym.Env,
    spec: str,
    inject_at: int | None = None,
    seed: int | None = None,
) -> gym.Env:
    """Apply shift specification to an environment.

    Args:
        env: The environment to wrap.
        spec: Shift string (e.g., 'none', 'mass:1.5', 'friction:0.5').
        inject_at: Optional agent step at which to inject the shift mid-episode.
        seed: Optional random seed for observation noise.

    Returns:
        The wrapped ShiftedEnv (or original env if spec is 'none' and inject_at is None).
    """
    if spec == "none" and inject_at is None:
        return env
    return ShiftedEnv(env=env, spec=spec, inject_at=inject_at, seed=seed)


# Alias so existing callers can use either name
apply_perturbation = apply_shift
