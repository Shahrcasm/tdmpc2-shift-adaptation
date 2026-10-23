"""Download released TD-MPC2 multitask checkpoints and verify them. Owner: M1 · Task: T005 (stub from T001).

Source: https://huggingface.co/nicklashansen/tdmpc2/resolve/main/multitask/<name>.pt
Writes/updates checkpoints/MANIFEST.csv with columns name,size_bytes,sha256,url and verifies
every file's sha256 against the value published by Hugging Face (see docs/RUNS.md).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import urllib.request
from pathlib import Path

try:
    import datdmpc  # noqa: F401
except ImportError:  # package not installed with `pip install -e .` yet
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from datdmpc import not_implemented


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--models", nargs="+", required=True, help="e.g. mt30-5M mt30-19M")
    p.add_argument("--dest", default="checkpoints", help="download folder (gitignored)")
    p.add_argument("--verify-only", action="store_true", help="only re-check sha256 of existing files")
    return p

def compute_sha256(path: Path) -> str:
    """Compute the SHA-256 hash of a file by reading 64 KB chunks."""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest().lower()


def load_manifest(manifest_path: Path) -> dict[str, dict]:
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest not found at {manifest_path}")
    records = {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records[row["name"].replace(".pt", "")] = row
            records[row["name"]] = row
    return records


def download_file(url: str, dest: Path) -> None:
    print(f"[get_checkpoints] Downloading from {url}...")
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    print(f"[get_checkpoints] Saved to {dest}")


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    dest_dir = Path(args.dest)
    manifest_path = Path("checkpoints/MANIFEST.csv")
    manifest = load_manifest(manifest_path)

    for model_name in args.models:
        if model_name not in manifest:
            print(f"[get_checkpoints] ERROR: Unknown model '{model_name}'. Available: mt30-5M, mt30-19M", file=sys.stderr)
            return 1

        info = manifest[model_name]
        filename = info["name"]
        expected_hash = info["sha256"].lower()
        target_path = dest_dir / filename

        if args.verify_only or target_path.is_file():
            if not target_path.is_file():
                print(f"[get_checkpoints] ERROR: File missing for verification: {target_path}", file=sys.stderr)
                return 1
            print(f"[get_checkpoints] Verifying sha256 for {filename}...")
            actual_hash = compute_sha256(target_path)
            if actual_hash != expected_hash:
                print(f"[get_checkpoints] FAILED: sha256 mismatch for {filename}!", file=sys.stderr)
                print(f"  Expected: {expected_hash}", file=sys.stderr)
                print(f"  Actual:   {actual_hash}", file=sys.stderr)
                return 1
            print(f"[get_checkpoints] {filename}: OK (sha256 matches)")
        else:
            download_file(info["url"], target_path)
            print(f"[get_checkpoints] Verifying sha256 for downloaded {filename}...")
            actual_hash = compute_sha256(target_path)
            if actual_hash != expected_hash:
                print(f"[get_checkpoints] FAILED: sha256 mismatch for downloaded {filename}!", file=sys.stderr)
                return 1
            print(f"[get_checkpoints] {filename}: OK (verified)")

    print("[get_checkpoints] All requested checkpoints are present and verified.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
