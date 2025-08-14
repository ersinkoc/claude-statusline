#!/usr/bin/env python3
"""
Unified Daemon for Claude Statusline System

SINGLE DAEMON - MANAGES ALL OPERATIONS:
- Continuously parses JSONL files
- Keeps smart_sessions_db.json up to date
- Writes active session data to live_session.json
- Manages all data processing and analysis operations
"""

import os
import sys
import time
import json
import threading
import logging
import signal
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List
import subprocess

from .instance_manager import InstanceManager
from .rebuild import DatabaseRebuilder
from .data_directory_utils import resolve_data_directory
from .safe_file_operations import safe_json_read, safe_json_write


class UnifiedDaemon:
    """Single daemon - manages all operations"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.running = False
        self.threads = []
        
        # File paths
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.live_session_file = self.data_dir / "live_session.json"
        self.daemon_status_file = self.data_dir / "daemon_status.json"
        self.log_file = self.data_dir / "unified_daemon.log"
        
        # Instance manager
        self.instance_manager = InstanceManager('unified_daemon', self.data_dir)
        
        # Configuration
        self.db_update_interval = 60  # 1 minute for faster updates
        self.live_update_interval = 30  # 30 seconds
        self.status_update_interval = 10  # 10 seconds
        
        # Thread events
        self.stop_event = threading.Event()
        
        # Setup logging
        self._setup_logging()
        
        # Last update times
        self.last_db_update = 0
        self.last_live_update = 0
        
        # Current session tracking
        self.current_session = None
        self.session_start_time = None
        
    def _setup_logging(self):
        """Setup daemon logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler() if '--debug' in sys.argv else logging.NullHandler()
            ]
        )
        self.logger = logging.getLogger('unified_daemon')
        
    def start(self) -> bool:
        """Start the daemon"""
        try:
            # Single instance check
            if not self.instance_manager.ensure_single_instance():
                self.logger.warning("Another daemon instance is already running")
                return False
            
            self.logger.info("Starting Unified Daemon")
            self.running = True
            
            # Setup signal handlers
            signal.signal(signal.SIGTERM, self._signal_handler)
            signal.signal(signal.SIGINT, self._signal_handler)
            
            # Start worker threads
            self._start_workers()
            
            # Main loop
            self._main_loop()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start daemon: {e}")
            return False
            
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
        
    def stop(self):
        """Stop the daemon"""
        self.logger.info("Stopping daemon...")
        self.running = False
        self.stop_event.set()
        
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=5)
        
        # Cleanup
        self.instance_manager.cleanup()
        self.logger.info("Daemon stopped")
        
    def _start_workers(self):
        """Start all worker threads"""
        # Database updater thread
        db_thread = threading.Thread(target=self._database_updater, daemon=True)
        db_thread.start()
        self.threads.append(db_thread)
        
        # Live session tracker thread
        live_thread = threading.Thread(target=self._live_session_tracker, daemon=True)
        live_thread.start()
        self.threads.append(live_thread)
        
        # Status writer thread
        status_thread = threading.Thread(target=self._status_writer, daemon=True)
        status_thread.start()
        self.threads.append(status_thread)
        
        self.logger.info("All worker threads started")
        
    def _main_loop(self):
        """Main daemon loop"""
        while self.running:
            try:
                # Main loop can handle special tasks or just sleep
                time.sleep(1)
                
                # Check if threads are still alive
                for thread in self.threads:
                    if not thread.is_alive():
                        self.logger.error(f"Thread {thread.name} died, restarting...")
                        # Could restart thread here if needed
                        
            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                
    def _database_updater(self):
        """Database update worker thread"""
        self.logger.info("Database updater thread started")
        
        while not self.stop_event.is_set():
            try:
                current_time = time.time()
                
                # Check if update needed
                if current_time - self.last_db_update >= self.db_update_interval:
                    self.logger.info("Updating database...")
                    
                    # Use DatabaseRebuilder to update from JSONL files
                    try:
                        rebuilder = DatabaseRebuilder(data_dir=self.data_dir)
                        rebuilder.rebuild_database()
                        self.last_db_update = current_time
                        self.logger.info("Database updated successfully")
                    except Exception as e:
                        self.logger.error(f"Database update failed: {e}")
                        
                # Sleep for a bit
                self.stop_event.wait(30)
                
            except Exception as e:
                self.logger.error(f"Error in database updater: {e}")
                self.stop_event.wait(60)
                
    def _live_session_tracker(self):
        """Live session tracking worker thread - extracts live data from database"""
        self.logger.info("Live session tracker thread started")
        
        while not self.stop_event.is_set():
            try:
                # Get current session from database
                session_info = self._get_current_session_from_db()
                
                if session_info:
                    # Calculate real-time metrics
                    start_time = datetime.fromisoformat(session_info["start_time"].replace("Z", "+00:00"))
                    duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                    
                    # Update live session file with extracted data
                    live_data = {
                        "session_id": session_info.get("session_id"),
                        "model": session_info.get("model", "Unknown"),
                        "start_time": session_info.get("start_time"),
                        "duration_seconds": int(duration),
                        "token_count": session_info.get("total_tokens", 0),
                        "cost_usd": session_info.get("total_cost", 0.0),
                        "messages": session_info.get("message_count", 0),
                        "last_update": datetime.now(timezone.utc).isoformat(),
                        "is_active": True,
                        "today_stats": self._get_today_stats()
                    }
                    
                    # Write to file
                    safe_json_write(live_data, self.live_session_file)
                    self.last_live_update = time.time()
                    
                else:
                    # No active session - still provide today's stats
                    live_data = {
                        "is_active": False,
                        "last_update": datetime.now(timezone.utc).isoformat(),
                        "today_stats": self._get_today_stats()
                    }
                    safe_json_write(live_data, self.live_session_file)
                            
                # Sleep for interval
                self.stop_event.wait(self.live_update_interval)
                
            except Exception as e:
                self.logger.error(f"Error in live session tracker: {e}")
                self.stop_event.wait(60)
                
    def _get_current_session_from_db(self) -> Optional[Dict[str, Any]]:
        """Get current active session from database"""
        try:
            if not self.db_file.exists():
                return None
                
            db_data = safe_json_read(self.db_file)
            if not db_data or "sessions" not in db_data:
                return None
                
            # Find active session (most recent within last 2 hours)
            sessions = db_data["sessions"]
            if not sessions:
                return None
                
            # Get most recent session
            now = datetime.now(timezone.utc)
            for session in sorted(sessions, key=lambda s: s.get("start_time", ""), reverse=True):
                if "start_time" in session:
                    start_time = datetime.fromisoformat(session["start_time"].replace("Z", "+00:00"))
                    age = now - start_time
                    
                    # Consider active if within last 2 hours and no end_time
                    if age < timedelta(hours=2) and not session.get("end_time"):
                        return session
                        
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting current session: {e}")
            return None
            
    def _get_today_stats(self) -> Dict[str, Any]:
        """Get today's statistics from database"""
        try:
            if not self.db_file.exists():
                return {"sessions": 0, "cost": 0.0, "tokens": 0}
                
            db_data = safe_json_read(self.db_file)
            if not db_data:
                return {"sessions": 0, "cost": 0.0, "tokens": 0}
                
            stats = db_data.get("statistics", {}).get("today", {})
            return {
                "sessions": stats.get("session_count", 0),
                "cost": stats.get("total_cost", 0.0),
                "tokens": stats.get("total_tokens", 0)
            }
            
        except Exception:
            return {"sessions": 0, "cost": 0.0, "tokens": 0}
            
    def _status_writer(self):
        """Write daemon status periodically"""
        self.logger.info("Status writer thread started")
        
        while not self.stop_event.is_set():
            try:
                status = {
                    "daemon": "unified_daemon",
                    "version": "1.0.0",
                    "running": True,
                    "pid": os.getpid(),
                    "start_time": datetime.now(timezone.utc).isoformat(),
                    "last_db_update": self.last_db_update,
                    "last_live_update": self.last_live_update,
                    "threads": {
                        "database_updater": self.threads[0].is_alive() if len(self.threads) > 0 else False,
                        "live_tracker": self.threads[1].is_alive() if len(self.threads) > 1 else False,
                        "status_writer": True
                    },
                    "files": {
                        "database": self.db_file.exists(),
                        "live_session": self.live_session_file.exists()
                    }
                }
                
                safe_json_write(status, self.daemon_status_file)
                
                # Sleep for interval
                self.stop_event.wait(self.status_update_interval)
                
            except Exception as e:
                self.logger.error(f"Error writing status: {e}")
                self.stop_event.wait(60)
                

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Unified Daemon for Claude Statusline')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    parser.add_argument('--stop', action='store_true', help='Stop running daemon')
    parser.add_argument('--status', action='store_true', help='Show daemon status')
    parser.add_argument('--restart', action='store_true', help='Restart daemon')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--data-dir', type=str, help='Data directory path')
    
    args = parser.parse_args()
    
    data_dir = Path(args.data_dir) if args.data_dir else None
    
    if args.stop or args.restart:
        # Stop existing daemon
        print("Stopping existing daemon...")
        instance_manager = InstanceManager('unified_daemon', resolve_data_directory(data_dir))
        if instance_manager.force_release():
            print("Daemon stopped")
        else:
            print("No daemon was running")
            
        if args.stop:
            return
            
    if args.status:
        # Show status
        status_file = resolve_data_directory(data_dir) / "daemon_status.json"
        if status_file.exists():
            status = safe_json_read(status_file)
            print(json.dumps(status, indent=2))
        else:
            print("Daemon is not running")
        return
        
    if args.daemon or args.restart:
        # Run as daemon
        if sys.platform == 'win32':
            # Windows: Run in background
            if not args.debug:
                # Detach from console
                import subprocess
                cmd = [sys.executable, __file__, '--daemon', '--debug']
                if args.data_dir:
                    cmd.extend(['--data-dir', args.data_dir])
                    
                subprocess.Popen(
                    cmd,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL
                )
                print("Daemon started in background")
                return
                
        daemon = UnifiedDaemon(data_dir=data_dir)
        daemon.start()
        
    else:
        parser.print_help()
        

if __name__ == "__main__":
    main()