#!/usr/bin/env python3
"""
Daily Report Generator for Claude Statusline
Generates detailed daily usage reports with local timezone support
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any
from collections import defaultdict
# No locale needed for general use

from .data_directory_utils import resolve_data_directory
from .safe_file_operations import safe_json_read


class DailyReportGenerator:
    """Generate daily usage reports from smart_sessions_db.json"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.prices_file = Path(__file__).parent / "prices.json"
        
        # Load database
        self.db = safe_json_read(self.db_file) if self.db_file.exists() else {}
        self.prices = safe_json_read(self.prices_file) if self.prices_file.exists() else {}
    
    def get_local_timezone_offset(self):
        """Get local timezone offset in hours"""
        local_offset = datetime.now().astimezone().utcoffset()
        return int(local_offset.total_seconds() / 3600)
    
    def format_number(self, num):
        """Format number with thousand separators"""
        return f"{int(num):,}"
    
    def format_currency(self, amount):
        """Format currency with proper decimals"""
        return f"${amount:,.2f}"
    
    def generate_daily_report(self, date_str: str = None):
        """Generate report for a specific day (default: today)"""
        if not date_str:
            # Use local date
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        print(f"\n{'='*80}")
        print(f"📊 DAILY REPORT - {date_str}")
        print(f"{'='*80}\n")
        
        # Get hourly data for the day
        hourly_data = self.db.get('hourly_statistics', {}).get(date_str, {})
        
        if not hourly_data:
            print("❌ No data found for this date!\n")
            return
        
        # Calculate daily totals
        total_messages = 0
        total_tokens = 0
        total_cost = 0.0
        model_usage = defaultdict(lambda: {'messages': 0, 'tokens': 0, 'cost': 0.0})
        hourly_activity = []
        
        # Get local timezone offset
        tz_offset = self.get_local_timezone_offset()
        
        for hour in range(24):
            # Adjust hour for local timezone
            utc_hour = (hour - tz_offset) % 24
            hour_key = f"{utc_hour:02d}:00"
            hour_data = hourly_data.get(hour_key, {})
            
            if hour_data.get('messages', 0) > 0:
                messages = hour_data['messages']
                tokens = hour_data.get('total_tokens', 0)
                cost = hour_data.get('cost', 0.0)
                
                total_messages += messages
                total_tokens += tokens
                total_cost += cost
                
                # Track model usage
                for model, stats in hour_data.get('models', {}).items():
                    model_usage[model]['messages'] += stats.get('messages', 0)
                    model_usage[model]['tokens'] += stats.get('total_tokens', 0)
                    model_usage[model]['cost'] += stats.get('cost', 0.0)
                
                # Track hourly activity (in local time)
                hourly_activity.append({
                    'hour': f"{hour:02d}:00",
                    'messages': messages,
                    'tokens': tokens,
                    'cost': cost
                })
        
        # Print summary
        print("📈 SUMMARY")
        print("-" * 40)
        print(f"Total Messages  : {self.format_number(total_messages)}")
        print(f"Total Tokens    : {self.format_number(total_tokens)}")
        print(f"Total Cost      : {self.format_currency(total_cost)}")
        print()
        
        # Print model breakdown
        if model_usage:
            print("🤖 MODEL USAGE")
            print("-" * 40)
            print(f"{'Model':<25} {'Messages':>10} {'Tokens':>15} {'Cost':>12}")
            print("-" * 40)
            
            for model, stats in sorted(model_usage.items(), key=lambda x: x[1]['cost'], reverse=True):
                model_name = self._get_model_display_name(model)
                print(f"{model_name:<25} {stats['messages']:>10,} {stats['tokens']:>15,} {self.format_currency(stats['cost']):>12}")
            print()
        
        # Print hourly activity
        if hourly_activity:
            print("⏰ HOURLY ACTIVITY (Local Time)")
            print("-" * 40)
            print(f"{'Hour':<10} {'Messages':>10} {'Tokens':>15} {'Cost':>12}")
            print("-" * 40)
            
            for activity in hourly_activity:
                print(f"{activity['hour']:<10} {activity['messages']:>10,} {activity['tokens']:>15,} {self.format_currency(activity['cost']):>12}")
            print()
        
        # Calculate work sessions
        sessions = self._calculate_work_sessions(date_str)
        if sessions:
            print("💼 WORK SESSIONS (5 Hours)")
            print("-" * 40)
            print(f"{'Session':<15} {'Start':<12} {'End':<12} {'Messages':>8} {'Cost':>12}")
            print("-" * 40)
            
            for i, session in enumerate(sessions, 1):
                start = session['start'].strftime('%H:%M')
                end = session['end'].strftime('%H:%M')
                print(f"Session #{i:<8} {start:<12} {end:<12} {session['messages']:>8,} {self.format_currency(session['cost']):>12}")
    
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
    
    def _calculate_work_sessions(self, date_str: str) -> List[Dict]:
        """Calculate 5-hour work sessions for a day"""
        sessions = []
        current_session_data = self.db.get('work_sessions', {}).get(date_str, [])
        
        for session in current_session_data:
            if isinstance(session, dict):
                try:
                    start = datetime.fromisoformat(session['session_start'].replace('Z', '+00:00'))
                    end = datetime.fromisoformat(session['session_end'].replace('Z', '+00:00'))
                    
                    # Convert to local timezone
                    start = start.astimezone()
                    end = end.astimezone()
                    
                    sessions.append({
                        'start': start,
                        'end': end,
                        'messages': session.get('message_count', 0),
                        'cost': session.get('cost', 0.0)
                    })
                except:
                    pass
        
        return sessions
    
    def generate_date_range_report(self, days: int = 7):
        """Generate report for last N days"""
        print(f"\n{'='*80}")
        print(f"📊 LAST {days} DAYS SUMMARY")
        print(f"{'='*80}\n")
        
        end_date = datetime.now()
        daily_stats = []
        
        for i in range(days):
            date = end_date - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            hourly_data = self.db.get('hourly_statistics', {}).get(date_str, {})
            
            if hourly_data:
                day_total = {'messages': 0, 'tokens': 0, 'cost': 0.0}
                
                for hour_data in hourly_data.values():
                    if hour_data.get('messages', 0) > 0:
                        day_total['messages'] += hour_data['messages']
                        day_total['tokens'] += hour_data.get('total_tokens', 0)
                        day_total['cost'] += hour_data.get('cost', 0.0)
                
                if day_total['messages'] > 0:
                    daily_stats.append({
                        'date': date_str,
                        'weekday': date.strftime('%A')[:3],
                        **day_total
                    })
        
        if daily_stats:
            print(f"{'Date':<12} {'Day':<5} {'Messages':>10} {'Tokens':>15} {'Cost':>12}")
            print("-" * 60)
            
            total = {'messages': 0, 'tokens': 0, 'cost': 0.0}
            
            for stat in reversed(daily_stats):
                print(f"{stat['date']:<12} {stat['weekday']:<5} {stat['messages']:>10,} {stat['tokens']:>15,} {self.format_currency(stat['cost']):>12}")
                total['messages'] += stat['messages']
                total['tokens'] += stat['tokens']
                total['cost'] += stat['cost']
            
            print("-" * 60)
            print(f"{'TOTAL':<17} {total['messages']:>10,} {total['tokens']:>15,} {self.format_currency(total['cost']):>12}")
            print()
            
            # Calculate averages
            avg_messages = total['messages'] / len(daily_stats)
            avg_tokens = total['tokens'] / len(daily_stats)
            avg_cost = total['cost'] / len(daily_stats)
            
            print(f"📊 Daily Average: {avg_messages:.0f} messages, {self.format_number(avg_tokens)} tokens, {self.format_currency(avg_cost)}")
        else:
            print(f"❌ No data found for the last {days} days!")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate daily Claude usage reports')
    parser.add_argument('--date', help='Specific date (YYYY-MM-DD)', default=None)
    parser.add_argument('--days', type=int, help='Last N days summary', default=0)
    
    args = parser.parse_args()
    
    generator = DailyReportGenerator()
    
    if args.days > 0:
        generator.generate_date_range_report(args.days)
    else:
        generator.generate_daily_report(args.date)


if __name__ == "__main__":
    main()