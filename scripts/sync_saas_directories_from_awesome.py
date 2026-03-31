#!/usr/bin/env python3

import json
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    awesome_repo = repo_root.parent / "awesome-launch-list"
    source_path = awesome_repo / "data" / "saas-directories.json"
    target_path = repo_root / "public" / "data" / "directories.json"

    if not source_path.exists():
        raise FileNotFoundError(f"Source dataset not found: {source_path}")

    with source_path.open("r", encoding="utf-8") as source_file:
        source_data = json.load(source_file)

    directories = source_data.get("directories")
    if not isinstance(directories, list):
        raise ValueError("Source dataset is missing a valid 'directories' list")

    synced_payload = {
        "note": "Synced from ../awesome-launch-list/data/saas-directories.json. Edit the awesome-launch-list copy first.",
        "metadata": source_data.get("metadata", {}),
        "directories": directories,
    }

    with target_path.open("w", encoding="utf-8") as target_file:
        json.dump(synced_payload, target_file, indent=2, ensure_ascii=False)
        target_file.write("\n")

    print(f"Synced {len(directories)} directories")
    print(f"Source: {source_path}")
    print(f"Target: {target_path}")


if __name__ == "__main__":
    main()