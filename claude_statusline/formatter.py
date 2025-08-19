#!/usr/bin/env python3
"""
Simple Visual Formatter for Claude Code
Supports colored output for better visibility
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from .templates import StatuslineTemplates
from .colored_templates import ColoredTemplates
from .custom_theme import CustomThemeBuilder

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Initialize colorama for cross-platform support
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Define dummy color constants if colorama is not available
    class Fore:
        BLACK = WHITE = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = ''
        LIGHTBLACK_EX = LIGHTWHITE_EX = LIGHTRED_EX = LIGHTGREEN_EX = ''
        LIGHTYELLOW_EX = LIGHTBLUE_EX = LIGHTMAGENTA_EX = LIGHTCYAN_EX = ''
        RESET = ''
    class Back:
        BLACK = WHITE = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = ''
        RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''


class SimpleVisualFormatter:
    """Visual formatter with optional color support"""
    
    def __init__(self, template_name: str = 'compact'):
        """Initialize visual formatter with color configuration"""
        self.git_branch = self._get_git_branch()
        self.current_dir = Path.cwd().name
        self.templates = StatuslineTemplates()
        self.colored_templates = ColoredTemplates()
        self.custom_builder = CustomThemeBuilder()
        self.template_name = template_name
        
        # Load color configuration
        self.config = self._load_config()
        self.colors_enabled = COLORS_AVAILABLE and self.config.get('display', {}).get('enable_colors', True)
        self.color_scheme = self.config.get('display', {}).get('color_scheme', {})
        
        # Map color names to colorama colors
        self.color_map = {
            'black': Fore.BLACK,
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
            'bright_black': Fore.LIGHTBLACK_EX,
            'bright_red': Fore.LIGHTRED_EX,
            'bright_green': Fore.LIGHTGREEN_EX,
            'bright_yellow': Fore.LIGHTYELLOW_EX,
            'bright_blue': Fore.LIGHTBLUE_EX,
            'bright_magenta': Fore.LIGHTMAGENTA_EX,
            'bright_cyan': Fore.LIGHTCYAN_EX,
            'bright_white': Fore.LIGHTWHITE_EX,
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json"""
        try:
            config_file = Path(__file__).parent / "config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def format_statusline(self, session_data: Dict[str, Any]) -> str:
        """
        Format session data with colored output
        
        Args:
            session_data: Session data dictionary
            
        Returns:
            Formatted statusline string with optional colors
        """
        try:
            # Check for custom theme first
            if self.template_name == 'custom':
                custom_theme = self.config.get('display', {}).get('custom_theme')
                if custom_theme:
                    return self.custom_builder.format_with_theme(custom_theme, session_data)
            
            # Check if it's a saved custom theme
            if self.template_name.startswith('custom_'):
                theme_file = self.template_name[7:] + '.json'
                theme_data = self.custom_builder.load_theme(theme_file)
                if theme_data:
                    return self.custom_builder.format_with_theme(theme_data, session_data)
            
            # Check for example custom themes
            from .custom_theme import EXAMPLE_THEMES
            if self.template_name in EXAMPLE_THEMES:
                return self.custom_builder.format_with_theme(EXAMPLE_THEMES[self.template_name], session_data)
            
            # Check if template exists in colored templates
            if self.colors_enabled and hasattr(self.colored_templates, 'templates'):
                if self.template_name in self.colored_templates.templates:
                    return self.colored_templates.templates[self.template_name](session_data)
            
            # If colors are disabled or template not in colored, use regular templates
            if not self.colors_enabled:
                return self.templates.format(self.template_name, session_data)
            
            # Build colored statusline for standard templates
            return self._format_colored_statusline(session_data)
            
        except Exception as e:
            # Fallback to basic format on error
            model = session_data.get('primary_model', '?')
            msgs = session_data.get('message_count', 0)
            cost = session_data.get('cost', 0.0)
            return f"[{model}] {msgs}msg ${cost:.2f} (Error: {str(e)[:20]})"
    
    def _format_colored_statusline(self, session_data: Dict[str, Any]) -> str:
        """Format statusline with colors based on template"""
        # Get color functions
        def get_color(key: str) -> str:
            color_name = self.color_scheme.get(key, 'white')
            return self.color_map.get(color_name, '')
        
        # Extract data
        model = self._format_model(session_data.get('primary_model', session_data.get('model', 'Unknown')))
        status = self._get_status(session_data)
        time_info = self._format_time_info(session_data)
        messages = session_data.get('message_count', 0)
        tokens = self._format_tokens(session_data.get('tokens', session_data.get('total_tokens', 0)))
        cost = session_data.get('cost', session_data.get('total_cost', 0.0))
        
        # Determine status color
        if 'LIVE' in status or 'ACTIVE' in status:
            status_color = get_color('status_live')
        elif 'EXPIRED' in status or 'OFF' in status:
            status_color = get_color('status_expired')
        elif 'NEW' in status:
            status_color = get_color('status_new')
        else:
            status_color = get_color('messages')
        
        # Build colored output based on template style
        if self.template_name == 'minimal':
            return f"{get_color('model')}{model}{Style.RESET_ALL} {get_color('messages')}{messages}m{Style.RESET_ALL} {get_color('cost')}${cost:.0f}{Style.RESET_ALL}"
        elif self.template_name == 'vim':
            return f"{status_color}--INSERT--{Style.RESET_ALL} {get_color('model')}{model}{Style.RESET_ALL} {get_color('messages')}{messages}L{Style.RESET_ALL} {get_color('cost')}${cost:.1f}{Style.RESET_ALL} {get_color('brackets')}[utf-8]{Style.RESET_ALL}"
        elif self.template_name == 'matrix':
            return f"{get_color('brackets')}[{Style.RESET_ALL}{Fore.GREEN}{model}{Style.RESET_ALL}{get_color('brackets')}]{Style.RESET_ALL} {status_color}{status}{Style.RESET_ALL} {get_color('time')}{time_info}{Style.RESET_ALL} {get_color('brackets')}|{Style.RESET_ALL} {get_color('messages')}{messages}msg{Style.RESET_ALL} {get_color('tokens')}{tokens}{Style.RESET_ALL} {get_color('cost')}${cost:.0f}{Style.RESET_ALL}"
        else:  # compact (default)
            return f"{get_color('brackets')}[{Style.RESET_ALL}{get_color('model')}{model}{Style.RESET_ALL}{get_color('brackets')}]{Style.RESET_ALL} {status_color}{status}{Style.RESET_ALL} {get_color('time')}{time_info}{Style.RESET_ALL} {get_color('brackets')}|{Style.RESET_ALL} {get_color('messages')}{messages}msg{Style.RESET_ALL} {get_color('tokens')}{tokens}{Style.RESET_ALL} {get_color('cost')}${cost:.0f}{Style.RESET_ALL}"
    
    def _get_status(self, session_data: Dict[str, Any]) -> str:
        """Get status text from session data"""
        remaining = session_data.get('remaining_seconds', 0)
        active = session_data.get('active', False)
        
        if active and remaining > 0:
            return 'LIVE'
        elif remaining > 0:
            return 'ACTIVE'
        else:
            return 'OFF'
    
    def _format_time_info(self, session_data: Dict[str, Any]) -> str:
        """Format time information"""
        end_time = session_data.get('session_end_time')
        if end_time:
            return f"~{end_time}"
        
        remaining = session_data.get('remaining_seconds', 0)
        if remaining > 0:
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            if hours > 0:
                return f"~{hours}:{minutes:02d}"
            else:
                return f"~{minutes}m"
        return ''
    
    def _format_model(self, model_name: str) -> str:
        """Format model name for display - readable but short"""
        if not model_name or model_name == 'Unknown':
            return 'Unknown'
        
        # Try to get display name from prices.json
        try:
            import json
            from pathlib import Path
            prices_file = Path(__file__).parent / 'prices.json'
            if prices_file.exists():
                with open(prices_file, 'r') as f:
                    prices = json.load(f)
                    models = prices.get('models', {})
                    if model_name in models:
                        # Return the name from prices.json as-is
                        return models[model_name].get('name', model_name)
        except:
            pass
        
        # Fallback to simple extraction if not in prices.json
        model_lower = model_name.lower()
        if 'opus' in model_lower:
            return 'Opus'
        elif 'sonnet' in model_lower:
            return 'Sonnet'
        elif 'haiku' in model_lower:
            return 'Haiku'
        else:
            # Take first part
            return model_name.replace('claude-', '').split('-')[0].title()
    
    def _format_time_remaining(self, remaining_seconds: int) -> str:
        """Format remaining time - readable"""
        if remaining_seconds <= 0:
            return "EXPIRED"
        
        hours = remaining_seconds // 3600
        minutes = (remaining_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m left"
    
    def _format_tokens(self, tokens: int) -> str:
        """Format token count - readable"""
        if tokens < 1000:
            return f"{tokens} tok"
        elif tokens < 1_000_000:
            k_value = tokens/1000
            if k_value < 100:
                return f"{k_value:.1f}k"
            else:
                return f"{k_value:.0f}k"
        else:
            m_value = tokens/1_000_000
            if m_value < 100:
                return f"{m_value:.1f}M"
            else:
                return f"{m_value:.0f}M"
    
    def _get_git_branch(self) -> Optional[str]:
        """Get current git branch"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=1
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _get_git_status(self) -> str:
        """Check if git working directory is clean"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'clean' if not result.stdout.strip() else 'modified'
        except:
            pass
        return 'unknown'


def main():
    """Test the simple visual formatter"""
    # Test data
    test_session = {
        'session_number': 119,
        'primary_model': 'claude-sonnet-4-20250514',
        'remaining_seconds': 7200,  # 2 hours
        'message_count': 682,
        'tokens': 64336669,
        'cost': 25.47,
        'active': True,
        'data_source': 'live',
        'session_end_time': '14:30'
    }
    
    formatter = SimpleVisualFormatter()
    output = formatter.format_statusline(test_session)
    print("Active session:", output)
    
    # Test expired session
    test_session['remaining_seconds'] = 0
    test_session['active'] = False
    test_session['session_end_time'] = None
    output = formatter.format_statusline(test_session)
    print("Expired session:", output)


if __name__ == "__main__":
    main()