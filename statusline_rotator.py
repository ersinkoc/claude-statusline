#!/usr/bin/env python3
"""
Rotating Statusline Display System

Displays different information in rotation:
- Main status (model, time, messages, cost)
- Daily summary (today's total usage)
- Weekly summary
- Fun facts and tips
- System status
"""

import json
import time
import random
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

from data_directory_utils import resolve_data_directory
from safe_file_operations import safe_json_read
from console_utils import safe_print


class StatuslineRotator:
    """Handles rotating statusline content"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.rotation_file = self.data_dir / "rotation_state.json"
        
        # Rotation interval (seconds between changes)
        self.rotation_interval = 10
        
        # Load prices for cost calculation
        self.prices = self._load_prices()
        
        # Fun facts and tips
        self.tips = [
            "💡 Tip: Use session_analyzer.py for detailed breakdowns",
            "📊 Fact: Claude processes millions of tokens daily",
            "🎯 Pro tip: 5-hour sessions optimize for deep work",
            "🔥 Hot tip: Check activity_heatmap.py for usage patterns",
            "⚡ Speed tip: Daemon updates every 60 seconds",
            "🎨 Fun: Claude can help with creative writing too!",
            "📈 Track: Your most productive hours with analytics",
            "💰 Save: Monitor costs with cost_analyzer.py",
            "🚀 Boost: Use cache tokens to reduce costs",
            "🧠 Smart: Opus 4.1 is the most capable model"
        ]
    
    def _load_prices(self) -> Dict[str, Any]:
        """Load model prices"""
        try:
            prices_file = Path(__file__).parent / "prices.json"
            if prices_file.exists():
                with open(prices_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {"models": {}}
    
    def get_rotation_index(self) -> int:
        """Get current rotation index based on time"""
        # Simple time-based rotation - only 2 modes now
        current_minute = int(time.time() / self.rotation_interval)
        return current_minute % 2  # Only 2 display modes: main status and total summary
    
    def save_rotation_state(self, index: int):
        """Save current rotation state"""
        try:
            state = {
                "index": index,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            with open(self.rotation_file, 'w') as f:
                json.dump(state, f)
        except:
            pass
    
    def format_main_status(self, session_data: Dict[str, Any]) -> str:
        """Format main status line (default)"""
        model = session_data.get('model', 'Unknown')
        model_name = self._get_model_display_name(model)
        
        # Session timing
        remaining = session_data.get('remaining_seconds', 0)
        if remaining > 0:
            status = "LIVE"
            if remaining > 3600:
                time_str = f"ends {(datetime.now() + timedelta(seconds=remaining)).strftime('%H:%M')}"
            else:
                time_str = f"{remaining//60}m left"
        else:
            status = "EXPIRED"
            time_str = "session ended"
        
        # Stats
        messages = session_data.get('message_count', 0)
        
        # Get tokens - check if values exist
        input_tokens = session_data.get('input_tokens', 0) or 0
        output_tokens = session_data.get('output_tokens', 0) or 0
        tokens = input_tokens + output_tokens
        
        # If no tokens, get today's total from hourly_statistics
        if tokens == 0:
            db = safe_json_read(self.db_file)
            today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            today_stats = db.get('hourly_statistics', {}).get(today, {})
            for hour_data in today_stats.values():
                tokens += hour_data.get('input_tokens', 0) + hour_data.get('output_tokens', 0)
        
        # Get cost
        cost = session_data.get('total_cost', 0) or 0
        if cost == 0:
            # Get today's total cost from hourly_statistics
            db = safe_json_read(self.db_file)
            today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            today_stats = db.get('hourly_statistics', {}).get(today, {})
            for hour_data in today_stats.values():
                cost += hour_data.get('cost', 0)
        
        # Format tokens
        if tokens >= 1_000_000:
            token_str = f"{tokens/1_000_000:.1f}M"
        elif tokens >= 1_000:
            token_str = f"{tokens/1_000:.0f}k"
        else:
            token_str = f"{tokens}t"
        
        return f"[{model_name}] [{status}] [{time_str}] [{messages}msg] [{token_str}] [${cost:.2f}]"
    
    def format_total_summary(self) -> str:
        """Format total summary - all time stats"""
        try:
            db = safe_json_read(self.db_file)
            
            # Calculate all-time totals from BOTH sources
            total_sessions = 0
            total_messages = 0
            total_cost = 0.0
            total_input = 0
            total_output = 0
            
            # First try work_sessions
            for day_sessions in db.get('work_sessions', {}).values():
                total_sessions += len(day_sessions)
                for session in day_sessions:
                    total_messages += session.get('message_count', 0)
                    total_cost += session.get('total_cost', 0)
                    total_input += session.get('input_tokens', 0)
                    total_output += session.get('output_tokens', 0)
            
            # If no token data in work_sessions, use hourly_statistics
            if total_input == 0 and total_output == 0:
                hs_cost = 0
                for day_hours in db.get('hourly_statistics', {}).values():
                    for hour_data in day_hours.values():
                        hs_cost += hour_data.get('cost', 0)
                        total_input += hour_data.get('input_tokens', 0)
                        total_output += hour_data.get('output_tokens', 0)
                # Use the higher cost value
                total_cost = max(total_cost, hs_cost)
            
            total_tokens = total_input + total_output
            
            if total_sessions == 0:
                return "📊 Total: No data yet - start your first session!"
            
            # Format tokens
            if total_tokens >= 1_000_000:
                token_str = f"{total_tokens/1_000_000:.1f}M"
            elif total_tokens >= 1_000:
                token_str = f"{total_tokens/1_000:.0f}k"
            else:
                token_str = str(total_tokens)
            
            # Calculate averages
            avg_cost_per_session = total_cost / total_sessions if total_sessions > 0 else 0
            avg_msg_per_session = total_messages / total_sessions if total_sessions > 0 else 0
            
            return f"[TOTAL] [{total_sessions} sessions] [{total_messages} msgs] [{token_str} tokens] [${total_cost:.2f}] [Avg: {avg_msg_per_session:.0f}msg/session ${avg_cost_per_session:.2f}/session]"
        
        except Exception as e:
            return f"📊 Total summary error: {str(e)}"
    
    def format_weekly_summary(self) -> str:
        """Format weekly summary"""
        try:
            db = safe_json_read(self.db_file)
            now = datetime.now(timezone.utc)
            week_start = now - timedelta(days=7)
            
            # Get last 7 days of sessions
            weekly_cost = 0
            weekly_messages = 0
            weekly_sessions = 0
            
            for i in range(7):
                day = (week_start + timedelta(days=i)).strftime('%Y-%m-%d')
                day_sessions = db.get('work_sessions', {}).get(day, [])
                weekly_sessions += len(day_sessions)
                weekly_messages += sum(s.get('message_count', 0) for s in day_sessions)
                weekly_cost += sum(s.get('total_cost', 0) for s in day_sessions)
            
            if weekly_sessions == 0:
                return "📊 This week: Time to build something amazing! 💪"
            
            avg_daily = weekly_cost / 7
            
            return f"📊 Week: {weekly_sessions} sessions | {weekly_messages} msgs | ${weekly_cost:.2f} total | ${avg_daily:.2f}/day avg"
        
        except:
            return "📊 This week: Let's make it productive! 🎯"
    
    def format_fun_tip(self) -> str:
        """Format a random fun tip"""
        return random.choice(self.tips)
    
    def format_system_status(self) -> str:
        """Format system status"""
        try:
            # Check daemon status
            daemon_status = self.data_dir / "daemon_status.json"
            if daemon_status.exists():
                status = safe_json_read(daemon_status)
                if status.get('running'):
                    last_update = status.get('last_db_update', 0)
                    if last_update:
                        age = int(time.time() - last_update)
                        if age < 120:
                            daemon_str = "✅ Daemon active"
                        else:
                            daemon_str = f"⚠️ Daemon stale ({age}s)"
                    else:
                        daemon_str = "🔄 Daemon starting"
                else:
                    daemon_str = "❌ Daemon stopped"
            else:
                daemon_str = "❓ Daemon unknown"
            
            # Check data freshness
            if self.db_file.exists():
                db_age = int(time.time() - self.db_file.stat().st_mtime)
                if db_age < 120:
                    data_str = "📊 Data fresh"
                else:
                    data_str = f"📊 Data {db_age//60}m old"
            else:
                data_str = "📊 No data"
            
            return f"⚙️ System: {daemon_str} | {data_str} | 🔧 All systems operational"
        
        except:
            return "⚙️ System: Statusline ready | Type 'python daily_report.py' for analytics"
    
    def format_productivity_insight(self) -> str:
        """Format productivity insights"""
        try:
            db = safe_json_read(self.db_file)
            
            # Find most productive hour
            hour_counts = {}
            for sessions in db.get('work_sessions', {}).values():
                for session in sessions:
                    start = session.get('session_start', '')
                    if start:
                        try:
                            hour = datetime.fromisoformat(start.replace('Z', '+00:00')).hour
                            hour_counts[hour] = hour_counts.get(hour, 0) + 1
                        except:
                            pass
            
            if hour_counts:
                best_hour = max(hour_counts, key=hour_counts.get)
                return f"🏆 Most productive hour: {best_hour:02d}:00 | You've had {hour_counts[best_hour]} sessions at this time"
            else:
                return "🏆 Start tracking to discover your most productive hours!"
        
        except:
            return "🏆 Productivity insights will appear as you work"
    
    def _get_model_display_name(self, model: str) -> str:
        """Get display name for model"""
        models = self.prices.get('models', {})
        if model in models:
            return models[model].get('name', model)
        return model.replace('claude-', '').replace('-', ' ').title()
    
    def get_rotated_content(self, session_data: Optional[Dict[str, Any]] = None) -> str:
        """Get content based on rotation - only 2 modes now"""
        index = self.get_rotation_index()
        
        # If no session data, show simple alternating messages
        if not session_data:
            messages = [
                "🚀 Claude Statusline ready | Start a session to track usage",
                "📊 No sessions recorded yet | Waiting for Claude Code activity"
            ]
            return messages[index % 2]
        
        # Only rotate between main status and total summary
        if index == 0:
            return self.format_main_status(session_data)
        else:  # index == 1
            return self.format_total_summary()


def main():
    """Test the rotator"""
    rotator = StatuslineRotator()
    
    # Load current session
    db_file = rotator.data_dir / "smart_sessions_db.json"
    session_data = None
    
    if db_file.exists():
        db = safe_json_read(db_file)
        session_data = db.get('current_session')
    
    # Show different rotations
    safe_print("Statusline Rotation Demo:")
    safe_print("-" * 60)
    
    for i in range(6):
        # Override rotation index for demo
        rotator.get_rotation_index = lambda: i
        content = rotator.get_rotated_content(session_data)
        safe_print(f"Mode {i}: {content}")
    
    safe_print("-" * 60)
    safe_print("\nIn real use, content rotates every 10 seconds")


if __name__ == "__main__":
    main()