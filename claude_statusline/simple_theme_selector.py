#!/usr/bin/env python3
"""
Simple Theme Selector - TEK SİSTEM
"""

import sys
import os
from claude_statusline.unified_powerline_system import UNIFIED_POWERLINE

def list_themes():
    """List all 100 themes with FULL POWERLINE render"""
    print("\n" + "="*100)
    print("                    POWERLINE THEME GALLERY - 100 THEMES")
    print("="*100)
    
    themes = UNIFIED_POWERLINE.list_themes()
    current = UNIFIED_POWERLINE.get_current_theme()
    
    print(f"\nTotal: {len(themes)} themes | Current: {current}")
    print("-"*100)
    
    # Show all themes with FULL POWERLINE RENDER
    for i, theme_name in enumerate(themes, 1):
        # Get FULL POWERLINE RENDER
        try:
            full_render = UNIFIED_POWERLINE.render_theme(theme_name)
        except:
            full_render = "[render error]"
        
        # Show theme number, name and FULL powerline
        indicator = ">>>" if theme_name == current else "   "
        print(f"{indicator} {i:3d}. {theme_name:<15}")
        print(f"        {full_render}")
        
        # Add separator every 5 themes
        if i % 5 == 0 and i < len(themes):
            print("-"*100)

def select_theme():
    """Interactive theme selection with FULL POWERLINE preview"""
    themes = UNIFIED_POWERLINE.list_themes()
    current = UNIFIED_POWERLINE.get_current_theme()
    
    print("\n" + "="*100)
    print("                    POWERLINE THEME SELECTOR - ALL 100 THEMES")
    print("="*100)
    print(f"\nCurrent theme: {current}")
    print("Type number to preview, 'set <number>' to apply, 'q' to quit")
    print("-"*100)
    
    # Show ALL themes with FULL powerline
    page_size = 10
    page = 0
    
    while True:
        start = page * page_size
        end = min(start + page_size, len(themes))
        
        print(f"\n--- Page {page + 1}/{(len(themes) + page_size - 1) // page_size} (Themes {start + 1}-{end}) ---\n")
        
        for i in range(start, end):
            theme = themes[i]
            indicator = ">>>" if theme == current else "   "
            
            # Get FULL POWERLINE RENDER
            try:
                full_render = UNIFIED_POWERLINE.render_theme(theme)
            except:
                full_render = "[render error]"
            
            print(f"{indicator} {i+1:3d}. {theme:<15}")
            print(f"        {full_render}")
            print()
        
        print("-"*100)
        print("Commands: [n]ext page, [p]rev page, <number> to preview, set <number> to apply, [q]uit")
        
        try:
            choice = input("Your choice: ").strip().lower()
            
            if choice == 'q':
                print("No changes made.")
                return
            elif choice == 'n':
                if end < len(themes):
                    page += 1
                else:
                    print("Already on last page!")
            elif choice == 'p':
                if page > 0:
                    page -= 1
                else:
                    print("Already on first page!")
            elif choice.startswith('set '):
                try:
                    num = int(choice[4:])
                    if 1 <= num <= len(themes):
                        selected_theme = themes[num - 1]
                        if UNIFIED_POWERLINE.set_current_theme(selected_theme):
                            print(f"\n[OK] Theme set to: {selected_theme}")
                            print("\nNew theme applied:")
                            print(UNIFIED_POWERLINE.render_theme(selected_theme))
                            current = selected_theme
                        else:
                            print("[ERROR] Failed to set theme")
                    else:
                        print(f"Invalid number! Choose 1-{len(themes)}")
                except ValueError:
                    print("Invalid number!")
            elif choice.isdigit():
                num = int(choice)
                if 1 <= num <= len(themes):
                    theme_name = themes[num - 1]
                    print(f"\n--- PREVIEW: {theme_name} ---")
                    print(UNIFIED_POWERLINE.render_theme(theme_name))
                    print()
                else:
                    print(f"Invalid number! Choose 1-{len(themes)}")
            else:
                print("Unknown command!")
        
        except KeyboardInterrupt:
            print("\nCancelled.")
            return

def preview_theme(theme_name):
    """Preview a specific theme with FULL POWERLINE RENDER"""
    if theme_name in UNIFIED_POWERLINE.list_themes():
        theme_info = UNIFIED_POWERLINE.get_theme(theme_name)
        
        print(f"THEME PREVIEW: {theme_name}")
        print("=" * 80)
        print(f"Name: {theme_info['name']}")
        print(f"Description: {theme_info['description']}")
        print(f"Widgets: {len(theme_info['segments'])}")
        print()
        
        # Show FULL POWERLINE RENDER
        print("Full Powerline Render:")
        try:
            full_render = UNIFIED_POWERLINE.render_theme(theme_name)
            print(full_render)
        except Exception as e:
            print(f"[Render error: {e}]")
        
        print()
        
        # Also show widget breakdown
        print("Widget Breakdown:")
        for segment in theme_info['segments']:
            widget = segment['widget']
            icon = segment['icon']
            color = segment['color']
            value = UNIFIED_POWERLINE.get_widget_value(widget)
            print(f"  {icon} {widget}: {value} ({color})")
        
        print()
        print("Status: [OK] Ready for Windows Terminal with RGB colors")
    else:
        print(f"Theme '{theme_name}' not found!")

def apply_theme(theme_name):
    """Apply a theme directly"""
    if theme_name in UNIFIED_POWERLINE.list_themes():
        if UNIFIED_POWERLINE.set_current_theme(theme_name):
            print(f"[OK] Theme '{theme_name}' applied!")
        else:
            print(f"[ERROR] Failed to apply theme '{theme_name}'")
    else:
        print(f"[ERROR] Theme '{theme_name}' not found!")
        print("Available themes:")
        themes = UNIFIED_POWERLINE.list_themes()
        for theme in themes[:10]:
            print(f"  - {theme}")
        if len(themes) > 10:
            print(f"  ... and {len(themes) - 10} more")

def main():
    """Main theme selector"""
    if len(sys.argv) < 2:
        print("Theme Commands:")
        print("  list     - List all themes")
        print("  select   - Interactive theme selection")
        print("  preview <theme> - Preview theme")
        print("  apply <theme>   - Apply theme")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'list':
        list_themes()
    elif cmd == 'select':
        select_theme()
    elif cmd == 'preview':
        if len(sys.argv) > 2:
            preview_theme(sys.argv[2])
        else:
            print("Usage: theme preview <theme_name>")
    elif cmd == 'apply':
        if len(sys.argv) > 2:
            apply_theme(sys.argv[2])
        else:
            print("Usage: theme apply <theme_name>")
    else:
        print(f"Unknown command: {cmd}")

if __name__ == '__main__':
    main()