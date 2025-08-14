#!/usr/bin/env python3
"""
Template Selector for Claude Statusline
Interactive template selection and preview
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any
from statusline_templates import StatuslineTemplates


class TemplateSelector:
    """Interactive template selector"""
    
    def __init__(self):
        """Initialize template selector"""
        self.config_file = Path(__file__).parent / "config.json"
        self.templates = StatuslineTemplates()
        self.sample_data = self._get_sample_data()
    
    def _get_sample_data(self) -> Dict[str, Any]:
        """Get sample data for preview"""
        # Try to get real data first
        try:
            data_dir = Path.home() / ".claude" / "data-statusline"
            live_session_file = data_dir / "live_session.json"
            
            if live_session_file.exists():
                with open(live_session_file, 'r') as f:
                    data = json.load(f)
                    if data and data.get('message_count', 0) > 0:
                        # Add session_end_time if not present
                        if 'session_end_time' not in data:
                            from datetime import datetime, timedelta, timezone
                            if data.get('session_start'):
                                try:
                                    start = data['session_start']
                                    if 'T' in start and '+' not in start and 'Z' not in start:
                                        start += '+00:00'
                                    start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                                    end_time = start_time + timedelta(hours=5)
                                    local_end = end_time.astimezone()
                                    data['session_end_time'] = local_end.strftime('%H:%M')
                                except:
                                    data['session_end_time'] = '17:00'
                        return data
        except:
            pass
        
        # Fallback to sample data
        return {
            'primary_model': 'Opus 4.1',
            'active': True,
            'session_number': 123,
            'session_end_time': '17:00',
            'message_count': 456,
            'tokens': 12345678,
            'cost': 89.99,
            'remaining_seconds': 7200
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load current configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_config(self, config: Dict[str, Any]):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def preview_all(self):
        """Preview all available templates"""
        print("\nClaude Statusline Template Gallery")
        print("=" * 70)
        print("\nUsing sample data for preview:")
        
        # Show sample data info
        model = self.sample_data.get('primary_model', 'Unknown')
        msgs = self.sample_data.get('message_count', 0)
        cost = self.sample_data.get('cost', 0.0)
        print(f"Model: {model}, Messages: {msgs}, Cost: ${cost:.2f}")
        print("-" * 70)
        
        templates = self.templates.list_templates()
        for i, template in enumerate(templates, 1):
            output = self.templates.format(template, self.sample_data)
            desc = self.templates.get_description(template)
            
            # Mark current template
            config = self.load_config()
            current = config.get('display', {}).get('template', 'compact')
            marker = " [CURRENT]" if template == current else ""
            
            print(f"\n{i:2}. {template:15} - {desc}{marker}")
            print(f"    {output}")
    
    def select_interactive(self):
        """Interactive template selection"""
        templates = self.templates.list_templates()
        
        print("\nSelect a template (1-{} or name):".format(len(templates)))
        print("Enter 'q' to quit without changing")
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            print("No changes made.")
            return False
        
        # Check if numeric choice
        try:
            index = int(choice) - 1
            if 0 <= index < len(templates):
                selected = templates[index]
            else:
                print(f"Invalid choice. Please enter 1-{len(templates)}")
                return False
        except ValueError:
            # Check if template name
            if choice in templates:
                selected = choice
            else:
                print(f"Unknown template: {choice}")
                return False
        
        # Update config
        config = self.load_config()
        if 'display' not in config:
            config['display'] = {}
        config['display']['template'] = selected
        
        self.save_config(config)
        print(f"\n[OK] Template changed to: {selected}")
        
        # Show preview
        output = self.templates.format(selected, self.sample_data)
        print(f"Preview: {output}")
        
        return True
    
    def set_template(self, template_name: str):
        """Set template directly"""
        templates = self.templates.list_templates()
        
        if template_name not in templates:
            print(f"[ERROR] Unknown template: {template_name}")
            print(f"Available templates: {', '.join(templates)}")
            return False
        
        config = self.load_config()
        if 'display' not in config:
            config['display'] = {}
        config['display']['template'] = template_name
        
        self.save_config(config)
        print(f"[OK] Template set to: {template_name}")
        
        # Show preview
        output = self.templates.format(template_name, self.sample_data)
        print(f"Preview: {output}")
        
        return True
    
    def get_current(self):
        """Get current template"""
        config = self.load_config()
        current = config.get('display', {}).get('template', 'compact')
        print(f"Current template: {current}")
        
        # Show current output
        output = self.templates.format(current, self.sample_data)
        print(f"Current format: {output}")
        
        return current


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Select statusline template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python select_template.py              # Interactive selection
  python select_template.py --list       # List all templates
  python select_template.py --set vim    # Set specific template
  python select_template.py --current    # Show current template

Available templates:
  compact, minimal, detailed, emoji, dev, vim, powerline, matrix,
  nerd, zen, hacker, corporate, creative, scientific, casual,
  discord, twitch, github, terminal, json
        """
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available templates'
    )
    
    parser.add_argument(
        '--set', '-s',
        metavar='TEMPLATE',
        help='Set specific template'
    )
    
    parser.add_argument(
        '--current', '-c',
        action='store_true',
        help='Show current template'
    )
    
    args = parser.parse_args()
    
    selector = TemplateSelector()
    
    if args.list:
        selector.preview_all()
    elif args.set:
        selector.set_template(args.set)
    elif args.current:
        selector.get_current()
    else:
        # Interactive mode
        selector.preview_all()
        print()
        selector.select_interactive()


if __name__ == "__main__":
    main()