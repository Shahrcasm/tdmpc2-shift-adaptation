"""Unit tests for perturbation wrappers (Task T101, owner M1).

These tests verify:
1. `parse_shift` grammar parsing, validation, and error handling.
2. Physical parameter scaling (mass, friction, actuator, gravity) on both standard
   and custom DMControl tasks.
3. Factor 1.0 identity check.
4. Persistence across `env.reset()`.
5. Observation noise correctness.
6. Action delay FIFO timing correctness.
7. Mid-episode injection timing (steps before injection are identical).
"""

import gymnasium as gym
import numpy as np
import pytest
import torch

from datdmpc import _upstream
from datdmpc.envs.perturb import (
    PHYSICAL_SHIFT_TYPES,
    SHIFT_TYPES,
    ShiftedEnv,
    apply_shift,
    parse_shift,
)


# ---------------------------------------------------------------------------
# 1. Grammar and Parsing Tests
# ---------------------------------------------------------------------------


def test_parse_shift_none():
    """Verify 'none' produces None."""
    assert parse_shift("none") is None


@pytest.mark.parametrize("shift_type", SHIFT_TYPES)
def test_parse_shift_valid_types(shift_type):
    """Verify every valid shift type parses properly with valid levels."""
    if shift_type == "action_delay":
        spec = f"{shift_type}:3"
        result = parse_shift(spec)
        assert result == ("action_delay", 3)
    elif shift_type == "obs_noise":
        spec = f"{shift_type}:0.05"
        result = parse_shift(spec)
        assert result == ("obs_noise", 0.05)
    else:
        spec = f"{shift_type}:1.5"
        result = parse_shift(spec)
        assert result == (shift_type, 1.5)


def test_parse_shift_invalid_syntax():
    """Verify malformed strings without colons raise ValueError."""
    with pytest.raises(ValueError, match="Invalid shift specification"):
        parse_shift("invalid_spec_string")

    with pytest.raises(ValueError, match="Exactly one colon"):
        parse_shift("mass:1.5:extra")


def test_parse_shift_unknown_type():
    """Verify unknown shift types raise ValueError."""
    with pytest.raises(ValueError, match="Unknown shift type"):
        parse_shift("temperature:2.0")


def test_parse_shift_invalid_levels():
    """Verify invalid numeric values and negative physical values raise ValueError."""
    # Non-numeric levels
    with pytest.raises(ValueError):
        parse_shift("mass:abc")

    with pytest.raises(ValueError):
        parse_shift("action_delay:1.5")  # Delay must be integer

    # Out of range levels
    with pytest.raises(ValueError, match="positive"):
        parse_shift("mass:0.0")  # Mass must be > 0

    with pytest.raises(ValueError, match="positive"):
        parse_shift("mass:-1.0")

    with pytest.raises(ValueError, match="non-negative"):
        parse_shift("action_delay:-1")

    with pytest.raises(ValueError, match="non-negative"):
        parse_shift("obs_noise:-0.1")


# ---------------------------------------------------------------------------
# Helper to create test environments
# ---------------------------------------------------------------------------


def _make_raw_env(task: str, seed: int = 0):
    """Create a raw DMControl environment for testing."""
    _upstream.configure_rendering(render=False)
    _upstream.ensure_upstream_on_path()
    from envs import make_env

    cfg = _upstream.UpstreamCfg(task=task, obs="state", seed=seed, multitask=False)
    return make_env(cfg)


# ---------------------------------------------------------------------------
# 2. Physical Shift Tests: Standard and Custom Tasks
# ---------------------------------------------------------------------------

# One standard task ("walker-walk") and one custom task ("walker-walk-backwards")
DOMAINS = ["walker-walk", "walker-walk-backwards"]


@pytest.mark.parametrize("task", DOMAINS)
@pytest.mark.parametrize("shift_type", PHYSICAL_SHIFT_TYPES)
def test_physical_shifts_change_model(task, shift_type):
    """Verify that applying <type>:k (k != 1) scales the physical array by k."""
    raw_env = _make_raw_env(task, seed=42)
    dm_env = _upstream.unwrap_dm_env(raw_env)
    physics = dm_env.physics

    # Snapshot nominal values
    nominal_body_mass = physics.model.body_mass.copy()
    nominal_geom_friction = physics.model.geom_friction.copy()
    nominal_actuator_gear = physics.model.actuator_gear.copy()
    nominal_gravity = physics.model.opt.gravity.copy()

    factor = 1.75
    shifted_env = apply_shift(raw_env, f"{shift_type}:{factor}")

    # Check that the targeted array equals nominal * factor
    if shift_type == "mass":
        assert np.allclose(physics.model.body_mass, nominal_body_mass * factor)
    elif shift_type == "friction":
        assert np.allclose(physics.model.geom_friction, nominal_geom_friction * factor)
    elif shift_type == "actuator":
        assert np.allclose(physics.model.actuator_gear, nominal_actuator_gear * factor)
    elif shift_type == "gravity":
        assert np.allclose(physics.model.opt.gravity, nominal_gravity * factor)


@pytest.mark.parametrize("shift_type", PHYSICAL_SHIFT_TYPES)
def test_physical_shift_factor_one_is_identical(shift_type):
    """Verify that <type>:1.0 leaves the physical parameter identical to nominal."""
    raw_env = _make_raw_env("walker-walk", seed=42)
    dm_env = _upstream.unwrap_dm_env(raw_env)
    physics = dm_env.physics

    if shift_type == "mass":
        nominal = physics.model.body_mass.copy()
    elif shift_type == "friction":
        nominal = physics.model.geom_friction.copy()
    elif shift_type == "actuator":
        nominal = physics.model.actuator_gear.copy()
    else:
        nominal = physics.model.opt.gravity.copy()

    apply_shift(raw_env, f"{shift_type}:1.0")

    if shift_type == "mass":
        current = physics.model.body_mass
    elif shift_type == "friction":
        current = physics.model.geom_friction
    elif shift_type == "actuator":
        current = physics.model.actuator_gear
    else:
        current = physics.model.opt.gravity

    assert np.array_equal(current, nominal)


@pytest.mark.parametrize("shift_type", PHYSICAL_SHIFT_TYPES)
def test_physical_shift_persists_across_reset_and_steps(shift_type):
    """Verify physical changes survive env.reset() and persist through steps."""
    raw_env = _make_raw_env("walker-walk", seed=42)
    dm_env = _upstream.unwrap_dm_env(raw_env)
    physics = dm_env.physics

    factor = 1.5
    shifted_env = apply_shift(raw_env, f"{shift_type}:{factor}")

    if shift_type == "mass":
        nominal = shifted_env.nominal_body_mass
    elif shift_type == "friction":
        nominal = shifted_env.nominal_geom_friction
    elif shift_type == "actuator":
        nominal = shifted_env.nominal_actuator_gear
    else:
        nominal = shifted_env.nominal_gravity

    expected = nominal * factor

    # Reset environment and verify parameter persists
    shifted_env.reset()

    if shift_type == "mass":
        assert np.allclose(physics.model.body_mass, expected)
    elif shift_type == "friction":
        assert np.allclose(physics.model.geom_friction, expected)
    elif shift_type == "actuator":
        assert np.allclose(physics.model.actuator_gear, expected)
    else:
        assert np.allclose(physics.model.opt.gravity, expected)

    # Step environment and verify parameter persists
    action = torch.zeros(shifted_env.action_space.shape, dtype=torch.float32)
    for _ in range(3):
        shifted_env.step(action)

    if shift_type == "mass":
        assert np.allclose(physics.model.body_mass, expected)
    elif shift_type == "friction":
        assert np.allclose(physics.model.geom_friction, expected)
    elif shift_type == "actuator":
        assert np.allclose(physics.model.actuator_gear, expected)
    else:
        assert np.allclose(physics.model.opt.gravity, expected)


# ---------------------------------------------------------------------------
# 3. Observation Noise Tests
# ---------------------------------------------------------------------------


def test_obs_noise_zero_leaves_identical():
    """Verify obs_noise:0 leaves observations identical to nominal."""
    raw_env = _make_raw_env("walker-walk", seed=10)
    shifted_env = apply_shift(raw_env, "obs_noise:0.0", seed=10)

    obs = shifted_env.reset()
    action = torch.zeros(shifted_env.action_space.shape, dtype=torch.float32)
    step_obs, _, _, _ = shifted_env.step(action)

    # Compare against an unshifted env with the same seed
    nominal_env = _make_raw_env("walker-walk", seed=10)
    nom_obs = nominal_env.reset()
    nom_step_obs, _, _, _ = nominal_env.step(action)

    if torch.is_tensor(obs):
        assert torch.allclose(obs, nom_obs)
        assert torch.allclose(step_obs, nom_step_obs)
    else:
        assert np.allclose(obs, nom_obs)
        assert np.allclose(step_obs, nom_step_obs)


def test_obs_noise_positive_modifies_obs():
    """Verify obs_noise with std > 0 changes observations."""
    nominal_env = _make_raw_env("walker-walk", seed=10)
    nom_obs = nominal_env.reset()

    raw_env = _make_raw_env("walker-walk", seed=10)
    shifted_env = apply_shift(raw_env, "obs_noise:0.1", seed=10)
    noisy_obs = shifted_env.reset()

    if torch.is_tensor(noisy_obs):
        diff = torch.abs(noisy_obs - nom_obs).max().item()
    else:
        diff = np.abs(noisy_obs - nom_obs).max()

    assert diff > 0.0, "Observation noise should have modified the observation"


# ---------------------------------------------------------------------------
# 4. Action Delay Tests
# ---------------------------------------------------------------------------


class MockActionTrackingEnv(gym.Env):
    """Simple mock environment to record the exact actions passed to step()."""

    def __init__(self, action_dim=2):
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(action_dim,))
        self.observation_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(4,))
        self.recorded_actions = []

        # Provide a minimal mock physics object to satisfy unwrap_dm_env
        class MockModel:
            body_mass = np.ones(5)
            geom_friction = np.ones((5, 3))
            actuator_gear = np.ones((5, 6))

            class MockOpt:
                gravity = np.array([0.0, 0.0, -9.81])

            opt = MockOpt()

        class MockPhysics:
            model = MockModel()

        self.physics = MockPhysics()

    def reset(self, **kwargs):
        self.recorded_actions.clear()
        return np.zeros(4, dtype=np.float32)

    def step(self, action):
        self.recorded_actions.append(np.array(action).copy())
        return np.zeros(4, dtype=np.float32), 0.0, False, {}


def test_action_delay_timing():
    """Verify action_delay:d makes action at step t equal action issued at step t - d."""
    mock_env = MockActionTrackingEnv(action_dim=2)
    delay_steps = 2
    delayed_env = ShiftedEnv(mock_env, spec=f"action_delay:{delay_steps}")
    delayed_env.reset()

    # Issue distinct actions: a0=[1,1], a1=[2,2], a2=[3,3], a3=[4,4]
    actions = [
        np.array([1.0, 1.0], dtype=np.float32),
        np.array([2.0, 2.0], dtype=np.float32),
        np.array([3.0, 3.0], dtype=np.float32),
        np.array([4.0, 4.0], dtype=np.float32),
    ]

    for act in actions:
        delayed_env.step(act)

    recorded = mock_env.recorded_actions
    assert len(recorded) == 4

    # Step 0 (t=0): Buffer has 0s, action applied must be zeros
    assert np.allclose(recorded[0], [0.0, 0.0])
    # Step 1 (t=1): Buffer still has 0s, action applied must be zeros
    assert np.allclose(recorded[1], [0.0, 0.0])
    # Step 2 (t=2): Action applied must be actions[2 - 2] = actions[0] = [1, 1]
    assert np.allclose(recorded[2], actions[0])
    # Step 3 (t=3): Action applied must be actions[3 - 2] = actions[1] = [2, 2]
    assert np.allclose(recorded[3], actions[1])


# ---------------------------------------------------------------------------
# 5. Mid-Episode Injection Tests
# ---------------------------------------------------------------------------


def test_mid_episode_injection_preserves_earlier_steps():
    """Verify steps before t_inject are completely identical to nominal."""
    seed = 42
    action = torch.tensor([0.2, -0.3, 0.1, 0.0, 0.5, -0.1], dtype=torch.float32)

    # 1. Run nominal environment for 5 steps
    nom_env = _make_raw_env("walker-walk", seed=seed)
    nom_env.reset()
    nom_obs_list = []
    for _ in range(5):
        obs, _, _, _ = nom_env.step(action)
        if torch.is_tensor(obs):
            nom_obs_list.append(obs.cpu().numpy().copy())
        else:
            nom_obs_list.append(obs.copy())

    # 2. Run shifted environment with injection at step 3
    raw_env = _make_raw_env("walker-walk", seed=seed)
    injected_env = apply_shift(raw_env, "mass:2.0", inject_at=3)
    injected_env.reset()

    injected_obs_list = []
    for _ in range(5):
        obs, _, _, _ = injected_env.step(action)
        if torch.is_tensor(obs):
            injected_obs_list.append(obs.cpu().numpy().copy())
        else:
            injected_obs_list.append(obs.copy())

    # Steps 0, 1, 2 (before step 3) must be 100% identical
    for step_idx in range(3):
        diff = np.max(np.abs(injected_obs_list[step_idx] - nom_obs_list[step_idx]))
        assert diff == 0.0, f"Step {step_idx} differed before injection point!"

    # Step 3 and beyond must differ because mass doubled
    step3_diff = np.max(np.abs(injected_obs_list[3] - nom_obs_list[3]))
    assert step3_diff > 0.0, "Step 3 should have diverged after injection!"
