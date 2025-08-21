#!/usr/bin/env python3
"""
Claude Statusline CLI - Main Entry Point
Unified command-line interface for all Claude Statusline tools
"""

import sys
import os
import argparse

# Force UTF-8 encoding on Windows for Unicode/nerd font support
if os.name == 'nt' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def print_help():
    """Print help message"""
    print("""
Claude Statusline CLI
=====================

Usage: claude-statusline <command> [options]

Core Commands:
--------------
  status          Show current session status
  daemon          Manage background daemon (--start, --status, --stop)
  rebuild         Rebuild database from JSONL files
  theme           Theme management (list, select, create, apply, preview)

Analytics:
----------
  sessions        Analyze session details
  costs           Analyze costs by model and time
  daily           Generate daily usage report
  heatmap         Show activity heatmap
  summary         Generate summary statistics
  models          Show model usage statistics
  analytics       Advanced usage analytics
  budget          Budget management and tracking

Utilities:
----------
  update-prices   Update model pricing data
  verify          Verify cost calculations
  rotate          Enable/disable statusline rotation

Options:
  -h, --help      Show this help message
  -v, --version   Show version information

Examples:
  claude-statusline status
  claude-statusline daemon --start
  claude-statusline theme select
  claude-statusline costs --today
""")

def main():
    """Main CLI entry point"""
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd in ['-h', '--help', 'help']:
        print_help()
        sys.exit(0)
    
    if cmd in ['-v', '--version', 'version']:
        print("claude-statusline v1.8.0")
        sys.exit(0)
    
    # Handle commands
    try:
        if cmd == 'status':
            from claude_statusline.statusline import StatuslineDisplay
            from claude_statusline.unified_theme_system import safe_unicode_print
            result = StatuslineDisplay().display()
            
            # Handle Unicode output safely
            if result == "[Powerline theme active]":
                # Unicode output was already sent directly to console
                pass
            else:
                # Use safe Unicode printing for any remaining output
                safe_output = safe_unicode_print(result)
                if safe_output:  # If function returned text instead of printing
                    print(safe_output)
            
        elif cmd == 'theme':
            from claude_statusline.unified_theme_system import THEME_SYSTEM
            
            if len(sys.argv) > 2:
                subcmd = sys.argv[2]
                if subcmd == 'list':
                    try:
                        THEME_SYSTEM.list_themes()
                    except UnicodeEncodeError:
                        # Fallback to safe listing
                        print("Theme listing with Unicode encoding issue - using safe mode")
                        themes = THEME_SYSTEM.get_all_themes()
                        for name, theme in themes.items():
                            print(f"  • {theme['name']} - {theme['description']}")
                elif subcmd == 'select':
                    THEME_SYSTEM.select_theme_interactive()
                elif subcmd == 'create':
                    THEME_SYSTEM.create_custom_theme()
                elif subcmd == 'preview':
                    if len(sys.argv) > 3:
                        from claude_statusline.unified_theme_system import safe_unicode_print
                        preview_result = THEME_SYSTEM.preview_theme(sys.argv[3])
                        safe_output = safe_unicode_print(preview_result)
                        if safe_output:
                            print(safe_output)
                    else:
                        print("Usage: theme preview <theme_name>")
                elif subcmd == 'apply':
                    if len(sys.argv) > 3:
                        if THEME_SYSTEM.set_current_theme(sys.argv[3]):
                            print(f"[OK] Theme '{sys.argv[3]}' applied")
                        else:
                            print(f"[X] Failed to apply theme")
                    else:
                        print("Usage: theme apply <theme_name>")
                else:
                    # Try as theme name
                    if THEME_SYSTEM.set_current_theme(subcmd):
                        print(f"[OK] Theme '{subcmd}' applied")
                    else:
                        print(f"Unknown command: {subcmd}")
            else:
                THEME_SYSTEM.select_theme_interactive()
                
        elif cmd == 'rebuild':
            print("=== DATABASE REBUILD ===")
            from claude_statusline.rebuild import DatabaseRebuilder
            rebuilder = DatabaseRebuilder()
            if rebuilder.rebuild_database():
                print("[OK] Database rebuild completed")
            else:
                print("[X] Database rebuild failed")
                
        elif cmd == 'daemon':
            from claude_statusline.daemon_manager import DaemonManager
            manager = DaemonManager()
            
            daemon_cmd = sys.argv[2] if len(sys.argv) > 2 else '--help'
            
            if daemon_cmd == '--start':
                print("=== STARTING DAEMON ===")
                if manager.start_daemon_if_needed():
                    print("[OK] Daemon started")
                else:
                    print("[X] Failed to start daemon")
            elif daemon_cmd == '--status':
                print("=== DAEMON STATUS ===")
                if manager.is_daemon_running():
                    print("[OK] Daemon is running")
                else:
                    print("[X] Daemon is not running")
            elif daemon_cmd == '--stop':
                print("=== STOPPING DAEMON ===")
                from claude_statusline.daemon import DaemonService
                daemon = DaemonService()
                daemon.stop()
            else:
                print("Daemon commands:")
                print("  daemon --start   Start the daemon")
                print("  daemon --status  Check daemon status")
                print("  daemon --stop    Stop the daemon")
                
        elif cmd == 'sessions':
            from claude_statusline.session_analyzer import main as sessions_main
            sessions_main()
            
        elif cmd == 'costs':
            from claude_statusline.cost_analyzer import main as costs_main
            costs_main()
            
        elif cmd == 'daily':
            from claude_statusline.daily_report import main as daily_main
            daily_main()
            
        elif cmd == 'heatmap':
            from claude_statusline.activity_heatmap import main as heatmap_main
            heatmap_main()
            
        elif cmd == 'summary':
            from claude_statusline.summary_report import main as summary_main
            summary_main()
            
        elif cmd == 'models':
            from claude_statusline.model_usage import main as models_main
            models_main()
            
        elif cmd == 'analytics':
            from claude_statusline.analytics_cli import AnalyticsCLI
            analytics = AnalyticsCLI()
            analytics.run()
            
        elif cmd == 'budget':
            from claude_statusline.budget_manager import main as budget_main
            budget_main()
            
        elif cmd == 'update-prices':
            from claude_statusline.update_prices import main as prices_main
            prices_main()
            
        elif cmd == 'verify':
            from claude_statusline.verify_costs import main as verify_main
            verify_main()
            
        elif cmd == 'rotate':
            from claude_statusline.statusline_rotator import main as rotate_main
            rotate_main()
            
        else:
            print(f"Unknown command: {cmd}")
            print("Run 'claude-statusline --help' for available commands")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled")
        sys.exit(0)
    except ImportError as e:
        print(f"Module not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()