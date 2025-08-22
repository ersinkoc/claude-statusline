#!/usr/bin/env python3
"""
Simple Interactive Theme Manager - Clean and Functional
"""

import sys
import os
import json
import random
import time
from claude_statusline.unified_powerline_system import UNIFIED_POWERLINE

class InteractiveThemeManager:
    def __init__(self):
        self.themes = UNIFIED_POWERLINE.list_themes()
        self.current_index = 0
        self.current_theme = UNIFIED_POWERLINE.get_current_theme()
        # Find current theme index
        try:
            self.current_index = self.themes.index(self.current_theme)
        except:
            pass
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_live_preview(self):
        """Simple interactive theme browser"""
        while True:
            self.clear_screen()
            theme_name = self.themes[self.current_index]
            theme_info = UNIFIED_POWERLINE.get_theme(theme_name)
            
            # Simple header
            print("\n" + "="*100)
            print(f"POWERLINE THEME SELECTOR - Theme {self.current_index + 1}/100")
            print("="*100)
            print()
            
            # Theme status
            if theme_name == self.current_theme:
                print(f">>> CURRENT: {theme_name} <<<\n")
            else:
                print(f"Theme: {theme_name}\n")
            
            # Live preview - the most important part
            print("PREVIEW:")
            print("-"*100)
            try:
                render = UNIFIED_POWERLINE.render_theme(theme_name)
                print(render)
            except Exception as e:
                print(f"[Preview Error: {e}]")
            print("-"*100)
            print()
            
            # Show widgets in simple list
            print(f"WIDGETS ({len(theme_info['segments'])} total):")
            widgets = theme_info['segments']
            for i, seg in enumerate(widgets, 1):
                widget = seg['widget']
                icon = seg.get('icon', '')
                value = UNIFIED_POWERLINE.get_widget_value(widget)
                color = seg['color']
                print(f"  {i:2}. {icon:2} {widget:<22} = {value:<15} [{color}]")
            
            print()
            print("="*100)
            print("COMMANDS:")
            print("  n/j = Next theme      p/k = Previous theme     ENTER = Apply this theme")
            print("  r   = Random theme    g   = Go to number       q     = Quit")
            print("  +10 = Jump forward   -10 = Jump back           /     = Search")
            print("="*100)
            
            # Simple command input
            cmd = input("Command: ").strip().lower()
            
            if cmd in ['q', 'quit', 'exit']:
                print("\nBye!")
                break
                
            elif cmd in ['n', 'j', 'next']:
                self.current_index = (self.current_index + 1) % 100
                
            elif cmd in ['p', 'k', 'prev', 'previous']:
                self.current_index = (self.current_index - 1) % 100
                
            elif cmd == '+10':
                self.current_index = (self.current_index + 10) % 100
                
            elif cmd == '-10':
                self.current_index = (self.current_index - 10) % 100
                
            elif cmd in ['', 'enter', 'apply']:
                if UNIFIED_POWERLINE.set_current_theme(theme_name):
                    print(f"\n[OK] Applied theme: {theme_name}")
                    self.current_theme = theme_name
                    time.sleep(1)
                else:
                    print(f"\n[ERROR] Failed to apply theme")
                    time.sleep(1)
                    
            elif cmd in ['r', 'random']:
                self.current_index = random.randint(0, 99)
                
            elif cmd in ['g', 'goto']:
                try:
                    num = int(input("Enter theme number (1-100): "))
                    if 1 <= num <= 100:
                        self.current_index = num - 1
                    else:
                        print("Invalid number! Must be 1-100")
                        time.sleep(1)
                except:
                    print("Invalid input!")
                    time.sleep(1)
                    
            elif cmd in ['/', 'search', 's']:
                search = input("Search for: ").lower()
                found = False
                # Search from current position
                for i in range(100):
                    idx = (self.current_index + i) % 100
                    if search in self.themes[idx].lower():
                        self.current_index = idx
                        found = True
                        break
                if not found:
                    print(f"Not found: {search}")
                    time.sleep(1)
                    
            elif cmd in ['b', 'build', 'builder']:
                self.theme_builder()
                
            elif cmd.isdigit():
                # Direct number input
                num = int(cmd)
                if 1 <= num <= 100:
                    self.current_index = num - 1
                else:
                    print(f"Invalid: {num}. Use 1-100")
                    time.sleep(1)
    
    def theme_builder(self):
        """Simple theme builder"""
        self.clear_screen()
        
        print("\n" + "="*100)
        print("THEME BUILDER")
        print("="*100)
        print()
        
        # Available widgets
        all_widgets = [
            'model_short', 'session_elapsed', 'session_remaining', 'session_end_local',
            'session_cost', 'message_count', 'input_tokens', 'output_tokens', 
            'tokens_total', 'cache_read_tokens', 'cache_write_tokens', 'git_branch',
            'folder_name', 'session_number', 'context_percentage', 'current_time',
            'cpu_usage', 'memory_usage'
        ]
        
        print("AVAILABLE WIDGETS:")
        for i, widget in enumerate(all_widgets, 1):
            value = UNIFIED_POWERLINE.get_widget_value(widget)
            print(f"  {i:2}. {widget:<22} = {value}")
        
        print("\nSelect widgets (comma separated numbers, e.g: 1,2,5,7,9)")
        print("Recommended: 6-11 widgets")
        
        try:
            selection = input("\nYour selection: ").strip()
            if not selection:
                print("No selection!")
                time.sleep(1)
                return
                
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_widgets = [all_widgets[i] for i in indices if 0 <= i < len(all_widgets)]
            
            if len(selected_widgets) < 3:
                print("Need at least 3 widgets!")
                time.sleep(1)
                return
            
            # Color selection
            print("\nCOLOR SCHEMES:")
            schemes = [
                ('Ocean', ['soft_blue', 'soft_cyan', 'soft_teal', 'deep_blue']),
                ('Sunset', ['soft_red', 'soft_orange', 'soft_yellow', 'soft_peach']),
                ('Purple', ['soft_purple', 'soft_violet', 'soft_lavender', 'deep_purple']),
                ('Earth', ['soft_brown', 'soft_green', 'soft_sand', 'soft_beige']),
                ('Mono', ['soft_black', 'soft_gray', 'medium_gray', 'light_gray']),
                ('Forest', ['deep_green', 'soft_green', 'soft_mint', 'soft_yellow']),
                ('Fire', ['deep_red', 'soft_red', 'soft_orange', 'soft_yellow']),
                ('Night', ['deep_blue', 'deep_purple', 'soft_black', 'soft_gray'])
            ]
            
            for i, (name, _) in enumerate(schemes, 1):
                print(f"  {i}. {name}")
            
            scheme_idx = int(input("\nSelect color scheme (1-8): ")) - 1
            if 0 <= scheme_idx < len(schemes):
                _, colors = schemes[scheme_idx]
            else:
                colors = schemes[0][1]
            
            # Build theme
            segments = []
            for i, widget in enumerate(selected_widgets):
                color = colors[i % len(colors)]
                
                # Auto icon selection
                if 'model' in widget:
                    icon = ''
                elif 'elapsed' in widget:
                    icon = ''
                elif 'remaining' in widget:
                    icon = '⏳'
                elif 'end' in widget:
                    icon = '⏰'
                elif 'cost' in widget:
                    icon = ''
                elif 'git' in widget:
                    icon = ''
                elif 'folder' in widget:
                    icon = ''
                elif 'message' in widget:
                    icon = ''
                elif 'input_token' in widget:
                    icon = '󰁔'
                elif 'output_token' in widget:
                    icon = '󰁏'
                elif 'tokens_total' in widget:
                    icon = ''
                elif 'cache' in widget:
                    icon = ''
                elif 'session_number' in widget:
                    icon = ''
                elif 'context' in widget:
                    icon = '󰔏'
                elif 'time' in widget:
                    icon = ''
                elif 'cpu' in widget:
                    icon = ''
                elif 'memory' in widget:
                    icon = ''
                else:
                    icon = ''
                
                segments.append({
                    'widget': widget,
                    'icon': icon,
                    'color': color
                })
            
            # Preview
            print("\nCUSTOM THEME PREVIEW:")
            print("-"*100)
            
            # Create temp theme for preview
            custom_theme = {
                'name': 'Custom Theme',
                'description': 'Your custom theme',
                'segments': segments
            }
            
            UNIFIED_POWERLINE.themes['_custom_preview'] = custom_theme
            try:
                render = UNIFIED_POWERLINE.render_theme('_custom_preview')
                print(render)
            except Exception as e:
                print(f"[Preview Error: {e}]")
            finally:
                del UNIFIED_POWERLINE.themes['_custom_preview']
            
            print("-"*100)
            
            # Save?
            save = input("\nSave this theme? (y/n): ").strip().lower()
            if save == 'y':
                name = input("Theme name: ").strip()
                if name:
                    theme_id = f"custom_{name.lower().replace(' ', '_')}"
                    
                    # Save to themes
                    UNIFIED_POWERLINE.themes[theme_id] = {
                        'name': name,
                        'description': f'Custom theme: {name}',
                        'segments': segments
                    }
                    
                    # Also save to file for persistence
                    try:
                        from claude_statusline.data_directory_utils import get_default_data_directory
                        data_dir = get_default_data_directory()
                        custom_file = data_dir / "custom_themes.json"
                        
                        # Load existing custom themes
                        custom_themes = {}
                        if custom_file.exists():
                            with open(custom_file, 'r') as f:
                                custom_themes = json.load(f)
                        
                        # Add new theme
                        custom_themes[theme_id] = {
                            'name': name,
                            'description': f'Custom theme: {name}',
                            'segments': segments
                        }
                        
                        # Save back
                        with open(custom_file, 'w') as f:
                            json.dump(custom_themes, f, indent=2)
                        
                        print(f"\n[OK] Theme saved: {theme_id}")
                        
                        # Apply?
                        apply = input("Apply this theme now? (y/n): ").strip().lower()
                        if apply == 'y':
                            UNIFIED_POWERLINE.set_current_theme(theme_id)
                            self.current_theme = theme_id
                            print(f"[OK] Applied: {theme_id}")
                    except Exception as e:
                        print(f"[ERROR] Save failed: {e}")
                    
                    time.sleep(2)
                    
        except KeyboardInterrupt:
            print("\nCancelled")
            time.sleep(1)
        except Exception as e:
            print(f"\n[ERROR]: {e}")
            time.sleep(2)

def main():
    """Entry point"""
    manager = InteractiveThemeManager()
    manager.show_live_preview()

if __name__ == "__main__":
    main()