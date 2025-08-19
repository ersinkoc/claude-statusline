#!/usr/bin/env python3
"""
Visual Theme Builder for Claude Statusline
Interactive theme creation with live preview
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
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

from .custom_theme import CustomThemeBuilder


class VisualThemeBuilder:
    """Interactive visual theme builder with live preview"""
    
    def __init__(self):
        """Initialize visual theme builder"""
        self.builder = CustomThemeBuilder()
        self.current_fields = []
        self.preview_data = self._get_preview_data()
        
        # Quick access fields grouped by category
        self.field_categories = {
            'Essential': {
                'model': '🤖 Model Name',
                'status_icon': '● Status',
                'messages': '💬 Messages',
                'cost_short': '💰 Cost'
            },
            'Time': {
                'time_remaining_short': '⏰ Time Left',
                'session_end': '🏁 End Time',
                'current_time': '🕐 Current'
            },
            'Git': {
                'git_branch': '🌿 Branch',
                'git_status': '📝 Status',
                'git_modified': '✏️ Modified'
            },
            'System': {
                'folder': '📁 Folder',
                'cpu': '🖥️ CPU',
                'memory': '🧠 Memory'
            },
            'Tokens': {
                'tokens': '🔢 Tokens',
                'tokens_raw': '# Raw Count'
            },
            'Separators': {
                'separator': '| Pipe',
                'arrow': '→ Arrow',
                'dot': '• Dot',
                'space': '_ Space'
            }
        }
        
        # Color presets
        self.color_presets = {
            'default': {'main': 'white', 'accent': 'cyan', 'status': 'green', 'alert': 'yellow'},
            'ocean': {'main': 'cyan', 'accent': 'blue', 'status': 'green', 'alert': 'yellow'},
            'forest': {'main': 'green', 'accent': 'yellow', 'status': 'bright_green', 'alert': 'red'},
            'sunset': {'main': 'yellow', 'accent': 'red', 'status': 'magenta', 'alert': 'bright_yellow'},
            'monochrome': {'main': 'white', 'accent': 'bright_white', 'status': 'white', 'alert': 'bright_white'},
            'neon': {'main': 'bright_magenta', 'accent': 'bright_cyan', 'status': 'bright_green', 'alert': 'bright_yellow'},
            'dark': {'main': 'bright_black', 'accent': 'white', 'status': 'green', 'alert': 'yellow'}
        }
        
        # Quick templates
        self.quick_templates = {
            'minimal': [
                {'type': 'model_short', 'color': 'cyan'},
                {'type': 'messages', 'color': 'white'},
                {'type': 'cost_short', 'color': 'yellow'}
            ],
            'developer': [
                {'type': 'model_short', 'color': 'cyan', 'brackets': 'square'},
                {'type': 'git_branch', 'color': 'green'},
                {'type': 'folder', 'color': 'magenta'},
                {'type': 'messages', 'color': 'white'},
                {'type': 'cost_short', 'color': 'yellow'}
            ],
            'detailed': [
                {'type': 'model', 'color': 'cyan'},
                {'type': 'status', 'color': 'green'},
                {'type': 'messages', 'color': 'white', 'suffix': ' msgs'},
                {'type': 'tokens', 'color': 'magenta'},
                {'type': 'cost', 'color': 'yellow'},
                {'type': 'time_remaining', 'color': 'red'}
            ],
            'git-focus': [
                {'type': 'git_branch', 'color': 'green', 'prefix': '⎇ '},
                {'type': 'git_status', 'color': 'yellow'},
                {'type': 'separator', 'color': 'bright_black'},
                {'type': 'model_short', 'color': 'cyan'},
                {'type': 'messages', 'color': 'white'}
            ],
            'system': [
                {'type': 'model_short', 'color': 'cyan'},
                {'type': 'cpu', 'color': 'yellow'},
                {'type': 'memory', 'color': 'magenta'},
                {'type': 'folder', 'color': 'blue'}
            ]
        }
    
    def _get_preview_data(self) -> Dict[str, Any]:
        """Get sample data for preview"""
        # Try real data first
        try:
            data_dir = Path.home() / ".claude" / "data-statusline"
            db_file = data_dir / "smart_sessions_db.json"
            
            if db_file.exists():
                with open(db_file, 'r') as f:
                    db_data = json.load(f)
                    current = db_data.get('current_session')
                    if current:
                        return current
        except:
            pass
        
        # Fallback sample data
        return {
            'primary_model': 'claude-opus-4-1-20250805',
            'model': 'claude-opus-4-1-20250805',
            'active': True,
            'session_number': 42,
            'message_count': 128,
            'tokens': 5432100,
            'cost': 45.67,
            'remaining_seconds': 9000,
            'session_end_time': '17:30'
        }
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print builder header"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  🎨 {Fore.YELLOW}Claude Statusline Visual Theme Builder{Style.RESET_ALL}                  {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    def show_preview(self):
        """Show live preview of current theme"""
        if not self.current_fields:
            preview = f"{Fore.LIGHTBLACK_EX}[No fields selected - add fields below]{Style.RESET_ALL}"
        else:
            theme = {
                'fields': self.current_fields,
                'separator': ' '
            }
            preview = self.builder.format_with_theme(theme, self.preview_data)
        
        # Preview box
        print(f"{Fore.GREEN}┌─ Live Preview ─────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│{Style.RESET_ALL} {preview}")
        print(f"{Fore.GREEN}└────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
    
    def show_current_fields(self):
        """Show current field configuration"""
        if not self.current_fields:
            print(f"{Fore.YELLOW}Current Fields:{Style.RESET_ALL} (empty)\n")
            return
        
        print(f"{Fore.YELLOW}Current Fields:{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}{'─' * 60}{Style.RESET_ALL}")
        
        for i, field in enumerate(self.current_fields, 1):
            field_type = field['type']
            color = field.get('color', 'white')
            prefix = field.get('prefix', '')
            suffix = field.get('suffix', '')
            brackets = field.get('brackets', '')
            
            # Get field info
            field_info = None
            for cat_fields in self.builder.available_fields.values():
                if field_type in self.builder.available_fields:
                    field_info = self.builder.available_fields[field_type]
                    break
            
            # Format display
            color_sample = f"{self._get_color_code(color)}███{Style.RESET_ALL}"
            extras = []
            if prefix: extras.append(f"prefix='{prefix}'")
            if suffix: extras.append(f"suffix='{suffix}'")
            if brackets: extras.append(f"[{brackets}]")
            extras_str = f" {Fore.LIGHTBLACK_EX}({', '.join(extras)}){Style.RESET_ALL}" if extras else ""
            
            print(f"  {i:2}. {color_sample} {field_type:20} {extras_str}")
        
        print()
    
    def show_quick_actions(self):
        """Show quick action menu"""
        print(f"{Fore.CYAN}Quick Actions:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Add Field       {Fore.GREEN}[2]{Style.RESET_ALL} Remove Field    {Fore.GREEN}[3]{Style.RESET_ALL} Reorder")
        print(f"  {Fore.GREEN}[4]{Style.RESET_ALL} Quick Template  {Fore.GREEN}[5]{Style.RESET_ALL} Color Preset    {Fore.GREEN}[6]{Style.RESET_ALL} Clear All")
        print(f"  {Fore.GREEN}[7]{Style.RESET_ALL} Save Theme     {Fore.GREEN}[8]{Style.RESET_ALL} Test Theme      {Fore.GREEN}[9]{Style.RESET_ALL} Exit")
        print()
    
    def add_field_interactive(self):
        """Add a field interactively"""
        self.clear_screen()
        self.print_header()
        
        print(f"{Fore.YELLOW}📋 Select Field to Add:{Style.RESET_ALL}\n")
        
        # Show categories
        field_list = []
        for cat_name, fields in self.field_categories.items():
            print(f"{Fore.CYAN}{cat_name}:{Style.RESET_ALL}")
            for field_type, display_name in fields.items():
                field_list.append(field_type)
                num = len(field_list)
                
                # Get example value
                example = self.builder._get_field_value(field_type, self.preview_data) or "N/A"
                print(f"  {Fore.GREEN}[{num:2}]{Style.RESET_ALL} {display_name:15} → {Fore.LIGHTBLACK_EX}{example}{Style.RESET_ALL}")
            print()
        
        # Get selection
        choice = input(f"\n{Fore.GREEN}Select field number (or Enter to cancel):{Style.RESET_ALL} ").strip()
        
        if not choice or not choice.isdigit():
            return
        
        idx = int(choice) - 1
        if 0 <= idx < len(field_list):
            field_type = field_list[idx]
            
            # Configure field
            print(f"\n{Fore.YELLOW}Configure {field_type}:{Style.RESET_ALL}")
            
            # Color selection
            print(f"\n{Fore.CYAN}Colors:{Style.RESET_ALL}")
            colors = ['white', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 
                     'bright_white', 'bright_red', 'bright_green', 'bright_yellow',
                     'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_black']
            
            for i, color in enumerate(colors, 1):
                sample = f"{self._get_color_code(color)}███{Style.RESET_ALL}"
                print(f"  {i:2}. {sample} {color}")
            
            color_choice = input(f"\n{Fore.GREEN}Color number (default: white):{Style.RESET_ALL} ").strip()
            color = 'white'
            if color_choice.isdigit():
                idx = int(color_choice) - 1
                if 0 <= idx < len(colors):
                    color = colors[idx]
            
            # Optional prefix/suffix
            prefix = input(f"{Fore.GREEN}Prefix (optional):{Style.RESET_ALL} ").strip()
            suffix = input(f"{Fore.GREEN}Suffix (optional):{Style.RESET_ALL} ").strip()
            
            # Brackets
            print(f"\n{Fore.CYAN}Brackets:{Style.RESET_ALL}")
            print("  1. None    2. [Square]   3. (Round)   4. {Curly}")
            print("  5. <Angle> 6. «Double»   7. |Pipe|")
            
            bracket_choice = input(f"{Fore.GREEN}Bracket style (default: none):{Style.RESET_ALL} ").strip()
            brackets = ''
            bracket_map = {'2': 'square', '3': 'round', '4': 'curly', 
                          '5': 'angle', '6': 'double_angle', '7': 'pipe'}
            if bracket_choice in bracket_map:
                brackets = bracket_map[bracket_choice]
            
            # Add field
            field_config = {'type': field_type, 'color': color}
            if prefix: field_config['prefix'] = prefix
            if suffix: field_config['suffix'] = suffix
            if brackets: field_config['brackets'] = brackets
            
            self.current_fields.append(field_config)
            print(f"\n{Fore.GREEN}✓ Field added!{Style.RESET_ALL}")
            input("Press Enter to continue...")
    
    def remove_field_interactive(self):
        """Remove a field interactively"""
        if not self.current_fields:
            print(f"{Fore.RED}No fields to remove!{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        self.show_current_fields()
        
        choice = input(f"{Fore.GREEN}Enter field number to remove (or Enter to cancel):{Style.RESET_ALL} ").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.current_fields):
                removed = self.current_fields.pop(idx)
                print(f"{Fore.GREEN}✓ Removed {removed['type']}{Style.RESET_ALL}")
                input("Press Enter to continue...")
    
    def reorder_fields_interactive(self):
        """Reorder fields interactively"""
        if len(self.current_fields) < 2:
            print(f"{Fore.RED}Need at least 2 fields to reorder!{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        self.show_current_fields()
        
        print(f"{Fore.YELLOW}Reorder Fields:{Style.RESET_ALL}")
        from_idx = input(f"{Fore.GREEN}Move field number:{Style.RESET_ALL} ").strip()
        to_idx = input(f"{Fore.GREEN}To position:{Style.RESET_ALL} ").strip()
        
        if from_idx.isdigit() and to_idx.isdigit():
            from_idx = int(from_idx) - 1
            to_idx = int(to_idx) - 1
            
            if 0 <= from_idx < len(self.current_fields) and 0 <= to_idx < len(self.current_fields):
                field = self.current_fields.pop(from_idx)
                self.current_fields.insert(to_idx, field)
                print(f"{Fore.GREEN}✓ Fields reordered!{Style.RESET_ALL}")
                input("Press Enter to continue...")
    
    def apply_quick_template(self):
        """Apply a quick template"""
        self.clear_screen()
        self.print_header()
        
        print(f"{Fore.YELLOW}Quick Templates:{Style.RESET_ALL}\n")
        
        templates = list(self.quick_templates.keys())
        for i, name in enumerate(templates, 1):
            # Preview template
            theme = {'fields': self.quick_templates[name], 'separator': ' '}
            preview = self.builder.format_with_theme(theme, self.preview_data)
            print(f"  {Fore.GREEN}[{i}]{Style.RESET_ALL} {name:12} → {preview}")
        
        choice = input(f"\n{Fore.GREEN}Select template number (or Enter to cancel):{Style.RESET_ALL} ").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(templates):
                template_name = templates[idx]
                self.current_fields = self.quick_templates[template_name].copy()
                print(f"{Fore.GREEN}✓ Applied {template_name} template!{Style.RESET_ALL}")
                input("Press Enter to continue...")
    
    def apply_color_preset(self):
        """Apply a color preset to all fields"""
        if not self.current_fields:
            print(f"{Fore.RED}No fields to apply colors to!{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        
        print(f"{Fore.YELLOW}Color Presets:{Style.RESET_ALL}\n")
        
        presets = list(self.color_presets.keys())
        for i, name in enumerate(presets, 1):
            preset = self.color_presets[name]
            samples = ' '.join(f"{self._get_color_code(c)}███{Style.RESET_ALL}" for c in preset.values())
            print(f"  {Fore.GREEN}[{i}]{Style.RESET_ALL} {name:12} {samples}")
        
        choice = input(f"\n{Fore.GREEN}Select preset number (or Enter to cancel):{Style.RESET_ALL} ").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(presets):
                preset_name = presets[idx]
                preset = self.color_presets[preset_name]
                
                # Apply colors based on field type
                for field in self.current_fields:
                    field_type = field['type']
                    if 'model' in field_type or 'folder' in field_type:
                        field['color'] = preset['main']
                    elif 'status' in field_type or 'git' in field_type:
                        field['color'] = preset['status']
                    elif 'cost' in field_type or 'time' in field_type:
                        field['color'] = preset['alert']
                    else:
                        field['color'] = preset['accent']
                
                print(f"{Fore.GREEN}✓ Applied {preset_name} color preset!{Style.RESET_ALL}")
                input("Press Enter to continue...")
    
    def save_theme(self):
        """Save current theme"""
        if not self.current_fields:
            print(f"{Fore.RED}No fields to save!{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        self.show_preview()
        
        name = input(f"{Fore.GREEN}Theme name:{Style.RESET_ALL} ").strip()
        if not name:
            return
        
        # Create theme
        theme = self.builder.create_theme(name, self.current_fields)
        
        # Add separator configuration
        print(f"\n{Fore.YELLOW}Separator between fields:{Style.RESET_ALL}")
        print("  1. Space    2. | Pipe    3. • Dot    4. → Arrow    5. Custom")
        sep_choice = input(f"{Fore.GREEN}Choice (default: space):{Style.RESET_ALL} ").strip()
        
        sep_map = {'1': ' ', '2': ' | ', '3': ' • ', '4': ' → '}
        if sep_choice in sep_map:
            theme['separator'] = sep_map[sep_choice]
        elif sep_choice == '5':
            custom_sep = input(f"{Fore.GREEN}Custom separator:{Style.RESET_ALL} ")
            theme['separator'] = custom_sep
        else:
            theme['separator'] = ' '
        
        # Save
        filepath = self.builder.save_theme(theme)
        print(f"\n{Fore.GREEN}✓ Theme saved to: {filepath}{Style.RESET_ALL}")
        
        # Apply?
        if input(f"\n{Fore.GREEN}Apply this theme now? (y/n):{Style.RESET_ALL} ").lower() == 'y':
            config_file = Path(__file__).parent / "config.json"
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except:
                config = {}
            
            config.setdefault('display', {})['template'] = f"custom_{name.lower().replace(' ', '_')}"
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"{Fore.GREEN}✓ Theme applied!{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")
    
    def test_theme(self):
        """Test theme with different data scenarios"""
        if not self.current_fields:
            print(f"{Fore.RED}No fields to test!{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        
        print(f"{Fore.YELLOW}Testing Theme with Different Scenarios:{Style.RESET_ALL}\n")
        
        # Different test scenarios
        scenarios = [
            {
                'name': 'Active Session',
                'data': {**self.preview_data, 'active': True, 'remaining_seconds': 7200}
            },
            {
                'name': 'Expired Session',
                'data': {**self.preview_data, 'active': False, 'remaining_seconds': 0}
            },
            {
                'name': 'High Cost',
                'data': {**self.preview_data, 'cost': 999.99, 'message_count': 5000}
            },
            {
                'name': 'Low Activity',
                'data': {**self.preview_data, 'message_count': 5, 'cost': 0.12}
            }
        ]
        
        theme = {'fields': self.current_fields, 'separator': ' '}
        
        for scenario in scenarios:
            preview = self.builder.format_with_theme(theme, scenario['data'])
            print(f"{Fore.CYAN}{scenario['name']}:{Style.RESET_ALL}")
            print(f"  {preview}\n")
        
        input("Press Enter to continue...")
    
    def _get_color_code(self, color_name: str):
        """Get colorama color code"""
        return self.builder.colors.get(color_name, '')
    
    def run(self):
        """Run the visual theme builder"""
        while True:
            self.clear_screen()
            self.print_header()
            self.show_preview()
            self.show_current_fields()
            self.show_quick_actions()
            
            choice = input(f"{Fore.GREEN}Select action:{Style.RESET_ALL} ").strip()
            
            if choice == '1':
                self.add_field_interactive()
            elif choice == '2':
                self.remove_field_interactive()
            elif choice == '3':
                self.reorder_fields_interactive()
            elif choice == '4':
                self.apply_quick_template()
            elif choice == '5':
                self.apply_color_preset()
            elif choice == '6':
                self.current_fields = []
                print(f"{Fore.GREEN}✓ Cleared all fields!{Style.RESET_ALL}")
                input("Press Enter to continue...")
            elif choice == '7':
                self.save_theme()
            elif choice == '8':
                self.test_theme()
            elif choice == '9' or choice.lower() == 'q':
                print(f"\n{Fore.YELLOW}Goodbye! 👋{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")
                input("Press Enter to continue...")


def main():
    """Main entry point"""
    builder = VisualThemeBuilder()
    builder.run()


if __name__ == "__main__":
    main()