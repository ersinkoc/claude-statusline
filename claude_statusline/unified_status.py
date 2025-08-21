#!/usr/bin/env python3
"""
Unified Status System - Tek bir statusline sistemi
Unified status display for both claude-status and claude-statusline
"""

import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from claude_statusline.unified_theme_system import THEME_SYSTEM

def get_unified_status():
    """Single statusline function - for all commands"""
    try:
        # Data directory
        data_dir = Path.home() / ".claude" / "data-statusline" 
        db_file = data_dir / "smart_sessions_db.json"
        config_file = Path(__file__).parent / "config.json"
        
        if not db_file.exists():
            return "Claude AI | No Data"
        
        # Load database
        with open(db_file, 'r', encoding='utf-8') as f:
            db_data = json.load(f)
        
        # Get current session or today's data
        now = datetime.now(timezone.utc)
        today_str = now.strftime('%Y-%m-%d')
        
        message_count = 0
        total_tokens = 0
        cost = 0.0
        model = "Claude"
        session_time = ""
        
        # Get today's sessions
        today_sessions = db_data.get('work_sessions', {}).get(today_str, [])
        
        if today_sessions:
            # Get current/last session
            last_session = today_sessions[-1]
            
            # Check if session is active (within 5 hours)
            session_start = datetime.fromisoformat(last_session.get('session_start', '').replace('Z', '+00:00'))
            session_end = session_start + timedelta(hours=5)
            
            if now < session_end:
                # Active session
                time_remaining = session_end - now
                hours = int(time_remaining.total_seconds() // 3600)
                minutes = int((time_remaining.total_seconds() % 3600) // 60)
                session_time = f"~{hours}:{minutes:02d}"
            else:
                session_time = "IDLE"
            
            # Get session data
            message_count = last_session.get('message_count', 0)
            total_tokens = last_session.get('total_tokens', 0)
            
            # Format model name
            model_full = last_session.get('primary_model', 'claude')
            if 'opus-4-1' in model_full.lower() or 'opus-4.1' in model_full.lower():
                model = 'Opus 4.1'
            elif 'opus' in model_full.lower():
                model = 'Opus'
            elif 'sonnet-4' in model_full.lower():
                model = 'Sonnet-4'
            elif 'sonnet' in model_full.lower():
                model = 'Sonnet'
            elif 'haiku' in model_full.lower():
                model = 'Haiku'
        
        # Calculate today's total cost
        hourly_data = db_data.get('hourly_statistics', {}).get(today_str, {})
        for hour_data in hourly_data.values():
            cost += hour_data.get('cost', 0)
        
        # Prepare data for theme system
        theme_data = {
            "model": model,
            "messages": str(message_count),
            "tokens": total_tokens,  # Theme system will format it
            "cost": f"{cost:.1f}",
            "sessions": "1",
            "session_time": session_time if session_time else "0:00",
            "efficiency": "100"
        }
        
        # Get current theme and apply it
        current_theme = THEME_SYSTEM.get_current_theme()
        result = THEME_SYSTEM.apply_theme(current_theme, theme_data)
        
        return result
        
    except Exception as e:
        return f"Claude AI | Error: {str(e)[:20]}"


def main():
    """Main entry point"""
    print(get_unified_status())


if __name__ == "__main__":
    main()