#!/usr/bin/env python3
"""
Simple Visual Formatter for Claude Code
Uses only basic ASCII characters and symbols that work in all terminals
"""

import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from statusline_templates import StatuslineTemplates


class SimpleVisualFormatter:
    """Simple visual formatter without colors or special Unicode"""
    
    def __init__(self, template_name: str = 'compact'):
        """Initialize simple visual formatter"""
        self.git_branch = self._get_git_branch()
        self.current_dir = Path.cwd().name
        self.templates = StatuslineTemplates()
        self.template_name = template_name
    
    def format_statusline(self, session_data: Dict[str, Any]) -> str:
        """
        Format session data using templates
        
        Args:
            session_data: Session data dictionary
            
        Returns:
            Formatted statusline string using selected template
        """
        try:
            # Use template system
            return self.templates.format(self.template_name, session_data)
            
        except Exception as e:
            # Fallback to basic format on error
            model = session_data.get('primary_model', '?')
            msgs = session_data.get('message_count', 0)
            cost = session_data.get('cost', 0.0)
            return f"[{model}] {msgs}msg ${cost:.2f} (Error: {str(e)[:20]})"
    
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