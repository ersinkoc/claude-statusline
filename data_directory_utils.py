#!/usr/bin/env python3
"""
Data Directory Utilities

Provides centralized data directory management for Claude Statusline components.
Ensures consistent use of .claude/data-statusline directory structure.
"""

import os
from pathlib import Path
from typing import Optional


def get_default_data_directory() -> Path:
    """
    Get the default data directory for Claude Statusline components.
    
    Priority order:
    1. ~/.claude/data-statusline (preferred)
    2. Current working directory / data (fallback)
    
    Returns:
        Path: The data directory path
    """
    try:
        # Try user's .claude directory first
        claude_dir = Path.home() / ".claude" / "data-statusline"
        
        # Check if .claude parent directory exists or can be created
        if claude_dir.parent.exists() or _can_create_directory(claude_dir.parent):
            # Ensure the data directory exists
            claude_dir.mkdir(parents=True, exist_ok=True)
            return claude_dir
            
    except (OSError, PermissionError):
        pass
    
    # Fallback to current working directory with .claude structure
    fallback_dir = Path.cwd() / ".claude" / "data-statusline"
    fallback_dir.mkdir(parents=True, exist_ok=True)
    return fallback_dir


def _can_create_directory(path: Path) -> bool:
    """
    Check if a directory can be created at the given path.
    
    Args:
        path: Directory path to check
        
    Returns:
        bool: True if directory can be created
    """
    try:
        # If it already exists, we can use it
        if path.exists():
            return True
            
        # Try to create and remove a test directory
        test_dir = path / ".test_write_permission"
        test_dir.mkdir(parents=True, exist_ok=True)
        test_dir.rmdir()
        return True
        
    except (OSError, PermissionError):
        return False


def resolve_data_directory(data_dir: Optional[Path] = None) -> Path:
    """
    Resolve the data directory to use, with optional override.
    
    Args:
        data_dir: Optional explicit data directory path
        
    Returns:
        Path: The resolved data directory path
    """
    if data_dir:
        # Explicit path provided, ensure it exists
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
    
    return get_default_data_directory()