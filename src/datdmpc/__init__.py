"""DA-TDMPC2 — Detect-and-Adapt TD-MPC2 (CSE 465).

Package layout and ownership: see AGENTS.md. The vendored upstream TD-MPC2 code lives in
third_party/tdmpc2/ (read-only) and is reached through ``datdmpc._upstream``.
"""

import sys
from pathlib import Path

__version__ = "0.1.0"

# `python scripts/<name>.py` puts scripts/ first on sys.path. scripts/profile.py (name fixed by
# the repository layout) would then shadow the standard-library `profile` module, which
# `cProfile` imports - and `import torch._dynamo` (pulled in by tensordict) imports cProfile.
# Every script imports `datdmpc` before torch, so drop scripts/ from sys.path here.
# Scripts never import each other, so nothing else depends on that entry.
_SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"


def _is_scripts_dir(entry: str) -> bool:
    try:
        return bool(entry) and Path(entry).resolve() == _SCRIPTS_DIR
    except OSError:
        return False


sys.path[:] = [entry for entry in sys.path if not _is_scripts_dir(entry)]

#: Exit code used by every not-yet-implemented script or module entry point.
NOT_IMPLEMENTED_EXIT_CODE = 3


def not_implemented(what: str, task_id: str, owner: str) -> int:
    """Print a uniform 'not implemented yet' message to stderr and return the exit code.

    Stubs created in T001 call this so that ``--help`` already documents the agreed
    interface while running the command fails loudly until the owner implements it.
    """
    print(
        f"[datdmpc] {what} is not implemented yet - see task {task_id} (owner {owner}). "
        "The command-line interface above is the agreed contract.",
        file=sys.stderr,
    )
    return NOT_IMPLEMENTED_EXIT_CODE
