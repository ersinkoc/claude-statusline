#!/usr/bin/env python3
"""
Custom Theme Builder for Claude Statusline
Allows users to create and customize their own statusline themes
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import psutil

try:
    from colorama import Fore, Back, Style, init
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


class CustomThemeBuilder:
    """Build and manage custom statusline themes"""
    
    def __init__(self):
        """Initialize custom theme builder"""
        self.config_dir = Path.home() / ".claude" / "data-statusline" / "themes"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Available fields that can be included
        self.available_fields = {
            # Model & Status
            'model': {'name': 'Model Name', 'icon': '🤖', 'example': 'Opus 4.1'},
            'model_short': {'name': 'Model Short', 'icon': '🔤', 'example': 'O4.1'},
            'status': {'name': 'Status', 'icon': '📊', 'example': 'LIVE'},
            'status_icon': {'name': 'Status Icon', 'icon': '🟢', 'example': '●'},
            
            # Session Info
            'session_number': {'name': 'Session #', 'icon': '#️⃣', 'example': '123'},
            'messages': {'name': 'Messages', 'icon': '💬', 'example': '456'},
            'tokens': {'name': 'Tokens', 'icon': '🔢', 'example': '12.3M'},
            'tokens_raw': {'name': 'Tokens Raw', 'icon': '🔢', 'example': '12345678'},
            'cost': {'name': 'Cost', 'icon': '💰', 'example': '$89.99'},
            'cost_short': {'name': 'Cost Short', 'icon': '💵', 'example': '$90'},
            
            # Time Info
            'time_remaining': {'name': 'Time Remaining', 'icon': '⏱️', 'example': '2h 30m'},
            'time_remaining_short': {'name': 'Time Short', 'icon': '⏰', 'example': '2:30'},
            'session_end': {'name': 'Session End', 'icon': '🏁', 'example': '17:00'},
            'current_time': {'name': 'Current Time', 'icon': '🕐', 'example': '14:30'},
            'date': {'name': 'Date', 'icon': '📅', 'example': '2025-08-19'},
            
            # Git Info
            'git_branch': {'name': 'Git Branch', 'icon': '🌿', 'example': 'main'},
            'git_status': {'name': 'Git Status', 'icon': '📝', 'example': 'clean'},
            'git_ahead': {'name': 'Git Ahead', 'icon': '⬆️', 'example': '↑3'},
            'git_behind': {'name': 'Git Behind', 'icon': '⬇️', 'example': '↓2'},
            'git_modified': {'name': 'Modified Files', 'icon': '✏️', 'example': 'M:5'},
            'git_untracked': {'name': 'Untracked Files', 'icon': '❓', 'example': 'U:2'},
            
            # System Info
            'folder': {'name': 'Folder Name', 'icon': '📁', 'example': 'my-project'},
            'full_path': {'name': 'Full Path', 'icon': '📂', 'example': '/home/user/project'},
            'cpu': {'name': 'CPU Usage', 'icon': '🖥️', 'example': 'CPU:45%'},
            'memory': {'name': 'Memory Usage', 'icon': '🧠', 'example': 'MEM:62%'},
            'disk': {'name': 'Disk Usage', 'icon': '💾', 'example': 'DISK:78%'},
            'battery': {'name': 'Battery', 'icon': '🔋', 'example': '85%'},
            'os': {'name': 'OS', 'icon': '💻', 'example': 'Windows'},
            
            # Custom Text
            'custom_text': {'name': 'Custom Text', 'icon': '✏️', 'example': 'Your Text'},
            'separator': {'name': 'Separator', 'icon': '|', 'example': '|'},
            'space': {'name': 'Space', 'icon': ' ', 'example': ' '},
            'arrow': {'name': 'Arrow', 'icon': '→', 'example': '→'},
            'dot': {'name': 'Dot', 'icon': '•', 'example': '•'},
        }
        
        # Available colors
        self.colors = {
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
            'none': ''
        }
        
        # Available brackets/decorations
        self.brackets = {
            'square': ('[', ']'),
            'round': ('(', ')'),
            'curly': ('{', '}'),
            'angle': ('<', '>'),
            'double_angle': ('«', '»'),
            'pipe': ('|', '|'),
            'slash': ('/', '/'),
            'backslash': ('\\', '\\'),
            'none': ('', '')
        }
    
    def create_theme(self, name: str, fields: List[Dict[str, Any]], 
                    default_color: str = 'white') -> Dict[str, Any]:
        """
        Create a custom theme
        
        Args:
            name: Theme name
            fields: List of field configurations
            default_color: Default color for fields
            
        Returns:
            Theme configuration dictionary
        """
        theme = {
            'name': name,
            'version': '1.0',
            'created': datetime.now().isoformat(),
            'default_color': default_color,
            'fields': fields
        }
        
        return theme
    
    def save_theme(self, theme: Dict[str, Any], filename: Optional[str] = None):
        """Save theme to file"""
        if not filename:
            filename = f"{theme['name'].lower().replace(' ', '_')}.json"
        
        filepath = self.config_dir / filename
        with open(filepath, 'w') as f:
            json.dump(theme, f, indent=2)
        
        return filepath
    
    def load_theme(self, filename: str) -> Dict[str, Any]:
        """Load theme from file"""
        filepath = self.config_dir / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    
    def list_saved_themes(self) -> List[str]:
        """List all saved custom themes"""
        themes = []
        for file in self.config_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    theme = json.load(f)
                    themes.append({
                        'filename': file.name,
                        'name': theme.get('name', 'Unknown'),
                        'fields': len(theme.get('fields', [])),
                        'created': theme.get('created', 'Unknown')
                    })
            except:
                pass
        return themes
    
    def format_with_theme(self, theme: Dict[str, Any], data: Dict[str, Any]) -> str:
        """
        Format statusline using custom theme
        
        Args:
            theme: Theme configuration
            data: Session data
            
        Returns:
            Formatted statusline string
        """
        output = []
        
        for field_config in theme.get('fields', []):
            field_type = field_config.get('type')
            color = field_config.get('color', theme.get('default_color', 'white'))
            prefix = field_config.get('prefix', '')
            suffix = field_config.get('suffix', '')
            brackets = field_config.get('brackets', 'none')
            
            # Get field value
            value = self._get_field_value(field_type, data)
            if value is None:
                continue
            
            # Apply brackets
            if brackets in self.brackets:
                left, right = self.brackets[brackets]
                value = f"{left}{value}{right}"
            
            # Apply prefix/suffix
            value = f"{prefix}{value}{suffix}"
            
            # Apply color
            if COLORS_AVAILABLE and color in self.colors:
                value = f"{self.colors[color]}{value}{Style.RESET_ALL}"
            
            output.append(value)
        
        # Join fields with configured separator
        separator = theme.get('separator', ' ')
        return separator.join(output)
    
    def _get_field_value(self, field_type: str, data: Dict[str, Any]) -> Optional[str]:
        """Get value for a specific field type"""
        # Model & Status fields
        if field_type == 'model':
            return self._format_model(data.get('primary_model', data.get('model', 'Unknown')))
        elif field_type == 'model_short':
            return self._format_model_short(data.get('primary_model', data.get('model', 'Unknown')))
        elif field_type == 'status':
            return 'LIVE' if data.get('active') else 'OFF'
        elif field_type == 'status_icon':
            return '●' if data.get('active') else '○'
        
        # Session fields
        elif field_type == 'session_number':
            return str(data.get('session_number', '?'))
        elif field_type == 'messages':
            return str(data.get('message_count', 0))
        elif field_type == 'tokens':
            return self._format_tokens(data.get('tokens', data.get('total_tokens', 0)))
        elif field_type == 'tokens_raw':
            return str(data.get('tokens', data.get('total_tokens', 0)))
        elif field_type == 'cost':
            cost = data.get('cost', data.get('total_cost', 0.0))
            return f"${cost:.2f}"
        elif field_type == 'cost_short':
            cost = data.get('cost', data.get('total_cost', 0.0))
            return f"${cost:.0f}"
        
        # Time fields
        elif field_type == 'time_remaining':
            return self._format_time_remaining(data.get('remaining_seconds', 0))
        elif field_type == 'time_remaining_short':
            remaining = data.get('remaining_seconds', 0)
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            return f"{hours}:{minutes:02d}"
        elif field_type == 'session_end':
            return data.get('session_end_time', '')
        elif field_type == 'current_time':
            return datetime.now().strftime('%H:%M')
        elif field_type == 'date':
            return datetime.now().strftime('%Y-%m-%d')
        
        # Git fields
        elif field_type == 'git_branch':
            return self._get_git_branch()
        elif field_type == 'git_status':
            return self._get_git_status()
        elif field_type == 'git_modified':
            count = self._get_git_modified_count()
            return f"M:{count}" if count > 0 else None
        elif field_type == 'git_untracked':
            count = self._get_git_untracked_count()
            return f"U:{count}" if count > 0 else None
        
        # System fields
        elif field_type == 'folder':
            return Path.cwd().name
        elif field_type == 'full_path':
            return str(Path.cwd())
        elif field_type == 'cpu':
            try:
                return f"CPU:{psutil.cpu_percent()}%"
            except:
                return None
        elif field_type == 'memory':
            try:
                return f"MEM:{psutil.virtual_memory().percent:.0f}%"
            except:
                return None
        elif field_type == 'disk':
            try:
                return f"DISK:{psutil.disk_usage('/').percent:.0f}%"
            except:
                return None
        elif field_type == 'battery':
            try:
                battery = psutil.sensors_battery()
                if battery:
                    return f"{battery.percent:.0f}%"
            except:
                return None
        elif field_type == 'os':
            import platform
            return platform.system()
        
        # Custom fields
        elif field_type == 'separator':
            return '|'
        elif field_type == 'space':
            return ' '
        elif field_type == 'arrow':
            return '→'
        elif field_type == 'dot':
            return '•'
        elif field_type == 'custom_text':
            return data.get('custom_text', '')
        
        return None
    
    def _format_model(self, model: str) -> str:
        """Format model name"""
        if not model or model == 'Unknown':
            return 'Unknown'
        
        # Try to get from prices.json
        try:
            prices_file = Path(__file__).parent / 'prices.json'
            if prices_file.exists():
                with open(prices_file, 'r') as f:
                    prices = json.load(f)
                    models = prices.get('models', {})
                    if model in models:
                        return models[model].get('name', model)
        except:
            pass
        
        # Fallback
        model_lower = model.lower()
        if 'opus' in model_lower:
            return 'Opus 4.1' if '4.1' in model else 'Opus'
        elif 'sonnet' in model_lower:
            return 'Sonnet 3.5' if '3.5' in model else 'Sonnet'
        elif 'haiku' in model_lower:
            return 'Haiku'
        
        return model.replace('claude-', '').split('-')[0].title()
    
    def _format_model_short(self, model: str) -> str:
        """Format model name short version"""
        model_lower = model.lower()
        if 'opus' in model_lower:
            return 'O4.1' if '4.1' in model else 'O'
        elif 'sonnet' in model_lower:
            return 'S3.5' if '3.5' in model else 'S'
        elif 'haiku' in model_lower:
            return 'H'
        return '?'
    
    def _format_tokens(self, tokens: int) -> str:
        """Format token count"""
        if tokens < 1000:
            return str(tokens)
        elif tokens < 1_000_000:
            return f"{tokens/1000:.1f}k"
        else:
            return f"{tokens/1_000_000:.1f}M"
    
    def _format_time_remaining(self, seconds: int) -> str:
        """Format remaining time"""
        if seconds <= 0:
            return 'EXPIRED'
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
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
        """Get git status"""
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
    
    def _get_git_modified_count(self) -> int:
        """Get count of modified files"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                timeout=1
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                return sum(1 for line in lines if line.startswith(' M') or line.startswith('M '))
        except:
            pass
        return 0
    
    def _get_git_untracked_count(self) -> int:
        """Get count of untracked files"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                timeout=1
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                return sum(1 for line in lines if line.startswith('??'))
        except:
            pass
        return 0


# Example custom themes
EXAMPLE_THEMES = {
    'developer_pro': {
        'name': 'Developer Pro',
        'separator': ' | ',
        'default_color': 'white',
        'fields': [
            {'type': 'model_short', 'color': 'cyan', 'brackets': 'square'},
            {'type': 'status_icon', 'color': 'green'},
            {'type': 'git_branch', 'color': 'blue', 'prefix': '🌿 '},
            {'type': 'git_status', 'color': 'yellow'},
            {'type': 'folder', 'color': 'magenta'},
            {'type': 'messages', 'color': 'white', 'suffix': 'msg'},
            {'type': 'cost_short', 'color': 'yellow'},
        ]
    },
    'minimal_clean': {
        'name': 'Minimal Clean',
        'separator': '  ',
        'default_color': 'bright_white',
        'fields': [
            {'type': 'model_short', 'color': 'bright_cyan'},
            {'type': 'messages', 'color': 'bright_white'},
            {'type': 'cost_short', 'color': 'bright_yellow'},
        ]
    },
    'system_monitor': {
        'name': 'System Monitor',
        'separator': ' • ',
        'default_color': 'green',
        'fields': [
            {'type': 'model', 'color': 'cyan'},
            {'type': 'cpu', 'color': 'yellow'},
            {'type': 'memory', 'color': 'magenta'},
            {'type': 'battery', 'color': 'green'},
            {'type': 'current_time', 'color': 'white'},
        ]
    },
    'git_focused': {
        'name': 'Git Focused',
        'separator': ' ',
        'default_color': 'white',
        'fields': [
            {'type': 'git_branch', 'color': 'green', 'prefix': '⎇ '},
            {'type': 'git_modified', 'color': 'yellow'},
            {'type': 'git_untracked', 'color': 'red'},
            {'type': 'separator', 'color': 'bright_black'},
            {'type': 'model_short', 'color': 'cyan'},
            {'type': 'messages', 'color': 'white'},
        ]
    },
    'full_info': {
        'name': 'Full Information',
        'separator': ' │ ',
        'default_color': 'white',
        'fields': [
            {'type': 'model', 'color': 'cyan', 'brackets': 'square'},
            {'type': 'status', 'color': 'green'},
            {'type': 'session_number', 'color': 'yellow', 'prefix': '#'},
            {'type': 'messages', 'color': 'white', 'suffix': ' messages'},
            {'type': 'tokens', 'color': 'magenta', 'suffix': ' tokens'},
            {'type': 'cost', 'color': 'yellow'},
            {'type': 'time_remaining', 'color': 'red'},
            {'type': 'git_branch', 'color': 'blue'},
            {'type': 'folder', 'color': 'bright_magenta'},
        ]
    }
}