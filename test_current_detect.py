#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

# Load database
db_file = Path.home() / ".claude" / "data-statusline" / "smart_sessions_db.json"
db = json.load(open(db_file))

now = datetime.now(timezone.utc)
today_str = now.strftime('%Y-%m-%d')
print(f"Now: {now.isoformat()}")
print(f"Today: {today_str}")

# Check if we have today's sessions
if today_str in db.get('work_sessions', {}):
    sessions = db['work_sessions'][today_str]
    print(f"Sessions today: {len(sessions)}")
    
    # Get the last session of today
    last_session = sessions[-1]
    print(f"Last session: {last_session['session_start']} to {last_session.get('session_end', 'ACTIVE')}")
    
    session_start = datetime.fromisoformat(last_session['session_start'].replace('Z', '+00:00'))
    
    # Check if session end time hasn't passed yet
    if 'session_end' in last_session:
        session_end = datetime.fromisoformat(last_session['session_end'].replace('Z', '+00:00'))
        print(f"Session end: {session_end.isoformat()}")
        print(f"Now < session_end? {now < session_end}")
        
        if now < session_end:
            print("WE ARE IN AN ACTIVE SESSION!")
            print(f"Should remove session_end and set as current_session")
        else:
            print("Session has already ended")
    else:
        print("No session_end - this IS the active session!")
else:
    print("No sessions today")