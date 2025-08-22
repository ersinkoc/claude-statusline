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

# Force UTF-8 encoding on Windows for Unicode/nerd font support
if os.name == 'nt' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

try:
    import psutil
except ImportError:
    psutil = None

from .data_directory_utils import resolve_data_directory
from .instance_manager import InstanceManager
from .safe_file_operations import safe_json_read, safe_json_write
from .statusline_rotator import StatuslineRotator
from .unified_powerline_system import UNIFIED_POWERLINE
from .console_utils import safe_print


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
        self.daemon_script = Path(__file__).parent / "daemon.py"
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
        
        # Get template from config
        self.template_name = self.config.get('display', {}).get('template', 'compact')
        
        # Use new enhanced systems
        self.theme_system = UNIFIED_POWERLINE
        # All functionality now in UNIFIED_POWERLINE
        
        # Load selected theme
        theme_config = safe_json_read(self.data_dir / "theme_config.json") or {}
        self.current_theme = theme_config.get('current_theme', 'nord')
        
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
        """Format the main session display using unified powerline system"""
        try:
            # Check if rotation is enabled
            if self.enable_rotation:
                # Use rotating content (keep for compatibility)
                result = self.statusline_rotator.get_rotated_content(session_data)
            else:
                # Use UNIFIED POWERLINE SYSTEM - TEK SİSTEM
                current_theme = UNIFIED_POWERLINE.get_current_theme()
                result = UNIFIED_POWERLINE.render_theme(current_theme)
                
            # Handle Unicode output safely for nerd fonts
            final_result = self._handle_unicode_output(result)
            
            # Keep RGB colors and Unicode - don't strip formatting for nerd fonts
            safe_result = final_result
            
            # Additional Windows console safety
            return self._make_console_safe(safe_result)
        
        except Exception as e:
            return self._format_error_display(f"Display error: {e}")
    
    def _handle_unicode_output(self, text: str) -> str:
        """Handle Unicode output for nerd fonts, bypassing Python encoding limitations"""
        import os
        import sys
        
        # Check if we have nerd font characters (powerline range)
        has_nerd_fonts = any(57344 <= ord(char) <= 63743 or 57520 <= ord(char) <= 57530 for char in text)  # Nerd fonts and powerline ranges
        
        if has_nerd_fonts and os.name == 'nt':
            # Force UTF-8 output for Windows with nerd fonts
            try:
                if hasattr(sys.stdout, 'buffer'):
                    # Output directly to buffer with UTF-8 encoding
                    encoded = text.encode('utf-8')
                    sys.stdout.buffer.write(encoded)
                    sys.stdout.buffer.write(b'\n')  # Add newline
                    sys.stdout.buffer.flush()
                    
                    # Always return the actual text for processing
                    return text  # Let both Claude Code and terminal see the content
            except Exception:
                pass
        
        return text
    
    def _make_claude_code_safe(self, text: str) -> str:
        """Make output safe for Claude Code consumption by removing complex formatting"""
        import re
        
        # Remove RGB color codes (\033[48;2;r;g;b;m format)
        text = re.sub(r'\x1b\[48;2;\d+;\d+;\d+m', '', text)  # Background RGB
        text = re.sub(r'\x1b\[38;2;\d+;\d+;\d+m', '', text)  # Foreground RGB
        
        # Remove ANSI color codes
        text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        
        # Only remove truly problematic nerd font characters if needed
        # Keep basic powerline characters for modern terminals
        very_problematic_chars = {
            # Only remove these if they cause real issues
        }
        
        for unicode_char, replacement in very_problematic_chars.items():
            text = text.replace(unicode_char, replacement)
        
        # Clean up multiple spaces but preserve newlines
        text = re.sub(r'[ \t]+', ' ', text)  # Only collapse spaces/tabs, not newlines
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        # If result is empty or too complex for Claude Code, optimize it
        if not text:
            return "Claude AI | No data"
        elif len(text) > 400:
            # For very long themes (RGB), create compact version for Claude Code
            return self._create_compact_version(text)
        elif len(text) > 200:
            # Remove ANSI codes but keep content for Claude Code compatibility
            import re
            clean_text = re.sub(r'\x1b\[[0-9;]*m', '', text)
            if len(clean_text) <= 200:
                return clean_text
            else:
                return self._create_compact_version(text)
        
        return text
    
    def _create_compact_version(self, text: str) -> str:
        """Create compact version of complex themes for Claude Code"""
        import re
        
        # Extract content from ANSI codes and emojis
        clean_text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        
        # Extract key information using regex patterns
        model_match = re.search(r'[🚀⚡💻🎮]\s*([A-Za-z0-9-]+)', clean_text)
        folder_match = re.search(r'[📁🏠🌌]\s*([A-Za-z0-9-_/\\]+)', clean_text)
        branch_match = re.search(r'[🌿⭐🔗]\s*([A-Za-z0-9-_/]+)', clean_text)
        messages_match = re.search(r'[💬🛸⚔️]\s*(\d+)', clean_text)
        cost_match = re.search(r'[\$💰💸]\s*([0-9.]+)', clean_text)
        
        # Build compact version with key info
        parts = []
        if model_match:
            parts.append(f"⚡ {model_match.group(1)}")
        if folder_match:
            parts.append(f"📁 {folder_match.group(1)}")
        if messages_match:
            parts.append(f"💬 {messages_match.group(1)}m")
        if cost_match:
            parts.append(f"💰 ${cost_match.group(1)}")
            
        if parts:
            return " ▶ ".join(parts)
        else:
            # Ultimate fallback - use basic data
            return "⚡ Claude ▶ 📁 Project ▶ 💬 Messages ▶ 💰 Cost"
    
    def _make_console_safe(self, text: str) -> str:
        """Smart console safety - only replace truly problematic characters"""
        # Only replace emojis and complex Unicode that cause real problems
        emoji_replacements = {
            '⚔️': '[S]',   # Crossed swords (emoji)
            '🔧': '[T]',   # Wrench (emoji) 
            '📊': '[C]',   # Chart (emoji)
            '💾': '[D]',   # Disk (emoji)
            '🔬': '[L]',   # Microscope (emoji)
            '📈': '[U]',   # Chart up (emoji)
            '₿': '$',      # Bitcoin (problematic encoding)
        }
        
        # Replace only problematic emojis
        for emoji, replacement in emoji_replacements.items():
            text = text.replace(emoji, replacement)
        
        # FORCE UNICODE: Always keep nerd fonts and powerline characters
        # We handle encoding issues with direct UTF-8 buffer output
        return text  # Always preserve Unicode characters
    
    def _build_comprehensive_theme_data(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive theme data with all available fields for professional themes"""
        import datetime
        
        # Basic session data
        # Handle both 'model' and 'primary_model' field names
        model = session_data.get('model', session_data.get('primary_model', 'Claude'))
        model_version = session_data.get('model_version', '4.1')
        messages = session_data.get('message_count', 0)
        # Handle both 'tokens' and 'total_tokens' field names
        total_tokens = session_data.get('tokens', session_data.get('total_tokens', 0))
        cost = session_data.get('cost', 0.0)
        
        # Token breakdown
        input_tokens = session_data.get('input_tokens', total_tokens // 2)
        output_tokens = session_data.get('output_tokens', total_tokens // 2)
        cache_read = session_data.get('cache_read_tokens', 0)
        cache_write = session_data.get('cache_write_tokens', 0)
        
        # Calculated metrics
        tokens_per_msg = int(total_tokens / max(messages, 1)) if messages > 0 else 0
        cost_per_msg = cost / max(messages, 1) if messages > 0 else 0.0
        efficiency = min(95, 70 + (messages * 2)) if messages > 0 else 0
        cache_hit_rate = int(cache_read / max(total_tokens, 1) * 100) if total_tokens > 0 else 0
        
        # Session info
        session_start = session_data.get('session_start', datetime.datetime.now(datetime.timezone.utc))
        if isinstance(session_start, str):
            try:
                session_start = datetime.datetime.fromisoformat(session_start.replace('Z', '+00:00'))
            except:
                session_start = datetime.datetime.now(datetime.timezone.utc)
        
        session_duration = datetime.datetime.now(datetime.timezone.utc) - session_start
        uptime_str = f"{int(session_duration.total_seconds() // 3600)}:{int((session_duration.total_seconds() % 3600) // 60):02d}"
        
        # Quality metrics (simulated based on session activity)
        coherence = min(95, 60 + (messages * 3))
        relevance = min(98, 65 + (messages * 2.5))
        creativity = min(90, 55 + (messages * 2))
        
        # Performance metrics (simulated)
        avg_response_time = 200 + (tokens_per_msg // 10)  # Simulate response time
        memory_usage = 25 + (messages % 40)  # Simulate memory usage
        
        # Productivity metrics
        productivity_level = "High" if efficiency > 80 else "Good" if efficiency > 60 else "Low"
        performance_level = "Good" if avg_response_time < 300 else "Slow"
        
        # System metrics (simulated for themes)
        import os
        import random
        import subprocess
        
        # Get folder name
        current_folder = os.path.basename(os.getcwd())
        
        # CPU and RAM (simulated for demo - can be made real with psutil)
        cpu_usage = random.randint(15, 85)
        ram_usage = random.randint(35, 90)
        
        # Git branch (if available)
        git_branch = "main"  # Default
        try:
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, timeout=1)
            if result.returncode == 0 and result.stdout.strip():
                git_branch = result.stdout.strip()
        except:
            git_branch = "main"
            
        # Session time remaining (5 hour sessions)
        session_remaining = max(0, 5*3600 - session_duration.total_seconds())
        time_left = f"{int(session_remaining//3600)}h{int((session_remaining%3600)//60)}m"
        
        # Network status (simulated)
        network_status = random.choice(["Online", "Sync", "Fast"])
        network_latency = random.randint(15, 120)
        
        return {
            # Basic data
            "model": model,
            "model_version": model_version,
            "messages": str(messages),
            "tokens": f"{total_tokens/1000:.1f}k",
            "cost": f"{cost:.1f}",
            
            # Token breakdown
            "input_tokens": input_tokens,
            "output_tokens": output_tokens, 
            "cache_read": cache_read,
            "cache_write": cache_write,
            "tokens_per_msg": tokens_per_msg,
            "cost_per_msg": f"{cost_per_msg:.3f}",
            
            # Performance metrics
            "efficiency": f"{efficiency}%",
            "cache_hit_rate": f"{cache_hit_rate}%",
            "avg_response_time": f"{avg_response_time}ms",
            "memory_usage": f"{memory_usage}%",
            
            # Session metrics
            "session_time": uptime_str,
            "session_number": f"#{session_data.get('session_number', '1')}",
            "uptime": uptime_str,
            "performance": performance_level,
            "productivity": productivity_level,
            
            # Quality scores
            "coherence": f"{coherence}%",
            "relevance": f"{relevance}%", 
            "creativity": f"{creativity}%",
            "quality_score": f"{(coherence + relevance + creativity) // 3}%",
            
            # Extended formatting
            "session_id": session_data.get('session_id', '561'),
            "sessions": "1",
            
            # Missing multiline fields
            "session_quality": performance_level,
            "tokens_formatted": f"{total_tokens/1000:.1f}k",
            "cache_tokens": cache_read + cache_write,
            "response_time": f"{avg_response_time}ms",
            "cache_hits": f"{cache_hit_rate}%",
            "cache_efficiency": f"{cache_hit_rate}%",  # Add cache_efficiency field
            
            # New extended fields for epic themes
            "folder": current_folder,
            "folder_name": current_folder,
            "project": current_folder,
            "git_branch": git_branch,
            "branch": git_branch,
            "cpu": str(cpu_usage),  # Don't add % here, templates will add it
            "cpu_usage": f"{cpu_usage}%",
            "ram": str(ram_usage),  # Don't add % here, templates will add it
            "ram_usage": f"{ram_usage}%",
            "memory": f"{ram_usage}%",
            "time_left": time_left,
            "session_remaining": time_left,
            "remaining": time_left,
            "network": network_status,
            "latency": f"{network_latency}ms",
            "ping": f"{network_latency}ms",
            
            # Model shorthand versions
            "model_short": model.replace("claude-", "").replace("opus", "Op").replace("sonnet", "So").replace("haiku", "Hk"),
            "model_name": model.split('-')[0] if '-' in model else model,
            
            # Short versions for compact themes
            "msg": str(messages),
            "tok": f"{total_tokens//1000}k",
            "sess": uptime_str,
            "eff": f"{efficiency}%",
            "qual": f"{(coherence + relevance + creativity) // 3}%"
        }
    
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
                import select
                # Check if there's data available (with timeout)
                if sys.platform == 'win32':
                    # Windows doesn't support select on stdin
                    # Skip stdin reading on Windows when called from CLI
                    stdin_data = ""
                else:
                    # Unix/Linux - use select with timeout
                    ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                    if ready:
                        stdin_data = sys.stdin.read().strip()
                    else:
                        stdin_data = ""
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
        
        # Handle Unicode output for ALL themes with nerd fonts
        has_powerline_chars = any(57344 <= ord(char) <= 63743 or 57520 <= ord(char) <= 57530 for char in output)
        
        if has_powerline_chars:
            # Unicode output was already sent to console via _handle_unicode_output
            # No need to print again - would cause double output or encoding issues
            pass
        elif output == "[Powerline theme active]":
            # Unicode output was already sent directly to console
            pass
        else:
            # ASCII content or non-powerline Unicode - use safe print
            safe_print(output)
        
        return 0
        
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        safe_print(f"⚠️ Statusline Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())