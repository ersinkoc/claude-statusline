#!/usr/bin/env python3
"""
Session Analyzer for Claude Statusline
Analyzes all work sessions and provides detailed insights
"""

import json
import sys
import io

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Tuple
from collections import defaultdict

from data_directory_utils import resolve_data_directory
from safe_file_operations import safe_json_read


class SessionAnalyzer:
    """Analyze Claude work sessions from smart_sessions_db.json"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.db = safe_json_read(self.db_file) if self.db_file.exists() else {}
        
    def analyze_all_sessions(self):
        """Analyze all work sessions"""
        print("\n" + "="*80)
        print("🔍 ALL WORK SESSIONS ANALYSIS")
        print("="*80 + "\n")
        
        work_sessions = self.db.get('work_sessions', {})
        
        if not work_sessions:
            print("❌ No work sessions found!")
            return
        
        all_sessions = []
        
        # Collect all sessions
        for date_str, sessions in work_sessions.items():
            for session in sessions:
                if isinstance(session, dict) and session.get('message_count', 0) > 0:
                    try:
                        session_copy = session.copy()
                        session_copy['date'] = date_str
                        all_sessions.append(session_copy)
                    except:
                        pass
        
        if not all_sessions:
            print("❌ No valid session data found!")
            return
        
        # Sort by session start time
        all_sessions.sort(key=lambda x: x.get('session_start', ''))
        
        # Calculate statistics
        total_sessions = len(all_sessions)
        total_messages = sum(s.get('message_count', 0) for s in all_sessions)
        total_tokens = sum(s.get('tokens', 0) for s in all_sessions)
        
        # Calculate total cost from hourly_statistics for accuracy
        hourly_stats = self.db.get('hourly_statistics', {})
        total_cost = 0
        for date_hours in hourly_stats.values():
            for hour_data in date_hours.values():
                total_cost += hour_data.get('cost', 0.0)
        
        # Model distribution - calculate from hourly_statistics for accuracy
        model_stats = defaultdict(lambda: {'count': 0, 'messages': 0, 'tokens': 0, 'cost': 0.0})
        
        # Calculate from hourly data
        for date_hours in hourly_stats.values():
            for hour_data in date_hours.values():
                models = hour_data.get('models', {})
                if isinstance(models, dict):
                    for model, mdata in models.items():
                        model_stats[model]['messages'] += mdata.get('messages', 0)
                        model_stats[model]['tokens'] += mdata.get('total_tokens', 0)
                        model_stats[model]['cost'] += mdata.get('cost', 0.0)
        
        # Count sessions by primary model
        for session in all_sessions:
            primary_model = session.get('primary_model', 'unknown')
            model_stats[primary_model]['count'] += 1
        
        # Time analysis
        session_durations = []
        incomplete_sessions = 0
        
        for session in all_sessions:
            
            # Duration analysis
            try:
                start = datetime.fromisoformat(session['session_start'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(session['session_end'].replace('Z', '+00:00'))
                duration = (end - start).total_seconds() / 3600
                
                if duration >= 4.5:  # Nearly complete sessions (4.5+ hours)
                    session_durations.append(duration)
                else:
                    incomplete_sessions += 1
            except:
                pass
        
        # Print overall statistics
        print("📊 OVERALL STATISTICS")
        print("-" * 40)
        print(f"Total Sessions  : {total_sessions}")
        print(f"Total Messages  : {total_messages:,}")
        print(f"Total Tokens    : {total_tokens:,}")
        print(f"Total Cost      : ${total_cost:,.2f}")
        print()
        
        if total_sessions > 0:
            avg_messages = total_messages / total_sessions
            avg_tokens = total_tokens / total_sessions
            avg_cost = total_cost / total_sessions
            
            print(f"Average per Session:")
            print(f"  Messages: {avg_messages:,.0f}")
            print(f"  Tokens  : {avg_tokens:,.0f}")
            print(f"  Cost    : ${avg_cost:,.2f}")
            print()
        
        # Print model distribution
        print("🤖 MODEL DISTRIBUTION")
        print("-" * 40)
        print(f"{'Model':<20} {'Sessions':>8} {'Messages':>10} {'Tokens':>15} {'Cost':>12}")
        print("-" * 40)
        
        for model, stats in sorted(model_stats.items(), key=lambda x: x[1]['cost'], reverse=True):
            model_name = self._get_model_display_name(model)
            print(f"{model_name:<20} {stats['count']:>8} {stats['messages']:>10,} {stats['tokens']:>15,} ${stats['cost']:>11,.2f}")
        print()
        
        # Session completion analysis
        if session_durations:
            avg_duration = sum(session_durations) / len(session_durations)
            print("⏱️ SESSION DURATIONS")
            print("-" * 40)
            print(f"Complete Sessions  : {len(session_durations)}")
            print(f"Incomplete Sessions: {incomplete_sessions}")
            print(f"Average Duration   : {avg_duration:.1f} hours")
            print()
        
        # Show recent sessions
        print("📅 RECENT 10 SESSIONS")
        print("-" * 40)
        print(f"{'Date':<12} {'Start':<8} {'Model':<15} {'Messages':>8} {'Cost':>10}")
        print("-" * 40)
        
        for session in all_sessions[-10:]:
            date = session.get('date', '?')
            try:
                start_time = datetime.fromisoformat(session['session_start'].replace('Z', '+00:00'))
                start_str = start_time.astimezone().strftime('%H:%M')
            except:
                start_str = '?'
            
            model = self._get_model_display_name(session.get('primary_model', 'unknown'))[:15]
            messages = session.get('message_count', 0)
            cost = session.get('cost', 0.0)
            
            print(f"{date:<12} {start_str:<8} {model:<15} {messages:>8,} ${cost:>9,.2f}")
    
    def analyze_session_patterns(self):
        """Analyze session patterns and habits"""
        print("\n" + "="*80)
        print("📈 WORK PATTERNS ANALYSIS")
        print("="*80 + "\n")
        
        work_sessions = self.db.get('work_sessions', {})
        
        # Time of day analysis
        hour_distribution = defaultdict(int)
        day_distribution = defaultdict(int)
        
        for date_str, sessions in work_sessions.items():
            try:
                date = datetime.fromisoformat(date_str + "T00:00:00+00:00")
                weekday = date.strftime('%A')
                day_distribution[weekday] += len(sessions)
            except:
                pass
            
            for session in sessions:
                if isinstance(session, dict):
                    try:
                        start = datetime.fromisoformat(session['session_start'].replace('Z', '+00:00'))
                        hour = start.astimezone().hour
                        hour_distribution[hour] += 1
                    except:
                        pass
        
        # Print day of week distribution
        print("📅 WEEKLY DISTRIBUTION")
        print("-" * 40)
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days_order:
            count = day_distribution.get(day, 0)
            if count > 0:
                bar = '█' * min(count * 2, 40)
                print(f"{day:<10} [{count:>3}] {bar}")
        print()
        
        # Print hour distribution
        print("⏰ HOURLY DISTRIBUTION")
        print("-" * 40)
        
        for hour in range(24):
            count = hour_distribution.get(hour, 0)
            if count > 0:
                bar = '█' * min(count, 30)
                print(f"{hour:02d}:00 [{count:>3}] {bar}")
        print()
        
        # Most productive times
        if hour_distribution:
            most_productive_hour = max(hour_distribution.items(), key=lambda x: x[1])
            print(f"🎯 Most Active Hour: {most_productive_hour[0]:02d}:00 ({most_productive_hour[1]} sessions)")
        
        if day_distribution:
            most_productive_day = max(day_distribution.items(), key=lambda x: x[1])
            print(f"🎯 Most Active Day : {most_productive_day[0]} ({most_productive_day[1]} sessions)")
    
    def find_longest_sessions(self, top_n: int = 5):
        """Find longest/most productive sessions"""
        print("\n" + "="*80)
        print(f"🏆 TOP {top_n} PRODUCTIVE SESSIONS")
        print("="*80 + "\n")
        
        work_sessions = self.db.get('work_sessions', {})
        all_sessions = []
        
        for date_str, sessions in work_sessions.items():
            for session in sessions:
                if isinstance(session, dict) and session.get('message_count', 0) > 0:
                    session_copy = session.copy()
                    session_copy['date'] = date_str
                    all_sessions.append(session_copy)
        
        # Sort by message count
        all_sessions.sort(key=lambda x: x.get('message_count', 0), reverse=True)
        
        print(f"{'Rank':<5} {'Date':<12} {'Time':<12} {'Model':<15} {'Messages':>8} {'Tokens':>12} {'Cost':>10}")
        print("-" * 80)
        
        for i, session in enumerate(all_sessions[:top_n], 1):
            date = session.get('date', '?')
            try:
                start = datetime.fromisoformat(session['session_start'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(session['session_end'].replace('Z', '+00:00'))
                start_str = start.astimezone().strftime('%H:%M')
                end_str = end.astimezone().strftime('%H:%M')
                time_range = f"{start_str}-{end_str}"
            except:
                time_range = "?"
            
            model = self._get_model_display_name(session.get('primary_model', 'unknown'))[:15]
            messages = session.get('message_count', 0)
            tokens = session.get('tokens', 0)
            cost = session.get('cost', 0.0)
            
            print(f"{i:<5} {date:<12} {time_range:<12} {model:<15} {messages:>8,} {tokens:>12,} ${cost:>9,.2f}")
    
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
    
    parser = argparse.ArgumentParser(description='Analyze Claude work sessions')
    parser.add_argument('--patterns', action='store_true', help='Show work patterns analysis')
    parser.add_argument('--top', type=int, help='Show top N productive sessions', default=0)
    
    args = parser.parse_args()
    
    analyzer = SessionAnalyzer()
    
    if args.patterns:
        analyzer.analyze_session_patterns()
    elif args.top > 0:
        analyzer.find_longest_sessions(args.top)
    else:
        analyzer.analyze_all_sessions()


if __name__ == "__main__":
    main()