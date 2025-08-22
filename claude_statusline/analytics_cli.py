#!/usr/bin/env python3
"""
Analytics CLI for Claude Statusline
Advanced analytics and reporting features
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_directory_utils import resolve_data_directory
from safe_file_operations import safe_json_read


class AnalyticsCLI:
    """Analytics CLI interface"""
    
    def __init__(self):
        self.data_dir = resolve_data_directory()
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.db_data = None
        
    def load_data(self):
        """Load database"""
        if not self.db_file.exists():
            print("No database found. Run 'claude-statusline rebuild' first.")
            return False
            
        self.db_data = safe_json_read(self.db_file)
        if not self.db_data:
            print("Invalid database format")
            return False
            
        # Check for either sessions or work_sessions
        if "sessions" not in self.db_data and "work_sessions" not in self.db_data:
            print("No session data found")
            return False
            
        return True
        
    def run(self):
        """Run analytics CLI"""
        if not self.load_data():
            return
            
        print("\n" + "="*60)
        print("CLAUDE STATUSLINE ANALYTICS")
        print("="*60)
        
        # Handle different database formats
        sessions = []
        
        # Try sessions key first (list format)
        if "sessions" in self.db_data and isinstance(self.db_data["sessions"], list):
            sessions = self.db_data["sessions"]
        # Try work_sessions (dict format with daily lists)
        elif "work_sessions" in self.db_data and isinstance(self.db_data["work_sessions"], dict):
            # Flatten all daily sessions into one list
            for day, day_sessions in self.db_data["work_sessions"].items():
                if isinstance(day_sessions, list):
                    sessions.extend(day_sessions)
        
        if not sessions:
            print("No sessions found")
            return
            
        # Calculate metrics
        total_sessions = len(sessions)
        total_messages = sum(s.get("message_count", 0) for s in sessions)
        # Handle different token field names
        total_tokens = sum(s.get("total_tokens", s.get("tokens", 0)) for s in sessions)
        # Handle different cost field names
        total_cost = sum(s.get("total_cost", s.get("cost", 0.0)) for s in sessions)
        
        print(f"\nOVERALL STATISTICS")
        print(f"  Sessions: {total_sessions}")
        print(f"  Messages: {total_messages:,}")
        print(f"  Tokens: {total_tokens:,}")
        print(f"  Total Cost: ${total_cost:.2f}")
        
        # Model breakdown
        print(f"\nMODEL USAGE")
        model_stats = defaultdict(lambda: {"count": 0, "cost": 0.0})
        
        for session in sessions:
            model = session.get("primary_model", "unknown")
            model_stats[model]["count"] += session.get("message_count", 0)
            model_stats[model]["cost"] += session.get("total_cost", session.get("cost", 0.0))
            
        for model, stats in sorted(model_stats.items(), key=lambda x: x[1]["cost"], reverse=True)[:5]:
            model_short = model.split("-")[2] if "-" in model and len(model.split("-")) > 2 else model
            print(f"  {model_short:20} {stats['count']:6} msgs  ${stats['cost']:8.2f}")
            
        # Daily breakdown (last 7 days)
        print(f"\nLAST 7 DAYS")
        daily_stats = defaultdict(lambda: {"messages": 0, "cost": 0.0})
        
        now = datetime.now()
        for session in sessions:
            try:
                # Handle different time field names
                time_field = session.get("start_time", session.get("session_start", ""))
                if not time_field:
                    continue
                start_time = datetime.fromisoformat(time_field.replace("Z", "+00:00"))
                start_time = start_time.replace(tzinfo=None)
                
                # Skip old sessions
                if (now - start_time).days > 7:
                    continue
                    
                day = start_time.strftime("%Y-%m-%d")
                daily_stats[day]["messages"] += session.get("message_count", 0)
                daily_stats[day]["cost"] += session.get("total_cost", 0.0)
            except:
                continue
                
        for day in sorted(daily_stats.keys())[-7:]:
            stats = daily_stats[day]
            print(f"  {day}: {stats['messages']:4} msgs  ${stats['cost']:7.2f}")
            
        # Current month
        print(f"\nCURRENT MONTH")
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_messages = 0
        month_cost = 0.0
        
        for session in sessions:
            try:
                # Handle different time field names
                time_field = session.get("start_time", session.get("session_start", ""))
                if not time_field:
                    continue
                start_time = datetime.fromisoformat(time_field.replace("Z", "+00:00"))
                start_time = start_time.replace(tzinfo=None)
                
                if start_time >= month_start:
                    month_messages += session.get("message_count", 0)
                    month_cost += session.get("total_cost", 0.0)
            except:
                continue
                
        print(f"  Messages: {month_messages:,}")
        print(f"  Cost: ${month_cost:.2f}")
        
        # Active session
        print(f"\nACTIVE SESSION")
        active_session = None
        
        for session in reversed(sessions):
            try:
                # Handle different end time field names
                end_field = session.get("end_time", session.get("session_end", ""))
                if end_field:
                    end_time = datetime.fromisoformat(end_field.replace("Z", "+00:00"))
                    end_time = end_time.replace(tzinfo=None)
                    
                    if (now - end_time).total_seconds() < 5 * 3600:  # 5 hours
                        active_session = session
                        break
            except:
                continue
                
        if active_session:
            model = active_session.get("primary_model", "unknown")
            if "-" in model and len(model.split("-")) > 2:
                model = model.split("-")[2]
            messages = active_session.get("message_count", 0)
            cost = active_session.get("total_cost", active_session.get("cost", 0.0))
            
            print(f"  Model: {model}")
            print(f"  Messages: {messages}")
            print(f"  Cost: ${cost:.2f}")
        else:
            print("  No active session")
            
        print("\n" + "="*60)


def main():
    """Main entry point"""
    analytics = AnalyticsCLI()
    analytics.run()


if __name__ == "__main__":
    main()