#!/usr/bin/env python3
"""
First-run initialization for Claude Statusline.
Creates data directory, copies default configs, and optionally runs initial rebuild.
"""

import sys
import os
import shutil
from pathlib import Path
from typing import List

from .data_directory_utils import get_default_data_directory
from .safe_file_operations import safe_json_write


def is_initialized() -> bool:
    """Quick check if claude-statusline has been initialized.

    Returns True if data directory exists and has config or database files.
    Does not create any directories or files.
    """
    try:
        data_dir = Path.home() / ".claude" / "data-statusline"
        if not data_dir.exists():
            return False
        return (data_dir / "theme_config.json").exists() or (data_dir / "smart_sessions_db.json").exists()
    except (OSError, PermissionError):
        return False


class Initializer:
    """Handles first-run setup for claude-statusline."""

    def __init__(self):
        self.package_dir = Path(__file__).parent
        self.data_dir = get_default_data_directory()
        self.actions: List[str] = []

    def run(self) -> bool:
        """Run the full initialization sequence. Idempotent - safe to run multiple times."""
        print("=" * 50)
        print("  Claude Statusline - First Run Setup")
        print("=" * 50)
        print()

        self._ensure_data_directory()
        self._ensure_config("config.json")
        self._ensure_config("prices.json")
        self._ensure_theme_config()

        has_data = self._check_claude_data()
        if has_data:
            self._run_rebuild()
        else:
            print("[i] No Claude Code data found at ~/.claude/projects/")
            print("    Database will be built automatically when you start using Claude Code.")
            print()
            self.actions.append("Skipped rebuild (no Claude Code data yet)")

        if sys.platform == "win32":
            self._check_windows_path()

        self._print_summary()
        return True

    def _ensure_data_directory(self):
        """Log data directory (already created by get_default_data_directory)."""
        print(f"[+] Data directory: {self.data_dir}")
        self.actions.append(f"Data directory: {self.data_dir}")

    def _ensure_config(self, filename: str):
        """Copy a config file from package dir to data dir if not present."""
        target = self.data_dir / filename
        source = self.package_dir / filename

        if target.exists():
            print(f"[=] {filename} already exists")
            self.actions.append(f"{filename}: already exists")
            return

        if source.exists():
            shutil.copy2(str(source), str(target))
            print(f"[+] Copied default {filename}")
            self.actions.append(f"{filename}: copied defaults")
        else:
            print(f"[!] {filename} not found in package")
            self.actions.append(f"{filename}: not available")

    def _ensure_theme_config(self):
        """Create default theme_config.json if not present."""
        target = self.data_dir / "theme_config.json"

        if target.exists():
            print("[=] theme_config.json already exists")
            self.actions.append("theme_config.json: already exists")
            return

        safe_json_write({"current_theme": "nord", "rotation_enabled": False}, target)
        print("[+] Created theme_config.json (theme: nord)")
        self.actions.append("theme_config.json: created with 'nord' theme")

    def _check_claude_data(self) -> bool:
        """Check if Claude Code JSONL data exists."""
        claude_projects = Path.home() / ".claude" / "projects"
        if not claude_projects.exists():
            return False
        return any(claude_projects.rglob("*.jsonl"))

    def _run_rebuild(self):
        """Run initial database rebuild."""
        print("[~] Running initial database rebuild...")
        try:
            from .rebuild import DatabaseRebuilder
            rebuilder = DatabaseRebuilder(data_dir=self.data_dir)
            if rebuilder.rebuild_database():
                self.actions.append("Database rebuilt successfully")
            else:
                self.actions.append("Database rebuild completed (no data)")
        except Exception as e:
            print(f"[!] Rebuild warning: {e}")
            self.actions.append(f"Database rebuild failed: {e}")

    def _check_windows_path(self):
        """Check if scripts directory is in PATH on Windows."""
        try:
            scripts_dir = Path(sys.executable).parent / "Scripts"
            # Also check user-level scripts dir
            user_scripts = Path.home() / "AppData" / "Roaming" / "Python" / f"Python{sys.version_info.major}{sys.version_info.minor}" / "Scripts"

            path_dirs = os.environ.get("PATH", "").split(os.pathsep)
            in_path = any(
                Path(p).resolve() == scripts_dir.resolve() or
                (user_scripts.exists() and Path(p).resolve() == user_scripts.resolve())
                for p in path_dirs if p.strip()
            )
            if not in_path:
                print()
                print("[!] Windows PATH notice:")
                print(f"    Scripts directory not in PATH.")
                print(f"    Run this in PowerShell to fix:")
                print(f'    $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")')
                print(f"    Or restart your terminal after installation.")
                self.actions.append("PATH: scripts dir not in PATH")
        except (OSError, ValueError):
            pass

    def _print_summary(self):
        """Print summary of actions taken."""
        print()
        print("-" * 50)
        print("  Setup Complete")
        print("-" * 50)
        for action in self.actions:
            print(f"  - {action}")
        print()
        print("  Next steps:")
        print("    claude-statusline status   - Show current status")
        print("    claude-statusline theme    - Browse themes")
        print("    claude-statusline --help   - All commands")
        print()
