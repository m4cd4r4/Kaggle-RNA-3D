#!/usr/bin/env python3
"""Utility functions for Kaggle API operations."""

from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path
import os

COMPETITION_NAME = "stanford-rna-3d-folding-2"
DATA_DIR = Path(__file__).parent.parent / "data" / "raw"


def authenticate():
    """Authenticate with Kaggle API."""
    api = KaggleApi()
    api.authenticate()
    print("✓ Kaggle API authenticated")
    return api


def download_competition_data(force=False):
    """Download all competition data files."""
    api = authenticate()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading data to: {DATA_DIR}")
    api.competition_download_files(
        COMPETITION_NAME,
        path=str(DATA_DIR),
        force=force,
        quiet=False
    )
    print("✓ Download complete")


def list_data_files():
    """List all competition data files."""
    api = authenticate()

    files = api.competition_list_files(COMPETITION_NAME)

    print(f"\nCompetition: {COMPETITION_NAME}")
    print(f"Total files: {len(files)}")
    print("\nFiles:")
    print("-" * 60)

    for f in files[:20]:  # Show first 20
        size_mb = f.size / (1024 * 1024) if hasattr(f, 'size') else 0
        print(f"{f.name:40s} {size_mb:>10.2f} MB")

    if len(files) > 20:
        print(f"... and {len(files) - 20} more files")


def submit_predictions(submission_file, message="Submission"):
    """Submit predictions to the competition."""
    api = authenticate()

    if not Path(submission_file).exists():
        raise FileNotFoundError(f"Submission file not found: {submission_file}")

    print(f"Submitting: {submission_file}")
    print(f"Message: {message}")

    api.competition_submit(
        file_name=str(submission_file),
        message=message,
        competition=COMPETITION_NAME
    )
    print("✓ Submission complete")


def check_leaderboard(top_n=10):
    """Check current leaderboard standings."""
    api = authenticate()

    try:
        leaderboard = api.competition_leaderboard_view(COMPETITION_NAME)

        print(f"\nLeaderboard for {COMPETITION_NAME}")
        print("=" * 60)
        print(f"{'Rank':>5} {'Team':40s} {'Score':>10s}")
        print("-" * 60)

        for entry in leaderboard[:top_n]:
            print(f"{entry.teamRank:>5} {entry.teamName[:40]:40s} {entry.score:>10.4f}")

    except Exception as e:
        print(f"Unable to fetch leaderboard: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python kaggle_utils.py download     # Download competition data")
        print("  python kaggle_utils.py list         # List data files")
        print("  python kaggle_utils.py leaderboard  # Check leaderboard")
        print("  python kaggle_utils.py submit FILE  # Submit predictions")
        sys.exit(1)

    command = sys.argv[1]

    if command == "download":
        download_competition_data()
    elif command == "list":
        list_data_files()
    elif command == "leaderboard":
        check_leaderboard()
    elif command == "submit":
        if len(sys.argv) < 3:
            print("Error: Please provide submission file")
            sys.exit(1)
        submit_predictions(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
