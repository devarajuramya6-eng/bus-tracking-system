"""
CityBus Enterprise Platform - Repository Archive Packager
File: scripts/create_repo_zip.py

Creates a complete repository ZIP archive INCLUDING .git history,
excluding temporary virtualenvs, pycache, and build artifacts.
"""

import os
import zipfile
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PARENT_DIR = os.path.dirname(REPO_ROOT)
ZIP_NAME = "repo-with-history.zip"
TARGET_PARENT_ZIP = os.path.join(PARENT_DIR, ZIP_NAME)
TARGET_LOCAL_ZIP = os.path.join(REPO_ROOT, ZIP_NAME)

EXCLUDE_DIRS = {
    '.venv', '.venv_lock', 'node_modules', 'coverage', 'dist', 'build', '__pycache__', '.pytest_cache'
}
EXCLUDE_FILES = {
    'repo-with-history.zip', 'bus-tracking-system.zip', 'citybus.db'
}


def should_exclude(rel_path):
    parts = rel_path.replace('\\', '/').split('/')
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
        if part.endswith('.pyc'):
            return True
    filename = os.path.basename(rel_path)
    if filename in EXCLUDE_FILES or filename.endswith('.zip'):
        return True
    return False


def create_archive():
    print(f"Packaging repository from: {REPO_ROOT}")
    print(f"Output target: {TARGET_PARENT_ZIP}")

    total_files = 0
    total_bytes = 0
    has_git = False

    with zipfile.ZipFile(TARGET_PARENT_ZIP, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(REPO_ROOT):
            # Do not prune .git!
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, PARENT_DIR)
                repo_rel_path = os.path.relpath(full_path, REPO_ROOT)

                if should_exclude(repo_rel_path):
                    continue

                if '.git' in repo_rel_path.split(os.sep):
                    has_git = True

                zip_entry_path = rel_path.replace('\\', '/')
                zipf.write(full_path, zip_entry_path)
                total_files += 1
                total_bytes += os.path.getsize(full_path)

    print(f"Archive created successfully!")
    print(f"Total files archived: {total_files}")
    print(f"Uncompressed size: {total_bytes / (1024*1024):.2f} MB")
    print(f"Archive size: {os.path.getsize(TARGET_PARENT_ZIP) / (1024*1024):.2f} MB")
    print(f".git directory included: {has_git}")

    # Also copy to local target if needed
    with open(TARGET_PARENT_ZIP, 'rb') as sf, open(TARGET_LOCAL_ZIP, 'wb') as df:
        df.write(sf.read())
    print(f"Copied archive to local workspace: {TARGET_LOCAL_ZIP}")


if __name__ == '__main__':
    create_archive()
