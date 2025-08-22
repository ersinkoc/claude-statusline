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
  theme           Interactive theme browser (100 themes)
  theme build     Create custom themes
  theme list      List all themes
  theme apply     Apply specific theme

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
  trends          Analyze usage trends and patterns

Utilities:
----------
  update-prices   Update model pricing data
  verify          Verify cost calculations
  rotate          Enable/disable statusline rotation
  health          System health monitoring

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
        print("claude-statusline v1.9.0")
        sys.exit(0)
    
    # Handle commands
    try:
        if cmd == 'status':
            from claude_statusline.statusline import StatuslineDisplay
            from claude_statusline.console_utils import safe_unicode_print
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
            # Theme management - interactive or simple
            if len(sys.argv) > 2:
                subcmd = sys.argv[2]
                if subcmd in ['interactive', 'browse', 'i']:
                    # Interactive theme browser
                    from claude_statusline.interactive_theme_manager import InteractiveThemeManager
                    manager = InteractiveThemeManager()
                    manager.show_live_preview()
                elif subcmd in ['build', 'builder', 'b']:
                    # Theme builder
                    from claude_statusline.interactive_theme_manager import InteractiveThemeManager
                    manager = InteractiveThemeManager()
                    manager.theme_builder()
                else:
                    # Original simple theme selector for list/apply/preview
                    from claude_statusline.simple_theme_selector import main as theme_main
                    sys.argv = ['theme'] + sys.argv[2:]
                    theme_main()
            else:
                # Default to interactive browser
                print("Starting interactive theme browser...")
                from claude_statusline.interactive_theme_manager import InteractiveThemeManager
                manager = InteractiveThemeManager()
                manager.show_live_preview()
                
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
            from claude_statusline.session_analyzer import SessionAnalyzer
            analyzer = SessionAnalyzer()
            
            # Parse subcommands
            if len(sys.argv) > 2 and sys.argv[2] == '--patterns':
                analyzer.analyze_usage_patterns()
            elif len(sys.argv) > 2 and sys.argv[2] == '--top':
                n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
                analyzer.get_top_sessions(n)
            else:
                analyzer.analyze_all_sessions()
            
        elif cmd == 'costs':
            from claude_statusline.cost_analyzer import CostAnalyzer
            analyzer = CostAnalyzer()
            
            # Parse subcommands
            if len(sys.argv) > 2 and sys.argv[2] == '--trends':
                days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
                analyzer.analyze_cost_trends(days)
            else:
                analyzer.analyze_costs()
            
        elif cmd == 'daily':
            from claude_statusline.daily_report import DailyReportGenerator
            generator = DailyReportGenerator()
            
            # Parse subcommands  
            date_str = None
            days = 7
            for i, arg in enumerate(sys.argv[2:], 2):
                if arg == '--date' and i+1 < len(sys.argv):
                    date_str = sys.argv[i+1]
                elif arg == '--days' and i+1 < len(sys.argv):
                    days = int(sys.argv[i+1])
            
            if date_str:
                generator.generate_daily_report(date_str)
            else:
                generator.generate_date_range_report(days)
            
        elif cmd == 'heatmap':
            from claude_statusline.activity_heatmap import ActivityHeatmapGenerator
            generator = ActivityHeatmapGenerator()
            
            # Parse subcommands
            if len(sys.argv) > 2:
                subcmd = sys.argv[2]
                if subcmd == '--monthly':
                    month = None
                    year = None
                    # Check for month/year arguments
                    for i, arg in enumerate(sys.argv[3:], 3):
                        if arg == '--month' and i+1 < len(sys.argv):
                            month = int(sys.argv[i+1])
                        elif arg == '--year' and i+1 < len(sys.argv):
                            year = int(sys.argv[i+1])
                    generator.generate_monthly_calendar(month, year)
                elif subcmd == '--peak':
                    generator.analyze_peak_hours()
                else:
                    generator.generate_weekly_heatmap()
            else:
                generator.generate_weekly_heatmap()
            
        elif cmd == 'summary':
            from claude_statusline.summary_report import SummaryReportGenerator
            generator = SummaryReportGenerator()
            
            # Parse subcommands
            if len(sys.argv) > 2:
                subcmd = sys.argv[2]
                if subcmd == '--weekly':
                    weeks = int(sys.argv[3]) if len(sys.argv) > 3 else 1
                    generator.generate_weekly_summary(weeks)
                elif subcmd == '--monthly':
                    months = int(sys.argv[3]) if len(sys.argv) > 3 else 1
                    generator.generate_monthly_summary(months)
                elif subcmd == '--all':
                    generator.generate_all_time_summary()
                else:
                    generator.generate_all_time_summary()
            else:
                generator.generate_all_time_summary()
            
        elif cmd == 'models':
            from claude_statusline.model_usage import ModelUsageAnalyzer
            analyzer = ModelUsageAnalyzer()
            
            # Parse subcommands
            if len(sys.argv) > 2 and sys.argv[2] == '--trends':
                days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
                analyzer.analyze_model_trends(days)
            else:
                analyzer.analyze_model_usage()
            
        elif cmd == 'analytics':
            from claude_statusline.analytics_cli import AnalyticsCLI
            analytics = AnalyticsCLI()
            analytics.run()
            
        elif cmd == 'budget':
            from claude_statusline.budget_manager import BudgetManager
            manager = BudgetManager()
            
            # Parse subcommands
            if len(sys.argv) > 2:
                subcmd = sys.argv[2]
                if subcmd == 'set':
                    # Set budget limits
                    period = sys.argv[3] if len(sys.argv) > 3 else 'monthly'
                    limit = float(sys.argv[4]) if len(sys.argv) > 4 else 200.0
                    manager.set_budget_limit(period, limit)
                elif subcmd == 'status':
                    manager.show_budget_status()
                elif subcmd == 'dashboard':
                    manager.show_dashboard()
                else:
                    manager.show_dashboard()
            else:
                manager.show_dashboard()
            
        elif cmd == 'update-prices':
            from claude_statusline.update_prices import PriceUpdater
            updater = PriceUpdater()
            
            # Parse subcommands
            force = False
            verify = False
            for arg in sys.argv[2:]:
                if arg == '--force':
                    force = True
                elif arg == '--verify':
                    verify = True
            
            if verify:
                updater.verify_prices()
            else:
                updater.update_prices(force=force)
            
        elif cmd == 'verify':
            from claude_statusline.verify_costs import main as verify_main
            verify_main()
            
        elif cmd == 'rotate':
            from claude_statusline.statusline_rotator import main as rotate_main
            rotate_main()
            
        elif cmd == 'trends':
            from claude_statusline.trend_analyzer import TrendAnalyzer
            analyzer = TrendAnalyzer()
            
            # Parse subcommands
            days = 30
            show_all = True
            
            for i, arg in enumerate(sys.argv[2:], 2):
                if arg == '--days' and i+1 < len(sys.argv):
                    days = int(sys.argv[i+1])
                elif arg == '--trends':
                    show_all = False
                    analyzer.analyze_usage_trends(days)
                elif arg == '--productivity':
                    show_all = False
                    analyzer.analyze_productivity_patterns()
                elif arg == '--efficiency':
                    show_all = False
                    analyzer.analyze_model_efficiency()
                elif arg == '--insights':
                    show_all = False
                    analyzer.generate_insights_report()
            
            if show_all:
                analyzer.analyze_usage_trends(days)
                analyzer.analyze_productivity_patterns()
                analyzer.analyze_model_efficiency()
                analyzer.generate_insights_report()
        
        elif cmd == 'health':
            from claude_statusline.health_monitor import HealthMonitor
            monitor = HealthMonitor()
            
            # Parse subcommands
            if len(sys.argv) > 2:
                subcmd = sys.argv[2]
                if subcmd == '--full':
                    monitor.run_comprehensive_health_check()
                elif subcmd == '--quick':
                    monitor.quick_status_check()
                elif subcmd == '--diagnostic':
                    monitor.generate_diagnostic_report()
                elif subcmd == '--monitor':
                    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
                    monitor.monitor_performance(duration)
                else:
                    monitor.quick_status_check()
            else:
                monitor.quick_status_check()
            
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