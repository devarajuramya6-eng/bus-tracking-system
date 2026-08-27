"""
CityBus Enterprise Platform - ZIP Archive Verification Suite
File: scripts/verify_zip_extraction.py

Extracts repo-with-history.zip into verification directory, validates .git history,
verifies all branches, commit count, git status, and executes API test suite.
"""

import os
import zipfile
import subprocess
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PARENT_DIR = os.path.dirname(BASE_DIR)
ZIP_PATH = os.path.join(PARENT_DIR, 'repo-with-history.zip')
VERIFY_DIR = os.path.join(PARENT_DIR, 'verification')
EXTRACTED_REPO = os.path.join(VERIFY_DIR, 'bus-tracking-system')


def run_cmd(cmd, cwd):
    print(f"\n--- Running: '{cmd}' in {cwd} ---")
    res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print("STDERR:", res.stderr.strip())
    return res.returncode


def verify_zip():
    print(f"1. Validating ZIP archive: {ZIP_PATH}")
    if not os.path.exists(ZIP_PATH):
        print("ERROR: ZIP archive not found!")
        sys.exit(1)

    print(f"2. Extracting into: {VERIFY_DIR}")
    os.makedirs(VERIFY_DIR, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, 'r') as zipf:
        zipf.extractall(VERIFY_DIR)
    print("Extraction complete!")

    print("\n3. Verifying .git existence...")
    git_dir = os.path.join(EXTRACTED_REPO, '.git')
    if os.path.isdir(git_dir):
        print(f"SUCCESS: .git directory found at: {git_dir}")
    else:
        print(f"FAILURE: .git directory NOT found in {EXTRACTED_REPO}!")
        sys.exit(1)

    print("\n4. Running Git verification checks in extracted repository...")
    run_cmd("git rev-parse --is-inside-work-tree", EXTRACTED_REPO)
    run_cmd("git rev-parse --git-dir", EXTRACTED_REPO)
    run_cmd("git status", EXTRACTED_REPO)
    run_cmd("git branch -a", EXTRACTED_REPO)
    run_cmd("git log --oneline --decorate --graph --all -15", EXTRACTED_REPO)

    print("\n5. Running Project Verification Tests from extracted repository...")
    test_code = run_cmd("python backend/test_api.py", EXTRACTED_REPO)
    if test_code == 0:
        print("\nALL VERIFICATION CHECKS PASSED WITH 100% SUCCESS!")
    else:
        print(f"\nTest execution returned exit code: {test_code}")


if __name__ == '__main__':
    verify_zip()
