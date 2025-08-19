#!/usr/bin/env python3
"""
Budget Manager for Claude Statusline
Advanced budget tracking, limits, and financial planning
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import calendar

from .data_directory_utils import resolve_data_directory
from .safe_file_operations import safe_json_read
from .console_utils import print_colored


class BudgetManager:
    """Comprehensive budget management and tracking system"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.budget_file = self.data_dir / "budget_config.json"
        
        self.db = safe_json_read(self.db_file) if self.db_file.exists() else {}
        self.budget_config = self.load_budget_config()
    
    def load_budget_config(self) -> Dict:
        """Load budget configuration or create default"""
        if self.budget_file.exists():
            return safe_json_read(self.budget_file)
        else:
            default_config = {
                "budgets": {
                    "daily": {"limit": 10.0, "enabled": False},
                    "weekly": {"limit": 50.0, "enabled": False}, 
                    "monthly": {"limit": 200.0, "enabled": True},
                    "yearly": {"limit": 2400.0, "enabled": False}
                },
                "model_limits": {},
                "project_budgets": {},
                "alerts": {
                    "enabled": True,
                    "warning_threshold": 0.8,  # 80% of budget
                    "critical_threshold": 0.95  # 95% of budget
                },
                "currency": "USD",
                "fiscal_year_start": "January"
            }
            with open(self.budget_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def save_budget_config(self):
        """Save current budget configuration"""
        with open(self.budget_file, 'w') as f:
            json.dump(self.budget_config, f, indent=2)
    
    def set_budget_limit(self, period: str, amount: float, enabled: bool = True):
        """Set budget limit for a specific period"""
        valid_periods = ['daily', 'weekly', 'monthly', 'yearly']
        if period not in valid_periods:
            print_colored(f"❌ Invalid period. Use: {', '.join(valid_periods)}", "red")
            return
        
        self.budget_config['budgets'][period] = {
            'limit': amount,
            'enabled': enabled
        }
        self.save_budget_config()
        
        status = "enabled" if enabled else "disabled"
        print_colored(f"✅ {period.title()} budget set to ${amount:.2f} ({status})", "green")
    
    def set_model_limit(self, model: str, daily_limit: float, monthly_limit: float = None):
        """Set spending limits for specific models"""
        self.budget_config['model_limits'][model] = {
            'daily_limit': daily_limit,
            'monthly_limit': monthly_limit or daily_limit * 30,
            'enabled': True
        }
        self.save_budget_config()
        
        print_colored(f"✅ Model '{model}' limits set: ${daily_limit:.2f}/day", "green")
        if monthly_limit:
            print_colored(f"   Monthly limit: ${monthly_limit:.2f}", "cyan")
    
    def set_project_budget(self, project_name: str, budget: float, start_date: str = None, end_date: str = None):
        """Set budget for specific projects/folders"""
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        if not end_date:
            # Default to 3 months
            end_date = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
        
        self.budget_config['project_budgets'][project_name] = {
            'budget': budget,
            'start_date': start_date,
            'end_date': end_date,
            'spent': 0.0,
            'enabled': True
        }
        self.save_budget_config()
        
        print_colored(f"✅ Project '{project_name}' budget: ${budget:.2f} ({start_date} to {end_date})", "green")
    
    def get_period_spending(self, period: str) -> float:
        """Calculate spending for a specific time period"""
        now = datetime.now()
        
        if period == 'daily':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'weekly':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'monthly':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == 'yearly':
            fiscal_start = self.budget_config.get('fiscal_year_start', 'January')
            if fiscal_start == 'January':
                start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                # Handle other fiscal year starts if needed
                start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return 0.0
        
        total_cost = 0.0
        hourly_stats = self.db.get('hourly_statistics', {})
        
        for date_str, hours in hourly_stats.items():
            try:
                session_date = datetime.strptime(date_str, "%Y-%m-%d")
                if session_date >= start_date and session_date <= now:
                    for hour_data in hours.values():
                        total_cost += hour_data.get('cost', 0.0)
            except ValueError:
                continue
        
        return total_cost
    
    def get_model_spending(self, model: str, period: str = 'daily') -> float:
        """Get spending for specific model in time period"""
        now = datetime.now()
        
        if period == 'daily':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'monthly':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start_date = now - timedelta(days=7)
        
        total_cost = 0.0
        hourly_stats = self.db.get('hourly_statistics', {})
        
        for date_str, hours in hourly_stats.items():
            try:
                session_date = datetime.strptime(date_str, "%Y-%m-%d")
                if session_date >= start_date and session_date <= now:
                    for hour_data in hours.values():
                        if hour_data.get('primary_model', '').startswith(model):
                            total_cost += hour_data.get('cost', 0.0)
            except ValueError:
                continue
        
        return total_cost
    
    def check_budget_status(self) -> Dict:
        """Check current budget status and generate alerts"""
        status = {
            'periods': {},
            'models': {},
            'projects': {},
            'alerts': []
        }
        
        # Check period budgets
        for period, config in self.budget_config['budgets'].items():
            if not config['enabled']:
                continue
                
            spent = self.get_period_spending(period)
            limit = config['limit']
            percentage = (spent / limit) * 100 if limit > 0 else 0
            
            status['periods'][period] = {
                'spent': spent,
                'limit': limit,
                'remaining': limit - spent,
                'percentage': percentage
            }
            
            # Generate alerts
            warning_threshold = self.budget_config['alerts']['warning_threshold']
            critical_threshold = self.budget_config['alerts']['critical_threshold']
            
            if percentage >= critical_threshold * 100:
                status['alerts'].append({
                    'type': 'critical',
                    'message': f"🚨 CRITICAL: {period} budget {percentage:.1f}% used (${spent:.2f}/${limit:.2f})"
                })
            elif percentage >= warning_threshold * 100:
                status['alerts'].append({
                    'type': 'warning', 
                    'message': f"⚠️ WARNING: {period} budget {percentage:.1f}% used (${spent:.2f}/${limit:.2f})"
                })
        
        # Check model limits
        for model, limits in self.budget_config['model_limits'].items():
            if not limits['enabled']:
                continue
                
            daily_spent = self.get_model_spending(model, 'daily')
            monthly_spent = self.get_model_spending(model, 'monthly')
            
            daily_limit = limits['daily_limit']
            monthly_limit = limits['monthly_limit']
            
            status['models'][model] = {
                'daily': {
                    'spent': daily_spent,
                    'limit': daily_limit,
                    'percentage': (daily_spent / daily_limit) * 100 if daily_limit > 0 else 0
                },
                'monthly': {
                    'spent': monthly_spent,
                    'limit': monthly_limit,
                    'percentage': (monthly_spent / monthly_limit) * 100 if monthly_limit > 0 else 0
                }
            }
        
        return status
    
    def display_budget_dashboard(self):
        """Display comprehensive budget dashboard"""
        print("\n" + "="*80)
        print_colored("💰 BUDGET DASHBOARD", "cyan", bold=True)
        print("="*80)
        
        status = self.check_budget_status()
        
        # Display alerts first
        if status['alerts']:
            print_colored("\n🚨 BUDGET ALERTS:", "red", bold=True)
            for alert in status['alerts']:
                color = "red" if alert['type'] == 'critical' else "yellow"
                print_colored(f"  {alert['message']}", color)
        
        # Period budgets
        print_colored("\n📅 PERIOD BUDGETS:", "blue", bold=True)
        for period, data in status['periods'].items():
            spent = data['spent']
            limit = data['limit']
            remaining = data['remaining']
            percentage = data['percentage']
            
            # Progress bar
            bar_length = 40
            filled_length = int(bar_length * percentage / 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            
            # Color coding
            if percentage >= 95:
                color = "red"
            elif percentage >= 80:
                color = "yellow"
            else:
                color = "green"
            
            print(f"  {period.upper():>8}: ", end="")
            print_colored(f"[{bar}] {percentage:5.1f}%", color)
            print(f"           ${spent:8.2f} / ${limit:8.2f} (Remaining: ${remaining:8.2f})")
        
        # Model spending
        if status['models']:
            print_colored("\n🤖 MODEL LIMITS:", "blue", bold=True)
            for model, data in status['models'].items():
                daily = data['daily']
                monthly = data['monthly']
                
                print(f"  {model}:")
                print(f"    Daily:   ${daily['spent']:6.2f} / ${daily['limit']:6.2f} ({daily['percentage']:5.1f}%)")
                print(f"    Monthly: ${monthly['spent']:6.2f} / ${monthly['limit']:6.2f} ({monthly['percentage']:5.1f}%)")
        
        # Spending trends (last 7 days)
        print_colored("\n📊 SPENDING TRENDS (Last 7 days):", "blue", bold=True)
        daily_spending = []
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            day_cost = 0.0
            hourly_stats = self.db.get('hourly_statistics', {})
            if date_str in hourly_stats:
                for hour_data in hourly_stats[date_str].values():
                    day_cost += hour_data.get('cost', 0.0)
            
            daily_spending.append((date_str, day_cost))
            
            # Simple bar chart
            bar_length = int(day_cost * 2) if day_cost < 25 else 50
            bar = "█" * bar_length
            print(f"  {date.strftime('%a %m-%d')}: ${day_cost:6.2f} {bar}")
        
        # Budget recommendations
        print_colored("\n💡 BUDGET RECOMMENDATIONS:", "blue", bold=True)
        avg_daily = sum(spending for _, spending in daily_spending) / 7
        projected_monthly = avg_daily * 30
        
        print(f"  • Average daily spending: ${avg_daily:.2f}")
        print(f"  • Projected monthly cost: ${projected_monthly:.2f}")
        
        monthly_budget = self.budget_config['budgets']['monthly']['limit']
        if projected_monthly > monthly_budget:
            over = projected_monthly - monthly_budget
            print_colored(f"  ⚠️ Projected to exceed monthly budget by ${over:.2f}!", "red")
            print_colored(f"  📉 Recommended daily limit: ${monthly_budget/30:.2f}", "yellow")
        else:
            remaining = monthly_budget - projected_monthly
            print_colored(f"  ✅ Within budget! Monthly surplus: ${remaining:.2f}", "green")
    
    def export_budget_report(self, format: str = 'json', output_file: str = None) -> str:
        """Export budget report in various formats"""
        status = self.check_budget_status()
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'budget_config': self.budget_config,
            'current_status': status,
            'summary': {
                'total_alerts': len(status['alerts']),
                'critical_alerts': len([a for a in status['alerts'] if a['type'] == 'critical']),
                'warning_alerts': len([a for a in status['alerts'] if a['type'] == 'warning'])
            }
        }
        
        if not output_file:
            output_file = f"budget_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        output_path = self.data_dir / output_file
        
        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2)
        elif format == 'csv':
            # Simple CSV export for period budgets
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Period', 'Spent', 'Limit', 'Remaining', 'Percentage'])
                for period, data in status['periods'].items():
                    writer.writerow([
                        period, data['spent'], data['limit'], 
                        data['remaining'], f"{data['percentage']:.1f}%"
                    ])
        
        print_colored(f"✅ Budget report exported to: {output_path}", "green")
        return str(output_path)


def main():
    """CLI entry point for budget manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Statusline Budget Manager')
    subparsers = parser.add_subparsers(dest='command', help='Budget management commands')
    
    # Set budget command
    set_parser = subparsers.add_parser('set', help='Set budget limits')
    set_parser.add_argument('period', choices=['daily', 'weekly', 'monthly', 'yearly'])
    set_parser.add_argument('amount', type=float, help='Budget amount in USD')
    set_parser.add_argument('--disable', action='store_true', help='Disable this budget')
    
    # Set model limit command
    model_parser = subparsers.add_parser('model-limit', help='Set model spending limits')
    model_parser.add_argument('model', help='Model name (e.g., claude-3-5-sonnet)')
    model_parser.add_argument('daily_limit', type=float, help='Daily spending limit')
    model_parser.add_argument('--monthly', type=float, help='Monthly spending limit')
    
    # Set project budget command
    project_parser = subparsers.add_parser('project', help='Set project budget')
    project_parser.add_argument('name', help='Project name')
    project_parser.add_argument('budget', type=float, help='Project budget')
    project_parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    project_parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    
    # Dashboard command
    subparsers.add_parser('dashboard', help='Show budget dashboard')
    
    # Status command
    subparsers.add_parser('status', help='Show budget status')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export budget report')
    export_parser.add_argument('--format', choices=['json', 'csv'], default='json')
    export_parser.add_argument('--output', help='Output filename')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    budget_manager = BudgetManager()
    
    if args.command == 'set':
        budget_manager.set_budget_limit(args.period, args.amount, not args.disable)
    elif args.command == 'model-limit':
        budget_manager.set_model_limit(args.model, args.daily_limit, args.monthly)
    elif args.command == 'project':
        budget_manager.set_project_budget(args.name, args.budget, args.start, args.end)
    elif args.command == 'dashboard':
        budget_manager.display_budget_dashboard()
    elif args.command == 'status':
        status = budget_manager.check_budget_status()
        if status['alerts']:
            for alert in status['alerts']:
                print(alert['message'])
        else:
            print_colored("✅ All budgets within limits", "green")
    elif args.command == 'export':
        budget_manager.export_budget_report(args.format, args.output)


if __name__ == "__main__":
    main()