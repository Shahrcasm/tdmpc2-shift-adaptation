"""Shared pytest setup (owner: M1).

Makes ``src/`` importable even if ``pip install -e .`` has not been run, and turns MuJoCo
rendering off before any test imports ``mujoco`` or ``dm_control``.
"""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from datdmpc import _upstream  # noqa: E402

_upstream.configure_rendering(render=False)
