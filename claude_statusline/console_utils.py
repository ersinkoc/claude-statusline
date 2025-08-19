#!/usr/bin/env python3
"""
Console Utilities for Claude Statusline System

Provides cross-platform console output handling, particularly for Windows
systems that may not support Unicode emojis properly.

Key Features:
- Safe Unicode printing with fallbacks
- Emoji to ASCII conversion
- Platform detection
- Console encoding detection
"""

import sys
import platform
from typing import Dict, Any

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        BLACK = WHITE = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = ''
        LIGHTBLACK_EX = LIGHTWHITE_EX = LIGHTRED_EX = LIGHTGREEN_EX = ''
        LIGHTYELLOW_EX = LIGHTBLUE_EX = LIGHTMAGENTA_EX = LIGHTCYAN_EX = ''
        RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''


class SafeConsoleOutput:
    """
    Safe console output handler with Unicode fallbacks
    """
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.emoji_fallbacks = {
            '🟢': 'LIVE',
            '🔵': 'NEW',
            '🟡': 'TRACK',
            '🔄': 'DB', 
            '🔴': 'EXPIRED',
            '💤': 'SLEEP',
            '⚠️': 'WARNING',
            '❌': 'ERROR',
            '✅': 'OK',
            '🧠': 'OPUS',
            '🎭': 'SONNET',
            '⚡': 'HAIKU',
            '🤖': 'AI',
            '💰': '$',
            '⏰': 'TIME',
            '⏱️': '',  # Timer emoji - just remove it
            '⏱': '',   # Alternative timer
            '🎯': 'TARGET',
            '📊': 'REPORT',
            '🏥': 'HEALTH',
            '🚨': 'ISSUES',
            '🔧': 'FIXES',
            '💡': 'TIPS',
            '📈': 'STATS',
            '🔍': 'SEARCH',
            '⭐': 'STAR',
            '🎉': 'SUCCESS',
            '🚀': 'LAUNCH',
            '📋': 'LIST',
            '📦': 'PACKAGE',
            '⚙️': 'CONFIG',
            '🔗': 'LINK',
            'ℹ️': 'INFO',
            '❓': '?',
            '🛑': 'STOP',
            '🧹': 'CLEAN',
            '🌿': 'GIT',
            '👑': 'ADMIN'
        }
    
    def safe_print(self, text: str, end: str = '\n', flush: bool = False):
        """
        Print text with safe Unicode handling
        
        Args:
            text: Text to print
            end: End character (default newline)
            flush: Whether to flush output buffer
        """
        try:
            print(text, end=end, flush=flush)
        except UnicodeEncodeError:
            # Convert emojis to ASCII fallbacks
            safe_text = self._convert_emojis_to_ascii(text)
            try:
                print(safe_text, end=end, flush=flush)
            except UnicodeEncodeError:
                # Last resort: strip all non-ASCII characters
                ascii_text = safe_text.encode('ascii', 'ignore').decode('ascii')
                print(ascii_text, end=end, flush=flush)
    
    def _convert_emojis_to_ascii(self, text: str) -> str:
        """Convert Unicode emojis to ASCII alternatives"""
        for emoji, fallback in self.emoji_fallbacks.items():
            text = text.replace(emoji, fallback)
        return text
    
    def format_for_console(self, text: str) -> str:
        """
        Format text for safe console display
        
        Args:
            text: Text to format
            
        Returns:
            Console-safe text
        """
        try:
            # Try encoding to the console's encoding
            if sys.stdout.encoding:
                text.encode(sys.stdout.encoding)
            return text
        except (UnicodeEncodeError, AttributeError):
            return self._convert_emojis_to_ascii(text)
    
    def is_unicode_supported(self) -> bool:
        """Check if console supports Unicode output"""
        try:
            test_text = "🟢 Test"
            test_text.encode(sys.stdout.encoding or 'utf-8')
            return True
        except (UnicodeEncodeError, AttributeError):
            return False


# Global console output handler
console = SafeConsoleOutput()


def safe_print(text: str, end: str = '\n', flush: bool = False):
    """Global function for safe console printing"""
    console.safe_print(text, end=end, flush=flush)


def format_for_console(text: str) -> str:
    """Global function for console-safe text formatting"""
    return console.format_for_console(text)


def print_colored(text: str, color: str = None, bold: bool = False):
    """Print colored text to console with colorama support"""
    if not COLORS_AVAILABLE or color is None:
        print(text)
        return
    
    # Map color names to colorama colors
    color_map = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'black': Fore.BLACK,
        'lightred': Fore.LIGHTRED_EX,
        'lightgreen': Fore.LIGHTGREEN_EX,
        'lightyellow': Fore.LIGHTYELLOW_EX,
        'lightblue': Fore.LIGHTBLUE_EX,
        'lightmagenta': Fore.LIGHTMAGENTA_EX,
        'lightcyan': Fore.LIGHTCYAN_EX,
    }
    
    color_code = color_map.get(color.lower(), '')
    style_code = Style.BRIGHT if bold else ''
    
    print(f"{style_code}{color_code}{text}{Style.RESET_ALL}")