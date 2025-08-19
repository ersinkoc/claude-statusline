#!/usr/bin/env python3
"""
Instance Manager for Claude Statusline System

Provides single-instance enforcement using PID-based file locking to prevent
race conditions and data corruption when multiple Claude Code windows
simultaneously trigger statusline operations.

Key Features:
- Cross-platform file locking (Windows msvcrt, Unix fcntl)
- Stale lock detection and cleanup
- Process validation to ensure legitimate locks
- Atomic lock file operations
- Graceful cleanup and error handling
"""

import os
import sys
import time
import tempfile
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Platform-specific imports
if sys.platform == 'win32':
    import msvcrt
else:
    import fcntl

import psutil


class InstanceManager:
    """
    Manages single instance enforcement for system components
    
    Uses PID-based file locking to ensure only one instance of critical
    components runs at a time, preventing data corruption and race conditions.
    """
    
    def __init__(self, component_name: str, lock_dir: Optional[Path] = None):
        """
        Initialize instance manager for a specific component
        
        Args:
            component_name: Unique identifier for the component (e.g., 'database_builder')
            lock_dir: Directory for lock files (defaults to current directory)
        """
        self.component_name = component_name
        self.lock_dir = lock_dir or Path.cwd()
        self.lock_file_path = self.lock_dir / f".{component_name}.lock"
        self.lock_file = None
        self.current_pid = os.getpid()
        
        # Ensure lock directory exists
        self.lock_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger(f"instance_manager.{component_name}")
    
    def ensure_single_instance(self) -> bool:
        """
        Ensure only one instance of this component is running
        
        Returns:
            True if this instance acquired the lock successfully
            False if another instance is already running
        """
        try:
            # Check for existing lock
            if self._is_locked_by_other_process():
                self.logger.info(f"Another instance of {self.component_name} is already running")
                return False
            
            # Attempt to acquire lock
            return self._acquire_lock()
            
        except Exception as e:
            self.logger.error(f"Failed to ensure single instance: {e}")
            return False
    
    def _is_locked_by_other_process(self) -> bool:
        """
        Check if lock file exists and is held by a running process
        
        Returns:
            True if another process holds the lock
            False if no valid lock exists
        """
        if not self.lock_file_path.exists():
            return False
        
        try:
            # Read PID from lock file
            with open(self.lock_file_path, 'r') as f:
                lock_data = f.read().strip()
            
            if not lock_data:
                # Empty lock file - remove it
                self._cleanup_stale_lock()
                return False
            
            # Parse lock data (format: PID:TIMESTAMP:COMPONENT)
            parts = lock_data.split(':')
            if len(parts) < 2:
                # Invalid format - remove stale lock
                self._cleanup_stale_lock()
                return False
            
            lock_pid = int(parts[0])
            lock_timestamp = float(parts[1])
            
            # Check if it's our own process
            if lock_pid == self.current_pid:
                return False
            
            # Check if the process is still running
            if self._is_process_running(lock_pid):
                # Verify the lock isn't too old (24 hours max)
                if time.time() - lock_timestamp > 86400:  # 24 hours
                    self.logger.warning(f"Lock held by PID {lock_pid} is very old, cleaning up")
                    self._cleanup_stale_lock()
                    return False
                return True
            else:
                # Process not running - clean up stale lock
                self.logger.info(f"Cleaning up stale lock from PID {lock_pid}")
                self._cleanup_stale_lock()
                return False
                
        except (ValueError, FileNotFoundError, PermissionError) as e:
            self.logger.warning(f"Error reading lock file: {e}, cleaning up")
            self._cleanup_stale_lock()
            return False
    
    def _is_process_running(self, pid: int) -> bool:
        """
        Check if a process with given PID is currently running
        
        Args:
            pid: Process ID to check
            
        Returns:
            True if process is running, False otherwise
        """
        try:
            return psutil.pid_exists(pid)
        except Exception:
            # Fallback to os-level check if psutil fails
            try:
                if sys.platform == 'win32':
                    # Windows: try to open the process
                    import ctypes
                    handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
                    if handle:
                        ctypes.windll.kernel32.CloseHandle(handle)
                        return True
                    return False
                else:
                    # Unix: send signal 0 (doesn't actually send signal, just checks if process exists)
                    os.kill(pid, 0)
                    return True
            except (OSError, ProcessLookupError):
                return False
    
    def _acquire_lock(self) -> bool:
        """
        Acquire the lock file for this instance
        
        Returns:
            True if lock was successfully acquired
            False if lock acquisition failed
        """
        try:
            # Create lock data
            lock_data = f"{self.current_pid}:{time.time()}:{self.component_name}"
            
            # Use atomic write operation
            temp_path = self.lock_file_path.with_suffix('.tmp')
            
            # Write to temporary file first
            with open(temp_path, 'w') as f:
                f.write(lock_data)
                f.flush()
                os.fsync(f.fileno())  # Force write to disk
            
            # Atomic rename
            if sys.platform == 'win32':
                # Windows requires removing target first
                if self.lock_file_path.exists():
                    os.remove(self.lock_file_path)
                os.rename(temp_path, self.lock_file_path)
            else:
                # Unix supports atomic rename
                os.rename(temp_path, self.lock_file_path)
            
            # Try to open the lock file for monitoring
            try:
                self.lock_file = open(self.lock_file_path, 'r+')
                if sys.platform != 'win32':
                    # Apply file lock on Unix systems
                    fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                else:
                    # Windows file locking
                    msvcrt.locking(self.lock_file.fileno(), msvcrt.LK_NBLCK, 1)
            except (OSError, IOError):
                # Lock file manipulation failed - another process might have acquired it
                self.lock_file = None
                return False
            
            self.logger.debug(f"Successfully acquired lock for {self.component_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to acquire lock: {e}")
            # Cleanup temporary file if it exists
            temp_path = self.lock_file_path.with_suffix('.tmp')
            if temp_path.exists():
                try:
                    os.remove(temp_path)
                except:
                    pass
            return False
    
    def _cleanup_stale_lock(self):
        """Remove stale lock file"""
        try:
            if self.lock_file_path.exists():
                # On Windows, try multiple methods to remove the file
                if sys.platform == 'win32':
                    try:
                        # First try normal removal
                        os.remove(self.lock_file_path)
                    except PermissionError:
                        # Try to forcefully unlock and remove
                        try:
                            import subprocess
                            # Use Windows handle.exe to force close file handles (if available)
                            subprocess.run(['cmd', '/c', f'del /f /q "{self.lock_file_path}"'], 
                                         capture_output=True, timeout=2)
                        except:
                            # Last resort: rename the file to a temp name
                            temp_name = self.lock_file_path.with_suffix('.old')
                            try:
                                os.rename(self.lock_file_path, temp_name)
                                os.remove(temp_name)
                            except:
                                pass
                else:
                    os.remove(self.lock_file_path)
                self.logger.debug(f"Cleaned up stale lock file: {self.lock_file_path}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup stale lock: {e}")
    
    def cleanup(self):
        """
        Release the lock and cleanup resources
        
        Should be called when the component shuts down gracefully
        """
        try:
            if self.lock_file:
                try:
                    if sys.platform != 'win32':
                        fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
                    else:
                        msvcrt.locking(self.lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                except:
                    pass  # Lock might already be released
                
                self.lock_file.close()
                self.lock_file = None
            
            # Remove lock file if it's ours
            if self.lock_file_path.exists():
                try:
                    with open(self.lock_file_path, 'r') as f:
                        lock_data = f.read().strip()
                    
                    if lock_data.startswith(f"{self.current_pid}:"):
                        os.remove(self.lock_file_path)
                        self.logger.debug(f"Cleaned up lock file for {self.component_name}")
                except:
                    pass  # Best effort cleanup
                    
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def is_locked(self) -> bool:
        """
        Check if this instance currently holds the lock
        
        Returns:
            True if this instance holds the lock
        """
        return self.lock_file is not None and not self.lock_file.closed
    
    def get_lock_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the current lock holder
        
        Returns:
            Dictionary with lock information or None if no lock exists
        """
        if not self.lock_file_path.exists():
            return None
        
        try:
            with open(self.lock_file_path, 'r') as f:
                lock_data = f.read().strip()
            
            parts = lock_data.split(':')
            if len(parts) >= 3:
                pid = int(parts[0])
                timestamp = float(parts[1])
                component = parts[2]
                
                return {
                    'pid': pid,
                    'timestamp': timestamp,
                    'component': component,
                    'age_seconds': time.time() - timestamp,
                    'process_running': self._is_process_running(pid),
                    'is_current_process': pid == self.current_pid
                }
        except Exception as e:
            self.logger.warning(f"Failed to parse lock info: {e}")
        
        return None
    
    def force_release(self) -> bool:
        """
        Force release the lock (use with caution)
        
        This should only be used by administrative tools or in emergency situations.
        
        Returns:
            True if lock was successfully removed
        """
        try:
            if self.lock_file:
                self.cleanup()
            
            if self.lock_file_path.exists():
                # On Windows, try multiple methods to remove the file
                if sys.platform == 'win32':
                    try:
                        os.remove(self.lock_file_path)
                    except PermissionError:
                        # Try Windows-specific force removal
                        try:
                            import subprocess
                            result = subprocess.run(['cmd', '/c', f'del /f /q "{self.lock_file_path}"'], 
                                                  capture_output=True, timeout=2)
                            if result.returncode != 0:
                                # Try renaming as last resort
                                temp_name = self.lock_file_path.with_suffix('.old')
                                os.rename(self.lock_file_path, temp_name)
                                try:
                                    os.remove(temp_name)
                                except:
                                    pass  # At least we renamed it
                        except Exception as e:
                            self.logger.error(f"Windows force removal failed: {e}")
                            return False
                else:
                    os.remove(self.lock_file_path)
                    
                self.logger.warning(f"Forcibly removed lock for {self.component_name}")
                return True
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to force release lock: {e}")
            return False
    
    def __enter__(self):
        """Context manager entry"""
        if self.ensure_single_instance():
            return self
        else:
            raise RuntimeError(f"Another instance of {self.component_name} is already running")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()


def main():
    """Test and demonstration of InstanceManager"""
    logging.basicConfig(level=logging.DEBUG)
    
    print("Testing InstanceManager...")
    
    # Test basic functionality
    manager = InstanceManager("test_component")
    
    if manager.ensure_single_instance():
        print("✅ Successfully acquired lock")
        
        # Test lock info
        info = manager.get_lock_info()
        if info:
            print(f"Lock info: PID={info['pid']}, Age={info['age_seconds']:.1f}s")
        
        # Simulate some work
        print("Simulating work for 2 seconds...")
        time.sleep(2)
        
        # Test second instance
        manager2 = InstanceManager("test_component")
        if not manager2.ensure_single_instance():
            print("✅ Second instance correctly rejected")
        else:
            print("❌ Second instance should have been rejected")
            manager2.cleanup()
        
        # Cleanup
        manager.cleanup()
        print("✅ Lock cleaned up")
        
        # Test acquisition after cleanup
        if manager.ensure_single_instance():
            print("✅ Lock can be re-acquired after cleanup")
            manager.cleanup()
        else:
            print("❌ Lock should be available after cleanup")
    else:
        print("❌ Failed to acquire initial lock")
    
    print("InstanceManager test complete")


if __name__ == "__main__":
    main()