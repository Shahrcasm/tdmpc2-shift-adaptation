"""Dynamics-shift wrappers for DMControl tasks. Owner: M1 · Task: T101 (stub created in T001).

Contract (to implement in T101):

* Shift SPEC grammar: ``none`` or ``<type>:<level>`` with type in :data:`SHIFT_TYPES`.
  ``mass``/``friction``/``actuator``/``gravity`` levels are multiplicative scale factors,
  ``obs_noise`` is the std of Gaussian noise added to observations, ``action_delay`` is an
  integer number of agent steps.
* Physical shifts edit the MuJoCo model of the innermost dm_control env
  (``datdmpc._upstream.unwrap_dm_env(env).physics.model``: ``body_mass``,
  ``geom_friction``, ``actuator_gear``, ``opt.gravity``) and must be re-applied after any
  model reload; observation/action shifts wrap ``reset``/``step``.
* Shifts can be applied at episode start or injected mid-episode (needed by T303/T304).
* ``tests/test_perturb.py`` proves that each physical parameter actually changed.
"""

from __future__ import annotations

SHIFT_TYPES = ("mass", "friction", "actuator", "gravity", "obs_noise", "action_delay")


def parse_shift(spec: str):
    """Parse ``'mass:1.5'`` -> ``('mass', 1.5)``; ``'none'`` -> ``None``."""
    raise NotImplementedError("datdmpc.envs.perturb.parse_shift - task T101 (owner M1)")


def apply_shift(env, spec: str):
    """Return ``env`` with the shift ``spec`` applied (wrapping or editing physics)."""
    raise NotImplementedError("datdmpc.envs.perturb.apply_shift - task T101 (owner M1)")
