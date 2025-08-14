#!/usr/bin/env python3
"""Verify cost calculations"""

import json
from pathlib import Path

db_file = Path.home() / ".claude" / "data-statusline" / "smart_sessions_db.json"

with open(db_file, 'r') as f:
    db = json.load(f)

# Calculate from hourly statistics
hourly_total = 0
for date, hours in db.get('hourly_statistics', {}).items():
    for hour, data in hours.items():
        hourly_total += data.get('cost', 0)

print(f"Cost from hourly_statistics: ${hourly_total:.2f}")

# Calculate from work sessions
session_total = 0
session_count = 0
for date, sessions in db.get('work_sessions', {}).items():
    for session in sessions:
        session_total += session.get('cost', 0)
        session_count += 1

print(f"Cost from work_sessions: ${session_total:.2f}")
print(f"Number of sessions: {session_count}")

if abs(hourly_total - session_total) > 1:
    print(f"\n⚠️ MISMATCH! Difference: ${abs(hourly_total - session_total):.2f}")
    print("Work sessions might be double-counting or miscalculating costs.")
else:
    print("\n✅ Costs match!")