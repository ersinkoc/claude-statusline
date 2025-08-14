#!/usr/bin/env python3
"""
Claude Statusline - Real-time session tracking and analytics for Claude Code

A comprehensive monitoring tool that provides real-time session information,
cost tracking, usage analytics, and customizable statusline displays for 
Claude Code sessions.
"""

__version__ = "1.3.3"
__author__ = "Ersin Koç"
__email__ = "ersinkoc@gmail.com"
__license__ = "MIT"

# Core imports (only import what actually exists)
from .statusline import StatuslineDisplay, main as statusline_main
from .daemon import UnifiedDaemon  
from .rebuild import DatabaseRebuilder
from .formatter import SimpleVisualFormatter
from .templates import StatuslineTemplates

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    
    # Core classes
    "StatuslineDisplay",
    "UnifiedDaemon",
    "DatabaseRebuilder",
    "SimpleVisualFormatter",
    "StatuslineTemplates",
    
    # Functions
    "statusline_main",
]