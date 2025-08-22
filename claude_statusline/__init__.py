#!/usr/bin/env python3
"""
Claude Statusline - Real-time session tracking and analytics for Claude Code

A comprehensive monitoring tool that provides real-time session information,
cost tracking, usage analytics, and customizable statusline displays for 
Claude Code sessions.
"""

__version__ = "1.8.0"
__author__ = "Ersin Koç"
__email__ = "ersinkoc@gmail.com"
__license__ = "MIT"

# Core imports
from .rebuild import DatabaseRebuilder
from .daemon import DaemonService
from .unified_status import get_unified_status
from .unified_theme_system import UnifiedThemeSystem, THEME_SYSTEM
from .statusline import StatuslineDisplay, main as statusline_main

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
    "UnifiedThemeSystem",
    "THEME_SYSTEM",
    
    # Functions
    "statusline_main",
    "get_unified_status",
]