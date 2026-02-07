#!/usr/bin/env python3
"""
Claude Statusline - Real-time session tracking and analytics for Claude Code

A comprehensive monitoring tool that provides real-time session information,
cost tracking, usage analytics, and customizable statusline displays for 
Claude Code sessions.
"""

__version__ = "2.0.0"
__author__ = "Ersin Koç"
__email__ = "ersinkoc@gmail.com"
__license__ = "MIT"

# Core imports
from .rebuild import DatabaseRebuilder
from .daemon import DaemonService
from .unified_powerline_system import UnifiedPowerlineSystem
from .statusline import StatuslineDisplay, main as statusline_main
from .model_utils import get_model_display_name, get_model_tier, is_claude_model

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",

    # Core classes
    "StatuslineDisplay",
    "DatabaseRebuilder",
    "DaemonService",
    "UnifiedPowerlineSystem",

    # Functions
    "statusline_main",

    # Model utilities
    "get_model_display_name",
    "get_model_tier",
    "is_claude_model",
]