#!/usr/bin/env python3
"""Check session data for token and cost information"""

import json
from pathlib import Path
import sys

def main():
    """Main function for checking session data"""
    # Load database
    db_file = Path.home() / ".claude" / "data-statusline" / "smart_sessions_db.json"
    
    if not db_file.exists():
        print(f"Database not found: {db_file}")
        print("Run 'claude-statusline rebuild' first to create the database.")
        sys.exit(1)
    
    try:
        with open(db_file, 'r') as f:
            db = json.load(f)
    except Exception as e:
        print(f"Error loading database: {e}")
        sys.exit(1)
    
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
    total_messages = 0
    
    for day, sessions in db.get('work_sessions', {}).items():
        total_sessions += len(sessions)
        for s in sessions:
            total_cost += s.get('total_cost', 0)
            total_messages += s.get('message_count', 0)
    
    print(f"Total sessions: {total_sessions}")
    print(f"Total messages: {total_messages}")
    print(f"Total cost: ${total_cost:.2f}")

if __name__ == "__main__":
    main()