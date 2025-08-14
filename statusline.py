#!/usr/bin/env python3
"""
Claude Statusline - Main Entry Point

THIS SCRIPT IS CALLED BY CLAUDE CODE
- Starts daemon if not running
- Reads live session data
- Outputs formatted statusline

Simple, fast and reliable.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, Tuple

try:
    import psutil
except ImportError:
    psutil = None

from data_directory_utils import resolve_data_directory
from instance_manager import InstanceManager
from safe_file_operations import safe_json_read, safe_json_write
from simple_visual_formatter import SimpleVisualFormatter
from statusline_rotator import StatuslineRotator
# from claude_native_formatter import ClaudeNativeFormatter
# from system_startup import SystemStartupManager
from console_utils import safe_print


class StatuslineDisplay:
    """
    Main statusline display system
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize simple statusline"""
        self.data_dir = resolve_data_directory(data_dir)
        
        # File paths
        self.live_session_file = self.data_dir / "live_session.json"
        self.daemon_status_file = self.data_dir / "daemon_status.json"
        self.daemon_script = Path(__file__).parent / "unified_daemon.py"
        self.db_file = self.data_dir / "smart_sessions_db.json"
        
        # Load configuration
        self.config = self._load_config()
        
        # Display configuration
        self.show_git_branch = self.config.get('display', {}).get('show_git_branch', True)
        self.show_admin_status = self.config.get('display', {}).get('show_admin_status', True)
        self.time_format = self.config.get('display', {}).get('time_format', '%H:%M')
        self.status_format = self.config.get('display', {}).get('status_format', 'compact')
        
        # Model icons and priorities
        self.model_icons = {
            'opus': '🧠',
            'sonnet': '🎭', 
            'haiku': '⚡',
            'unknown': '🤖'
        }
        
        # Model name patterns for classification
        self.model_patterns = {
            'opus': ['opus', 'claude-opus'],
            'sonnet': ['sonnet', 'claude-sonnet'],
            'haiku': ['haiku', 'claude-haiku']
        }
        
        # Cost display precision
        self.cost_precision = self.config.get('reporting', {}).get('cost_precision', 6)
        
        # Simple visual formatter for better compatibility
        self.simple_visual_formatter = SimpleVisualFormatter()
        
        # Rotating statusline for variety
        self.statusline_rotator = StatuslineRotator(data_dir=self.data_dir)
        
        # Enable rotation based on config or environment
        self.enable_rotation = self.config.get('display', {}).get('enable_rotation', False)
    
    def _ensure_live_tracker_running(self):
        """Ensure live session tracker is running as daemon"""
        try:
            if not psutil:
                # If psutil is not available, just try to start the tracker
                self._start_tracker_simple()
                return
            
            # Check for improved tracker first
            tracker_pid_file = self.data_dir / '.live_tracker.pid'
            tracker_health_file = self.data_dir / '.tracker_health.json'
            
            # Check if tracker is healthy
            needs_restart = False
            
            if tracker_pid_file.exists():
                try:
                    with open(tracker_pid_file, 'r') as f:
                        pid = int(f.read().strip())
                    
                    # Check if process exists and is running
                    if psutil.pid_exists(pid):
                        try:
                            proc = psutil.Process(pid)
                            if 'python' in proc.name().lower():
                                # Check health status
                                if tracker_health_file.exists():
                                    with open(tracker_health_file, 'r') as f:
                                        health = json.load(f)
                                    
                                    # Check if health is recent (within last 60 seconds)
                                    health_time = datetime.fromisoformat(health['timestamp'].replace('Z', '+00:00'))
                                    now = datetime.now(timezone.utc)
                                    age = (now - health_time).total_seconds()
                                    
                                    if age < 60 and health.get('status') in ['running', 'healthy']:
                                        # Tracker is healthy
                                        return
                                    else:
                                        # Tracker might be stuck
                                        needs_restart = True
                                else:
                                    # No health file, might be starting up
                                    return
                            else:
                                # Not our process
                                needs_restart = True
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            needs_restart = True
                    else:
                        needs_restart = True
                        
                except Exception:
                    needs_restart = True
            else:
                needs_restart = True
            
            if not needs_restart:
                return
            
            # Try to use improved tracker first
            script_dir = Path(__file__).parent
            improved_tracker = script_dir / 'live_session_tracker_improved.py'
            tracker_script = script_dir / 'live_session_tracker.py'
            
            # Choose which tracker to use
            if improved_tracker.exists():
                tracker_to_use = improved_tracker
            elif tracker_script.exists():
                tracker_to_use = tracker_script
            else:
                return
            
            # Build command
            python_executable = sys.executable
            cmd = [python_executable, str(tracker_to_use), '--daemon', '--restart',
                   '--data-dir', str(self.data_dir)]
            
            # Start the tracker
            if sys.platform == 'win32':
                # Windows: Detached process
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                DETACHED_PROCESS = 0x00000008
                CREATE_NO_WINDOW = 0x08000000
                
                subprocess.Popen(
                    cmd,
                    creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS | CREATE_NO_WINDOW,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    cwd=str(script_dir)
                )
            else:
                # Unix: Daemon process
                subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                    cwd=str(script_dir)
                )
            
            # Wait for startup
            time.sleep(0.3)
            
        except Exception:
            # Silently fail - statusline should work even without live tracker
            pass
    
    def _start_tracker_simple(self):
        """Simple tracker start without psutil"""
        try:
            script_dir = Path(__file__).parent
            improved_tracker = script_dir / 'live_session_tracker_improved.py'
            tracker_script = script_dir / 'live_session_tracker.py'
            
            # Choose which tracker to use
            if improved_tracker.exists():
                tracker_to_use = improved_tracker
            elif tracker_script.exists():
                tracker_to_use = tracker_script
            else:
                return
            
            # Build command
            python_executable = sys.executable
            cmd = [python_executable, str(tracker_to_use), '--daemon',
                   '--data-dir', str(self.data_dir)]
            
            # Start the tracker
            if sys.platform == 'win32':
                # Windows: Detached process
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                DETACHED_PROCESS = 0x00000008
                CREATE_NO_WINDOW = 0x08000000
                
                subprocess.Popen(
                    cmd,
                    creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS | CREATE_NO_WINDOW,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    cwd=str(script_dir)
                )
            else:
                # Unix: Daemon process
                subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                    cwd=str(script_dir)
                )
        except Exception:
            pass
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json"""
        try:
            script_dir = Path(__file__).parent
            config_file = script_dir / "config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        # Default configuration
        return {
            'display': {
                'show_git_branch': True,
                'show_admin_status': True,
                'time_format': '%H:%M',
                'status_format': 'compact'
            },
            'reporting': {
                'cost_precision': 6
            }
        }
    
    def display(self, timeout: int = 5, claude_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate statusline display with orchestration
        
        Args:
            timeout: Maximum time for orchestration (seconds)
            claude_data: Live session data from Claude Code (if available)
            
        Returns:
            Formatted statusline string
        """
        start_time = time.time()
        
        try:
            # Ensure daemon is running (single instance)
            self._ensure_daemon_running()
            # If we have Claude Code live data, try to use it but fallback to local data
            if claude_data:
                # Update database current session with live data
                self._update_session_from_claude_data(claude_data)
                
                session_data = self._process_claude_data(claude_data)
                if session_data:
                    return self._format_session_display(session_data)
                # If Claude data processing failed, continue to local data
            
            # Always ensure live tracker is running first
            self._ensure_live_tracker_running()
            
            # Quick data check - if we have any data, skip system startup for speed
            if self._has_any_data():
                # Data exists, skip startup orchestration for performance
                pass
            else:
                # Ensure system components are running (master coordination)
                # startup_manager = SystemStartupManager(data_dir=self.data_dir, config=self.config)
                # startup_result = startup_manager.ensure_system_running()
                pass  # Skip startup manager for now
            
            # Load session data with priority order
            session_data = self._load_session_data()
            
            # Generate display - always try to use session data if available
            if session_data:
                display_text = self._format_session_display(session_data)
            else:
                # Try to get basic session info from live data even if old
                basic_data = self._get_basic_session_data()
                if basic_data:
                    display_text = self._format_session_display(basic_data)
                else:
                    display_text = self._format_fallback_display()
            
            # Add performance indicator if orchestration was slow (disabled for cleaner display)
            # elapsed = time.time() - start_time
            # if elapsed > 1.0:
            #     display_text += f" ⏱{elapsed:.1f}s"
            
            return display_text
            
        except Exception as e:
            # Emergency fallback
            return self._format_error_display(str(e))
    
    def _process_claude_data(self, claude_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process live Claude Code session data
        
        Args:
            claude_data: JSON data from Claude Code stdin
            
        Returns:
            Formatted session data or None
        """
        try:
            # IMPORTANT FIX: If Claude Code sends empty/minimal data, prefer our local data
            # Claude Code might just be sending a heartbeat with no real session info
            
            # First, check if Claude Code data is meaningful
            session_id = claude_data.get('session', {}).get('id', '')
            model_info = claude_data.get('model', {})
            
            # If Claude Code data is minimal/empty, use our local database entirely
            if not session_id or not model_info:
                return self._load_session_data()  # Use local database completely
            
            # Load our local data for real metrics
            live_data = self._load_live_session_data()
            if not live_data:
                # No local data, try database
                return self._load_database_current_session()
            
            # Extract Claude Code info for model name and directory
            session_id = claude_data.get('session', {}).get('id', '')
            model_info = claude_data.get('model', {})
            workspace_info = claude_data.get('workspace', {})
            model_name = model_info.get('display_name', model_info.get('name', 'Unknown'))
            
            # If we have good local data, use it!
            if live_data and live_data.get('message_count', 0) > 0:
                # Calculate real remaining time based on session start
                remaining_seconds = self._calculate_remaining_time(live_data)
                
                # Try to get current message count from JSONL if available
                current_message_count = live_data.get('message_count', 0)
                if claude_data.get('transcript_path'):
                    try:
                        # Quick count of lines in JSONL file
                        jsonl_path = Path(claude_data['transcript_path'])
                        if jsonl_path.exists():
                            with open(jsonl_path, 'r', encoding='utf-8') as f:
                                # Count non-empty lines (each is a message)
                                line_count = sum(1 for line in f if line.strip())
                                # Each exchange typically has 2 entries (user + assistant)
                                current_message_count = max(current_message_count, line_count // 2)
                    except:
                        pass  # Fall back to stored count
                
                # Calculate session end time
                session_end_time = None
                if live_data.get('session_start'):
                    try:
                        session_start = live_data['session_start']
                        if 'T' in session_start and '+' not in session_start and 'Z' not in session_start:
                            session_start += '+00:00'
                        start_time = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
                        end_time = start_time + timedelta(hours=5)
                        # Convert to local time for display
                        local_end_time = end_time.astimezone()
                        session_end_time = local_end_time.strftime('%H:%M')
                    except:
                        pass
                
                # Use most recent model (last in models list) or Claude Code's model info
                models_list = live_data.get('models', [model_name])
                most_recent_model = models_list[-1] if models_list else model_name
                
                # Use our tracked data with most recent model
                return {
                    'data_source': 'live_with_claude',
                    'active': remaining_seconds > 0,  # Active only if time remains
                    'session_number': live_data.get('session_number', '?'),
                    'primary_model': most_recent_model,
                    'current_dir': workspace_info.get('current_dir', ''),
                    'live_session_id': session_id,
                    'message_count': current_message_count,
                    'tokens': live_data.get('tokens', 0),
                    'cost': live_data.get('cost', 0.0),
                    'models': live_data.get('models', [model_name]),
                    'remaining_seconds': remaining_seconds,
                    'session_end_time': session_end_time
                }
            
            # Fallback: Try to match with database
            matched_session = self._match_database_session(session_id)
            if matched_session and matched_session.get('message_count', 0) > 0:
                remaining_seconds = self._calculate_remaining_time(matched_session)
                
                # Calculate session end time
                session_end_time = None
                if matched_session.get('session_start'):
                    try:
                        session_start = matched_session['session_start']
                        if 'T' in session_start and '+' not in session_start and 'Z' not in session_start:
                            session_start += '+00:00'
                        start_time = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
                        end_time = start_time + timedelta(hours=5)
                        local_end_time = end_time.astimezone()
                        session_end_time = local_end_time.strftime('%H:%M')
                    except:
                        pass
                
                # Use most recent model from database
                models_list = matched_session.get('models', [model_name])
                most_recent_model = models_list[-1] if models_list else model_name
                
                session_data = matched_session.copy()
                session_data.update({
                    'data_source': 'claude_live',
                    'active': remaining_seconds > 0,
                    'primary_model': most_recent_model,
                    'current_dir': workspace_info.get('current_dir', ''),
                    'live_session_id': session_id,
                    'remaining_seconds': remaining_seconds,
                    'session_end_time': session_end_time
                })
                return session_data
            
            # Last resort: Use whatever we have but with zeros (original behavior)
            return {
                'data_source': 'claude_only',
                'active': True,
                'session_number': '?',
                'primary_model': model_name,
                'current_dir': workspace_info.get('current_dir', ''),
                'live_session_id': session_id,
                'message_count': 0,
                'tokens': 0,
                'cost': 0.0,
                'models': [model_name],
                'remaining_seconds': 0
            }
        
        except Exception:
            return None
    
    def _match_database_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Try to match Claude Code session with our database sessions
        
        Args:
            session_id: Session ID from Claude Code
            
        Returns:
            Matching session data or None
        """
        try:
            if not self.db_file.exists():
                return None
            
            with open(self.db_file, 'r') as f:
                db_data = json.load(f)
            
            # Check current session first
            current_session = db_data.get('current_session')
            if current_session and current_session.get('live_session_id') == session_id:
                return current_session
            
            # Check all sessions for matching session ID
            for session in db_data.get('sessions', []):
                if session.get('live_session_id') == session_id:
                    return session
            
            # Check smart work sessions
            for session in db_data.get('smart_work_sessions', []):
                if session.get('live_session_id') == session_id:
                    return session
            
            return None
        
        except Exception:
            return None
    
    def _calculate_remaining_time(self, session_data: Dict[str, Any]) -> int:
        """
        Calculate remaining time for a session
        
        Args:
            session_data: Session data from database
            
        Returns:
            Remaining seconds (0 if expired)
        """
        try:
            # Calculate based on session start time
            session_start = session_data.get('session_start', '')
            if session_start:
                # Parse session start time
                if 'T' in session_start and '+' not in session_start and 'Z' not in session_start:
                    # Add UTC timezone if missing
                    session_start += '+00:00'
                
                start_time = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
                now = datetime.now(timezone.utc)
                
                # Sessions are 5 hours long
                session_duration = timedelta(hours=5)
                end_time = start_time + session_duration
                
                remaining_seconds = (end_time - now).total_seconds()
                return max(0, int(remaining_seconds))
            
            # Fallback to session_end if available
            session_end = session_data.get('session_end', '')
            if session_end:
                # Parse session end time
                if 'T' in session_end and '+' not in session_end and 'Z' not in session_end:
                    # Add UTC timezone if missing
                    session_end += '+00:00'
                
                end_time = datetime.fromisoformat(session_end.replace('Z', '+00:00'))
                now = datetime.now(timezone.utc)
                
                remaining_seconds = (end_time - now).total_seconds()
                return max(0, int(remaining_seconds))
            
            return 0
        
        except Exception:
            return 0
    
    def _load_session_data(self) -> Optional[Dict[str, Any]]:
        """
        Load session data with fallback priority:
        1. Live session data (always use if exists)
        2. Database current session
        3. None (use fallback display)
        """
        # DISABLED: Skip live session data - daemon is buggy, use database directly
        pass
        
        # Fallback to database current session
        db_data = self._load_database_current_session()
        if db_data:
            db_data['data_source'] = 'database'
            
            # Use model field directly (it contains the full model name)
            if 'model' in db_data:
                db_data['primary_model'] = db_data['model']
            # Fallback to models list if available
            elif db_data.get('models'):
                db_data['primary_model'] = db_data['models'][-1]
            
            # Calculate session end time for display
            if db_data.get('session_start'):
                try:
                    session_start = db_data['session_start']
                    if 'T' in session_start and '+' not in session_start and 'Z' not in session_start:
                        session_start += '+00:00'
                    start_time = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
                    end_time = start_time + timedelta(hours=5)
                    local_end_time = end_time.astimezone()
                    db_data['session_end_time'] = local_end_time.strftime('%H:%M')
                except:
                    pass
            
            # Always calculate real remaining time (ignore database value)
            db_data['remaining_seconds'] = self._calculate_remaining_time(db_data)
            
            # Also update active status based on remaining time  
            db_data['active'] = db_data['remaining_seconds'] > 0
            
            return db_data
        
        return None
    
    def _load_live_session_data(self) -> Optional[Dict[str, Any]]:
        """Load live session data if available"""
        try:
            if not self.live_session_file.exists():
                return None
            
            # Always read fresh data
            with open(self.live_session_file, 'r') as f:
                data = json.load(f)
            
            # Ensure we have actual data with content
            if data and data.get('message_count', 0) >= 0:
                return data
            
            return None
        
        except Exception:
            return None
    
    def _load_database_current_session(self) -> Optional[Dict[str, Any]]:
        """Load current session from database"""
        try:
            if not self.db_file.exists():
                return None
            
            with open(self.db_file, 'r') as f:
                db_data = json.load(f)
            
            return db_data.get('current_session')
        
        except Exception:
            return None
    
    def _get_basic_session_data(self) -> Optional[Dict[str, Any]]:
        """Get basic session data even if not recent"""
        # Try live session data first (even if old)
        live_data = self._load_live_session_data()
        if live_data:
            live_data['data_source'] = 'live_old'
            return live_data
        
        # Try database current session
        db_data = self._load_database_current_session()
        if db_data:
            db_data['data_source'] = 'database_old'
            return db_data
        
        return None
    
    def _is_live_data_recent(self, live_data: Dict[str, Any]) -> bool:
        """Check if live data is recent enough to use"""
        # Not used anymore - we always use live data if it exists
        return True
    
    def _format_session_display(self, session_data: Dict[str, Any]) -> str:
        """Format the main session display using appropriate formatter"""
        try:
            # Check if rotation is enabled
            if self.enable_rotation:
                # Use rotating content
                return self.statusline_rotator.get_rotated_content(session_data)
            else:
                # Use simple visual formatter
                return self.simple_visual_formatter.format_statusline(session_data)
        
        except Exception as e:
            return self._format_error_display(f"Display error: {e}")
    
    def _format_legacy_display(self, session_data: Dict[str, Any]) -> str:
        """Legacy text-only formatting"""
        try:
            # Determine status indicator
            status_indicator = self._get_status_indicator(session_data)
            
            # Session information
            session_number = session_data.get('session_number', '?')
            
            # Model information
            model_info = self._format_model_info(session_data)
            
            # Time remaining
            time_info = self._format_time_info(session_data)
            
            # Usage statistics
            stats_info = self._format_stats_info(session_data)
            
            # Cost information
            cost_info = self._format_cost_info(session_data)
            
            # System information
            system_info = self._format_system_info()
            
            # Combine into final display
            if self.status_format == 'detailed':
                return f"{status_indicator} Session #{session_number} | {model_info} | {time_info} | {stats_info} | {cost_info} | {system_info}"
            elif self.status_format == 'minimal':
                return f"{status_indicator} #{session_number} | {model_info} | {time_info}"
            else:  # compact (default)
                return f"{status_indicator} #{session_number} | {model_info} | {time_info} | {stats_info} | {cost_info}"
        
        except Exception as e:
            return self._format_error_display(f"Legacy display error: {e}")
    
    def _get_status_indicator(self, session_data: Dict[str, Any]) -> str:
        """Get status indicator emoji and text"""
        data_source = session_data.get('data_source', 'unknown')
        is_active = session_data.get('active', False)
        remaining_seconds = session_data.get('remaining_seconds', 0)
        
        if data_source in ['claude_live', 'live_with_claude'] and is_active:
            return "🟢 LIVE"
        elif data_source == 'claude_only' and is_active:
            return "🔵 NEW"
        elif data_source == 'live' and remaining_seconds > 0:
            return "🟢 LIVE"  # Live tracker data is always live
        elif data_source == 'database' and remaining_seconds > 0:
            return "🔄 DB"
        else:
            return "🔴 EXPIRED"
    
    def _format_model_info(self, session_data: Dict[str, Any]) -> str:
        """Format model information with icons and prioritization"""
        # Try 'model' first (from current_session), then 'primary_model' (from work_sessions)
        primary_model = session_data.get('model') or session_data.get('primary_model', 'unknown')
        models = session_data.get('models', [])
        
        # Get model type and icon
        model_type = self._classify_model(primary_model)
        icon = self.model_icons.get(model_type, '🤖')
        
        # Model display name
        model_name = self._get_model_display_name(primary_model)
        
        if len(models) > 1:
            return f"{icon} {model_name} (+{len(models)-1})"
        else:
            return f"{icon} {model_name}"
    
    def _classify_model(self, model: str) -> str:
        """Classify model into type category"""
        model_lower = model.lower()
        
        for model_type, patterns in self.model_patterns.items():
            if any(pattern in model_lower for pattern in patterns):
                return model_type
        
        return 'unknown'
    
    def _get_model_display_name(self, model: str) -> str:
        """Get display name for model from prices.json"""
        # Try to get name from prices.json
        try:
            prices_file = Path(__file__).parent / 'prices.json'
            if prices_file.exists():
                import json
                with open(prices_file, 'r') as f:
                    prices = json.load(f)
                    models = prices.get('models', {})
                    if model in models:
                        return models[model].get('name', model)
        except:
            pass
        
        # Fallback to simple formatting
        return model.replace('claude-', '').replace('-', ' ').title()
    
    def _format_time_info(self, session_data: Dict[str, Any]) -> str:
        """Format time information - shows end time or remaining time"""
        # Prefer showing session end time if available
        session_end_time = session_data.get('session_end_time')
        if session_end_time:
            return f"ends {session_end_time}"
        
        # Fallback to remaining time
        remaining_seconds = session_data.get('remaining_seconds', 0)
        
        if remaining_seconds <= 0:
            return "EXPIRED"
        elif remaining_seconds < 3600:  # Less than 1 hour
            minutes = remaining_seconds // 60
            return f"{minutes}m left"
        else:  # 1 hour or more
            hours = remaining_seconds // 3600
            minutes = (remaining_seconds % 3600) // 60
            return f"{hours}h {minutes}m left"
    
    def _format_stats_info(self, session_data: Dict[str, Any]) -> str:
        """Format usage statistics"""
        message_count = session_data.get('message_count', 0)
        tokens = session_data.get('tokens', 0)
        
        # Format token count
        if tokens >= 1_000_000:
            token_display = f"{tokens/1_000_000:.1f}M"
        elif tokens >= 1_000:
            token_display = f"{tokens/1_000:.1f}K"
        else:
            token_display = str(tokens)
        
        return f"{message_count} msgs | {token_display} tokens"
    
    def _format_cost_info(self, session_data: Dict[str, Any]) -> str:
        """Format cost information"""
        cost = session_data.get('cost', 0.0)
        
        if cost == 0.0:
            return "$0.00"
        elif cost < 0.01:
            return f"${cost:.{self.cost_precision}f}"
        elif cost < 1.0:
            return f"${cost:.4f}"
        else:
            return f"${cost:.2f}"
    
    def _format_system_info(self) -> str:
        """Format system information (git branch, directory, admin status)"""
        info_parts = []
        
        # Git branch
        if self.show_git_branch:
            branch = self._get_git_branch()
            if branch:
                info_parts.append(f"🌿 {branch}")
        
        # Current directory
        try:
            cwd = Path.cwd().name
            if cwd:
                info_parts.append(cwd)
        except:
            pass
        
        # Admin status
        if self.show_admin_status and self._is_admin():
            info_parts.append("👑")
        
        return " | ".join(info_parts) if info_parts else ""
    
    def _get_git_branch(self) -> Optional[str]:
        """Get current git branch"""
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _is_admin(self) -> bool:
        """Check if running as administrator/root"""
        try:
            if sys.platform == 'win32':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False
    
    def _format_fallback_display(self) -> str:
        """Format fallback display when no session data available"""
        system_info = self._format_system_info()
        if system_info:
            return f"💤 No active session | {system_info}"
        else:
            return "💤 No active session"
    
    def _format_error_display(self, error: str) -> str:
        """Format error display for critical failures"""
        return f"⚠️ Claude Statusline Error: {error[:50]}"
    
    def _has_recent_data(self) -> bool:
        """
        Check if we have recent data available for fast display
        
        Returns:
            True if data is fresh enough to skip orchestration
        """
        try:
            # Check if both database and live session files exist and are recent
            if self.db_file.exists() and self.live_session_file.exists():
                db_age = time.time() - self.db_file.stat().st_mtime
                live_age = time.time() - self.live_session_file.stat().st_mtime
                
                # Database should be recent (last 10 minutes)
                # Live session should be very recent (last 5 minutes)
                return db_age < 600 and live_age < 300
            
            return False
            
        except Exception:
            return False
    
    def _has_any_data(self) -> bool:
        """
        Check if we have any data available (recent or old)
        
        Returns:
            True if any data files exist
        """
        try:
            return (
                (self.db_file.exists() and self.db_file.stat().st_size > 0) or
                (self.live_session_file.exists() and self.live_session_file.stat().st_size > 0)
            )
        except Exception:
            return False
    
    def _ensure_daemon_running(self):
        """Ensure unified daemon is running"""
        try:
            # Simple check for daemon status file
            daemon_status_file = self.data_dir / "daemon_status.json"
            
            # If no daemon status file or it's old, try starting daemon
            if not daemon_status_file.exists():
                self._start_daemon()
            else:
                # Check if daemon is still healthy
                try:
                    with open(daemon_status_file, 'r') as f:
                        status = json.load(f)
                    
                    # Check age of status
                    status_time = datetime.fromisoformat(status.get('timestamp', ''))
                    age = (datetime.now(timezone.utc) - status_time).total_seconds()
                    
                    if age > 300:  # 5 minutes
                        self._start_daemon()
                except:
                    self._start_daemon()
        except Exception:
            pass  # Silently fail - statusline should work even without daemon
    
    def _start_daemon(self):
        """Start unified daemon"""
        try:
            script_dir = Path(__file__).parent
            daemon_script = script_dir / "unified_daemon.py"
            
            if not daemon_script.exists():
                return
            
            # Start daemon
            cmd = [sys.executable, str(daemon_script), '--daemon', '--data-dir', str(self.data_dir)]
            
            if sys.platform == 'win32':
                # Windows: Detached process
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                DETACHED_PROCESS = 0x00000008
                CREATE_NO_WINDOW = 0x08000000
                
                subprocess.Popen(
                    cmd,
                    creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS | CREATE_NO_WINDOW,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    cwd=script_dir
                )
            else:
                # Unix: Daemon process
                subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                    cwd=script_dir
                )
        except Exception:
            pass
    
    def _update_session_from_claude_data(self, claude_data: Dict[str, Any]):
        """Update session data from Claude Code live data"""
        try:
            # Load current database
            if not self.db_file.exists():
                return
            
            with open(self.db_file, 'r') as f:
                db_data = json.load(f)
            
            # Get session info from Claude Code
            session_id = claude_data.get('session', {}).get('id', '')
            if not session_id:
                return
            
            # Update current session with live session ID
            current_session = db_data.get('current_session', {})
            if current_session:
                current_session['live_session_id'] = session_id
                
                # Write back to database
                with open(self.db_file, 'w') as f:
                    json.dump(db_data, f, indent=2)
        
        except Exception:
            pass  # Silently fail


def main():
    """Main entry point for statusline display"""
    try:
        # Initialize display system
        display = StatuslineDisplay()
        
        # Read Claude Code JSON input from stdin if available
        claude_session_data = None
        if not sys.stdin.isatty():
            try:
                stdin_data = sys.stdin.read().strip()
                if stdin_data:
                    # Debug: Log what Claude Code is sending us
                    debug_file = display.data_dir / "claude_stdin_debug.json"
                    debug_file.parent.mkdir(exist_ok=True)
                    with open(debug_file, 'w') as f:
                        f.write(stdin_data + '\n')
                    
                    claude_session_data = json.loads(stdin_data)
            except (json.JSONDecodeError, Exception) as e:
                # Log the error too
                debug_file = display.data_dir / "claude_stdin_error.txt"
                with open(debug_file, 'w') as f:
                    f.write(f"Error: {e}\nData: {stdin_data[:500] if 'stdin_data' in locals() else 'No data'}\n")
                # Fallback to standalone mode if JSON parsing fails
                claude_session_data = None
        
        # Generate and output statusline
        output = display.display(timeout=5, claude_data=claude_session_data)
        
        # Use safe printing to handle Unicode issues
        safe_print(output)
        
        return 0
        
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        safe_print(f"⚠️ Statusline Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())