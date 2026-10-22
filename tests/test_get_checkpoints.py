"""Tests for scripts/get_checkpoints.py and checkpoints/MANIFEST.csv (Task T005, owner M1)."""

import csv
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "checkpoints" / "MANIFEST.csv"
SCRIPT_PATH = REPO_ROOT / "scripts" / "get_checkpoints.py"


def test_manifest_format():
    """Verify MANIFEST.csv exists and has the required columns and models."""
    assert MANIFEST_PATH.is_file(), "checkpoints/MANIFEST.csv missing"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 2, f"Expected 2 rows in MANIFEST.csv, got {len(reader)}"
    names = {row["name"] for row in reader}
    assert "mt30-5M.pt" in names
    assert "mt30-19M.pt" in names
    for row in reader:
        assert int(row["size_bytes"]) > 0
        assert len(row["sha256"]) == 64
        assert row["url"].startswith("https://huggingface.co/")


def test_verify_real_checkpoints():
    """Run --verify-only on the real downloaded checkpoints."""
    cmd = [sys.executable, str(SCRIPT_PATH), "--models", "mt30-5M", "mt30-19M", "--verify-only"]
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert result.returncode == 0, f"Verify failed:\n{result.stderr}\n{result.stdout}"
    assert "OK (sha256 matches)" in result.stdout


def test_corrupted_file_fails(tmp_path):
    """Verify that a corrupted checkpoint causes the script to exit with code 1."""
    fake_dest = tmp_path / "checkpoints"
    fake_dest.mkdir()
    fake_ckpt = fake_dest / "mt30-5M.pt"
    fake_ckpt.write_bytes(b"corrupted bytes that do not match the real hash")

    cmd = [
        sys.executable,
        str(SCRIPT_PATH),
        "--models",
        "mt30-5M",
        "--dest",
        str(fake_dest),
        "--verify-only",
    ]
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert result.returncode == 1, "Script should have failed with exit code 1 on hash mismatch"
    assert "mismatch" in result.stderr or "mismatch" in result.stdout
