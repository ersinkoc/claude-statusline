#!/usr/bin/env python3
"""
Summary Report Generator for Claude Statusline
Generates comprehensive weekly/monthly/all-time summaries
"""

import json
import sys
import io

from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import statistics

from .data_directory_utils import resolve_data_directory
from .safe_file_operations import safe_json_read


class SummaryReportGenerator:
    """Generate comprehensive summary reports"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.prices_file = Path(__file__).parent / "prices.json"
        
        self.db = safe_json_read(self.db_file) if self.db_file.exists() else {}
        self.prices = safe_json_read(self.prices_file) if self.prices_file.exists() else {}
    
    def generate_all_time_summary(self):
        """Generate all-time usage summary"""
        print("\n" + "="*80)
        print("🌟 ALL-TIME USAGE SUMMARY")
        print("="*80 + "\n")
        
        # Get build info
        build_info = self.db.get('build_info', {})
        
        print("📊 DATABASE STATISTICS")
        print("-" * 40)
        print(f"Total Files Processed    : {build_info.get('total_files_processed', 0):,}")
        print(f"Total Messages           : {build_info.get('total_messages_in_tracking', 0):,}")
        print(f"Active Days              : {build_info.get('total_active_days', 0)}")
        print(f"Total Active Hours       : {build_info.get('total_active_hours', 0):,}")
        print(f"Work Sessions Created    : {build_info.get('smart_work_sessions_created', 0)}")
        print(f"Last Updated             : {build_info.get('last_updated', 'Unknown')}")
        print()
        
        # Calculate totals from hourly statistics
        hourly_stats = self.db.get('hourly_statistics', {})
        
        total_messages = 0
        total_tokens = 0
        total_cost = 0.0
        model_totals = defaultdict(lambda: {'messages': 0, 'tokens': 0, 'cost': 0.0})
        dates_with_activity = set()
        
        for date_str, hours in hourly_stats.items():
            daily_messages = 0
            
            for hour_data in hours.values():
                messages = hour_data.get('messages', 0)
                
                if messages > 0:
                    total_messages += messages
                    total_tokens += hour_data.get('total_tokens', 0)
                    total_cost += hour_data.get('cost', 0.0)
                    daily_messages += messages
                    
                    models = hour_data.get('models', {})
                    if isinstance(models, dict):
                        for model, stats in models.items():
                            model_totals[model]['messages'] += stats.get('messages', 0)
                            model_totals[model]['tokens'] += stats.get('total_tokens', 0)
                            model_totals[model]['cost'] += stats.get('cost', 0.0)
            
            if daily_messages > 0:
                dates_with_activity.add(date_str)
        
        # Print grand totals
        print("💰 GRAND TOTALS")
        print("-" * 40)
        print(f"Total Messages  : {total_messages:,}")
        print(f"Total Tokens    : {total_tokens:,}")
        print(f"Total Cost      : ${total_cost:,.2f}")
        print(f"Active Days     : {len(dates_with_activity)}")
        
        if dates_with_activity:
            avg_daily_messages = total_messages / len(dates_with_activity)
            avg_daily_cost = total_cost / len(dates_with_activity)
            print(f"Daily Average   : {avg_daily_messages:.0f} messages, ${avg_daily_cost:.2f}")
        print()
        
        # Model breakdown
        if model_totals:
            print("🤖 MODEL BREAKDOWN")
            print("-" * 40)
            print(f"{'Model':<20} {'Messages':>10} {'Tokens':>15} {'Cost':>12} {'% of Cost':>10}")
            print("-" * 40)
            
            for model, stats in sorted(model_totals.items(), key=lambda x: x[1]['cost'], reverse=True):
                model_name = self._get_model_display_name(model)[:20]
                pct = (stats['cost'] / total_cost * 100) if total_cost > 0 else 0
                print(f"{model_name:<20} {stats['messages']:>10,} {stats['tokens']:>15,} ${stats['cost']:>11,.2f} {pct:>9.1f}%")
        
        # Date range
        if dates_with_activity:
            sorted_dates = sorted(dates_with_activity)
            first_date = sorted_dates[0]
            last_date = sorted_dates[-1]
            
            print("\n📅 TIME PERIOD")
            print("-" * 40)
            print(f"First Activity  : {first_date}")
            print(f"Last Activity   : {last_date}")
            
            # Calculate span
            try:
                first = datetime.fromisoformat(first_date + "T00:00:00")
                last = datetime.fromisoformat(last_date + "T00:00:00")
                span = (last - first).days + 1
                print(f"Time Span       : {span} days")
            except:
                pass
    
    def generate_weekly_summary(self, weeks: int = 4):
        """Generate weekly summaries"""
        print("\n" + "="*80)
        print(f"📅 WEEKLY SUMMARIES (Last {weeks} Weeks)")
        print("="*80 + "\n")
        
        # Calculate week boundaries
        today = datetime.now()
        current_week_start = today - timedelta(days=today.weekday())
        
        weekly_stats = []
        
        for week_num in range(weeks):
            week_start = current_week_start - timedelta(weeks=week_num)
            week_end = week_start + timedelta(days=6)
            
            week_data = {
                'start': week_start,
                'end': week_end,
                'messages': 0,
                'tokens': 0,
                'cost': 0.0,
                'active_days': 0,
                'models': defaultdict(int)
            }
            
            # Collect data for this week
            for day_offset in range(7):
                date = week_start + timedelta(days=day_offset)
                date_str = date.strftime("%Y-%m-%d")
                
                hourly_data = self.db.get('hourly_statistics', {}).get(date_str, {})
                daily_messages = 0
                
                for hour_data in hourly_data.values():
                    messages = hour_data.get('messages', 0)
                    
                    if messages > 0:
                        week_data['messages'] += messages
                        week_data['tokens'] += hour_data.get('total_tokens', 0)
                        week_data['cost'] += hour_data.get('cost', 0.0)
                        daily_messages += messages
                        
                        for model in hour_data.get('models', {}):
                            week_data['models'][model] += 1
                
                if daily_messages > 0:
                    week_data['active_days'] += 1
            
            if week_data['messages'] > 0:
                weekly_stats.append(week_data)
        
        if not weekly_stats:
            print("❌ No weekly data found!")
            return
        
        # Print weekly summaries
        for i, week in enumerate(reversed(weekly_stats)):
            week_label = "This Week" if i == len(weekly_stats) - 1 else f"{len(weekly_stats) - i - 1} Weeks Ago"
            
            print(f"📊 {week_label}: {week['start'].strftime('%Y-%m-%d')} to {week['end'].strftime('%Y-%m-%d')}")
            print("-" * 40)
            print(f"Messages     : {week['messages']:,}")
            print(f"Tokens       : {week['tokens']:,}")
            print(f"Cost         : ${week['cost']:,.2f}")
            print(f"Active Days  : {week['active_days']}/7")
            
            if week['active_days'] > 0:
                daily_avg = week['messages'] / week['active_days']
                print(f"Daily Average: {daily_avg:.0f} messages")
            
            if week['models']:
                primary_model = max(week['models'].items(), key=lambda x: x[1])[0]
                print(f"Primary Model: {self._get_model_display_name(primary_model)}")
            print()
        
        # Week-over-week comparison
        if len(weekly_stats) >= 2:
            self._print_week_comparison(weekly_stats)
    
    def generate_monthly_summary(self, months: int = 3):
        """Generate monthly summaries"""
        print("\n" + "="*80)
        print(f"📆 MONTHLY SUMMARIES (Last {months} Months)")
        print("="*80 + "\n")
        
        monthly_stats = []
        today = datetime.now()
        
        for month_offset in range(months):
            # Calculate month boundaries
            if month_offset == 0:
                month = today.month
                year = today.year
            else:
                month = today.month - month_offset
                year = today.year
                
                while month <= 0:
                    month += 12
                    year -= 1
            
            month_data = {
                'month': month,
                'year': year,
                'messages': 0,
                'tokens': 0,
                'cost': 0.0,
                'active_days': 0,
                'sessions': 0
            }
            
            # Collect data for this month
            hourly_stats = self.db.get('hourly_statistics', {})
            
            for date_str, hours in hourly_stats.items():
                try:
                    date = datetime.fromisoformat(date_str + "T00:00:00")
                    
                    if date.year == year and date.month == month:
                        daily_messages = 0
                        
                        for hour_data in hours.values():
                            messages = hour_data.get('messages', 0)
                            
                            if messages > 0:
                                month_data['messages'] += messages
                                month_data['tokens'] += hour_data.get('total_tokens', 0)
                                month_data['cost'] += hour_data.get('cost', 0.0)
                                daily_messages += messages
                        
                        if daily_messages > 0:
                            month_data['active_days'] += 1
                except:
                    pass
            
            # Count sessions
            work_sessions = self.db.get('work_sessions', {})
            for date_str, sessions in work_sessions.items():
                try:
                    date = datetime.fromisoformat(date_str + "T00:00:00")
                    if date.year == year and date.month == month:
                        month_data['sessions'] += len(sessions)
                except:
                    pass
            
            if month_data['messages'] > 0:
                monthly_stats.append(month_data)
        
        if not monthly_stats:
            print("❌ No monthly data found!")
            return
        
        # Print monthly summaries
        for month_data in reversed(monthly_stats):
            month_name = datetime(month_data['year'], month_data['month'], 1).strftime('%B %Y')
            
            print(f"📊 {month_name}")
            print("-" * 40)
            print(f"Messages       : {month_data['messages']:,}")
            print(f"Tokens         : {month_data['tokens']:,}")
            print(f"Cost           : ${month_data['cost']:,.2f}")
            print(f"Active Days    : {month_data['active_days']}")
            print(f"Work Sessions  : {month_data['sessions']}")
            
            if month_data['active_days'] > 0:
                daily_avg = month_data['messages'] / month_data['active_days']
                daily_cost_avg = month_data['cost'] / month_data['active_days']
                print(f"Daily Average  : {daily_avg:.0f} messages, ${daily_cost_avg:.2f}")
            print()
        
        # Month-over-month comparison
        if len(monthly_stats) >= 2:
            self._print_month_comparison(monthly_stats)
    
    def _print_week_comparison(self, weekly_stats):
        """Print week-over-week comparison"""
        print("📈 WEEK-OVER-WEEK COMPARISON")
        print("-" * 40)
        
        for i in range(len(weekly_stats) - 1):
            prev_week = weekly_stats[i]
            curr_week = weekly_stats[i + 1]
            
            msg_change = curr_week['messages'] - prev_week['messages']
            cost_change = curr_week['cost'] - prev_week['cost']
            
            msg_pct = (msg_change / prev_week['messages'] * 100) if prev_week['messages'] > 0 else 0
            cost_pct = (cost_change / prev_week['cost'] * 100) if prev_week['cost'] > 0 else 0
            
            week_label = f"Week {len(weekly_stats) - i - 1} → Week {len(weekly_stats) - i}"
            
            print(f"{week_label}:")
            print(f"  Messages: {'+' if msg_change >= 0 else ''}{msg_change:,} ({'+' if msg_pct >= 0 else ''}{msg_pct:.1f}%)")
            print(f"  Cost: {'+' if cost_change >= 0 else ''}${cost_change:.2f} ({'+' if cost_pct >= 0 else ''}{cost_pct:.1f}%)")
        print()
    
    def _print_month_comparison(self, monthly_stats):
        """Print month-over-month comparison"""
        print("📈 MONTH-OVER-MONTH COMPARISON")
        print("-" * 40)
        
        for i in range(len(monthly_stats) - 1):
            prev_month = monthly_stats[i]
            curr_month = monthly_stats[i + 1]
            
            msg_change = curr_month['messages'] - prev_month['messages']
            cost_change = curr_month['cost'] - prev_month['cost']
            
            msg_pct = (msg_change / prev_month['messages'] * 100) if prev_month['messages'] > 0 else 0
            cost_pct = (cost_change / prev_month['cost'] * 100) if prev_month['cost'] > 0 else 0
            
            prev_name = datetime(prev_month['year'], prev_month['month'], 1).strftime('%B')
            curr_name = datetime(curr_month['year'], curr_month['month'], 1).strftime('%B')
            
            print(f"{prev_name} → {curr_name}:")
            print(f"  Messages: {'+' if msg_change >= 0 else ''}{msg_change:,} ({'+' if msg_pct >= 0 else ''}{msg_pct:.1f}%)")
            print(f"  Cost: {'+' if cost_change >= 0 else ''}${cost_change:.2f} ({'+' if cost_pct >= 0 else ''}{cost_pct:.1f}%)")
        print()
    
    def _get_model_display_name(self, model: str) -> str:
        """Get display name for model"""
        if 'opus' in model.lower():
            return '🧠 Opus'
        elif 'sonnet' in model.lower():
            return '🎭 Sonnet'
        elif 'haiku' in model.lower():
            return '⚡ Haiku'
        else:
            return model[:20]


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate summary reports')
    parser.add_argument('--weekly', type=int, help='Show last N weeks', default=0)
    parser.add_argument('--monthly', type=int, help='Show last N months', default=0)
    parser.add_argument('--all', action='store_true', help='Show all-time summary')
    
    args = parser.parse_args()
    
    generator = SummaryReportGenerator()
    
    if args.weekly > 0:
        generator.generate_weekly_summary(args.weekly)
    elif args.monthly > 0:
        generator.generate_monthly_summary(args.monthly)
    elif args.all:
        generator.generate_all_time_summary()
    else:
        # Default: show all-time summary
        generator.generate_all_time_summary()


if __name__ == "__main__":
    main()