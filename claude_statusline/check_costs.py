#!/usr/bin/env python3
"""Quick cost checker"""

import json
from pathlib import Path
import sys

def main():
    """Main function for cost checking"""
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
    
    total_cost = 0
    model_costs = {}
    token_counts = {}
    
    for date, hours in db.get('hourly_statistics', {}).items():
        for hour, data in hours.items():
            cost = data.get('cost', 0)
            total_cost += cost
            
            models = data.get('models', {})
            if isinstance(models, dict):
                for model, mdata in models.items():
                    if model not in model_costs:
                        model_costs[model] = 0
                        token_counts[model] = {'input': 0, 'output': 0, 'cache': 0, 'cache_read': 0}
                    
                    model_costs[model] += mdata.get('cost', 0)
                    token_counts[model]['input'] += mdata.get('input_tokens', 0)
                    token_counts[model]['output'] += mdata.get('output_tokens', 0)
                    token_counts[model]['cache'] += mdata.get('cache_creation_input_tokens', 0)
                    token_counts[model]['cache_read'] += mdata.get('cache_read_input_tokens', 0)
    
    print(f"Total Cost: ${total_cost:.2f}")
    print("\nBy Model:")
    for model, cost in sorted(model_costs.items(), key=lambda x: x[1], reverse=True):
        tokens = token_counts[model]
        total_tokens = sum(tokens.values())
        print(f"\n{model[:40]}:")
        print(f"  Cost: ${cost:.2f}")
        print(f"  Input: {tokens['input']:,}")
        print(f"  Output: {tokens['output']:,}")
        print(f"  Cache: {tokens['cache']:,}")
        print(f"  Cache Read: {tokens['cache_read']:,}")
        print(f"  Total Tokens: {total_tokens:,}")

if __name__ == "__main__":
    main()