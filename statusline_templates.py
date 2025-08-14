#!/usr/bin/env python3
"""
Statusline Templates for Claude Code
Different formats and styles for various preferences
"""

from typing import Dict, Any, List
from datetime import datetime
import random


class StatuslineTemplates:
    """Collection of statusline templates"""
    
    def __init__(self):
        """Initialize templates"""
        self.templates = {
            'compact': self.compact_format,
            'minimal': self.minimal_format,
            'detailed': self.detailed_format,
            'emoji': self.emoji_format,
            'dev': self.developer_format,
            'vim': self.vim_style_format,
            'powerline': self.powerline_format,
            'matrix': self.matrix_format,
            'nerd': self.nerd_format,
            'zen': self.zen_format,
            'hacker': self.hacker_format,
            'corporate': self.corporate_format,
            'creative': self.creative_format,
            'scientific': self.scientific_format,
            'casual': self.casual_format,
            'discord': self.discord_format,
            'twitch': self.twitch_format,
            'github': self.github_format,
            'terminal': self.terminal_format,
            'json': self.json_format
        }
        
        # Template descriptions
        self.descriptions = {
            'compact': 'Default compact format',
            'minimal': 'Ultra minimal, only essentials',
            'detailed': 'All information visible',
            'emoji': 'Rich emoji indicators',
            'dev': 'Developer-friendly format',
            'vim': 'Vim statusline style',
            'powerline': 'Powerline-inspired segments',
            'matrix': 'Matrix/cyberpunk theme',
            'nerd': 'Nerd font icons style',
            'zen': 'Clean and peaceful',
            'hacker': 'L33t hacker style',
            'corporate': 'Professional business format',
            'creative': 'Artistic and playful',
            'scientific': 'Scientific notation style',
            'casual': 'Friendly casual format',
            'discord': 'Discord status style',
            'twitch': 'Streaming style format',
            'github': 'GitHub activity style',
            'terminal': 'Classic terminal style',
            'json': 'JSON structured format'
        }
    
    def format(self, template_name: str, session_data: Dict[str, Any]) -> str:
        """
        Format session data with specified template
        
        Args:
            template_name: Name of template to use
            session_data: Session data dictionary
            
        Returns:
            Formatted statusline string
        """
        if template_name not in self.templates:
            template_name = 'compact'
        
        return self.templates[template_name](session_data)
    
    def compact_format(self, data: Dict[str, Any]) -> str:
        """Default compact format"""
        model = data.get('primary_model', 'Unknown')
        status = 'LIVE' if data.get('active') else 'OFF'
        end_time = data.get('session_end_time', 'N/A')
        msgs = data.get('message_count', 0)
        tokens = self._format_tokens(data.get('tokens', 0))
        cost = data.get('cost', 0.0)
        
        return f"[{model}] {status} ~{end_time} | {msgs}msg {tokens} ${cost:.1f}"
    
    def minimal_format(self, data: Dict[str, Any]) -> str:
        """Ultra minimal format"""
        model = self._short_model(data.get('primary_model', '?'))
        msgs = data.get('message_count', 0)
        cost = data.get('cost', 0.0)
        
        return f"{model} {msgs}m ${cost:.0f}"
    
    def detailed_format(self, data: Dict[str, Any]) -> str:
        """Detailed format with all information"""
        model = data.get('primary_model', 'Unknown')
        status = 'ACTIVE' if data.get('active') else 'INACTIVE'
        session = data.get('session_number', '?')
        end_time = data.get('session_end_time', 'N/A')
        msgs = data.get('message_count', 0)
        tokens = data.get('tokens', 0)
        cost = data.get('cost', 0.0)
        remaining = data.get('remaining_seconds', 0)
        
        hours = remaining // 3600
        mins = (remaining % 3600) // 60
        
        return (f"Session #{session} | Model: {model} | Status: {status} | "
                f"Ends: {end_time} | Messages: {msgs} | Tokens: {tokens:,} | "
                f"Cost: ${cost:.2f} | Remaining: {hours}h {mins}m")
    
    def emoji_format(self, data: Dict[str, Any]) -> str:
        """Emoji-rich format (ASCII safe)"""
        model_emoji = self._get_model_emoji_ascii(data.get('primary_model', ''))
        status_emoji = "(o)" if data.get('active') else "(x)"
        msgs = data.get('message_count', 0)
        tokens = self._format_tokens(data.get('tokens', 0))
        cost = data.get('cost', 0.0)
        end_time = data.get('session_end_time', 'N/A')
        
        return f"{model_emoji} {status_emoji} @{end_time} #{msgs} >{tokens} ${cost:.1f}"
    
    def developer_format(self, data: Dict[str, Any]) -> str:
        """Developer-friendly format"""
        model = self._short_model(data.get('primary_model', '?'))
        pid = 'LIVE' if data.get('active') else 'DEAD'
        msgs = data.get('message_count', 0)
        tokens = data.get('tokens', 0) // 1000  # in K
        cost = data.get('cost', 0.0)
        end_time = data.get('session_end_time', 'N/A')
        
        return f"[{model}:{pid}] t={end_time} m={msgs} tok={tokens}k c=${cost:.2f}"
    
    def vim_style_format(self, data: Dict[str, Any]) -> str:
        """Vim statusline style"""
        model = self._short_model(data.get('primary_model', '?'))
        mode = 'INSERT' if data.get('active') else 'NORMAL'
        msgs = data.get('message_count', 0)
        cost = data.get('cost', 0.0)
        
        return f"--{mode}-- {model} {msgs}L ${cost:.1f} [utf-8]"
    
    def powerline_format(self, data: Dict[str, Any]) -> str:
        """Powerline-style segments"""
        model = self._short_model(data.get('primary_model', '?'))
        status = 'ON' if data.get('active') else 'OFF'
        msgs = data.get('message_count', 0)
        tokens = self._format_tokens(data.get('tokens', 0))
        cost = data.get('cost', 0.0)
        
        # Using > as segment separator (ASCII compatible)
        return f" {model} > {status} > {msgs}m > {tokens} > ${cost:.1f} "
    
    def matrix_format(self, data: Dict[str, Any]) -> str:
        """Matrix/cyberpunk theme"""
        model = self._short_model(data.get('primary_model', '?'))
        status = '1' if data.get('active') else '0'
        msgs = data.get('message_count', 0)
        tokens = data.get('tokens', 0) // 1000
        cost = data.get('cost', 0.0)
        
        return f"[{status}] <{model}> ::MSG:{msgs} ::TOK:{tokens}k ::CR:${cost:.2f}::"
    
    def nerd_format(self, data: Dict[str, Any]) -> str:
        """Nerd font style (using ASCII alternatives)"""
        model = self._short_model(data.get('primary_model', '?'))
        status = '>' if data.get('active') else 'x'
        msgs = data.get('message_count', 0)
        tokens = self._format_tokens(data.get('tokens', 0))
        cost = data.get('cost', 0.0)
        
        return f"{status} {model} | {msgs} | {tokens} | ${cost:.1f}"
    
    def zen_format(self, data: Dict[str, Any]) -> str:
        """Clean and peaceful format"""
        model = data.get('primary_model', 'Unknown')
        msgs = data.get('message_count', 0)
        cost = data.get('cost', 0.0)
        
        return f"{model} • {msgs} messages • ${cost:.2f}"
    
    def hacker_format(self, data: Dict[str, Any]) -> str:
        """L33t hacker style"""
        model = self._to_leet(self._short_model(data.get('primary_model', '?')))
        status = 'PWN3D' if data.get('active') else 'N00B'
        msgs = data.get('message_count', 0)
        tokens = data.get('tokens', 0) // 1000
        cost = data.get('cost', 0.0)
        
        return f"[{status}] {model} m5g:{msgs} t0k:{tokens}k c0st:${cost:.0f}"
    
    def corporate_format(self, data: Dict[str, Any]) -> str:
        """Professional business format"""
        model = data.get('primary_model', 'N/A')
        status = 'Active' if data.get('active') else 'Idle'
        msgs = data.get('message_count', 0)
        cost = data.get('cost', 0.0)
        
        return f"Model: {model} | Status: {status} | Units: {msgs} | Cost: ${cost:.2f} USD"
    
    def creative_format(self, data: Dict[str, Any]) -> str:
        """Artistic and playful format"""
        model = self._short_model(data.get('primary_model', '?'))
        status = '~flowing~' if data.get('active') else '...paused...'
        msgs = data.get('message_count', 0)
        tokens = self._format_tokens(data.get('tokens', 0))
        cost = data.get('cost', 0.0)
        
        return f"*{model}* {status} [{msgs} thoughts] [{tokens} words] [${cost:.1f} spent]"
    
    def scientific_format(self, data: Dict[str, Any]) -> str:
        """Scientific notation style"""
        model = self._short_model(data.get('primary_model', '?'))
        status = 'T' if data.get('active') else 'F'
        msgs = data.get('message_count', 0)
        tokens = data.get('tokens', 0)
        cost = data.get('cost', 0.0)
        
        # Scientific notation for large numbers
        if tokens > 1000000:
            tok_str = f"{tokens/1e6:.2e}"
        else:
            tok_str = str(tokens)
        
        return f"Model={model} Active={status} N={msgs} Tokens={tok_str} Cost={cost:.4f}"
    
    def casual_format(self, data: Dict[str, Any]) -> str:
        """Friendly casual format"""
        model = self._short_model(data.get('primary_model', '?'))
        status = 'chatting' if data.get('active') else 'away'
        msgs = data.get('message_count', 0)
        cost = data.get('cost', 0.0)
        
        return f"{model} is {status} - {msgs} messages so far (${cost:.2f})"
    
    def discord_format(self, data: Dict[str, Any]) -> str:
        """Discord status style"""
        model = self._short_model(data.get('primary_model', '?'))
        status = 'Online' if data.get('active') else 'Idle'
        msgs = data.get('message_count', 0)
        
        return f"Playing Claude {model} • {status} • {msgs} messages"
    
    def twitch_format(self, data: Dict[str, Any]) -> str:
        """Streaming style format"""
        model = self._short_model(data.get('primary_model', '?'))
        status = 'LIVE' if data.get('active') else 'OFFLINE'
        msgs = data.get('message_count', 0)
        viewers = random.randint(10, 1000)  # Fun fake viewer count
        
        return f"[{status}] Coding with {model} | Chat: {msgs} | Viewers: {viewers}"
    
    def github_format(self, data: Dict[str, Any]) -> str:
        """GitHub activity style"""
        model = self._short_model(data.get('primary_model', '?'))
        msgs = data.get('message_count', 0)
        tokens = data.get('tokens', 0) // 1000
        
        commits = msgs // 10  # Fake commit count
        
        return f"@{model} • {commits} commits • {msgs} conversations • {tokens}k tokens"
    
    def terminal_format(self, data: Dict[str, Any]) -> str:
        """Classic terminal style"""
        model = self._short_model(data.get('primary_model', '?'))
        msgs = data.get('message_count', 0)
        cost = data.get('cost', 0.0)
        
        return f"claude@{model}:~$ {msgs} msgs | ${cost:.2f}"
    
    def json_format(self, data: Dict[str, Any]) -> str:
        """JSON structured format (single line)"""
        model = self._short_model(data.get('primary_model', '?'))
        status = data.get('active', False)
        msgs = data.get('message_count', 0)
        tokens = data.get('tokens', 0)
        cost = data.get('cost', 0.0)
        
        return f'{{"model":"{model}","active":{str(status).lower()},"msgs":{msgs},"tokens":{tokens},"cost":{cost:.2f}}}'
    
    # Helper methods
    def _format_tokens(self, tokens: int) -> str:
        """Format token count"""
        if tokens < 1000:
            return f"{tokens}"
        elif tokens < 1_000_000:
            return f"{tokens/1000:.1f}k"
        else:
            return f"{tokens/1_000_000:.1f}M"
    
    def _short_model(self, model: str) -> str:
        """Get short model name"""
        if not model:
            return '?'
        
        model_lower = model.lower()
        if 'opus' in model_lower:
            if '4.1' in model:
                return 'O4.1'
            elif '4' in model:
                return 'O4'
            return 'Opus'
        elif 'sonnet' in model_lower:
            if '4' in model:
                return 'S4'
            elif '3.7' in model:
                return 'S3.7'
            elif '3.5' in model:
                return 'S3.5'
            return 'Sonnet'
        elif 'haiku' in model_lower:
            if '4' in model:
                return 'H4'
            elif '3.5' in model:
                return 'H3.5'
            return 'Haiku'
        
        return model[:5]
    
    def _get_model_emoji_ascii(self, model: str) -> str:
        """Get ASCII emoji for model"""
        model_lower = model.lower()
        if 'opus' in model_lower:
            return "[O]"
        elif 'sonnet' in model_lower:
            return "[S]"
        elif 'haiku' in model_lower:
            return "[H]"
        return "[?]"
    
    def _to_leet(self, text: str) -> str:
        """Convert to l33t speak"""
        leet_map = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0',
            'A': '4', 'E': '3', 'I': '1', 'O': '0',
            's': '5', 'S': '5', 't': '7', 'T': '7'
        }
        return ''.join(leet_map.get(c, c) for c in text)
    
    def list_templates(self) -> List[str]:
        """Get list of available templates"""
        return list(self.templates.keys())
    
    def get_description(self, template_name: str) -> str:
        """Get template description"""
        return self.descriptions.get(template_name, 'Unknown template')


def demo():
    """Demo all templates"""
    # Sample data
    sample_data = {
        'primary_model': 'Opus 4.1',
        'active': True,
        'session_number': 123,
        'session_end_time': '17:00',
        'message_count': 456,
        'tokens': 12345678,
        'cost': 89.99,
        'remaining_seconds': 7200
    }
    
    templates = StatuslineTemplates()
    
    print("Claude Statusline Template Gallery")
    print("=" * 60)
    print()
    
    for template in templates.list_templates():
        output = templates.format(template, sample_data)
        desc = templates.get_description(template)
        print(f"{template:15} - {desc}")
        print(f"  {output}")
        print()


if __name__ == "__main__":
    demo()