#!/usr/bin/env python3
"""
Simple Visual Formatter for Claude Code
Uses only basic ASCII characters and symbols that work in all terminals
"""

import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class SimpleVisualFormatter:
    """Simple visual formatter without colors or special Unicode"""
    
    def __init__(self):
        """Initialize simple visual formatter"""
        self.git_branch = self._get_git_branch()
        self.current_dir = Path.cwd().name
    
    def format_statusline(self, session_data: Dict[str, Any]) -> str:
        """
        Format session data with simple visual elements
        
        Args:
            session_data: Session data dictionary
            
        Returns:
            Formatted simple visual statusline string
        """
        try:
            # Extract session info
            session_number = session_data.get('session_number', '?')
            model_name = session_data.get('primary_model', 'Unknown')
            remaining_seconds = session_data.get('remaining_seconds', 0)
            message_count = session_data.get('message_count', 0)
            tokens = session_data.get('tokens', 0)
            cost = session_data.get('cost', 0.0)
            is_active = session_data.get('active', False)
            
            # Format components
            parts = []
            
            # Session status with brackets
            model_short = self._format_model(model_name)
            status_text = "LIVE" if is_active else "OFF"
            session_part = f"[{model_short}] [{status_text}]"
            parts.append(session_part)
            
            # Time info with brackets
            session_end_time = session_data.get('session_end_time')
            if session_end_time:
                time_display = f"ends {session_end_time}"
            else:
                time_display = self._format_time_remaining(remaining_seconds)
            time_part = f"[{time_display}]"
            parts.append(time_part)
            
            # Usage info with clear separators
            token_display = self._format_tokens(tokens)
            usage_part = f"[{message_count}msg] [{token_display}] [${cost:.2f}]"
            parts.append(usage_part)
            
            # Context info
            if self.current_dir:
                context_part = f"[{self.current_dir[:12]}]"
                if self.git_branch:
                    git_display = self.git_branch[:8] if len(self.git_branch) > 8 else self.git_branch
                    git_status = self._get_git_status()
                    git_symbol = "*" if git_status != 'clean' else ""
                    context_part += f"[{git_display}{git_symbol}]"
                parts.append(context_part)
            
            # Current time
            current_time = datetime.now().strftime("%H:%M")
            time_part = f"[{current_time}]"
            parts.append(time_part)
            
            return " ".join(parts)
            
        except Exception as e:
            return f"[ERROR: {str(e)[:30]}]"
    
    def _format_model(self, model_name: str) -> str:
        """Format model name for display from prices.json"""
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
                        # Return the name from prices.json
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
            # Take first word and limit length
            first_part = model_name.replace('claude-', '').split('-')[0]
            return first_part[:8].title()
    
    def _format_time_remaining(self, remaining_seconds: int) -> str:
        """Format remaining time"""
        if remaining_seconds <= 0:
            return "EXPIRED"
        
        hours = remaining_seconds // 3600
        minutes = (remaining_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h{minutes:02d}m"
        else:
            return f"{minutes}m"
    
    def _format_tokens(self, tokens: int) -> str:
        """Format token count with proper units"""
        if tokens < 1000:
            return f"{tokens}t"
        elif tokens < 1_000_000:
            return f"{tokens/1000:.1f}K"
        else:
            return f"{tokens/1_000_000:.1f}M"
    
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