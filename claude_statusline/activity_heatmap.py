#!/usr/bin/env python3
"""
Activity Heatmap Generator for Claude Statusline
Creates visual heatmaps of usage patterns
"""

import json
import sys
import io

from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

from .data_directory_utils import resolve_data_directory
from .safe_file_operations import safe_json_read


class ActivityHeatmapGenerator:
    """Generate activity heatmaps and time-based analysis"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.db = safe_json_read(self.db_file) if self.db_file.exists() else {}
    
    def generate_weekly_heatmap(self):
        """Generate weekly activity heatmap"""
        print("\n" + "="*80)
        print("🔥 WEEKLY ACTIVITY HEATMAP")
        print("="*80 + "\n")
        
        # Initialize 7x24 grid (days x hours)
        heatmap = defaultdict(lambda: defaultdict(int))
        
        hourly_stats = self.db.get('hourly_statistics', {})
        
        for date_str, hours in hourly_stats.items():
            try:
                date = datetime.fromisoformat(date_str + "T00:00:00")
                weekday = date.weekday()  # 0=Monday, 6=Sunday
                
                for hour_str, hour_data in hours.items():
                    hour = int(hour_str.split(':')[0])
                    messages = hour_data.get('messages', 0)
                    
                    if messages > 0:
                        # Convert UTC to local time
                        local_hour = (hour + self._get_timezone_offset()) % 24
                        heatmap[weekday][local_hour] += messages
            except:
                pass
        
        if not heatmap:
            print("❌ No activity data found!")
            return
        
        # Find max value for normalization
        max_messages = max(
            max(hours.values()) 
            for hours in heatmap.values()
        ) if heatmap else 0
        
        # Print heatmap
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        print("Hour  ", end="")
        for hour in range(24):
            print(f"{hour:02d} ", end="")
        print()
        print("-" * 80)
        
        for day_idx, day_name in enumerate(days):
            print(f"{day_name:<6}", end="")
            
            for hour in range(24):
                messages = heatmap[day_idx][hour]
                
                if messages == 0:
                    print("·  ", end="")
                else:
                    intensity = min(9, int((messages / max_messages) * 9)) if max_messages > 0 else 0
                    if intensity <= 2:
                        print("░  ", end="")
                    elif intensity <= 4:
                        print("▒  ", end="")
                    elif intensity <= 6:
                        print("▓  ", end="")
                    else:
                        print("█  ", end="")
            print()
        
        print("\nLegend: · = 0  ░ = Low  ▒ = Medium  ▓ = High  █ = Very High")
        
        # Print statistics
        self._print_heatmap_statistics(heatmap)
    
    def generate_monthly_calendar(self, month: int = None, year: int = None):
        """Generate monthly calendar view"""
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
        
        print("\n" + "="*80)
        print(f"📅 MONTHLY ACTIVITY CALENDAR - {year}/{month:02d}")
        print("="*80 + "\n")
        
        # Collect daily statistics
        daily_stats = {}
        hourly_stats = self.db.get('hourly_statistics', {})
        
        for date_str, hours in hourly_stats.items():
            try:
                date = datetime.fromisoformat(date_str + "T00:00:00")
                
                if date.year == year and date.month == month:
                    total_messages = sum(
                        hour_data.get('messages', 0) 
                        for hour_data in hours.values()
                    )
                    total_cost = sum(
                        hour_data.get('cost', 0.0) 
                        for hour_data in hours.values()
                    )
                    
                    daily_stats[date.day] = {
                        'messages': total_messages,
                        'cost': total_cost
                    }
            except:
                pass
        
        if not daily_stats:
            print("❌ No data for this month!")
            return
        
        # Print calendar
        import calendar
        cal = calendar.monthcalendar(year, month)
        
        print("  Mon    Tue    Wed    Thu    Fri    Sat    Sun")
        print("-" * 50)
        
        for week in cal:
            for day in week:
                if day == 0:
                    print("       ", end="")
                else:
                    if day in daily_stats:
                        messages = daily_stats[day]['messages']
                        if messages > 100:
                            marker = "███"
                        elif messages > 50:
                            marker = "▓▓▓"
                        elif messages > 0:
                            marker = "░░░"
                        else:
                            marker = "   "
                        print(f"{day:>2} {marker} ", end="")
                    else:
                        print(f"{day:>2}     ", end="")
            print()
        
        print("\n" + "-" * 50)
        
        # Print month summary
        total_messages = sum(s['messages'] for s in daily_stats.values())
        total_cost = sum(s['cost'] for s in daily_stats.values())
        active_days = len([s for s in daily_stats.values() if s['messages'] > 0])
        
        print(f"Active Days    : {active_days}")
        print(f"Total Messages : {total_messages:,}")
        print(f"Total Cost     : ${total_cost:,.2f}")
        
        if active_days > 0:
            print(f"Daily Average  : {total_messages // active_days:,} messages, ${total_cost / active_days:.2f}")
    
    def analyze_peak_hours(self):
        """Analyze and display peak activity hours"""
        print("\n" + "="*80)
        print("⏱️ PEAK HOURS ANALYSIS")
        print("="*80 + "\n")
        
        hourly_totals = defaultdict(lambda: {'messages': 0, 'cost': 0.0, 'days': set()})
        
        hourly_stats = self.db.get('hourly_statistics', {})
        
        for date_str, hours in hourly_stats.items():
            for hour_str, hour_data in hours.items():
                hour = int(hour_str.split(':')[0])
                messages = hour_data.get('messages', 0)
                
                if messages > 0:
                    # Convert to local time
                    local_hour = (hour + self._get_timezone_offset()) % 24
                    hourly_totals[local_hour]['messages'] += messages
                    hourly_totals[local_hour]['cost'] += hour_data.get('cost', 0.0)
                    hourly_totals[local_hour]['days'].add(date_str)
        
        if not hourly_totals:
            print("❌ No activity data found!")
            return
        
        # Sort by messages
        sorted_hours = sorted(
            hourly_totals.items(), 
            key=lambda x: x[1]['messages'], 
            reverse=True
        )
        
        # Print hourly distribution
        print("HOURLY ACTIVITY DISTRIBUTION (Local Time)")
        print("-" * 60)
        print(f"{'Hour':<8} {'Messages':>10} {'Cost':>10} {'Days Active':>12} {'Bar'}")
        print("-" * 60)
        
        max_messages = sorted_hours[0][1]['messages'] if sorted_hours else 0
        
        for hour in range(24):
            if hour in hourly_totals:
                stats = hourly_totals[hour]
                bar_length = int((stats['messages'] / max_messages) * 30) if max_messages > 0 else 0
                bar = '█' * bar_length
                
                print(f"{hour:02d}:00    {stats['messages']:>10,} ${stats['cost']:>9,.2f} {len(stats['days']):>12} {bar}")
        
        print("\n" + "-" * 60)
        
        # Identify patterns
        print("\n📊 INSIGHTS")
        print("-" * 40)
        
        # Peak hours
        peak_hours = sorted_hours[:3]
        print("Peak Activity Hours:")
        for hour, stats in peak_hours:
            print(f"  {hour:02d}:00 - {stats['messages']:,} messages")
        
        # Work pattern detection
        morning_activity = sum(
            hourly_totals[h]['messages'] 
            for h in range(6, 12) 
            if h in hourly_totals
        )
        afternoon_activity = sum(
            hourly_totals[h]['messages'] 
            for h in range(12, 18) 
            if h in hourly_totals
        )
        evening_activity = sum(
            hourly_totals[h]['messages'] 
            for h in range(18, 24) 
            if h in hourly_totals
        )
        night_activity = sum(
            hourly_totals[h]['messages'] 
            for h in range(0, 6) 
            if h in hourly_totals
        )
        
        total_activity = morning_activity + afternoon_activity + evening_activity + night_activity
        
        if total_activity > 0:
            print("\nWork Pattern Distribution:")
            print(f"  Morning   (06-12): {morning_activity:>6,} ({morning_activity/total_activity*100:.1f}%)")
            print(f"  Afternoon (12-18): {afternoon_activity:>6,} ({afternoon_activity/total_activity*100:.1f}%)")
            print(f"  Evening   (18-00): {evening_activity:>6,} ({evening_activity/total_activity*100:.1f}%)")
            print(f"  Night     (00-06): {night_activity:>6,} ({night_activity/total_activity*100:.1f}%)")
            
            # Determine work style
            if night_activity / total_activity > 0.3:
                print("\n🦉 Night Owl - Significant late-night activity")
            elif morning_activity / total_activity > 0.4:
                print("\n🌅 Early Bird - Most productive in mornings")
            elif afternoon_activity / total_activity > 0.4:
                print("\n☀️ Afternoon Peak - Most active after lunch")
            else:
                print("\n⚖️ Balanced - Activity spread throughout the day")
    
    def _print_heatmap_statistics(self, heatmap):
        """Print statistics from heatmap data"""
        print("\n" + "-" * 40)
        print("📊 HEATMAP STATISTICS")
        print("-" * 40)
        
        # Find most active day/hour combinations
        activities = []
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day_idx, hours in heatmap.items():
            for hour, messages in hours.items():
                if messages > 0:
                    activities.append({
                        'day': days[day_idx],
                        'hour': hour,
                        'messages': messages
                    })
        
        if activities:
            activities.sort(key=lambda x: x['messages'], reverse=True)
            
            print("Most Active Time Slots:")
            for activity in activities[:5]:
                print(f"  {activity['day']} {activity['hour']:02d}:00 - {activity['messages']:,} messages")
            
            # Calculate day totals
            day_totals = defaultdict(int)
            for day_idx, hours in heatmap.items():
                day_totals[days[day_idx]] = sum(hours.values())
            
            if day_totals:
                most_active_day = max(day_totals.items(), key=lambda x: x[1])
                print(f"\nMost Active Day: {most_active_day[0]} ({most_active_day[1]:,} messages)")
    
    def _get_timezone_offset(self):
        """Get local timezone offset from UTC"""
        import time
        if time.daylight:
            return -time.altzone // 3600
        else:
            return -time.timezone // 3600


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate activity heatmaps')
    parser.add_argument('--monthly', action='store_true', help='Show monthly calendar')
    parser.add_argument('--month', type=int, help='Month for calendar (1-12)')
    parser.add_argument('--year', type=int, help='Year for calendar')
    parser.add_argument('--peak', action='store_true', help='Show peak hours analysis')
    
    args = parser.parse_args()
    
    generator = ActivityHeatmapGenerator()
    
    if args.monthly:
        generator.generate_monthly_calendar(args.month, args.year)
    elif args.peak:
        generator.analyze_peak_hours()
    else:
        generator.generate_weekly_heatmap()


if __name__ == "__main__":
    main()