#!/usr/bin/env python3
"""
Interactive Theme Manager for Claude Statusline
Easy theme selection, search, and customization
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import subprocess

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

from .templates import StatuslineTemplates
from .colored_templates import ColoredTemplates
from .custom_theme import CustomThemeBuilder, EXAMPLE_THEMES
from .formatter import SimpleVisualFormatter


class ThemeManager:
    """Manage and select themes interactively"""
    
    def __init__(self):
        """Initialize theme manager"""
        self.config_file = Path(__file__).parent / "config.json"
        self.templates = StatuslineTemplates()
        self.colored_templates = ColoredTemplates()
        self.custom_builder = CustomThemeBuilder()
        self.formatter = SimpleVisualFormatter()
        
        # Get all available themes
        self.all_themes = self._get_all_themes()
        
        # Load sample data for preview
        self.sample_data = self._get_sample_data()
    
    def _get_all_themes(self) -> Dict[str, Dict[str, Any]]:
        """Get all available themes from all sources"""
        themes = {}
        
        # Standard templates
        for name in self.templates.list_templates():
            themes[name] = {
                'type': 'standard',
                'description': self.templates.get_description(name),
                'category': 'Standard'
            }
        
        # Colored templates
        colored_categories = {
            'vscode': 'Developer', 'intellij': 'Developer', 'sublime': 'Developer',
            'atom': 'Developer', 'neovim': 'Developer', 'emacs': 'Developer',
            'minecraft': 'Gaming', 'cyberpunk': 'Gaming', 'retro': 'Gaming',
            'arcade': 'Gaming', 'rpg': 'Gaming',
            'executive': 'Professional', 'analyst': 'Professional',
            'consultant': 'Professional', 'startup': 'Professional',
            'rainbow': 'Creative', 'neon': 'Creative', 'pastel': 'Creative',
            'gradient': 'Creative', 'artistic': 'Creative',
            'windows': 'System', 'macos': 'System', 'ubuntu': 'System', 'arch': 'System',
            'twitter': 'Social', 'instagram': 'Social', 'youtube': 'Social',
            'linkedin': 'Social', 'reddit': 'Social',
            'christmas': 'Seasonal', 'halloween': 'Seasonal', 'summer': 'Seasonal',
            'winter': 'Seasonal', 'space': 'Nature', 'ocean': 'Nature',
            'forest': 'Nature', 'desert': 'Nature',
            'mono': 'Minimal', 'duo': 'Minimal', 'noir': 'Minimal', 'clean': 'Minimal',
            'emoji_party': 'Fun', 'kawaii': 'Fun', 'leetspeak': 'Fun',
            'pirate': 'Fun', 'robot': 'Fun', 'wizard': 'Fun'
        }
        
        for name in self.colored_templates.templates:
            themes[name] = {
                'type': 'colored',
                'description': f"Colored {name.replace('_', ' ').title()} theme",
                'category': colored_categories.get(name, 'Colored')
            }
        
        # Example custom themes
        for name, theme_data in EXAMPLE_THEMES.items():
            themes[name] = {
                'type': 'custom',
                'description': theme_data['name'],
                'category': 'Custom Examples',
                'data': theme_data
            }
        
        # User saved custom themes
        for theme_info in self.custom_builder.list_saved_themes():
            name = theme_info['filename'].replace('.json', '')
            themes[f"custom_{name}"] = {
                'type': 'saved_custom',
                'description': theme_info['name'],
                'category': 'My Themes',
                'filename': theme_info['filename']
            }
        
        return themes
    
    def _get_sample_data(self) -> Dict[str, Any]:
        """Get sample data for preview"""
        # Try to get real data first
        try:
            data_dir = Path.home() / ".claude" / "data-statusline"
            db_file = data_dir / "smart_sessions_db.json"
            
            if db_file.exists():
                with open(db_file, 'r') as f:
                    db_data = json.load(f)
                    current = db_data.get('current_session')
                    if current and current.get('message_count', 0) > 0:
                        return current
        except:
            pass
        
        # Fallback to sample data
        return {
            'primary_model': 'claude-opus-4-1-20250805',
            'model': 'claude-opus-4-1-20250805',
            'active': True,
            'session_number': 123,
            'session_end_time': '17:00',
            'message_count': 456,
            'tokens': 12345678,
            'total_tokens': 12345678,
            'cost': 89.99,
            'total_cost': 89.99,
            'remaining_seconds': 7200
        }
    
    def search_themes(self, query: str) -> List[str]:
        """Search themes by name or description"""
        query_lower = query.lower()
        matches = []
        
        for name, info in self.all_themes.items():
            if (query_lower in name.lower() or 
                query_lower in info['description'].lower() or
                query_lower in info['category'].lower()):
                matches.append(name)
        
        return matches
    
    def preview_theme(self, theme_name: str) -> str:
        """Generate preview for a theme"""
        if theme_name not in self.all_themes:
            return "Theme not found"
        
        theme_info = self.all_themes[theme_name]
        
        if theme_info['type'] == 'standard':
            return self.templates.format(theme_name, self.sample_data)
        elif theme_info['type'] == 'colored':
            if hasattr(self.colored_templates.templates.get(theme_name), '__call__'):
                return self.colored_templates.templates[theme_name](self.sample_data)
        elif theme_info['type'] == 'custom':
            return self.custom_builder.format_with_theme(theme_info['data'], self.sample_data)
        elif theme_info['type'] == 'saved_custom':
            theme_data = self.custom_builder.load_theme(theme_info['filename'])
            if theme_data:
                return self.custom_builder.format_with_theme(theme_data, self.sample_data)
        
        return "Preview not available"
    
    def interactive_select(self):
        """Interactive theme selection with categories and search"""
        print(f"\n{Fore.CYAN}🎨 Claude Statusline Theme Manager{Style.RESET_ALL}")
        print("=" * 80)
        
        # Group themes by category
        categories = {}
        for name, info in self.all_themes.items():
            category = info['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(name)
        
        # Sort categories
        category_order = ['My Themes', 'Custom Examples', 'Standard', 'Developer', 
                         'Gaming', 'Professional', 'Creative', 'System', 'Social',
                         'Seasonal', 'Nature', 'Minimal', 'Fun', 'Colored']
        sorted_categories = []
        for cat in category_order:
            if cat in categories:
                sorted_categories.append(cat)
        for cat in categories:
            if cat not in sorted_categories:
                sorted_categories.append(cat)
        
        while True:
            print(f"\n{Fore.YELLOW}Commands:{Style.RESET_ALL}")
            print("  📝 search <query> - Search themes")
            print("  🔢 <number>      - Select theme by number")
            print("  👁️  preview <name> - Preview specific theme")
            print("  ➕ create        - Create custom theme")
            print("  💾 save          - Save current theme")
            print("  ❌ quit          - Exit")
            print()
            
            # Display categories and themes
            theme_index = 1
            theme_map = {}
            
            for category in sorted_categories:
                theme_names = categories[category]
                if not theme_names:
                    continue
                
                # Category header with emoji
                category_emoji = {
                    'My Themes': '⭐', 'Custom Examples': '🎯', 'Standard': '📦',
                    'Developer': '💻', 'Gaming': '🎮', 'Professional': '💼',
                    'Creative': '🎨', 'System': '🖥️', 'Social': '📱',
                    'Seasonal': '🎄', 'Nature': '🌿', 'Minimal': '⚡', 'Fun': '🎉'
                }.get(category, '📌')
                
                print(f"\n{Fore.CYAN}{category_emoji} {category}{Style.RESET_ALL}")
                print("-" * 40)
                
                for theme_name in sorted(theme_names):
                    info = self.all_themes[theme_name]
                    current = self._is_current_theme(theme_name)
                    
                    # Format display
                    marker = f" {Fore.GREEN}✓{Style.RESET_ALL}" if current else ""
                    print(f"  {theme_index:3}. {theme_name:25} {Fore.LIGHTBLACK_EX}{info['description'][:40]}{Style.RESET_ALL}{marker}")
                    
                    theme_map[theme_index] = theme_name
                    theme_index += 1
            
            # Get user input
            print()
            choice = input(f"{Fore.GREEN}➜{Style.RESET_ALL} ").strip()
            
            if choice.lower() == 'quit' or choice.lower() == 'q':
                break
            
            elif choice.lower().startswith('search '):
                query = choice[7:]
                matches = self.search_themes(query)
                if matches:
                    print(f"\n{Fore.YELLOW}Search results for '{query}':{Style.RESET_ALL}")
                    for i, match in enumerate(matches[:20], 1):
                        preview = self.preview_theme(match)
                        print(f"  {match:25} → {preview}")
                else:
                    print(f"{Fore.RED}No themes found matching '{query}'{Style.RESET_ALL}")
            
            elif choice.lower().startswith('preview '):
                theme_name = choice[8:]
                if theme_name in self.all_themes:
                    preview = self.preview_theme(theme_name)
                    print(f"\n{Fore.YELLOW}Preview of {theme_name}:{Style.RESET_ALL}")
                    print(f"  {preview}")
                else:
                    print(f"{Fore.RED}Theme '{theme_name}' not found{Style.RESET_ALL}")
            
            elif choice.lower() == 'create':
                self.create_custom_theme()
            
            elif choice.isdigit():
                num = int(choice)
                if num in theme_map:
                    theme_name = theme_map[num]
                    self.apply_theme(theme_name)
                    print(f"\n{Fore.GREEN}✓ Applied theme: {theme_name}{Style.RESET_ALL}")
                    
                    # Show preview after applying
                    preview = self.preview_theme(theme_name)
                    print(f"\n{Fore.CYAN}Preview:{Style.RESET_ALL} {preview}")
                    
                    # Show commands after selection
                    print(f"\n{Fore.YELLOW}Commands:{Style.RESET_ALL}")
                    print("  📝 search <query> - Search themes")
                    print("  🔢 <number>      - Select theme by number")
                    print("  👁️  preview <name> - Preview specific theme")
                    print("  ➕ create        - Create custom theme")
                    print("  💾 save          - Save current theme")
                    print("  ❌ quit          - Exit")
                else:
                    print(f"{Fore.RED}Invalid selection{Style.RESET_ALL}")
            
            else:
                print(f"{Fore.RED}Unknown command{Style.RESET_ALL}")
    
    def create_custom_theme(self):
        """Interactive custom theme creation"""
        print(f"\n{Fore.CYAN}🛠️  Create Custom Theme{Style.RESET_ALL}")
        print("=" * 60)
        
        name = input("Theme name: ").strip()
        if not name:
            print(f"{Fore.RED}Name required{Style.RESET_ALL}")
            return
        
        print("\nSelect fields to include (enter numbers separated by space):")
        print("\nAvailable fields:")
        
        field_list = list(self.custom_builder.available_fields.items())
        for i, (field_name, field_info) in enumerate(field_list, 1):
            print(f"  {i:2}. {field_info['icon']} {field_info['name']:20} Example: {field_info['example']}")
        
        selections = input("\nEnter field numbers: ").strip().split()
        
        fields = []
        for sel in selections:
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(field_list):
                    field_name, _ = field_list[idx]
                    
                    # Ask for color
                    print(f"\nConfiguring {field_name}:")
                    color_choices = list(self.custom_builder.colors.keys())
                    print(f"Colors: {', '.join(color_choices[:8])}")
                    color = input("Color (default: white): ").strip() or 'white'
                    
                    fields.append({
                        'type': field_name,
                        'color': color if color in self.custom_builder.colors else 'white'
                    })
        
        if not fields:
            print(f"{Fore.RED}No fields selected{Style.RESET_ALL}")
            return
        
        # Create and save theme
        theme = self.custom_builder.create_theme(name, fields)
        filepath = self.custom_builder.save_theme(theme)
        
        print(f"\n{Fore.GREEN}✓ Theme saved to: {filepath}{Style.RESET_ALL}")
        
        # Preview
        preview = self.custom_builder.format_with_theme(theme, self.sample_data)
        print(f"Preview: {preview}")
        
        # Apply?
        if input("\nApply this theme? (y/n): ").lower() == 'y':
            self.apply_custom_theme(theme)
    
    def apply_theme(self, theme_name: str):
        """Apply a theme to config"""
        config = self._load_config()
        config['display']['template'] = theme_name
        self._save_config(config)
    
    def apply_custom_theme(self, theme: Dict[str, Any]):
        """Apply a custom theme"""
        config = self._load_config()
        config['display']['template'] = 'custom'
        config['display']['custom_theme'] = theme
        self._save_config(config)
    
    def _is_current_theme(self, theme_name: str) -> bool:
        """Check if theme is currently active"""
        config = self._load_config()
        return config.get('display', {}).get('template') == theme_name
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)


def main():
    """Main entry point for theme manager"""
    manager = ThemeManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            # List all themes
            for name, info in manager.all_themes.items():
                print(f"{name:30} {info['category']:15} {info['description']}")
        
        elif command == 'search' and len(sys.argv) > 2:
            # Search themes
            query = ' '.join(sys.argv[2:])
            matches = manager.search_themes(query)
            for match in matches:
                preview = manager.preview_theme(match)
                print(f"{match:30} → {preview}")
        
        elif command == 'preview' and len(sys.argv) > 2:
            # Preview a theme
            theme_name = sys.argv[2]
            preview = manager.preview_theme(theme_name)
            print(preview)
        
        elif command == 'apply' and len(sys.argv) > 2:
            # Apply a theme
            theme_name = sys.argv[2]
            manager.apply_theme(theme_name)
            print(f"Applied theme: {theme_name}")
        
        elif command == 'create':
            # Create custom theme
            manager.create_custom_theme()
        
        else:
            # Interactive mode
            manager.interactive_select()
    else:
        # Interactive mode
        manager.interactive_select()


if __name__ == "__main__":
    main()