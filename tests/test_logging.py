"""Tests for datdmpc.eval.logging (Task T006, owner M1)."""

import csv
import json
from pathlib import Path

import yaml
from datdmpc.eval.logging import EPISODES_COLUMNS, RunLogger, make_run_id


def test_make_run_id():
    """Verify run_id format and colon-to-dash replacement."""
    run_id = make_run_id("checkpoints/mt30-5M.pt", "walker-walk", "mass:1.5", "B0", 0)
    assert run_id == "mt30-5M__walker-walk__mass-1.5__B0__seed0"
    assert ":" not in run_id


def test_logger_schema_and_resume(tmp_path):
    """Test full logging lifecycle: file creation, row flushing, and resume logic."""
    out_dir = tmp_path / "results"
    run_id = "test-ckpt__walker-walk__none__B0__seed0"
    config = {"task": "walker-walk", "episodes": 2, "seed": 0}

    # Session 1: run episodes 0 and 1
    logger = RunLogger(out_dir, run_id, config, tier="T0", device="cpu", resume=False)
    assert not logger.has_episode(0)
    logger.log_episode(
        episode=0,
        ep_return=150.5,
        length=500,
        wall_time_s=12.2,
        task="walker-walk",
    )
    logger.log_episode(
        episode=1,
        ep_return=250.0,
        length=500,
        wall_time_s=11.8,
        task="walker-walk",
    )
    summary = logger.finish()

    assert summary["n_episodes"] == 2
    assert summary["mean_return"] == 200.25

    # Check files exist
    run_dir = out_dir / run_id
    assert (run_dir / "config.yaml").is_file()
    assert (run_dir / "episodes.csv").is_file()
    assert (run_dir / "summary.json").is_file()
    assert (run_dir / "env.txt").is_file()
    assert (run_dir / "git_sha.txt").is_file()

    # Check CSV header and row count
    with open(run_dir / "episodes.csv", "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    assert reader[0] == EPISODES_COLUMNS
    assert len(reader) == 3  # header + 2 episodes

    # Session 2: Resume and run episode 2
    resumed = RunLogger(out_dir, run_id, config, tier="T0", device="cpu", resume=True)
    assert resumed.has_episode(0)
    assert resumed.has_episode(1)
    assert not resumed.has_episode(2)

    resumed.log_episode(
        episode=2,
        ep_return=300.0,
        length=500,
        wall_time_s=11.5,
        task="walker-walk",
    )
    resumed_summary = resumed.finish()

    assert resumed_summary["n_episodes"] == 3
    with open(run_dir / "episodes.csv", "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert len(rows) == 4  # header + 3 episodes
