#!/usr/bin/env python3
"""
Unified Powerline System - TEK SİSTEM, 100 TEMA
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path
import subprocess

class UnifiedPowerlineSystem:
    """TEK POWERLINE SİSTEMİ - 100 TEMA"""
    
    def __init__(self):
        # SOFT RGB color definitions - more pleasant to the eyes
        self.colors = {
            # Soft grayscale
            'soft_black': {'bg': '\x1b[48;2;30;30;35m', 'fg': '\x1b[38;2;30;30;35m', 'text': '\x1b[97m'},
            'soft_gray': {'bg': '\x1b[48;2;60;65;70m', 'fg': '\x1b[38;2;60;65;70m', 'text': '\x1b[97m'},
            'medium_gray': {'bg': '\x1b[48;2;90;95;100m', 'fg': '\x1b[38;2;90;95;100m', 'text': '\x1b[97m'},
            'light_gray': {'bg': '\x1b[48;2;140;145;150m', 'fg': '\x1b[38;2;140;145;150m', 'text': '\x1b[97m'},
            'soft_white': {'bg': '\x1b[48;2;220;225;230m', 'fg': '\x1b[38;2;220;225;230m', 'text': '\x1b[30m'},
            
            # Soft warm colors
            'soft_red': {'bg': '\x1b[48;2;180;90;90m', 'fg': '\x1b[38;2;180;90;90m', 'text': '\x1b[97m'},
            'soft_orange': {'bg': '\x1b[48;2;200;140;90m', 'fg': '\x1b[38;2;200;140;90m', 'text': '\x1b[97m'},
            'soft_yellow': {'bg': '\x1b[48;2;200;180;100m', 'fg': '\x1b[38;2;200;180;100m', 'text': '\x1b[30m'},
            'soft_peach': {'bg': '\x1b[48;2;220;180;140m', 'fg': '\x1b[38;2;220;180;140m', 'text': '\x1b[30m'},
            'soft_pink': {'bg': '\x1b[48;2;200;140;160m', 'fg': '\x1b[38;2;200;140;160m', 'text': '\x1b[97m'},
            
            # Soft cool colors
            'soft_blue': {'bg': '\x1b[48;2;90;120;180m', 'fg': '\x1b[38;2;90;120;180m', 'text': '\x1b[97m'},
            'soft_cyan': {'bg': '\x1b[48;2;100;160;180m', 'fg': '\x1b[38;2;100;160;180m', 'text': '\x1b[97m'},
            'soft_teal': {'bg': '\x1b[48;2;80;140;140m', 'fg': '\x1b[38;2;80;140;140m', 'text': '\x1b[97m'},
            'soft_green': {'bg': '\x1b[48;2;120;160;120m', 'fg': '\x1b[38;2;120;160;120m', 'text': '\x1b[97m'},
            'soft_mint': {'bg': '\x1b[48;2;140;200;160m', 'fg': '\x1b[38;2;140;200;160m', 'text': '\x1b[30m'},
            
            # Soft purple shades
            'soft_purple': {'bg': '\x1b[48;2;140;120;180m', 'fg': '\x1b[38;2;140;120;180m', 'text': '\x1b[97m'},
            'soft_violet': {'bg': '\x1b[48;2;160;140;200m', 'fg': '\x1b[38;2;160;140;200m', 'text': '\x1b[97m'},
            'soft_lavender': {'bg': '\x1b[48;2;180;160;200m', 'fg': '\x1b[38;2;180;160;200m', 'text': '\x1b[30m'},
            
            # Earth tones
            'soft_brown': {'bg': '\x1b[48;2;140;110;90m', 'fg': '\x1b[38;2;140;110;90m', 'text': '\x1b[97m'},
            'soft_beige': {'bg': '\x1b[48;2;180;160;140m', 'fg': '\x1b[38;2;180;160;140m', 'text': '\x1b[30m'},
            'soft_sand': {'bg': '\x1b[48;2;200;180;150m', 'fg': '\x1b[38;2;200;180;150m', 'text': '\x1b[30m'},
            
            # Deep soft colors
            'deep_blue': {'bg': '\x1b[48;2;50;70;100m', 'fg': '\x1b[38;2;50;70;100m', 'text': '\x1b[97m'},
            'deep_green': {'bg': '\x1b[48;2;60;90;70m', 'fg': '\x1b[38;2;60;90;70m', 'text': '\x1b[97m'},
            'deep_purple': {'bg': '\x1b[48;2;80;60;100m', 'fg': '\x1b[38;2;80;60;100m', 'text': '\x1b[97m'},
            'deep_red': {'bg': '\x1b[48;2;120;60;60m', 'fg': '\x1b[38;2;120;60;60m', 'text': '\x1b[97m'},
            
            # Keep some original colors for compatibility
            'black': {'bg': '\x1b[48;2;30;30;35m', 'fg': '\x1b[38;2;30;30;35m', 'text': '\x1b[97m'},
            'white': {'bg': '\x1b[48;2;220;225;230m', 'fg': '\x1b[38;2;220;225;230m', 'text': '\x1b[30m'},
            'red': {'bg': '\x1b[48;2;180;90;90m', 'fg': '\x1b[38;2;180;90;90m', 'text': '\x1b[97m'},
            'green': {'bg': '\x1b[48;2;120;160;120m', 'fg': '\x1b[38;2;120;160;120m', 'text': '\x1b[97m'},
            'blue': {'bg': '\x1b[48;2;90;120;180m', 'fg': '\x1b[38;2;90;120;180m', 'text': '\x1b[97m'},
            'yellow': {'bg': '\x1b[48;2;200;180;100m', 'fg': '\x1b[38;2;200;180;100m', 'text': '\x1b[30m'},
            'cyan': {'bg': '\x1b[48;2;100;160;180m', 'fg': '\x1b[38;2;100;160;180m', 'text': '\x1b[97m'},
            'magenta': {'bg': '\x1b[48;2;160;140;200m', 'fg': '\x1b[38;2;160;140;200m', 'text': '\x1b[97m'},
            'orange': {'bg': '\x1b[48;2;200;140;90m', 'fg': '\x1b[38;2;200;140;90m', 'text': '\x1b[97m'},
            'purple': {'bg': '\x1b[48;2;140;120;180m', 'fg': '\x1b[38;2;140;120;180m', 'text': '\x1b[97m'},
            'pink': {'bg': '\x1b[48;2;200;140;160m', 'fg': '\x1b[38;2;200;140;160m', 'text': '\x1b[97m'},
            'teal': {'bg': '\x1b[48;2;80;140;140m', 'fg': '\x1b[38;2;80;140;140m', 'text': '\x1b[97m'},
            'gray': {'bg': '\x1b[48;2;90;95;100m', 'fg': '\x1b[38;2;90;95;100m', 'text': '\x1b[97m'},
            'dark_gray': {'bg': '\x1b[48;2;60;65;70m', 'fg': '\x1b[38;2;60;65;70m', 'text': '\x1b[97m'},
            'light_gray': {'bg': '\x1b[48;2;140;145;150m', 'fg': '\x1b[38;2;140;145;150m', 'text': '\x1b[97m'},
            'dark_blue': {'bg': '\x1b[48;2;50;70;100m', 'fg': '\x1b[38;2;50;70;100m', 'text': '\x1b[97m'},
            'dark_green': {'bg': '\x1b[48;2;60;90;70m', 'fg': '\x1b[38;2;60;90;70m', 'text': '\x1b[97m'},
            'dark_red': {'bg': '\x1b[48;2;120;60;60m', 'fg': '\x1b[38;2;120;60;60m', 'text': '\x1b[97m'},
            'lime': {'bg': '\x1b[48;2;140;200;160m', 'fg': '\x1b[38;2;140;200;160m', 'text': '\x1b[30m'},
            'navy': {'bg': '\x1b[48;2;50;70;100m', 'fg': '\x1b[38;2;50;70;100m', 'text': '\x1b[97m'},
        }
        
        # Better Unicode/Nerd font icons - minimal and clean
        self.icons = [
            # Nerd font powerline symbols and icons
            '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '',
            # Basic Unicode symbols
            '▶', '◀', '▲', '▼', '◆', '◇', '○', '●',
            '□', '■', '▪', '▫', '◉', '◎', '◈', '◊',
            '⬢', '⬡', '⬟', '⬠', '⬤', '⬥', '⬦', '⬧',
            # Minimal text indicators
            '»', '«', '›', '‹', '•', '·', '×', '÷',
            '±', '≈', '≠', '≤', '≥', '∞', '∑', '∏',
        ]
        
        # Generate 100 themes
        self.themes = self._generate_100_themes()
        
        # Load real session data
        self.session_data = self._load_real_session_data()
    
    def _generate_100_themes(self):
        """Generate 100 powerline themes"""
        # Use fixed seed for consistent themes
        random.seed(42)
        themes = {}
        
        # Base theme names
        base_names = [
            'cyber', 'matrix', 'fire', 'ocean', 'neon', 'space', 'quantum', 'neural',
            'dark', 'light', 'forest', 'ice', 'storm', 'solar', 'lunar', 'cosmic',
            'retro', 'modern', 'classic', 'elite', 'pro', 'ultra', 'mega', 'super',
            'alpha', 'beta', 'gamma', 'delta', 'omega', 'prime', 'turbo', 'nitro'
        ]
        
        # Color schemes
        color_schemes = [
            ['black', 'red', 'yellow', 'green', 'blue'],
            ['dark_blue', 'blue', 'cyan', 'white'],
            ['red', 'orange', 'yellow', 'white'],
            ['dark_green', 'green', 'lime', 'white'],
            ['black', 'purple', 'magenta', 'pink'],
            ['navy', 'blue', 'cyan', 'light_gray'],
            ['dark_red', 'red', 'orange', 'yellow'],
            ['black', 'dark_gray', 'gray', 'light_gray', 'white'],
            ['purple', 'magenta', 'pink', 'white'],
            ['teal', 'cyan', 'blue', 'white'],
            ['dark_green', 'green', 'yellow', 'orange'],
            ['black', 'red', 'magenta', 'cyan'],
        ]
        
        # Generate themes
        for i in range(100):
            base_name = random.choice(base_names)
            theme_name = f"{base_name}_{i+1:03d}"
            colors = random.choice(color_schemes)
            
            # Random widget count (6-11)
            widget_count = random.randint(6, 11)
            
            # Build widgets with logical grouping
            widgets = []
            
            # 1. Start with model info
            widgets.append('model_short')
            
            # 2. Add session/time info (choose ONE)
            time_widgets = ['session_elapsed', 'session_remaining', 'session_end_local']
            widgets.append(random.choice(time_widgets))
            
            # 3. Group token widgets together (1-3 consecutive)
            token_widgets = ['tokens_total', 'input_tokens', 'output_tokens', 'cache_read_tokens']
            num_token_widgets = random.randint(1, min(3, widget_count - 4))  # Leave room for other widgets
            selected_tokens = random.sample(token_widgets, num_token_widgets)
            widgets.extend(selected_tokens)  # Add all token widgets consecutively
            
            # 4. Add cost info
            widgets.append('session_cost')
            
            # 5. Fill remaining with other widgets
            needed = widget_count - len(widgets)
            if needed > 0:
                # System/info widgets
                info_widgets = ['git_branch', 'message_count', 'session_number', 'current_time', 'folder_name']
                # Performance widgets  
                perf_widgets = ['cpu_usage', 'memory_usage', 'context_percentage']
                
                all_additional = info_widgets + perf_widgets
                
                # Prefer certain widgets for better UX
                priority_widgets = []
                if 'git_branch' in all_additional:
                    priority_widgets.append('git_branch')
                    all_additional.remove('git_branch')
                if 'folder_name' in all_additional:
                    priority_widgets.append('folder_name')
                    all_additional.remove('folder_name')
                
                # Add priority widgets first
                for w in priority_widgets[:needed]:
                    widgets.append(w)
                    needed -= 1
                
                # Fill remaining slots
                if needed > 0:
                    selected = random.sample(all_additional, min(needed, len(all_additional)))
                    widgets.extend(selected)
            
            # Create theme with CREATIVE & DIVERSE icons
            segments = []
            
            # Creative icon pools - much more variety!
            model_icons = ['', '', '', '', '', '', '', '', '󰚩', '󱚤', '󰧑', '󰢚']
            elapsed_icons = ['', '', '', '', '󰥔', '', '󰔟', '󱑍']
            remaining_icons = ['⏳', '⌛', '', '', '󰔚', '󱎫', '󰦖']
            end_time_icons = ['⏰', '', '', '󰀠', '󰃰', '󱑊', '󱑋']
            cost_icons = ['', '', '', '󰈐', '󰳼', '󱥿', '󰉁', '󰎗']
            git_icons = ['', '', '', '', '󰊢', '󰘬', '󱓋']
            msg_icons = ['', '', '', '󰍡', '󰻞', '󰏪', '󱅫', '󰭻']
            token_in_icons = ['󰁔', '󰁕', '', '󰈑', '󱃾', '󰩳']
            token_out_icons = ['󰁏', '󰁖', '', '󰈐', '󱂿', '󰩴']
            token_total_icons = ['', '', '󰪺', '󰧮', '󱁿', '󰾆']
            cache_icons = ['', '', '', '󰍛', '󱂺', '󰓦']
            cpu_icons = ['', '', '󰻠', '󰍛', '󰘚', '󱓇']
            memory_icons = ['', '', '󰑭', '󰍛', '󰒋', '󱂵']
            percent_icons = ['󰔏', '', '󱨇', '󰪞', '󱘲', '󰓅']
            session_icons = ['', '󰎕', '󰎈', '󰲠', '󰲢', '󱗜']
            time_icons = ['', '', '󰅐', '󰔛', '󱑍', '󱦟']
            
            # More creative selection with theme-based variety
            theme_style = random.choice(['tech', 'minimal', 'fancy', 'retro', 'modern'])
            
            for j, widget in enumerate(widgets):
                color = colors[j % len(colors)]
                
                # Select icon based on widget and theme style
                if widget == 'model_short':
                    if theme_style == 'tech':
                        icon = random.choice(['', '', ''])
                    elif theme_style == 'minimal':
                        icon = random.choice(['', '󰧑'])
                    else:
                        icon = random.choice(model_icons)
                        
                elif widget == 'session_elapsed':
                    icon = random.choice(elapsed_icons)
                    
                elif widget == 'session_cost':
                    if theme_style == 'minimal':
                        icon = random.choice(['', ''])
                    else:
                        icon = random.choice(cost_icons)
                        
                elif widget == 'git_branch':
                    # Always use git icon for branch
                    icon = random.choice(['', '', '', ''])  # Git-specific icons
                    
                elif widget in ['session_end_time', 'session_end_local']:
                    icon = random.choice(end_time_icons)
                    
                elif widget == 'session_remaining':
                    icon = random.choice(remaining_icons)
                    
                elif widget == 'message_count':
                    icon = random.choice(msg_icons)
                    
                elif widget == 'input_tokens':
                    icon = random.choice(token_in_icons)
                    
                elif widget == 'output_tokens':
                    icon = random.choice(token_out_icons)
                    
                elif widget == 'tokens_total':
                    icon = random.choice(token_total_icons)
                    
                elif widget == 'cache_read_tokens':
                    icon = random.choice(cache_icons)
                    
                elif widget == 'current_time':
                    icon = random.choice(time_icons)
                    
                elif widget == 'cpu_usage':
                    icon = random.choice(cpu_icons)
                    
                elif widget == 'memory_usage':
                    icon = random.choice(memory_icons)
                    
                elif widget == 'session_number':
                    icon = random.choice(session_icons)
                    
                elif widget == 'context_percentage':
                    icon = random.choice(percent_icons)
                    
                elif widget == 'folder_name':
                    # Always use folder icon
                    folder_icons = ['', '', '', '', '', '']
                    icon = random.choice(folder_icons)
                    
                elif widget == 'cache_write_tokens':
                    # Cache write icons
                    icon = random.choice(['', '', '', ''])
                    
                else:
                    icon = random.choice(['', '', '󰇙', '󱗖'])
                
                segments.append({
                    'widget': widget,
                    'icon': icon,
                    'color': color
                })
            
            themes[theme_name] = {
                'name': theme_name.replace('_', ' ').title(),
                'description': f'Powerline theme #{i+1} with {len(segments)} widgets',
                'segments': segments
            }
        
        return themes
    
    def _load_real_session_data(self):
        """Load REAL session data"""
        try:
            from claude_statusline.data_directory_utils import get_default_data_directory
            data_dir = get_default_data_directory()
            db_path = data_dir / "smart_sessions_db.json"
            
            with open(db_path, 'r', encoding='utf-8') as f:
                db_data = json.load(f)
            
            return db_data.get('current_session', {})
        except Exception:
            return {}
    
    def get_widget_value(self, widget_type):
        """Get REAL widget value"""
        if not self.session_data:
            return "N/A"
        
        try:
            if widget_type == 'model_short':
                model = self.session_data.get('model', '')
                if 'opus-4' in model:
                    return 'Opus-4'
                elif 'sonnet-4' in model:
                    return 'Sonnet-4'
                elif 'sonnet' in model:
                    return 'Sonnet'
                else:
                    return 'Claude'
            
            elif widget_type == 'session_elapsed':
                try:
                    from datetime import timezone
                    start_str = self.session_data.get('session_start')
                    if start_str:
                        if 'T' in start_str and '+' not in start_str and 'Z' not in start_str:
                            start_str += '+00:00'
                        start_time = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                        now = datetime.now(timezone.utc)
                        elapsed = now - start_time
                        hours = int(elapsed.total_seconds() // 3600)
                        minutes = int((elapsed.total_seconds() % 3600) // 60)
                        if hours > 0:
                            return f"{hours}h{minutes:02d}m"
                        else:
                            return f"{minutes}m"
                except:
                    pass
                return "0m"
            
            elif widget_type == 'session_cost':
                cost = self.session_data.get('cost', 0)
                return f"${cost:.1f}"
            
            elif widget_type == 'message_count':
                count = self.session_data.get('message_count', 0)
                if count >= 1000:
                    return f"{count//1000}k"
                return str(count)
            
            elif widget_type == 'tokens_total':
                tokens = self.session_data.get('tokens', 0)
                if tokens >= 1000000:
                    return f"{tokens//1000000}M"
                elif tokens >= 1000:
                    return f"{tokens//1000}k"
                return str(tokens)
            
            elif widget_type == 'input_tokens':
                tokens = self.session_data.get('input_tokens', 0)
                if tokens >= 1000:
                    return f"{tokens//1000}k"
                return str(tokens)
            
            elif widget_type == 'output_tokens':
                tokens = self.session_data.get('output_tokens', 0)
                if tokens >= 1000:
                    return f"{tokens//1000}k"
                return str(tokens)
            
            elif widget_type == 'cache_read_tokens':
                tokens = self.session_data.get('cache_read_tokens', 0)
                if tokens >= 1000000:
                    return f"{tokens//1000000}M"
                elif tokens >= 1000:
                    return f"{tokens//1000}k"
                return str(tokens)
            
            elif widget_type == 'git_branch':
                try:
                    result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                          capture_output=True, text=True, timeout=2)
                    if result.returncode == 0:
                        branch = result.stdout.strip()
                        if len(branch) > 15:
                            return branch[:12] + "..."
                        return branch
                except:
                    pass
                return "main"
            
            elif widget_type == 'session_number':
                num = self.session_data.get('session_number', 1)
                return f"#{num}"
            
            elif widget_type == 'context_percentage':
                return "75%"  # Mock for now
            
            elif widget_type == 'current_time':
                return datetime.now().strftime("%H:%M")
            
            elif widget_type == 'cpu_usage':
                return "25%"  # Mock for now
            
            elif widget_type == 'memory_usage':
                return "68%"  # Mock for now
            
            elif widget_type == 'folder_name':
                # Get current folder name
                import os
                folder = os.path.basename(os.getcwd())
                if len(folder) > 15:
                    return folder[:12] + "..."
                return folder
            
            elif widget_type == 'cache_write_tokens':
                # Cache write tokens available too!
                tokens = self.session_data.get('cache_write_tokens', 0)
                if tokens >= 1000000:
                    return f"{tokens//1000000}M"
                elif tokens >= 1000:
                    return f"{tokens//1000}k"
                return str(tokens)
            
            elif widget_type == 'session_end_time':
                # Calculate session end time (5 hours from start)
                try:
                    from datetime import timedelta
                    session_start = self.session_data.get('session_start', '')
                    if session_start:
                        start_dt = datetime.fromisoformat(session_start)
                        end_dt = start_dt + timedelta(hours=5)
                        return end_dt.strftime("%H:%M UTC")
                except:
                    pass
                return "--:--"
            
            elif widget_type == 'session_remaining':
                # Calculate remaining time in session
                try:
                    from datetime import timedelta
                    session_start = self.session_data.get('session_start', '')
                    if session_start:
                        start_dt = datetime.fromisoformat(session_start)
                        now_dt = datetime.now(start_dt.tzinfo)
                        elapsed = now_dt - start_dt
                        remaining = timedelta(hours=5) - elapsed
                        if remaining.total_seconds() > 0:
                            hours = int(remaining.total_seconds() // 3600)
                            minutes = int((remaining.total_seconds() % 3600) // 60)
                            return f"{hours}h{minutes:02d}m"
                        else:
                            return "ended"
                except:
                    pass
                return "--:--"
            
            elif widget_type == 'session_end_local':
                # Session end in system's local timezone
                try:
                    from datetime import timedelta, timezone
                    session_start = self.session_data.get('session_start', '')
                    if session_start:
                        start_dt = datetime.fromisoformat(session_start)
                        end_dt = start_dt + timedelta(hours=5)
                        
                        # Convert to system's local timezone
                        # First ensure we have UTC timezone info
                        if end_dt.tzinfo is None:
                            end_dt = end_dt.replace(tzinfo=timezone.utc)
                        
                        # Convert to local time using system's timezone
                        local_end = end_dt.astimezone()
                        return local_end.strftime("%H:%M")
                except:
                    pass
                return "--:--"
            
            else:
                return "N/A"
        
        except Exception:
            return "ERR"
    
    def render_theme(self, theme_name, force_simple=False):
        """Render powerline theme - ALWAYS with nerd fonts"""
        # NO CHECKS - JUST RENDER POWERLINE!
        
        if theme_name not in self.themes:
            theme_name = list(self.themes.keys())[0]
        
        theme = self.themes[theme_name]
        segments = theme['segments']
        
        # First line - regular powerline segments
        result = "⧂ "  # Start with circle with small circle icon
        
        for i, segment in enumerate(segments):
            # Get REAL widget value
            widget_value = self.get_widget_value(segment['widget'])
            icon = segment['icon']
            color_name = segment['color']
            color_info = self.colors[color_name]
            
            # Create segment content
            content = f" {icon} {widget_value} "
            
            # Apply segment colors - USE ACTUAL ESCAPE CODES NOT STRINGS
            segment_output = color_info['bg'] + color_info['text'] + content + '\x1b[0m'
            result += segment_output
            
            # Add PERFECT powerline triangle
            if i < len(segments) - 1:
                next_segment = segments[i + 1]
                next_color_name = next_segment['color']
                next_color_info = self.colors[next_color_name]
                
                # PERFECT triangle logic
                triangle_bg = next_color_info['bg']
                triangle_fg = color_info['fg']
                
                separator = triangle_bg + triangle_fg + '\ue0b0' + '\x1b[0m'
                result += separator
            else:
                # Add final triangle after last widget
                # Triangle color = last widget bg, background = terminal default
                final_triangle = '\x1b[0m' + color_info['fg'] + '\ue0b0' + '\x1b[0m'
                result += final_triangle
        
        # Second line - progress bar with block characters
        result += "\n"
        result += self._render_progress_bar()
        
        return result
    
    def _render_progress_bar(self):
        """Render a progress bar for the second line"""
        # Calculate session progress
        session_progress = self._calculate_session_progress()
        
        # Get session elapsed and remaining time
        elapsed_str = self.get_widget_value('session_elapsed')
        remaining_str = self.get_widget_value('session_remaining')
        
        # Progress bar settings
        bar_width = 30
        filled = int(bar_width * session_progress)
        empty = bar_width - filled
        
        # Create block characters for progress
        filled_blocks = '◼' * filled
        empty_blocks = '◻' * empty
        
        # Choose colors
        if session_progress < 0.33:
            # Green for fresh session
            bar_color = self.colors['soft_green']
        elif session_progress < 0.66:
            # Yellow for mid session
            bar_color = self.colors['soft_yellow']
        else:
            # Orange/red for ending session
            bar_color = self.colors['soft_orange']
        
        # Build progress bar with powerline style
        progress_bar = "⧂ "  # Start with circle with small circle icon
        
        # Left segment with elapsed time
        left_color = self.colors['soft_gray']
        progress_bar += left_color['bg'] + left_color['text']
        progress_bar += f" ⏱ {elapsed_str} "
        progress_bar += '\x1b[0m'
        
        # Triangle transition
        progress_bar += bar_color['bg'] + left_color['fg'] + '\ue0b0' + '\x1b[0m'
        
        # Progress bar segment
        progress_bar += bar_color['bg'] + bar_color['text']
        progress_bar += f" [{filled_blocks}{empty_blocks}] ❱ {session_progress*100:.0f}% "
        progress_bar += '\x1b[0m'
        
        # Triangle transition
        right_color = self.colors['soft_blue']
        progress_bar += right_color['bg'] + bar_color['fg'] + '\ue0b0' + '\x1b[0m'
        
        # Right segment with remaining time
        progress_bar += right_color['bg'] + right_color['text']
        progress_bar += f" {remaining_str} ⏳ "
        progress_bar += '\x1b[0m'
        
        # Final triangle
        progress_bar += '\x1b[0m' + right_color['fg'] + '\ue0b0' + '\x1b[0m'
        
        return progress_bar
    
    def _calculate_session_progress(self):
        """Calculate session progress (0.0 to 1.0)"""
        try:
            session_start = self.session_data.get('session_start')
            if not session_start:
                return 0.0
            
            from datetime import timedelta
            if 'T' in session_start and '+' not in session_start and 'Z' not in session_start:
                session_start += '+00:00'
            start_dt = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
            now_dt = datetime.now(timezone.utc)
            elapsed = now_dt - start_dt
            total_duration = timedelta(hours=5)
            
            progress = elapsed.total_seconds() / total_duration.total_seconds()
            return min(1.0, max(0.0, progress))
        except:
            return 0.0
    
    def render_simple_theme(self, theme_name):
        """Simple ASCII fallback for broken terminals"""
        if theme_name not in self.themes:
            theme_name = list(self.themes.keys())[0]
        
        theme = self.themes[theme_name]
        segments = theme['segments']
        
        parts = []
        for segment in segments[:6]:  # Show up to 6 widgets
            widget = segment['widget']
            widget_value = self.get_widget_value(widget)
            
            # Shorten widget names for display
            if widget == 'model_short':
                parts.append(f"{widget_value}")
            elif widget == 'session_elapsed':
                parts.append(f"{widget_value}")
            elif widget == 'session_cost':
                parts.append(f"{widget_value}")
            elif widget == 'git_branch':
                parts.append(f"git:{widget_value}")
            elif widget == 'message_count':
                parts.append(f"{widget_value}msg")
            elif widget == 'tokens_total':
                parts.append(f"{widget_value}tok")
            else:
                parts.append(f"{widget_value}")
        
        return " | ".join(parts)
    
    def _check_terminal_capability(self):
        """Check if terminal supports ANSI colors"""
        import os
        import sys
        
        # Check for Windows Terminal
        if os.environ.get('WT_SESSION'):
            return True
        
        # Check for known good terminals
        term = os.environ.get('TERM', '').lower()
        if any(x in term for x in ['xterm', '256color', 'screen', 'tmux', 'alacritty', 'kitty']):
            return True
        
        # Check for ConEmu/cmder
        if os.environ.get('ConEmuPID'):
            return True
        
        # Windows check - if not in good terminal, likely cmd.exe
        if sys.platform == 'win32':
            # Check if we're in VS Code terminal
            if os.environ.get('TERM_PROGRAM') == 'vscode':
                return True
            # Windows Terminal is detected via WT_SESSION above
            # So if we get here, it's likely cmd.exe or PowerShell without WT
            return False
        
        return True
    
    def list_themes(self):
        """List all themes"""
        return list(self.themes.keys())
    
    def get_theme(self, theme_name):
        """Get theme info"""
        return self.themes.get(theme_name)
    
    def set_current_theme(self, theme_name):
        """Set current theme in config"""
        try:
            from claude_statusline.data_directory_utils import get_default_data_directory
            data_dir = get_default_data_directory()
            config_path = data_dir / "theme_config.json"
            
            config = {
                "current_theme": theme_name,
                "rotation_enabled": False
            }
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            return True
        except Exception:
            return False
    
    def get_current_theme(self):
        """Get current theme from config"""
        try:
            from claude_statusline.data_directory_utils import get_default_data_directory
            data_dir = get_default_data_directory()
            config_path = data_dir / "theme_config.json"
            
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                return config.get('current_theme', list(self.themes.keys())[0])
        except Exception:
            pass
        
        return list(self.themes.keys())[0]

# Global instance
UNIFIED_POWERLINE = UnifiedPowerlineSystem()