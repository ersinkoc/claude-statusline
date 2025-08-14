#!/usr/bin/env python3
import json
from pathlib import Path

# Load database
db_file = Path.home() / ".claude" / "data-statusline" / "smart_sessions_db.json"
db = json.load(open(db_file))

current_session = db.get('current_session', {})
print("Current session from DB:")
print(f"  model: {current_session.get('model', 'NOT SET')}")
print(f"  primary_model: {current_session.get('primary_model', 'NOT SET')}")
print(f"  session_number: {current_session.get('session_number')}")
print(f"  message_count: {current_session.get('message_count')}")

# Test the statusline
from statusline import StatusLine
sl = StatusLine()

# Get session data as statusline would
session_data = sl._get_session_data()
print("\nSession data in statusline:")
print(f"  model: {session_data.get('model', 'NOT SET')}")
print(f"  primary_model: {session_data.get('primary_model', 'NOT SET')}")
print(f"  message_count: {session_data.get('message_count')}")

# Test model info formatting
model_info = sl._format_model_info(session_data)
print(f"\nFormatted model info: {model_info}")