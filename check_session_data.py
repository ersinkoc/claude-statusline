#!/usr/bin/env python3
"""Check session data for token and cost information"""

import json
from pathlib import Path

# Load database
db_file = Path.home() / ".claude" / "data-statusline" / "smart_sessions_db.json"
db = json.load(open(db_file))

print("=== CURRENT SESSION ===")
cs = db.get('current_session', {})
print(f"Messages: {cs.get('message_count')}")
print(f"Input tokens: {cs.get('input_tokens')}")
print(f"Output tokens: {cs.get('output_tokens')}")
print(f"Total cost: ${cs.get('total_cost')}")
print(f"Model: {cs.get('model')}")

print("\n=== SAMPLE SESSION WITH COST ===")
# Find a session with cost > 0
found = False
for day, sessions in db.get('work_sessions', {}).items():
    for s in sessions:
        if s.get('total_cost', 0) > 0:
            print(f'Date: {day}')
            print(f'Messages: {s.get("message_count")}')
            print(f'Input tokens: {s.get("input_tokens")}')
            print(f'Output tokens: {s.get("output_tokens")}')
            print(f'Total cost: ${s.get("total_cost")}')
            print(f'Model: {s.get("primary_model")}')
            found = True
            break
    if found:
        break

if not found:
    print("No sessions with cost > 0 found")

print("\n=== TOTAL STATS ===")
total_sessions = 0
total_cost = 0
total_input = 0
total_output = 0

for sessions in db.get('work_sessions', {}).values():
    total_sessions += len(sessions)
    for s in sessions:
        total_cost += s.get('total_cost', 0)
        total_input += s.get('input_tokens', 0)
        total_output += s.get('output_tokens', 0)

print(f"Total sessions: {total_sessions}")
print(f"Total cost: ${total_cost:.2f}")
print(f"Total input tokens: {total_input:,}")
print(f"Total output tokens: {total_output:,}")
print(f"Total tokens: {total_input + total_output:,}")

print("\n=== HOURLY STATISTICS ===")
hs = db.get('hourly_statistics', {})
hs_total_cost = 0
hs_total_input = 0
hs_total_output = 0

for day_hours in hs.values():
    for hour_data in day_hours.values():
        hs_total_cost += hour_data.get('cost', 0)
        hs_total_input += hour_data.get('input_tokens', 0)
        hs_total_output += hour_data.get('output_tokens', 0)

print(f"Hourly stats total cost: ${hs_total_cost:.2f}")
print(f"Hourly stats input tokens: {hs_total_input:,}")
print(f"Hourly stats output tokens: {hs_total_output:,}")
print(f"Hourly stats total tokens: {hs_total_input + hs_total_output:,}")