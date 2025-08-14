#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

# Load database
db_file = Path.home() / ".claude" / "data-statusline" / "smart_sessions_db.json"
db = json.load(open(db_file))

# Check current session
current = db.get("current_session", {})
print("Current session:", json.dumps(current, indent=2))

# Check today's work sessions  
today = db.get("work_sessions", {}).get("2025-08-14", [])
print(f"\nSessions today: {len(today)}")

if today:
    last = today[-1]
    print(f"Last session:")
    print(f"  Start: {last['session_start']}")
    print(f"  End: {last.get('session_end', 'ACTIVE')}")
    print(f"  Messages: {last.get('message_count', 0)}")
    tokens = last.get('tokens', 0)
    if isinstance(tokens, dict):
        tokens = tokens.get('total', 0)
    print(f"  Tokens: {tokens:,}")
    
    cost = last.get('cost', 0)
    if isinstance(cost, dict):
        cost = cost.get('total', 0)
    print(f"  Cost: ${cost:.2f}")
    print(f"  Fields: {list(last.keys())[:10]}")
    
    # Check if this should be the current session
    now = datetime.now(timezone.utc)
    start = datetime.fromisoformat(last['session_start'].replace('Z', '+00:00'))
    if not last.get('session_end'):
        age = (now - start).total_seconds() / 3600
        print(f"  Age: {age:.1f} hours")
        if age < 5:
            print(f"  -> This should be the CURRENT session!")
        else:
            print(f"  -> Session expired {age-5:.1f} hours ago")