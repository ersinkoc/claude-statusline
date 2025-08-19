#!/usr/bin/env python3
"""
Claude Statusline CLI - Main Entry Point
Unified command-line interface for all Claude Statusline tools
"""

import sys
import argparse
from typing import List, Dict, Any

# Import all modules
from . import statusline
from . import daemon
from . import rebuild
from . import template_selector
from . import daily_report
from . import cost_analyzer
from . import activity_heatmap
from . import summary_report
from . import session_analyzer
from . import model_usage
from . import check_costs
from . import verify_costs
from . import check_current
from . import check_session_data
from . import update_prices
from . import statusline_rotator
from . import theme_manager
from . import usage_analytics
from . import budget_manager

# Tool categories and descriptions
TOOLS = {
    'core': {
        'description': 'Core functionality',
        'commands': {
            'status': {
                'module': statusline,
                'help': 'Show current session status'
            },
            'daemon': {
                'module': daemon,
                'help': 'Manage background daemon'
            },
            'rebuild': {
                'module': rebuild,
                'help': 'Rebuild database from JSONL files'
            }
        }
    },
    'reports': {
        'description': 'Analytics and reporting',
        'commands': {
            'sessions': {
                'module': session_analyzer,
                'help': 'Analyze session details'
            },
            'costs': {
                'module': cost_analyzer,
                'help': 'Analyze costs by model and time'
            },
            'daily': {
                'module': daily_report,
                'help': 'Generate daily usage report'
            },
            'heatmap': {
                'module': activity_heatmap,
                'help': 'Show activity heatmap'
            },
            'summary': {
                'module': summary_report,
                'help': 'Generate summary statistics'
            },
            'models': {
                'module': model_usage,
                'help': 'Show model usage statistics'
            },
            'analytics': {
                'module': usage_analytics,
                'help': 'Advanced usage analytics and insights'
            }
        }
    },
    'check': {
        'description': 'Verification and validation',
        'commands': {
            'check-costs': {
                'module': check_costs,
                'help': 'Verify cost calculations'
            },
            'verify': {
                'module': verify_costs,
                'help': 'Verify cost integrity'
            },
            'current': {
                'module': check_current,
                'help': 'Check current session detection'
            },
            'session-data': {
                'module': check_session_data,
                'help': 'Check session data parsing'
            }
        }
    },
    'manage': {
        'description': 'Configuration and management',
        'commands': {
            'template': {
                'module': template_selector,
                'help': 'Select statusline display template'
            },
            'update-prices': {
                'module': update_prices,
                'help': 'Update model pricing data'
            },
            'rotate': {
                'module': statusline_rotator,
                'help': 'Enable/disable statusline rotation'
            },
            'theme': {
                'module': theme_manager,
                'help': 'Interactive theme manager (search, preview, create custom themes)'
            },
            'budget': {
                'module': budget_manager,
                'help': 'Budget management and cost tracking'
            },
            'visual-builder': {
                'module': None,  # Will handle directly
                'help': 'Visual theme builder with live preview'
            }
        }
    }
}

def print_help():
    """Print the help message"""
    print("\nClaude Statusline CLI")
    print("=====================\n")
    print("Usage: claude-statusline <command> [options]\n")
    
    for category_name, category in TOOLS.items():
        print(f"\n{category['description']}:")
        print("-" * (len(category['description']) + 1))
        
        for cmd_name, cmd_info in category['commands'].items():
            print(f"  {cmd_name:<15} {cmd_info['help']}")
    
    print("\nOptions:")
    print("  -h, --help      Show this help message")
    print("  -v, --version   Show version information")
    print("\nExamples:")
    print("  claude-statusline status")
    print("  claude-statusline daemon --start")
    print("  claude-statusline costs --today")
    print("  claude-statusline theme")
    print("  claude-statusline visual-builder")

def get_version():
    """Get the package version"""
    try:
        from . import __version__
        return __version__
    except ImportError:
        return "1.3.0"

def find_command(cmd: str) -> tuple:
    """Find command in tool categories"""
    for category_name, category in TOOLS.items():
        if cmd in category['commands']:
            return category_name, category['commands'][cmd]
    return None, None

def main():
    """Main entry point"""
    # Handle no arguments
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)
    
    # Get the command
    cmd = sys.argv[1]
    
    # Handle special flags
    if cmd in ['-h', '--help', 'help']:
        print_help()
        sys.exit(0)
    
    if cmd in ['-v', '--version', 'version']:
        print(f"claude-statusline v{get_version()}")
        sys.exit(0)
    
    # Find the command
    category, command_info = find_command(cmd)
    
    if not command_info:
        print(f"Error: Unknown command '{cmd}'")
        print("Run 'claude-statusline --help' for available commands")
        sys.exit(1)
    
    # Execute the command by calling its main function
    try:
        # Handle special commands directly
        if cmd == 'visual-builder':
            from .theme_builder import main as visual_builder_main
            visual_builder_main()
            return
        
        # Pass remaining arguments to the module
        original_argv = sys.argv.copy()
        sys.argv = [cmd] + sys.argv[2:]
        
        # Call the module's main function
        if hasattr(command_info['module'], 'main'):
            command_info['module'].main()
        else:
            print(f"Error: Module for '{cmd}' doesn't have a main() function")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error executing '{cmd}': {e}")
        sys.exit(1)
    finally:
        # Restore original argv if it was set
        if 'original_argv' in locals():
            sys.argv = original_argv

if __name__ == "__main__":
    main()