#!/usr/bin/env python3
"""
Background Daemon for Claude Statusline
Continuously updates the database every 60 seconds
"""

import sys
import os
import time
import json
import threading
import signal
from pathlib import Path
from datetime import datetime, timezone

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_statusline.data_directory_utils import resolve_data_directory
from claude_statusline.safe_file_operations import safe_json_read, safe_json_write
from claude_statusline.rebuild import DatabaseRebuilder


class DaemonService:
    """Background daemon service"""
    
    def __init__(self):
        self.data_dir = resolve_data_directory()
        self.lock_file = self.data_dir / ".unified_daemon.lock"
        self.status_file = self.data_dir / "daemon_status.json"
        self.running = False
        self.rebuilder = DatabaseRebuilder()
        self.update_interval = 60  # seconds
        
    def start(self):
        """Start the daemon"""
        print("🚀 Starting Claude Statusline Daemon...")
        
        # Check if already running
        if self.is_running():
            print("⚠️ Daemon is already running")
            return False
            
        # Create lock file with PID
        try:
            pid = os.getpid()
            safe_json_write({"pid": pid, "started": datetime.now(timezone.utc).isoformat()}, self.lock_file)
            
            # Register signal handlers
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            self.running = True
            print(f"✓ Daemon started (PID: {pid})")
            
            # Start update loop
            self._update_loop()
            
        except Exception as e:
            print(f"✗ Failed to start daemon: {e}")
            return False
            
        return True
        
    def stop(self):
        """Stop the daemon"""
        print("🛑 Stopping daemon...")
        self.running = False
        
        # Remove lock file
        if self.lock_file.exists():
            try:
                self.lock_file.unlink()
                print("✓ Daemon stopped")
            except Exception as e:
                print(f"⚠️ Could not remove lock file: {e}")
                
    def is_running(self):
        """Check if daemon is running"""
        if not self.lock_file.exists():
            return False
            
        try:
            lock_data = safe_json_read(self.lock_file)
            if not isinstance(lock_data, dict) or "pid" not in lock_data:
                return False
        except Exception:
            # Lock file is corrupted or unreadable
            return False
            
        pid = lock_data["pid"]
        
        # Check if process exists
        try:
            if sys.platform == "win32":
                try:
                    import psutil
                    return psutil.pid_exists(pid)
                except ImportError:
                    import subprocess
                    result = subprocess.run(
                        ["tasklist", "/FI", f"PID eq {pid}"],
                        capture_output=True,
                        text=True
                    )
                    # Check for exact PID match to avoid partial matches
                    for line in result.stdout.strip().splitlines():
                        parts = line.split()
                        if len(parts) >= 2 and parts[1] == str(pid):
                            return True
                    return False
            else:
                os.kill(pid, 0)
                return True
        except (OSError, ProcessLookupError, Exception):
            # Process doesn't exist, clean up lock
            if self.lock_file.exists():
                try:
                    self.lock_file.unlink()
                except Exception:
                    pass
            return False
            
    def _update_loop(self):
        """Main update loop"""
        while self.running:
            try:
                # Update status
                self._update_status("running")
                
                # Rebuild database
                print(f"🔄 Updating database... ({datetime.now(timezone.utc).strftime('%H:%M:%S')})")
                if self.rebuilder.rebuild_database():
                    print("✓ Database updated successfully")
                else:
                    print("⚠️ Database update failed")
                    
                # Wait for next update (check running flag every 5 seconds)
                elapsed = 0
                while elapsed < self.update_interval and self.running:
                    sleep_chunk = min(5, self.update_interval - elapsed)
                    time.sleep(sleep_chunk)
                    elapsed += sleep_chunk
                    
            except Exception as e:
                print(f"⚠️ Update error: {e}")
                time.sleep(5)  # Wait before retry
                
    def _update_status(self, status):
        """Update daemon status file"""
        status_data = {
            "status": status,
            "pid": os.getpid(),
            "last_update": datetime.now(timezone.utc).isoformat(),
            "update_interval": self.update_interval
        }
        safe_json_write(status_data, self.status_file)
        
    def _signal_handler(self, signum, frame):
        """Handle termination signals"""
        print(f"\n📍 Received signal {signum}")
        self.stop()
        sys.exit(0)


def main():
    """Main entry point for daemon"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Statusline Daemon")
    parser.add_argument("--start", action="store_true", help="Start daemon")
    parser.add_argument("--stop", action="store_true", help="Stop daemon")
    parser.add_argument("--status", action="store_true", help="Check daemon status")
    parser.add_argument("--restart", action="store_true", help="Restart daemon")
    
    args = parser.parse_args()
    
    daemon = DaemonService()
    
    if args.start:
        daemon.start()
    elif args.stop:
        daemon.stop()
    elif args.status:
        if daemon.is_running():
            print("✓ Daemon is running")
            try:
                status = safe_json_read(daemon.status_file)
            except Exception:
                status = None
            if status:
                print(f"  PID: {status.get('pid', 'unknown')}")
                print(f"  Last update: {status.get('last_update', 'unknown')}")
        else:
            print("✗ Daemon is not running")
    elif args.restart:
        daemon.stop()
        time.sleep(2)
        daemon.start()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()