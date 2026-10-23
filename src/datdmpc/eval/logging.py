"""Resume-safe per-episode result logging. Owner: M1 · Task: T006."""

from __future__ import annotations

import csv
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import yaml

EPISODES_COLUMNS = [
    "run_id",
    "task",
    "task_idx",
    "shift_type",
    "shift_level",
    "method",
    "seed",
    "episode",
    "return",
    "length",
    "wall_time_s",
    "tier",
    "shard",
    "timestamp",
]


def make_run_id(ckpt: str | Path, task: str, shift: str, method: str, seed: int | str) -> str:
    """Format: <ckpt-stem>__<task>__<shift>__<method>__seed<seed> with ':' -> '-'."""
    ckpt_stem = Path(ckpt).stem
    shift_str = str(shift).replace(":", "-")
    raw = f"{ckpt_stem}__{task}__{shift_str}__{method}__seed{seed}"
    return raw.replace(":", "-")


def _get_git_sha() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return "unknown"


def _gather_env_info(tier: str, device: str) -> str:
    lines = [
        f"os: {platform.system()} {platform.release()} ({platform.version()})",
        f"cpu: {platform.processor() or platform.machine()}",
        f"python: {sys.version.split()[0]}",
        f"tier: {tier}",
        f"device: {device}",
    ]
    for pkg in ("torch", "numpy", "mujoco", "dm_control", "tensordict"):
        try:
            mod = __import__(pkg)
            lines.append(f"{pkg}: {getattr(mod, '__version__', 'unknown')}")
        except ImportError:
            lines.append(f"{pkg}: missing")
    return "\n".join(lines) + "\n"


class RunLogger:
    """Writes results schema: config.yaml, episodes.csv, summary.json, env.txt, git_sha.txt."""

    def __init__(
        self,
        out_dir: str | Path,
        run_id: str,
        config: dict[str, Any],
        tier: str = "T0",
        device: str = "cpu",
        shard: str | None = None,
        resume: bool = False,
    ) -> None:
        self.run_id = run_id
        self.tier = tier
        self.device = device
        self.shard = shard or "1/1"
        self.run_dir = Path(out_dir) / run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)

        self.episodes_file = self.run_dir / "episodes.csv"
        self.summary_file = self.run_dir / "summary.json"
        self.config_file = self.run_dir / "config.yaml"
        self.env_file = self.run_dir / "env.txt"
        self.git_file = self.run_dir / "git_sha.txt"

        self.completed_episodes: set[int] = set()
        self.returns: list[float] = []

        # If resume, read finished episodes from existing CSV
        if resume and self.episodes_file.is_file():
            with open(self.episodes_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        ep = int(row["episode"])
                        ret = float(row["return"])
                        self.completed_episodes.add(ep)
                        self.returns.append(ret)
                    except (ValueError, KeyError):
                        continue

        # Write or update metadata files
        if not self.config_file.is_file() or not resume:
            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.safe_dump(config, f, default_flow_style=False)

        if not self.env_file.is_file():
            self.env_file.write_text(_gather_env_info(tier, device), encoding="utf-8")

        if not self.git_file.is_file():
            self.git_file.write_text(_get_git_sha() + "\n", encoding="utf-8")

        # Initialize CSV header if file is empty or does not exist
        if not self.episodes_file.is_file() or self.episodes_file.stat().st_size == 0:
            with open(self.episodes_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(EPISODES_COLUMNS)

    def has_episode(self, episode_idx: int) -> bool:
        """Return True if episode_idx is already logged and flushed."""
        return episode_idx in self.completed_episodes

    def log_episode(
        self,
        episode: int,
        ep_return: float,
        length: int,
        wall_time_s: float,
        task: str,
        task_idx: int = 0,
        shift_type: str = "none",
        shift_level: float | str = 0.0,
        method: str = "B0",
        seed: int = 0,
    ) -> None:
        """Append one finished episode to episodes.csv and flush immediately."""
        now_iso = datetime.now(timezone.utc).isoformat()
        row = [
            self.run_id,
            task,
            task_idx,
            shift_type,
            shift_level,
            method,
            seed,
            episode,
            round(float(ep_return), 4),
            int(length),
            round(float(wall_time_s), 4),
            self.tier,
            self.shard,
            now_iso,
        ]

        with open(self.episodes_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
            f.flush()

        self.completed_episodes.add(episode)
        self.returns.append(float(ep_return))

    def finish(self, extra: dict[str, Any] | None = None) -> dict[str, Any]:
        """Compute mean return, CI95, write summary.json, and return summary dict."""
        num_episodes = len(self.returns)

        if num_episodes > 0:
            returns_array = np.array(self.returns, dtype=np.float64)
            mean = float(np.mean(returns_array))
        else:
            returns_array = np.array([0.0], dtype=np.float64)
            mean = 0.0

        # Calculate 95% confidence interval using standard error of the mean
        if num_episodes > 1:
            std_err = float(np.std(returns_array, ddof=1) / np.sqrt(num_episodes))
            ci95_low = mean - 1.96 * std_err
            ci95_high = mean + 1.96 * std_err
        else:
            ci95_low = mean
            ci95_high = mean

        summary = {
            "run_id": self.run_id,
            "n_episodes": num_episodes,
            "mean_return": round(mean, 4),
            "ci95_low": round(ci95_low, 4),
            "ci95_high": round(ci95_high, 4),
            "tier": self.tier,
            "shard": self.shard,
        }
        if extra:
            summary.update(extra)

        with open(self.summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        return summary
