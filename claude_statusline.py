#!/usr/bin/env python3
"""
Claude Statusline CLI - Main Entry Point
Unified command-line interface for all Claude Statusline tools
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any

# Tool categories and descriptions
TOOLS = {
    'core': {
        'description': 'Core functionality',
        'commands': {
            'status': {
                'script': 'statusline.py',
                'help': 'Show current session status'
            },
            'daemon': {
                'script': 'unified_daemon.py',
                'help': 'Manage background daemon',
                'args': ['--daemon', '--status', '--stop', '--restart']
            },
            'rebuild': {
                'script': 'rebuild_database.py',
                'help': 'Rebuild database from JSONL files'
            }
        }
    },
    'reports': {
        'description': 'Analytics and reporting',
        'commands': {
            'sessions': {
                'script': 'session_analyzer.py',
                'help': 'Analyze session details'
            },
            'costs': {
                'script': 'cost_analyzer.py',
                'help': 'Analyze costs by model and time'
            },
            'daily': {
                'script': 'daily_report.py',
                'help': 'Generate daily usage report'
            },
            'heatmap': {
                'script': 'activity_heatmap.py',
                'help': 'Show activity heatmap'
            },
            'models': {
                'script': 'model_usage.py',
                'help': 'Show model usage statistics'
            },
            'summary': {
                'script': 'summary_report.py',
                'help': 'Generate summary report'
            }
        }
    },
    'check': {
        'description': 'Debugging and verification',
        'commands': {
            'current': {
                'script': 'check_current.py',
                'help': 'Check current session detection'
            },
            'costs': {
                'script': 'check_costs.py',
                'help': 'Verify cost calculations'
            },
            'verify': {
                'script': 'verify_costs.py',
                'help': 'Verify cost accuracy'
            },
            'session': {
                'script': 'check_session_data.py',
                'help': 'Check session data integrity'
            }
        }
    },
    'manage': {
        'description': 'Management and maintenance',
        'commands': {
            'update-prices': {
                'script': 'update_prices.py',
                'help': 'Update model prices from repository'
            },
            'template': {
                'script': 'select_template.py',
                'help': 'Select statusline display template'
            },
            'test': {
                'script': 'test_statusline.py',
                'help': 'Test statusline functionality'
            }
        }
    }
}


class ClaudeStatuslineCLI:
    """Main CLI handler for Claude Statusline"""
    
    def __init__(self):
        """Initialize CLI"""
        self.script_dir = Path(__file__).parent
        self.python = sys.executable
    
    def run_script(self, script: str, args: List[str] = None) -> int:
        """
        Run a Python script with arguments
        
        Args:
            script: Script filename
            args: Additional arguments
            
        Returns:
            Exit code
        """
        script_path = self.script_dir / script
        if not script_path.exists():
            print(f"[ERROR] Script not found: {script}")
            return 1
        
        cmd = [self.python, str(script_path)]
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(cmd, cwd=str(self.script_dir))
            return result.returncode
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user")
            return 130
        except Exception as e:
            print(f"[ERROR] Failed to run {script}: {e}")
            return 1
    
    def print_help(self):
        """Print comprehensive help message"""
        print("""
Claude Statusline CLI - Unified Interface
==========================================

Usage: claude-statusline <category> <command> [options]

Categories and Commands:
""")
        
        for category, info in TOOLS.items():
            print(f"\n{category.upper()} - {info['description']}")
            print("-" * 40)
            
            for cmd, details in info['commands'].items():
                print(f"  {cmd:15} {details['help']}")
                if 'args' in details:
                    print(f"  {'':15} Options: {', '.join(details['args'])}")
        
        print("""
Examples:
---------
  # Show current status
  claude-statusline core status
  
  # Start daemon
  claude-statusline core daemon --daemon
  
  # Generate cost report
  claude-statusline reports costs
  
  # Update prices
  claude-statusline manage update-prices
  
  # Quick shortcuts (most common commands)
  claude-statusline status      # Show status
  claude-statusline daemon      # Manage daemon
  claude-statusline costs       # Cost report
  claude-statusline daily       # Daily report

For detailed help on a specific command:
  claude-statusline <category> <command> --help
""")
    
    def main(self):
        """Main CLI entry point"""
        if len(sys.argv) < 2:
            self.print_help()
            return 0
        
        # Quick shortcuts for common commands
        shortcuts = {
            'status': ('core', 'status'),
            'daemon': ('core', 'daemon'),
            'rebuild': ('core', 'rebuild'),
            'costs': ('reports', 'costs'),
            'daily': ('reports', 'daily'),
            'sessions': ('reports', 'sessions'),
            'update-prices': ('manage', 'update-prices'),
            'help': (None, None),
            '--help': (None, None),
            '-h': (None, None)
        }
        
        first_arg = sys.argv[1]
        
        # Handle help
        if first_arg in ['help', '--help', '-h']:
            self.print_help()
            return 0
        
        # Check for shortcuts
        if first_arg in shortcuts:
            category, command = shortcuts[first_arg]
            if category is None:
                self.print_help()
                return 0
            remaining_args = sys.argv[2:]
        else:
            # Parse category and command
            if len(sys.argv) < 3:
                # Maybe it's a category?
                if first_arg in TOOLS:
                    print(f"\n{first_arg.upper()} Commands:")
                    print("-" * 40)
                    for cmd, details in TOOLS[first_arg]['commands'].items():
                        print(f"  {cmd:15} {details['help']}")
                    print(f"\nUsage: claude-statusline {first_arg} <command> [options]")
                else:
                    print(f"[ERROR] Unknown command: {first_arg}")
                    print("Run 'claude-statusline help' for available commands")
                return 1
            
            category = sys.argv[1]
            command = sys.argv[2]
            remaining_args = sys.argv[3:]
        
        # Validate category and command
        if category not in TOOLS:
            print(f"[ERROR] Unknown category: {category}")
            print("Available categories:", ', '.join(TOOLS.keys()))
            return 1
        
        if command not in TOOLS[category]['commands']:
            print(f"[ERROR] Unknown command '{command}' in category '{category}'")
            print(f"Available commands in {category}:")
            for cmd in TOOLS[category]['commands']:
                print(f"  - {cmd}")
            return 1
        
        # Run the command
        script_info = TOOLS[category]['commands'][command]
        script = script_info['script']
        
        print(f"[INFO] Running: {script_info['help']}")
        print("-" * 50)
        
        return self.run_script(script, remaining_args)


def main():
    """Main entry point"""
    cli = ClaudeStatuslineCLI()
    sys.exit(cli.main())


if __name__ == "__main__":
    main()