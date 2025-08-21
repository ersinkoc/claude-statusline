#!/usr/bin/env python3
"""
Unified Theme System - Single theme/template management system
Handles all theme and template needs
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Import professional themes
try:
    from .professional_powerline import ProfessionalPowerline, get_professional_themes
    PROFESSIONAL_AVAILABLE = True
except ImportError:
    PROFESSIONAL_AVAILABLE = False

def safe_unicode_print(text: str) -> str:
    """Force UTF-8 Unicode output with nerd font support"""
    
    # Force UTF-8 output on Windows
    if os.name == 'nt':
        try:
            # Set console to UTF-8 mode
            import subprocess
            subprocess.run(['chcp', '65001'], capture_output=True, shell=True)
            
            # Try to write directly to stdout buffer as UTF-8
            if hasattr(sys.stdout, 'buffer'):
                encoded = text.encode('utf-8')
                sys.stdout.buffer.write(encoded)
                sys.stdout.buffer.flush()
                return ""  # Already printed
        except Exception:
            pass
    
    # Return text for normal printing
    return text

def convert_to_ascii_fallback(text: str) -> str:
    """Convert Unicode themes to ASCII fallback versions"""
    # First, remove all ANSI escape sequences (both \033 and \x1b formats)
    import re
    # Handle raw string format \033
    result = re.sub(r'\\033\[[0-9;:]*m', '', text)
    # Handle actual escape sequences \x1b
    result = re.sub(r'\x1b\[[0-9;:]*m', '', result)
    
    # Unicode to ASCII replacements
    replacements = {
        # Powerline arrows (nerd fonts)
        '\ue0b0': '>',  # Right arrow
        '\ue0b2': '<',  # Left arrow  
        '\ue0b1': '/',  # Right arrow thin
        '\ue0b3': '\\', # Left arrow thin
        
        # Common emojis to ASCII
        '⚡': '[*]', '🌊': '~', '💻': '[PC]', '🔥': '[!]',
        '🌿': '&', '📁': '[DIR]', '🌙': 'o', '💰': '$',
        '🎮': '[GAME]', '⚔️': '[X]', '🏆': '[WIN]', '💎': '*',
        '🎲': '[D]', '🚀': '^', '⭐': '*', '🌌': '.',
        '🛸': '()', '💼': '[BAG]', '📊': '[CHT]', '📈': '/',
        '🎯': 'O', '🔧': '[T]', '⚙️': '@', '🌍': '(O)',
        '🥷': '[N]', '🌲': '[T]', '🌅': '[S]', '🔴': '(R)',
        '🏠': '[H]', '🔗': '-', '💾': '[M]', '📡': '[A]',
        '🐠': '<>', '🪸': 'C', '🗼': '|', '⛵': 'S',
        '🌳': 'T', '🍂': '~', '🐿️': 's', '🌰': 'o',
        '👔': '[S]', '🏢': '[B]', '📊': '[C]', '🎯': 'O',
    }
    
    # Apply replacements
    for unicode_char, ascii_replacement in replacements.items():
        result = result.replace(unicode_char, ascii_replacement)
    
    # Remove any remaining non-ASCII characters
    try:
        result = result.encode('ascii', errors='replace').decode('ascii')
    except:
        # If still failing, use very basic cleanup
        result = ''.join(c if ord(c) < 128 else '?' for c in result)
    
    return result

def check_nerd_font_support():
    """Force enable nerd font support - assume user has nerd fonts installed"""
    # Always return True - user wants nerd font support
    return True

def get_safe_separators():
    """Get safe separators based on font support"""
    if check_nerd_font_support():
        return {
            'arrow_right': '\ue0b0',
            'arrow_left': '\ue0b2', 
            'rounded_right': '\ue0b4',
            'rounded_left': '\ue0b6',
            'flame_right': '\ue0c0',
            'flame_left': '\ue0c2',
            'triangle_right': '\ue0b8',
            'triangle_left': '\ue0ba',
        }
    else:
        return {
            'arrow_right': '>',
            'arrow_left': '<',
            'rounded_right': ')',
            'rounded_left': '(',
            'flame_right': '>',
            'flame_left': '<',
            'triangle_right': '>',
            'triangle_left': '<',
        }

class UnifiedThemeSystem:
    """Unified theme system - both built-in themes and custom builder"""
    
    def __init__(self):
        self.config_file = Path(__file__).parent / "config.json"
        self.custom_themes_file = Path.home() / ".claude" / "data-statusline" / "custom_themes.json"
        
        # Initialize professional powerline if available
        if PROFESSIONAL_AVAILABLE:
            self.professional_powerline = ProfessionalPowerline()
        else:
            self.professional_powerline = None
        
        # Built-in themes (renkli, renksiz, multiline)
        self.builtin_themes = {
            # === MINIMALIST THEMES ===
            "minimal": {
                "name": "Minimal",
                "description": "Clean and simple",
                "template": "{model} | {messages}msg ${cost}",
                "multiline": False,
                "colored": False
            },
            "compact": {
                "name": "Compact", 
                "description": "Space-efficient display",
                "template": "[{model}] {messages}m {tokens} ${cost}",
                "multiline": False,
                "colored": False
            },
            
            # === COLORED THEMES ===
            "pro": {
                "name": "Professional",
                "description": "Clean with colors",
                "template": "[PRO] {model} | Sessions: {sessions} | Messages: {messages} | Cost: ${cost}",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Fore.CYAN,
                    "messages": Fore.GREEN,
                    "cost": Fore.YELLOW,
                    "separator": Fore.WHITE
                }
            },
            "hacker": {
                "name": "Hacker",
                "description": "Matrix-style green",
                "template": ">> {model} :: MSG[{messages}] :: TOK[{tokens}] :: ${cost}",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Fore.GREEN,
                    "messages": Fore.LIGHTGREEN_EX,
                    "tokens": Fore.GREEN,
                    "cost": Fore.LIGHTGREEN_EX,
                    "separator": Fore.GREEN
                }
            },
            "fire": {
                "name": "Fire",
                "description": "Warm red/orange theme",
                "template": "🔥 {model} | {messages} msgs | {tokens} tokens | ${cost}",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Fore.RED,
                    "messages": Fore.LIGHTYELLOW_EX,
                    "tokens": Fore.YELLOW,
                    "cost": Fore.LIGHTRED_EX,
                    "separator": Fore.RED
                }
            },
            "ocean": {
                "name": "Ocean",
                "description": "Cool blue theme",
                "template": "🌊 {model} ~ {messages}msg ~ {tokens} ~ ${cost}",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Fore.BLUE,
                    "messages": Fore.CYAN,
                    "tokens": Fore.LIGHTBLUE_EX,
                    "cost": Fore.LIGHTCYAN_EX,
                    "separator": Fore.BLUE
                }
            },
            
            # === MULTILINE THEMES ===
            "dashboard": {
                "name": "Dashboard",
                "description": "Multi-line detailed view",
                "template": "╔══ CLAUDE STATUS ══╗\n║ Model: {model}\n║ Messages: {messages}\n║ Tokens: {tokens}\n║ Cost: ${cost}\n╚═══════════════════╝",
                "multiline": True,
                "colored": True,
                "colors": {
                    "model": Fore.CYAN,
                    "messages": Fore.GREEN,
                    "tokens": Fore.YELLOW,
                    "cost": Fore.RED,
                    "box": Fore.WHITE
                }
            },
            "detailed": {
                "name": "Detailed",
                "description": "Full information display",
                "template": "=== Claude AI Status ===\nModel: {model}\nSession: {session_time}\nMessages: {messages}\nTokens: {tokens}\nCost: ${cost}\nEfficiency: {efficiency}%",
                "multiline": True,
                "colored": False
            },
            
            # === EMOJI THEMES ===
            "emoji": {
                "name": "Emoji",
                "description": "Fun with emojis",
                "template": "🤖 {model} | 💬 {messages} | 🪙 {tokens} | 💰 ${cost}",
                "multiline": False,
                "colored": False
            },
            "zen": {
                "name": "Zen",
                "description": "Calm and peaceful",
                "template": "☯ {model} • {messages} messages • ${cost}",
                "multiline": False,
                "colored": False
            },
            
            # === PROFESSIONAL POWERLINE THEMES ===
            "powerline_pro": {
                "name": "Powerline Pro",
                "description": "Professional segments with colors",
                "template": "",
                "multiline": False,
                "colored": True,
                "powerline": True,
                "segments": [
                    {"content": "Model: {model}", "bg": "blue", "fg": "white"},
                    {"content": "Ctx: {tokens}k", "bg": "yellow", "fg": "black"},
                    {"content": "${cost}", "bg": "red", "fg": "white"},
                    {"content": "{messages}msg", "bg": "green", "fg": "black"}
                ]
            },
            "powerline_git": {
                "name": "Git Style",
                "description": "Git-inspired colorful segments",
                "template": "",
                "multiline": False,
                "colored": True,
                "powerline": True,
                "segments": [
                    {"content": "{model}", "bg": "magenta", "fg": "white"},
                    {"content": "In: {messages}", "bg": "cyan", "fg": "black"},
                    {"content": "Out: {tokens}k", "bg": "green", "fg": "black"},
                    {"content": "${cost}", "bg": "red", "fg": "white"}
                ]
            },
            "powerline_elegant": {
                "name": "Elegant Flow",
                "description": "Soft gradient-like segments",
                "template": "",
                "multiline": False,
                "colored": True,
                "powerline": True,
                "segments": [
                    {"content": "{model}", "bg": "blue", "fg": "white"},
                    {"content": "{tokens}k", "bg": "lightblue", "fg": "black"},
                    {"content": "${cost}", "bg": "lightyellow", "fg": "black"},
                    {"content": "{messages}msg", "bg": "lightgreen", "fg": "black"}
                ]
            },
            "nerd_elite": {
                "name": "Nerd Elite",
                "description": "Elite nerd font powerline",
                "template": "  {model}   {messages}   {tokens}   ${cost} ",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Back.MAGENTA + Fore.WHITE,
                    "messages": Back.CYAN + Fore.BLACK,
                    "tokens": Back.YELLOW + Fore.BLACK,
                    "cost": Back.RED + Fore.WHITE
                }
            },
            "rounded_powerline": {
                "name": "Rounded Powerline",
                "description": "Soft rounded powerline segments",
                "template": " {model}  {messages}msg  {tokens}  ${cost} ",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Back.BLUE + Fore.WHITE,
                    "messages": Back.GREEN + Fore.BLACK,
                    "tokens": Back.YELLOW + Fore.BLACK,
                    "cost": Back.RED + Fore.WHITE
                }
            },
            "cosmic_beam": {
                "name": "Cosmic Beam",
                "description": "Futuristic cosmic design",
                "template": "  {model}   {messages}   {tokens}   ${cost} ",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Back.MAGENTA + Fore.YELLOW,
                    "messages": Back.BLUE + Fore.WHITE,
                    "tokens": Back.CYAN + Fore.BLACK,
                    "cost": Back.RED + Fore.WHITE
                }
            },
            "diamond_sharp": {
                "name": "Diamond Sharp",
                "description": "Sharp diamond separators",
                "template": " {model}  {messages}  {tokens}  ${cost} ",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Back.LIGHTBLUE_EX + Fore.BLACK,
                    "messages": Back.LIGHTGREEN_EX + Fore.BLACK,
                    "tokens": Back.LIGHTYELLOW_EX + Fore.BLACK,
                    "cost": Back.LIGHTRED_EX + Fore.BLACK
                }
            },
            "terminal_hacker": {
                "name": "Terminal Hacker",
                "description": "Hacker terminal with nerd icons",
                "template": "  {model}   {messages}msg   {tokens}   ${cost} ",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Fore.GREEN,
                    "messages": Fore.LIGHTGREEN_EX,
                    "tokens": Fore.GREEN,
                    "cost": Fore.YELLOW
                }
            },
            "gradient_flow": {
                "name": "Gradient Flow",
                "description": "Smooth gradient transitions",
                "template": " {model}  {messages}  {tokens}  ${cost} ",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Back.BLUE + Fore.WHITE,
                    "messages": Back.LIGHTBLUE_EX + Fore.BLACK,
                    "tokens": Back.CYAN + Fore.BLACK,
                    "cost": Back.LIGHTCYAN_EX + Fore.BLACK
                }
            },
            "neon_glow": {
                "name": "Neon Glow",
                "description": "Cyberpunk neon aesthetic",
                "template": " {model}  {messages}  {tokens}  ${cost} ",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Back.MAGENTA + Fore.YELLOW,
                    "messages": Back.CYAN + Fore.MAGENTA,
                    "tokens": Back.YELLOW + Fore.MAGENTA,
                    "cost": Back.RED + Fore.YELLOW
                }
            },
            "arrow_stream": {
                "name": "Arrow Stream",
                "description": "Dynamic arrow flow",
                "template": " {model}  {messages}msg  {tokens}  ${cost} ",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Back.BLUE + Fore.WHITE,
                    "messages": Back.GREEN + Fore.WHITE,
                    "tokens": Back.YELLOW + Fore.BLACK,
                    "cost": Back.RED + Fore.WHITE
                }
            },
            "bubble_pop": {
                "name": "Bubble Pop",
                "description": "Playful bubble design",
                "template": " {model}   {messages}   {tokens}   ${cost} ",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Back.LIGHTMAGENTA_EX + Fore.BLACK,
                    "messages": Back.LIGHTGREEN_EX + Fore.BLACK,
                    "tokens": Back.LIGHTYELLOW_EX + Fore.BLACK,
                    "cost": Back.LIGHTRED_EX + Fore.BLACK
                }
            },
            "lightning_bolt": {
                "name": "Lightning Bolt",
                "description": "Electric energy theme",
                "template": "⚡  {model}  ⚡  {messages}  ⚡  {tokens}  ⚡  ${cost} ",
                "multiline": False,
                "colored": True,
                "colors": {
                    "model": Back.YELLOW + Fore.BLACK,
                    "messages": Back.BLUE + Fore.WHITE,
                    "tokens": Back.CYAN + Fore.BLACK,
                    "cost": Back.RED + Fore.WHITE
                }
            }
        }
        
        # Load custom themes
        self.custom_themes = self._load_custom_themes()
        
        # Load professional themes
        self.professional_themes = get_professional_themes() if PROFESSIONAL_AVAILABLE else {}
    
    def _load_custom_themes(self) -> Dict:
        """Load user's custom themes"""
        if self.custom_themes_file.exists():
            try:
                with open(self.custom_themes_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_custom_themes(self):
        """Save custom themes"""
        self.custom_themes_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.custom_themes_file, 'w') as f:
            json.dump(self.custom_themes, f, indent=2)
    
    def get_all_themes(self) -> Dict:
        """Get all available themes"""
        all_themes = {}
        all_themes.update(self.builtin_themes)
        all_themes.update(self.custom_themes)
        all_themes.update(self.professional_themes)
        return all_themes
    
    def _render_powerline(self, theme: Dict, data: Dict) -> str:
        """Render true powerline segments with safe fallbacks"""
        segments = theme.get("segments", [])
        if not segments:
            return f"{data['model']} | {data['messages']}msg ${data['cost']}"
        
        # Color mapping for backgrounds
        bg_colors = {
            "blue": Back.BLUE, "lightblue": Back.LIGHTBLUE_EX,
            "green": Back.GREEN, "lightgreen": Back.LIGHTGREEN_EX,
            "yellow": Back.YELLOW, "lightyellow": Back.LIGHTYELLOW_EX,
            "red": Back.RED, "lightred": Back.LIGHTRED_EX,
            "magenta": Back.MAGENTA, "lightmagenta": Back.LIGHTMAGENTA_EX,
            "cyan": Back.CYAN, "lightcyan": Back.LIGHTCYAN_EX,
            "white": Back.WHITE, "black": Back.BLACK
        }
        
        # Foreground colors
        fg_colors = {
            "white": Fore.WHITE, "black": Fore.BLACK, "red": Fore.RED,
            "green": Fore.GREEN, "yellow": Fore.YELLOW, "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA, "cyan": Fore.CYAN
        }
        
        # Check font support
        has_nerd_fonts = check_nerd_font_support()
        arrow_right = '\ue0b0' if has_nerd_fonts else '>'
        
        result_parts = []
        
        try:
            for i, segment in enumerate(segments):
                # Get colors
                bg_key = segment.get("bg", "blue")
                fg_key = segment.get("fg", "white")
                bg_color = bg_colors.get(bg_key, Back.BLUE)
                fg_color = fg_colors.get(fg_key, Fore.WHITE)
                
                # Format content safely
                try:
                    content = segment["content"].format(**data)
                except (KeyError, ValueError):
                    content = str(segment.get("content", "?"))
                
                # Always use colored segments (even without nerd fonts they look good)
                segment_part = f"{bg_color}{fg_color} {content} {Style.RESET_ALL}"
                result_parts.append(segment_part)
                
                # Add separators
                if i < len(segments) - 1:
                    if has_nerd_fonts:
                        # Real powerline arrows
                        next_bg = segments[i + 1].get("bg", "blue")
                        next_bg_color = bg_colors.get(next_bg, Back.BLUE)
                        current_bg_as_fg = self._bg_to_fg_color(bg_key)
                        arrow_part = f"{next_bg_color}{current_bg_as_fg}{arrow_right}{Style.RESET_ALL}"
                        result_parts.append(arrow_part)
                    else:
                        # Simple bracket separators that look good
                        result_parts.append(f"{Style.RESET_ALL}]{Fore.WHITE}[{Style.RESET_ALL}")
                else:
                    # Final ending
                    if has_nerd_fonts:
                        current_bg_as_fg = self._bg_to_fg_color(bg_key)
                        final_arrow = f"{current_bg_as_fg}{arrow_right}{Style.RESET_ALL}"
                        result_parts.append(final_arrow)
                    # No final character needed for bracket style
            
            result = "".join(result_parts)
            
            # For nerd fonts on Windows, skip encoding test and use safe output
            if has_nerd_fonts and os.name == 'nt':
                return result  # Let safe_unicode_print handle it
            
            # Test if result can be encoded safely (non-Windows or no nerd fonts)
            try:
                result.encode(sys.stdout.encoding or 'utf-8', 'strict')
                return result
            except UnicodeEncodeError:
                pass  # Fall through to fallback
            
        except Exception:
            # Ultimate fallback - simple format
            fallback_parts = []
            for segment in segments:
                try:
                    content = segment["content"].format(**data)
                    fallback_parts.append(f"[{content}]")
                except:
                    fallback_parts.append("[?]")
            return ">".join(fallback_parts) + ">"
    
    def _bg_to_fg_color(self, bg_color_name: str) -> str:
        """Convert background color name to corresponding foreground color"""
        bg_to_fg_map = {
            "blue": Fore.BLUE,
            "lightblue": Fore.LIGHTBLUE_EX,
            "green": Fore.GREEN,
            "lightgreen": Fore.LIGHTGREEN_EX,
            "yellow": Fore.YELLOW,
            "lightyellow": Fore.LIGHTYELLOW_EX,
            "red": Fore.RED,
            "lightred": Fore.LIGHTRED_EX,
            "magenta": Fore.MAGENTA,
            "lightmagenta": Fore.LIGHTMAGENTA_EX,
            "cyan": Fore.CYAN,
            "lightcyan": Fore.LIGHTCYAN_EX,
            "white": Fore.WHITE,
            "black": Fore.BLACK
        }
        return bg_to_fg_map.get(bg_color_name, Fore.BLUE)
    
    def _render_epic_powerline(self, theme: Dict, data: Dict) -> str:
        """Render epic powerline themes with RGB colors and full feature support"""
        segments = theme.get("segments", [])
        if not segments:
            return f"{data['model']} | {data['messages']}msg ${data['cost']}"
        
        try:
            result_parts = []
            has_nerd_fonts = check_nerd_font_support()
            arrow_right = '\ue0b0' if has_nerd_fonts else '>'
            
            for i, segment in enumerate(segments):
                # Get RGB colors for epic themes
                bg_color = segment.get("bg", "blue")
                fg_color = segment.get("fg", "white")
                
                # Convert RGB colors if they're from epic themes
                if bg_color in ['cyber_dark', 'cyber_purple', 'cyber_blue', 'cyber_green', 'cyber_pink',
                               'ocean_deep', 'ocean_blue', 'ocean_teal', 'ocean_aqua', 'ocean_foam',
                               'sunset_orange', 'sunset_red', 'sunset_yellow', 'sunset_pink', 'sunset_purple',
                               'forest_dark', 'forest_green', 'forest_lime', 'forest_moss', 'forest_mint',
                               'game_red', 'game_blue', 'game_purple', 'game_green', 'game_orange',
                               'neon_pink', 'neon_cyan', 'neon_yellow', 'neon_purple', 'neon_green',
                               'pro_navy', 'pro_blue', 'pro_silver', 'pro_gold', 'pro_platinum',
                               'mono_black', 'mono_dark', 'mono_gray', 'mono_silver', 'mono_white']:
                    # Use RGB colors from epic themes
                    from .epic_powerline_mega_themes import rgb_to_ansi_bg, rgb_to_ansi_fg
                    bg_ansi = rgb_to_ansi_bg(bg_color)
                    fg_ansi = rgb_to_ansi_fg(fg_color) if fg_color != "white" and fg_color != "black" else ""
                    
                    # Format content safely
                    try:
                        content = segment["content"].format(**data)
                    except (KeyError, ValueError):
                        content = str(segment.get("content", "?"))
                    
                    # Create segment with RGB colors
                    if fg_ansi:
                        segment_part = f"{bg_ansi}{fg_ansi} {content} \033[0m"
                    else:
                        fg_std = "\033[37m" if fg_color == "white" else "\033[30m"
                        segment_part = f"{bg_ansi}{fg_std} {content} \033[0m"
                    
                    result_parts.append(segment_part)
                    
                    # Add powerline separators for RGB themes
                    if i < len(segments) - 1 and has_nerd_fonts:
                        next_bg = segments[i + 1].get("bg", "blue")
                        next_bg_ansi = rgb_to_ansi_bg(next_bg)
                        current_fg_ansi = rgb_to_ansi_fg(bg_color)
                        arrow_part = f"{next_bg_ansi}{current_fg_ansi}{arrow_right}\033[0m"
                        result_parts.append(arrow_part)
                    elif i < len(segments) - 1:
                        result_parts.append(">")
                else:
                    # Fallback to standard colorama colors
                    return self._render_powerline(theme, data)
            
            return "".join(result_parts)
            
        except Exception:
            # Fallback for any RGB rendering issues
            return self._render_powerline(theme, data)
    
    def _render_multiline_professional(self, theme: Dict, data: Dict) -> str:
        """Render multi-line professional theme with Windows-safe powerline"""
        try:
            lines = []
            segments_list = theme.get("segments", [])
            
            # Use appropriate separator based on nerd font support
            has_nerd_fonts = check_nerd_font_support()
            sep = '\ue0b0' if has_nerd_fonts else '▶'  # Nerd font or basic arrow
            
            for line_segments in segments_list:
                line_parts = []
                for segment in line_segments:
                    content = segment.get("content", "")
                    # Format content with data
                    try:
                        formatted_content = content.format(**data)
                        line_parts.append(formatted_content)
                    except KeyError:
                        line_parts.append(content)
                
                # Join segments with separator
                if line_parts:
                    lines.append(sep.join(line_parts))
            
            return "\n".join(lines)
            
        except Exception:
            # Fallback for multiline
            return f"{data['model']}\n{data['messages']}msg | {data['tokens']}\n${data['cost']}"
    
    def apply_theme(self, theme_name: str, data: Dict) -> str:
        """Apply a theme to data and return formatted string"""
        themes = self.get_all_themes()
        
        if theme_name not in themes:
            theme_name = "minimal"  # Fallback
        
        theme = themes[theme_name]
        
        # Check if this is a powerline theme
        if theme.get("powerline", False):
            return self._render_powerline(theme, data)
        
        # Check if this is a professional theme
        if theme_name in self.professional_themes and self.professional_powerline:
            prof_theme = self.professional_themes[theme_name]
            if prof_theme.get("multiline", False):
                return self._render_multiline_professional(prof_theme, data)
            else:
                return self._render_epic_powerline(prof_theme, data)
        
        template = theme.get("template", "{model} | {messages}msg ${cost}")
        
        # Prepare data with defaults
        formatted_data = {
            "model": data.get("model", "Claude"),
            "messages": data.get("messages", "0"),
            "tokens": data.get("tokens", "0"),
            "cost": data.get("cost", "0.0"),
            "sessions": data.get("sessions", "1"),
            "session_time": data.get("session_time", "0:00"),
            "efficiency": data.get("efficiency", "100")
        }
        
        # Format tokens
        tokens = formatted_data["tokens"]
        if isinstance(tokens, str):
            formatted_data["tokens"] = tokens
        elif tokens > 1_000_000:
            formatted_data["tokens"] = f"{tokens/1_000_000:.1f}M"
        elif tokens > 1_000:
            formatted_data["tokens"] = f"{tokens/1_000:.1f}K"
        else:
            formatted_data["tokens"] = str(tokens)
        
        # Apply template
        result = template
        
        # Check if we should use safe characters
        if not check_nerd_font_support():
            # Replace nerd font characters with safe alternatives
            nerd_replacements = {
                '\ue0b0': '>',    # Arrow right
                '\ue0b2': '<',    # Arrow left
                '\ue0b4': ')',    # Rounded right
                '\ue0b6': '(',    # Rounded left
                '\ue0c0': '>',    # Flame right
                '\ue0c2': '<',    # Flame left
                '\ue0b8': '>',    # Triangle right
                '\ue0ba': '<',    # Triangle left
                '\ue0c4': '>',    # Diamond right
                '\ue0c5': '<',    # Diamond left
                '\ue0c6': '[',    # Left bracket
                '\ue0c7': ']',    # Right bracket
                '\ue0bc': '~',    # Curve
                '\ue0be': '~',    # Curve
                '\uf85a': 'AI',   # Robot icon
                '\uf4a5': 'MSG',  # Message icon
                '\uf0e4': 'TOK',  # Token icon
                '\uf155': '$',    # Dollar icon
                '\uf621': '#',    # Hash
                '\uf8c9': '*',    # Star
                '\uf4b8': '$',    # Cost
                '\uf8a4': 'T',    # Token
                '\uf49a': 'M',    # Message
                '\uf489': '>',    # Terminal
                '\ue795': 'AI',   # AI
                '\uf6a9': 'FL',   # Flag
                '⚡': '*',         # Lightning
            }
            
            for nerd_char, safe_char in nerd_replacements.items():
                result = result.replace(nerd_char, safe_char)
        
        # If colored theme, apply colors
        if theme.get("colored", False) and "colors" in theme:
            colors = theme["colors"]
            for field, color in colors.items():
                if field in formatted_data:
                    # Replace field with colored version
                    field_pattern = "{" + field + "}"
                    if field_pattern in result:
                        colored_value = f"{color}{formatted_data[field]}{Style.RESET_ALL}"
                        result = result.replace(field_pattern, colored_value)
        
        # Format remaining fields
        try:
            result = result.format(**formatted_data)
        except Exception:
            # If template has issues, use minimal
            result = f"{formatted_data['model']} | {formatted_data['messages']}msg ${formatted_data['cost']}"
        
        # Final safety check - ensure output is printable
        try:
            result.encode(sys.stdout.encoding or 'utf-8')
            return result
        except (UnicodeEncodeError, AttributeError):
            # Last resort - ASCII only
            safe_result = result.encode('ascii', 'replace').decode('ascii')
            return safe_result
    
    def preview_theme(self, theme_name: str) -> str:
        """Preview a theme with sample data"""
        # Comprehensive sample data for epic themes
        sample_data = {
            # Basic data
            "model": "Opus 4.1",
            "model_short": "Op-4.1",
            "model_name": "claude",
            "messages": "42",
            "tokens": "58.5k",
            "cost": "15.5",
            "sessions": "3",
            "session_time": "2:45",
            "efficiency": "92",
            
            # Extended fields for epic themes
            "folder": "MyProject",
            "folder_name": "MyProject", 
            "project": "MyProject",
            "git_branch": "main",
            "branch": "main",
            "cpu": "45",
            "cpu_usage": "45%",
            "ram": "67",
            "ram_usage": "67%",
            "memory": "67%",
            "time_left": "3h15m",
            "session_remaining": "3h15m",
            "remaining": "3h15m",
            "network": "Online",
            "latency": "45ms",
            "ping": "45ms",
            
            # Quality metrics
            "coherence": "88%",
            "relevance": "92%",
            "creativity": "85%",
            "quality_score": "88%",
            "productivity": "High",
            "performance": "Good",
            
            # Short versions
            "msg": "42",
            "tok": "58k",
            "sess": "2:45",
            "eff": "92%",
            "qual": "88%",
            
            # Missing template variables
            "tokens_formatted": "58.5k",
            "model_version": "4.1",
            "model_tier": "Premium",
            "session_quality": "88%",
            "session_id": "s2024",
            "uptime": "4h30m",
            "cost_per_msg": "0.37",
            "response_time": "1.2s",
            "memory_usage": "67%",
            "context_used": "45k",
            "context_limit": "200k",
            "input_tokens": "32k",
            "output_tokens": "26.5k",
            "cache_tokens": "12k",
            "cache_hits": "8",
            "cache_efficiency": "89%",
            "throughput": "45 tok/s",
            "model_short_version": "Op-4.1"
        }
        
        # Apply theme and clean up for preview
        result = self.apply_theme(theme_name, sample_data)
        
        # Return FULL RGB and Unicode output for proper preview
        # Don't remove ANSI codes - keep them for colorful display!
        return result
    
    def select_theme_interactive(self):
        """Interactive theme selector with preview"""
        themes = self.get_all_themes()
        theme_list = list(themes.keys())
        
        print(f"\n{Back.BLUE}{Fore.WHITE} THEME SELECTOR {Style.RESET_ALL}\n")
        
        # Group themes by category
        categories = {
            "Minimal": ["minimal", "compact"],
            "Colored": ["pro", "hacker", "fire", "ocean"],
            "Multi-line": ["dashboard", "detailed"],
            "Emoji": ["emoji", "zen"],
            "True Powerline": ["powerline_pro", "powerline_git", "powerline_elegant"],
            "Powerline": ["powerline_classic", "nerd_elite", "rounded_powerline", "cosmic_beam"],
            "Advanced": ["diamond_sharp", "terminal_hacker", "gradient_flow", "neon_glow"],
            "Dynamic": ["arrow_stream", "bubble_pop", "lightning_bolt"],
            "Custom": [k for k in self.custom_themes.keys()]
        }
        
        # Add professional theme categories if available
        if PROFESSIONAL_AVAILABLE and self.professional_themes:
            prof_categories = {}
            for theme_name, theme_data in self.professional_themes.items():
                category = theme_data.get("category", "Professional")
                if category not in prof_categories:
                    prof_categories[category] = []
                prof_categories[category].append(theme_name)
            
            categories.update(prof_categories)
        
        index = 1
        theme_map = {}
        
        for category, theme_names in categories.items():
            if theme_names:  # Only show category if it has themes
                print(f"\n{Fore.YELLOW}=== {category} Themes ==={Style.RESET_ALL}")
                for theme_name in theme_names:
                    if theme_name in themes:
                        theme = themes[theme_name]
                        preview = self.preview_theme(theme_name)
                        
                        # Handle multiline previews
                        if theme.get("multiline", False):
                            print(f"\n{Fore.CYAN}[{index}] {theme['name']}{Style.RESET_ALL}")
                            print(f"    {Fore.WHITE}{theme['description']}{Style.RESET_ALL}")
                            print(f"    Preview:")
                            for line in preview.split('\n'):
                                print(f"    {line}")
                        else:
                            print(f"{Fore.CYAN}[{index}] {theme['name']:<15}{Style.RESET_ALL} {preview}")
                        
                        theme_map[str(index)] = theme_name
                        index += 1
        
        # Add create custom option
        print(f"\n{Fore.MAGENTA}[C] Create Custom Theme{Style.RESET_ALL}")
        print(f"{Fore.RED}[Q] Quit{Style.RESET_ALL}")
        
        # Get user choice
        choice = input(f"\n{Fore.GREEN}Select theme (1-{index-1}/C/Q): {Style.RESET_ALL}").strip().upper()
        
        if choice == 'Q':
            print("Cancelled")
            return
        elif choice == 'C':
            self.create_custom_theme()
        elif choice in theme_map:
            selected = theme_map[choice]
            self.set_current_theme(selected)
            print(f"\n{Fore.GREEN}[OK] Theme '{themes[selected]['name']}' applied!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid selection{Style.RESET_ALL}")
    
    def create_custom_theme(self):
        """Interactive custom theme builder"""
        print(f"\n{Back.MAGENTA}{Fore.WHITE} CUSTOM THEME BUILDER {Style.RESET_ALL}\n")
        
        # Get theme name
        name = input(f"{Fore.CYAN}Theme name: {Style.RESET_ALL}").strip()
        if not name:
            print("Cancelled")
            return
        
        # Get description
        description = input(f"{Fore.CYAN}Description: {Style.RESET_ALL}").strip()
        
        # Choose fields to include
        print(f"\n{Fore.YELLOW}Available fields:{Style.RESET_ALL}")
        fields = {
            "1": ("model", "Model name (e.g., Opus 4.1)"),
            "2": ("messages", "Message count"),
            "3": ("tokens", "Token count"),
            "4": ("cost", "Total cost"),
            "5": ("sessions", "Session count"),
            "6": ("session_time", "Session duration"),
            "7": ("efficiency", "Efficiency score")
        }
        
        for key, (field, desc) in fields.items():
            print(f"  [{key}] {field:<15} - {desc}")
        
        selected_fields = input(f"\n{Fore.CYAN}Select fields (e.g., 1,2,4): {Style.RESET_ALL}").strip()
        
        # Build template
        template_parts = []
        field_list = []
        
        for num in selected_fields.split(','):
            num = num.strip()
            if num in fields:
                field_name, _ = fields[num]
                field_list.append(field_name)
        
        if not field_list:
            field_list = ["model", "messages", "cost"]  # Default
        
        # Choose separators
        print(f"\n{Fore.YELLOW}Separator options:{Style.RESET_ALL}")
        separators = {
            "1": " | ",
            "2": " • ",
            "3": " :: ",
            "4": " ~ ",
            "5": " / ",
            "6": " - ",
            "7": " > "
        }
        
        for key, sep in separators.items():
            print(f"  [{key}] '{sep}'")
        
        sep_choice = input(f"\n{Fore.CYAN}Choose separator (1-7): {Style.RESET_ALL}").strip()
        separator = separators.get(sep_choice, " | ")
        
        # Build template string
        template = ""
        for i, field in enumerate(field_list):
            if field == "cost":
                template += "${cost}"
            elif field == "efficiency":
                template += "{efficiency}%"
            elif field == "messages":
                template += "{messages}msg"
            elif field == "tokens":
                template += "{tokens}tok"
            else:
                template += "{" + field + "}"
            
            if i < len(field_list) - 1:
                template += separator
        
        # Ask for coloring
        use_colors = input(f"\n{Fore.CYAN}Use colors? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
        
        colors = {}
        if use_colors:
            color_options = {
                "1": ("RED", Fore.RED),
                "2": ("GREEN", Fore.GREEN),
                "3": ("BLUE", Fore.BLUE),
                "4": ("YELLOW", Fore.YELLOW),
                "5": ("CYAN", Fore.CYAN),
                "6": ("MAGENTA", Fore.MAGENTA),
                "7": ("WHITE", Fore.WHITE)
            }
            
            print(f"\n{Fore.YELLOW}Color options:{Style.RESET_ALL}")
            for key, (name, color) in color_options.items():
                print(f"  [{key}] {color}{name}{Style.RESET_ALL}")
            
            for field in field_list:
                color_choice = input(f"Color for {field} (1-7, Enter to skip): ").strip()
                if color_choice in color_options:
                    _, color = color_options[color_choice]
                    colors[field] = color
        
        # Multiline?
        multiline = input(f"\n{Fore.CYAN}Multi-line display? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
        
        # Create theme
        theme_key = name.lower().replace(" ", "_")
        self.custom_themes[theme_key] = {
            "name": name,
            "description": description,
            "template": template,
            "multiline": multiline,
            "colored": use_colors,
            "colors": colors if use_colors else {}
        }
        
        # Save custom themes
        self._save_custom_themes()
        
        # Preview
        print(f"\n{Fore.GREEN}[OK] Theme created!{Style.RESET_ALL}")
        print(f"\nPreview:")
        preview = self.preview_theme(theme_key)
        if multiline:
            for line in preview.split('\n'):
                print(f"  {line}")
        else:
            print(f"  {preview}")
        
        # Apply?
        if input(f"\n{Fore.CYAN}Apply this theme now? (y/n): {Style.RESET_ALL}").strip().lower() == 'y':
            self.set_current_theme(theme_key)
            print(f"{Fore.GREEN}[OK] Theme applied!{Style.RESET_ALL}")
    
    def set_current_theme(self, theme_name: str):
        """Set the current active theme"""
        try:
            # Load config
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {}
            
            # Update theme
            config['current_theme'] = theme_name
            config['theme_system'] = 'unified'
            
            # Save config
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error setting theme: {e}")
            return False
    
    def get_current_theme(self) -> str:
        """Get current active theme name"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                return config.get('current_theme', 'minimal')
        except:
            pass
        return 'minimal'
    
    def list_themes(self):
        """List all available themes"""
        themes = self.get_all_themes()
        current = self.get_current_theme()
        
        print(f"\n{Back.BLUE}{Fore.WHITE} AVAILABLE THEMES {Style.RESET_ALL}\n")
        
        # Dynamically build categories
        categories = {
            "Minimal": ["minimal", "compact"],
            "Colored": ["pro", "hacker", "fire", "ocean"],
            "Multi-line": ["dashboard", "detailed"],
            "Emoji": ["emoji", "zen"],
            "Powerline": ["powerline_classic", "nerd_elite", "rounded_powerline", "cosmic_beam"],
            "Advanced": ["diamond_sharp", "terminal_hacker", "gradient_flow", "neon_glow"],
            "Dynamic": ["arrow_stream", "bubble_pop", "lightning_bolt"],
            "Custom": list(self.custom_themes.keys())
        }
        
        # Add professional theme categories if available
        if PROFESSIONAL_AVAILABLE and self.professional_themes:
            prof_categories = {}
            for theme_name, theme_data in self.professional_themes.items():
                category = theme_data.get("category", "Professional")
                if category not in prof_categories:
                    prof_categories[category] = []
                prof_categories[category].append(theme_name)
            categories.update(prof_categories)
        
        for category, theme_names in categories.items():
            if theme_names:
                print(f"\n{Fore.YELLOW}{category}:{Style.RESET_ALL}")
                for name in theme_names:
                    if name in themes:
                        theme = themes[name]
                        marker = " *" if name == current else ""
                        
                        # Show all themes with preview (rendered form)
                        print(f"  • {theme['name']}{marker} - {theme['description']}")
                        
                        # Show simplified preview for theme list
                        try:
                            preview = self.preview_theme(name)
                            
                            # Strip ANSI codes for theme list display
                            import re
                            # Remove all ANSI escape sequences
                            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                            preview_clean = ansi_escape.sub('', preview)
                            
                            # Also clean up raw escape codes that weren't processed
                            preview_clean = re.sub(r'\[48;2;\d+;\d+;\d+m', '', preview_clean)
                            preview_clean = re.sub(r'\[38;2;\d+;\d+;\d+m', '', preview_clean)
                            preview_clean = re.sub(r'\[0m', '', preview_clean)
                            preview_clean = re.sub(r'\[\d+m', '', preview_clean)
                            
                            # Truncate if too long
                            if len(preview_clean) > 80:
                                preview_clean = preview_clean[:80] + "..."
                            
                            # Show clean preview
                            print(f"    ▶ {preview_clean}")
                        except Exception as e:
                            # Fallback to theme name only
                            print(f"    ▶ [{theme.get('name', name)}]")


# Global instance
THEME_SYSTEM = UnifiedThemeSystem()


def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "list":
            THEME_SYSTEM.list_themes()
        elif cmd == "select":
            THEME_SYSTEM.select_theme_interactive()
        elif cmd == "create":
            THEME_SYSTEM.create_custom_theme()
        elif cmd == "preview":
            if len(sys.argv) > 2:
                theme = sys.argv[2]
                print(THEME_SYSTEM.preview_theme(theme))
            else:
                print("Usage: theme preview <theme_name>")
        elif cmd == "apply":
            if len(sys.argv) > 2:
                theme = sys.argv[2]
                if THEME_SYSTEM.set_current_theme(theme):
                    print(f"[OK] Theme '{theme}' applied")
                else:
                    print(f"[X] Failed to apply theme '{theme}'")
            else:
                print("Usage: theme apply <theme_name>")
        else:
            print("Unknown command")
    else:
        # Default to interactive selector
        THEME_SYSTEM.select_theme_interactive()


if __name__ == "__main__":
    main()