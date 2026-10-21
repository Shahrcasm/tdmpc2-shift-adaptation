"""Tests for scripts/smoke_test.py and the agreed CLI contracts of all stubs (owner: M1, T001)."""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


def _load_script(name):
    spec = importlib.util.spec_from_file_location(f"_script_{name}", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_smoke_tiny_runs_and_mass_changes(capsys):
    smoke = _load_script("smoke_test")
    assert smoke.main(["--mode", "tiny", "--steps", "5"]) == 0
    out = capsys.readouterr().out
    assert "[smoke] OK" in out and "mass_factor: 1.5" in out


def test_smoke_tiny_as_a_real_script():
    # Runs exactly like a person/CI does (scripts/ on sys.path[0]); guards the stdlib-`profile`
    # shadowing problem described in src/datdmpc/__init__.py.
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "smoke_test.py"), "--mode", "tiny", "--steps", "3"],
        cwd=REPO, capture_output=True, text=True, timeout=300,
    )
    assert result.returncode == 0, result.stderr[-3000:]
    assert "[smoke] OK" in result.stdout


def test_smoke_tiny_rejects_unsupported_shift():
    smoke = _load_script("smoke_test")
    with pytest.raises(SystemExit):
        smoke.main(["--mode", "tiny", "--steps", "2", "--shift", "friction:0.5"])


def test_smoke_full_fails_cleanly_without_checkpoint(tmp_path):
    smoke = _load_script("smoke_test")
    assert smoke.main(["--mode", "full", "--ckpt", str(tmp_path / "missing.pt")]) == 1


@pytest.mark.parametrize(
    "script",
    ["get_checkpoints", "smoke_test", "eval", "profile", "adapt", "detect", "build_registry", "make_figures"],
)
def test_every_script_has_help(script):
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / f"{script}.py"), "--help"],
        cwd=REPO, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout


@pytest.mark.parametrize("module", ["datdmpc.closed_loop", "datdmpc.diagnostics.ranking_fidelity"])
def test_module_entry_points_have_help(module):
    result = subprocess.run(
        [sys.executable, "-m", module, "--help"],
        cwd=REPO, capture_output=True, text=True, timeout=120,
        env={**__import__("os").environ, "PYTHONPATH": str(REPO / "src")},
    )
    assert result.returncode == 0, result.stderr


def test_stub_exits_with_not_implemented_code():
    from datdmpc import NOT_IMPLEMENTED_EXIT_CODE

    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "build_registry.py")],
        cwd=REPO, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == NOT_IMPLEMENTED_EXIT_CODE
    assert "T501" in result.stderr
