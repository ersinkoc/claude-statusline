#!/usr/bin/env python3
"""
Database Rebuilder for Claude Statusline
Rebuilds smart_sessions_db.json from JSONL files
"""

import json
import os
import sys
import io
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import Dict, List, Any, Optional

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        # Only wrap if not already wrapped
        if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if not isinstance(sys.stderr, io.TextIOWrapper) or sys.stderr.encoding != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        # If already wrapped or closed, skip
        pass

from claude_statusline.data_directory_utils import resolve_data_directory
from claude_statusline.safe_file_operations import safe_json_read, safe_json_write


class DatabaseRebuilder:
    """Rebuild smart_sessions_db.json from JSONL files"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.file_tracking_file = self.data_dir / "file_tracking.json"
        self.prices_file = Path(__file__).parent / "prices.json"
        
        # Claude projects directory
        self.claude_projects = Path.home() / ".claude" / "projects"
        
        # Load prices
        self.prices = safe_json_read(self.prices_file) if self.prices_file.exists() else {}
        
        # Session duration (5 hours)
        self.session_duration = timedelta(hours=5)
        
        print(f"📁 Data directory: {self.data_dir}")
        print(f"📁 Claude projects: {self.claude_projects}")
    
    def rebuild_database(self):
        """Rebuild the entire database from scratch"""
        print("\n🔨 REBUILDING DATABASE FROM JSONL FILES...")
        print("=" * 60)
        
        # Find all JSONL files
        jsonl_files = list(self.claude_projects.rglob("*.jsonl"))
        print(f"📂 Found {len(jsonl_files)} JSONL files")
        
        if not jsonl_files:
            print("❌ No JSONL files found!")
            return
        
        # Initialize data structures
        hourly_statistics = defaultdict(lambda: defaultdict(lambda: {
            'messages': 0,
            'input_tokens': 0,
            'output_tokens': 0,
            'cache_creation_input_tokens': 0,
            'cache_read_input_tokens': 0,
            'total_tokens': 0,
            'cost': 0.0,
            'models': defaultdict(lambda: {
                'messages': 0,
                'input_tokens': 0,
                'output_tokens': 0,
                'cache_creation_input_tokens': 0,
                'cache_read_input_tokens': 0,
                'total_tokens': 0,
                'cost': 0.0
            })
        }))
        
        work_sessions = defaultdict(list)
        file_tracking = {}
        total_messages = 0
        active_days = set()
        active_hours = set()
        
        # Process each JSONL file
        for jsonl_file in jsonl_files:
            print(f"📄 Processing: {jsonl_file.name}")
            
            try:
                with open(jsonl_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                file_messages = 0
                processed_count = 0
                
                for line in lines:
                    try:
                        data = json.loads(line.strip())
                        
                        # Only process assistant messages (they have usage info)
                        if data.get('type') == 'assistant' and 'message' in data:
                            msg = data['message']
                            
                            # Get timestamp
                            timestamp_str = data.get('timestamp', '')
                            if not timestamp_str:
                                continue
                            
                            # Parse timestamp
                            if timestamp_str.endswith('Z'):
                                timestamp_str = timestamp_str[:-1] + '+00:00'
                            timestamp = datetime.fromisoformat(timestamp_str)
                            
                            # Get date and hour
                            date_str = timestamp.strftime('%Y-%m-%d')
                            hour_str = timestamp.strftime('%H:00')
                            
                            # Get model
                            model = msg.get('model', 'unknown')
                            
                            # Skip synthetic models (test/debug messages)
                            if 'synthetic' in model.lower():
                                continue
                            
                            # Get usage
                            usage = msg.get('usage', {})
                            input_tokens = usage.get('input_tokens', 0)
                            output_tokens = usage.get('output_tokens', 0)
                            cache_creation = usage.get('cache_creation_input_tokens', 0)
                            cache_read = usage.get('cache_read_input_tokens', 0)
                            
                            # Debug: Check if we're getting real usage data
                            if usage and (input_tokens > 0 or output_tokens > 0 or cache_creation > 0 or cache_read > 0):
                                processed_count += 1
                                total = input_tokens + output_tokens + cache_creation + cache_read
                                if processed_count <= 3:  # Only log first few
                                    print(f"  ✓ Found usage: in={input_tokens}, out={output_tokens}, cache_w={cache_creation}, cache_r={cache_read}, total={total}")
                            
                            # Calculate cost
                            cost = self._calculate_cost(model, usage)
                            
                            # Update hourly statistics
                            hour_data = hourly_statistics[date_str][hour_str]
                            hour_data['messages'] += 1
                            hour_data['input_tokens'] += input_tokens
                            hour_data['output_tokens'] += output_tokens
                            hour_data['cache_creation_input_tokens'] += cache_creation
                            hour_data['cache_read_input_tokens'] += cache_read
                            hour_data['total_tokens'] += (input_tokens + output_tokens + cache_creation + cache_read)
                            hour_data['cost'] += cost
                            
                            # Update model statistics
                            model_data = hour_data['models'][model]
                            model_data['messages'] += 1
                            model_data['input_tokens'] += input_tokens
                            model_data['output_tokens'] += output_tokens
                            model_data['cache_creation_input_tokens'] += cache_creation
                            model_data['cache_read_input_tokens'] += cache_read
                            model_data['total_tokens'] += (input_tokens + output_tokens + cache_creation + cache_read)
                            model_data['cost'] += cost
                            
                            total_messages += 1
                            file_messages += 1
                            active_days.add(date_str)
                            active_hours.add(f"{date_str} {hour_str}")
                    
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        continue
                
                # Track file
                file_tracking[str(jsonl_file)] = {
                    'messages': file_messages,
                    'last_modified': os.path.getmtime(jsonl_file),
                    'size': os.path.getsize(jsonl_file)
                }
                
            except Exception as e:
                print(f"  ⚠️ Error processing file: {e}")
        
        # Build work sessions from hourly data
        print("\n🔧 Building work sessions...")
        
        for date_str in sorted(hourly_statistics.keys()):
            daily_hours = hourly_statistics[date_str]
            
            # Find continuous work periods
            active_hours_list = []
            for hour_str, hour_data in daily_hours.items():
                if hour_data['messages'] > 0:
                    hour = int(hour_str.split(':')[0])
                    active_hours_list.append((hour, hour_data))
            
            if not active_hours_list:
                continue
            
            # Sort by hour
            active_hours_list.sort(key=lambda x: x[0])
            
            # Group into sessions (5-hour windows)
            current_session = None
            
            for hour, hour_data in active_hours_list:
                # Check if we need a new session
                if current_session is None:
                    # Start new session
                    session_start = datetime.fromisoformat(f"{date_str}T{hour:02d}:00:00+00:00")
                    session_end = session_start + self.session_duration
                    
                    current_session = {
                        'session_start': session_start.isoformat(),
                        'session_end': session_end.isoformat(),
                        'message_count': 0,
                        'tokens': 0,
                        'cost': 0.0,  # Will accumulate from hourly data
                        'models': [],
                        'primary_model': 'unknown'
                    }
                    
                # Add hour data to current session
                current_session['message_count'] += hour_data['messages']
                current_session['tokens'] += hour_data['total_tokens']
                # Accumulate cost from hourly data (CRITICAL FIX)
                current_session['cost'] = current_session.get('cost', 0.0) + hour_data['cost']
                
                # Track models
                for model in hour_data['models']:
                    if model not in current_session['models']:
                        current_session['models'].append(model)
                
                # Check if session should end
                session_end = datetime.fromisoformat(current_session['session_end'])
                current_hour_time = datetime.fromisoformat(f"{date_str}T{hour:02d}:00:00+00:00")
                
                if current_hour_time >= session_end:
                    # Save current session and start new one
                    if current_session['message_count'] > 0:
                        # Determine primary model
                        if current_session['models']:
                            if len(current_session['models']) == 1:
                                current_session['primary_model'] = current_session['models'][0]
                            else:
                                # For multiple models, use the first one as primary for now
                                current_session['primary_model'] = current_session['models'][0]
                        
                        work_sessions[date_str].append(current_session)
                    
                    # Start new session
                    session_start = datetime.fromisoformat(f"{date_str}T{hour:02d}:00:00+00:00")
                    session_end = session_start + self.session_duration
                    
                    current_session = {
                        'session_start': session_start.isoformat(),
                        'session_end': session_end.isoformat(),
                        'message_count': hour_data['messages'],
                        'tokens': hour_data['total_tokens'],
                        'cost': hour_data['cost'],  # Include cost from hourly data
                        'models': list(hour_data['models'].keys()),
                        'primary_model': 'unknown'
                    }
            
            # Save last session
            if current_session and current_session['message_count'] > 0:
                # Determine primary model
                if current_session['models']:
                    # If only one model, use it. Otherwise keep as unknown for now
                    # (could be improved to count actual usage)
                    if len(current_session['models']) == 1:
                        current_session['primary_model'] = current_session['models'][0]
                    else:
                        # For multiple models, use the first one as primary for now
                        current_session['primary_model'] = current_session['models'][0]
                
                work_sessions[date_str].append(current_session)
        
        # Convert defaultdicts to regular dicts for JSON serialization
        # Also determine primary_model for each hour
        hourly_statistics_final = {}
        for date, hours in hourly_statistics.items():
            hourly_statistics_final[date] = {}
            for hour, hour_data in hours.items():
                # Determine primary model (most used model in this hour)
                primary_model = None
                max_messages = 0
                for model_name, model_data in hour_data['models'].items():
                    if model_data['messages'] > max_messages:
                        max_messages = model_data['messages']
                        primary_model = model_name
                
                hourly_statistics_final[date][hour] = {
                    **hour_data,
                    'models': dict(hour_data['models']),
                    'primary_model': primary_model or 'unknown'
                }
        
        hourly_statistics = hourly_statistics_final
        
        work_sessions = dict(work_sessions)
        
        # Find current active session
        current_session_data = {}
        now = datetime.now(timezone.utc)
        today_str = now.strftime('%Y-%m-%d')
        
        # Check if we have today's sessions
        if today_str in work_sessions and work_sessions[today_str]:
            # Get the last session of today
            last_session = work_sessions[today_str][-1]
            session_start = datetime.fromisoformat(last_session['session_start'].replace('Z', '+00:00'))
            
            # Check if session end time hasn't passed yet
            if 'session_end' in last_session:
                session_end = datetime.fromisoformat(last_session['session_end'].replace('Z', '+00:00'))
                if now < session_end:
                    # We're in an active session!
                    # Remove session_end since it's still active
                    last_session.pop('session_end', None)
                    
                    # Calculate session cost and tokens from hourly_statistics for the session period
                    session_cost = 0.0
                    session_input_tokens = 0
                    session_output_tokens = 0
                    session_cache_read = 0
                    session_cache_write = 0
                    session_start_hour = session_start.hour
                    session_end_hour = min(now.hour + 1, 24)  # Include current hour
                    
                    if today_str in hourly_statistics:
                        for hour in range(session_start_hour, session_end_hour):
                            hour_str = f"{hour:02d}:00"  # FIX: Use proper hour format like "06:00" not "6"
                            if hour_str in hourly_statistics[today_str]:
                                hour_data = hourly_statistics[today_str][hour_str]
                                session_cost += hour_data.get('cost', 0.0)
                                session_input_tokens += hour_data.get('input_tokens', 0)
                                session_output_tokens += hour_data.get('output_tokens', 0)
                                session_cache_read += hour_data.get('cache_read_input_tokens', 0)
                                session_cache_write += hour_data.get('cache_creation_input_tokens', 0)
                    
                    # Set as current session with detailed token breakdown
                    current_session_data = {
                        'session_number': len(work_sessions[today_str]),
                        'session_start': last_session['session_start'],
                        'message_count': last_session['message_count'],
                        'tokens': last_session['tokens'],
                        'input_tokens': session_input_tokens,
                        'output_tokens': session_output_tokens,
                        'cache_read_tokens': session_cache_read,
                        'cache_write_tokens': session_cache_write,
                        'cost': session_cost,  # Use calculated cost from hourly_statistics
                        'model': last_session.get('primary_model', 'unknown'),
                        'last_update': now.isoformat()
                    }
                    print(f"\n🔴 ACTIVE SESSION DETECTED: Started {session_start.strftime('%H:%M')} - {last_session['message_count']} messages")
        
        # Build final database
        database = {
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'current_session': current_session_data,
            'build_info': {
                'total_files_processed': len(jsonl_files),
                'total_messages_in_tracking': total_messages,
                'total_active_days': len(active_days),
                'total_active_hours': len(active_hours),
                'smart_work_sessions_created': sum(len(sessions) for sessions in work_sessions.values()),
                'files_tracked': len(file_tracking)
            },
            'hourly_statistics': hourly_statistics,
            'work_sessions': work_sessions
        }
        
        # Save database
        print(f"\n💾 Saving database to: {self.db_file}")
        safe_json_write(database, self.db_file)
        
        # Save file tracking
        print(f"💾 Saving file tracking to: {self.file_tracking_file}")
        safe_json_write(file_tracking, self.file_tracking_file)
        
        # Print summary
        print("\n" + "=" * 60)
        print("✅ DATABASE REBUILD COMPLETE!")
        print(f"📊 Total messages processed: {total_messages:,}")
        print(f"📅 Active days: {len(active_days)}")
        print(f"⏰ Active hours: {len(active_hours)}")
        print(f"💼 Work sessions created: {sum(len(sessions) for sessions in work_sessions.values())}")
        print(f"📁 Files tracked: {len(file_tracking)}")
    
    def _calculate_cost(self, model: str, usage: Dict) -> float:
        """Calculate cost for given model and usage"""
        model_prices = self._get_model_prices(model)
        
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        cache_creation = usage.get('cache_creation_input_tokens', 0)
        cache_read = usage.get('cache_read_input_tokens', 0)
        
        input_cost = (input_tokens / 1_000_000) * model_prices.get('input', 15.0)
        output_cost = (output_tokens / 1_000_000) * model_prices.get('output', 75.0)
        cache_cost = (cache_creation / 1_000_000) * model_prices.get('cache_write_5m', 18.75)
        cache_read_cost = (cache_read / 1_000_000) * model_prices.get('cache_read', 1.5)
        
        total_cost = input_cost + output_cost + cache_cost + cache_read_cost
        
        # Debug logging for zero costs
        if total_cost == 0 and (input_tokens > 0 or output_tokens > 0 or cache_creation > 0 or cache_read > 0):
            print(f"  ⚠️ Zero cost despite tokens: model={model}, usage={usage}, prices={model_prices}")
        
        return total_cost
    
    def _get_model_prices(self, model: str) -> Dict:
        """Get pricing for a specific model"""
        models = self.prices.get('models', {})
        
        # Try exact match first
        if model in models:
            return models[model]
        
        # Try partial match
        for model_key, prices in models.items():
            if model_key in model or model in model_key:
                return prices
        
        # Return fallback pricing
        return self.prices.get('fallback_pricing', {
            'input': 15.0,
            'output': 75.0,
            'cache_write_5m': 18.75,
            'cache_read': 1.5
        })


def main():
    """Main entry point"""
    rebuilder = DatabaseRebuilder()
    rebuilder.rebuild_database()


if __name__ == "__main__":
    main()