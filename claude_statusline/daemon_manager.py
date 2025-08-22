#!/usr/bin/env python3
"""
Daemon Manager - Manages daemon system and provides live session data
Unified entry point for claude-statusline status command
"""

import json
import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class DaemonManager:
    """Manages daemon and provides live data"""
    
    def __init__(self):
        self.data_dir = Path.home() / ".claude" / "data-statusline"
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.daemon_status_file = self.data_dir / "daemon_status.json"
        self.lock_file = self.data_dir / ".unified_daemon.lock"
        self.config_file = Path(__file__).parent / "config.json"
        
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def is_daemon_running(self):
        """Check if daemon is running"""
        try:
            # First check if lock file exists
            if not self.lock_file.exists():
                return False
            
            # Read lock file
            with open(self.lock_file, 'r') as f:
                lock_data = json.load(f)
            
            if not isinstance(lock_data, dict) or "pid" not in lock_data:
                return False
                
            pid = lock_data["pid"]
            
            # Check if process exists (Windows)
            if os.name == 'nt':
                import subprocess
                result = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {pid}"],
                    capture_output=True,
                    text=True
                )
                return str(pid) in result.stdout
            else:
                # Unix/Linux
                try:
                    os.kill(pid, 0)
                    return True
                except:
                    return False
            
        except Exception:
            return False
    
    def start_daemon_if_needed(self):
        """Start daemon if needed"""
        if self.is_daemon_running():
            return True
        
        print(f"{Fore.YELLOW}Starting daemon...{Style.RESET_ALL}")
        
        try:
            # Start daemon in background
            daemon_script = Path(__file__).parent / "daemon.py"
            
            if daemon_script.exists():
                # For Windows
                if os.name == 'nt':
                    subprocess.Popen([sys.executable, str(daemon_script), "--start"], 
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    # For Linux/Mac
                    subprocess.Popen([sys.executable, str(daemon_script), "--start"], 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
                
                # Wait for daemon to start (max 10 seconds)
                for _ in range(20):  # 20 * 0.5 = 10 saniye
                    time.sleep(0.5)
                    if self.is_daemon_running():
                        print(f"{Fore.GREEN}[OK] Daemon started{Style.RESET_ALL}")
                        return True
                
                print(f"{Fore.YELLOW}[!] Daemon may have started, please check...{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}Daemon script not found: {daemon_script}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}Daemon startup error: {e}{Style.RESET_ALL}")
            return False
    
    def build_database_if_needed(self):
        """Build database if needed"""
        if not self.db_file.exists():
            print(f"{Fore.YELLOW}Database not found, creating...{Style.RESET_ALL}")
            
            try:
                # Import and run rebuild module
                from rebuild import DatabaseRebuilder
                rebuilder = DatabaseRebuilder()
                
                if rebuilder.rebuild_database():
                    print(f"{Fore.GREEN}✓ Database created{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}Database creation failed{Style.RESET_ALL}")
                    return False
                    
            except ImportError:
                # Create basic database if rebuild module not found
                print(f"{Fore.YELLOW}Rebuild module not found, creating basic database...{Style.RESET_ALL}")
                self._create_basic_database()
                return True
            except Exception as e:
                print(f"{Fore.RED}Database creation error: {e}{Style.RESET_ALL}")
                return False
        
        return True
    
    def _create_basic_database(self):
        """Create basic database"""
        basic_db = {
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'work_sessions': {},
            'hourly_statistics': {},
            'summary': {
                'total_sessions': 0,
                'total_messages': 0,
                'total_tokens': 0,
                'total_cost': 0.0
            }
        }
        
        with open(self.db_file, 'w') as f:
            json.dump(basic_db, f, indent=2)
    
    def load_current_data(self):
        """Load current data"""
        try:
            if not self.db_file.exists():
                return None
            
            with open(self.db_file, 'r', encoding='utf-8') as f:
                db_data = json.load(f)
            
            return self._extract_current_session_data(db_data)
            
        except Exception as e:
            print(f"{Fore.RED}Data loading error: {e}{Style.RESET_ALL}")
            return None
    
    def _extract_current_session_data(self, db_data):
        """Extract current session data from database"""
        now = datetime.now(timezone.utc)
        today_str = now.strftime('%Y-%m-%d')
        
        # Default data
        data = {
            'primary_model': 'claude-sonnet-4-20250514',
            'message_count': 0,
            'tokens': 0,
            'cost': 0.0,
            'session_duration_minutes': 0,
            'efficiency_score': 85.0,
            'status': 'INACTIVE'
        }
        
        # Check today's sessions
        today_sessions = db_data.get('work_sessions', {}).get(today_str, [])
        
        if today_sessions:
            # Get last session
            last_session = today_sessions[-1]
            
            data.update({
                'primary_model': last_session.get('primary_model', data['primary_model']),
                'message_count': last_session.get('message_count', 0),
                'tokens': last_session.get('tokens', 0),
                'status': 'ACTIVE' if 'session_end' not in last_session else 'COMPLETED'
            })
            
            # Calculate session duration
            try:
                start_str = last_session.get('session_start', '')
                if start_str:
                    start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                    
                    if 'session_end' in last_session:
                        end = datetime.fromisoformat(last_session['session_end'].replace('Z', '+00:00'))
                    else:
                        end = now
                    
                    duration_minutes = (end - start).total_seconds() / 60
                    data['session_duration_minutes'] = int(duration_minutes)
                    
                    # If session is still active and less than 5 hours have passed, mark as ACTIVE
                    if 'session_end' not in last_session and duration_minutes <= 300:  # 5 saat
                        data['status'] = 'ACTIVE'
                        
            except (ValueError, TypeError):
                pass
        
        # Calculate today's total cost
        today_cost = 0
        hourly_data = db_data.get('hourly_statistics', {}).get(today_str, {})
        for hour_data in hourly_data.values():
            today_cost += hour_data.get('cost', 0)
        
        data['cost'] = today_cost
        
        # Calculate efficiency
        if data['message_count'] > 0 and data['tokens'] > 0:
            tokens_per_msg = data['tokens'] / data['message_count']
            if tokens_per_msg < 1000:
                data['efficiency_score'] = 90 + (tokens_per_msg / 100)
            elif tokens_per_msg < 3000:
                data['efficiency_score'] = 85 + ((3000 - tokens_per_msg) / 400)
            else:
                data['efficiency_score'] = 75
                
            data['efficiency_score'] = min(100, max(0, data['efficiency_score']))
        
        return data
    
    def get_current_theme(self):
        """Get current theme"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                theme_name = config.get('current_theme', 'fire_king')
                theme_system = config.get('theme_system', 'wow_themes')
                
                return theme_name, theme_system
        except Exception:
            pass
        
        return 'fire_king', 'wow_themes'
    
    def get_statusline(self):
        """Main statusline function - called by Claude Code"""
        try:
            # Prepare data directory
            self.ensure_data_directory()
            
            # Check and create database
            if not self.build_database_if_needed():
                return "Claude AI | Database Error"
            
            # Start daemon
            if not self.start_daemon_if_needed():
                print(f"{Fore.YELLOW}⚠ Could not start daemon, using existing data{Style.RESET_ALL}")
            
            # Load data
            data = self.load_current_data()
            if not data:
                return "Claude AI | No Data"
            
            # Simple format output
            return f"Claude | {data['message_count']}msg | ${data['cost']:.1f}"
                
        except Exception as e:
            return f"Claude AI | Error: {str(e)[:20]}"
    
    def status_command(self):
        """Status command - called from CLI"""
        print(f"{Back.BLUE}{Fore.WHITE} CLAUDE STATUSLINE STATUS {Style.RESET_ALL}")
        
        # System status
        print(f"\n{Fore.YELLOW}>> System Status:{Style.RESET_ALL}")
        print(f"  Database: {Fore.GREEN}OK{Style.RESET_ALL}" if self.db_file.exists() else f"  Database: {Fore.RED}FAIL{Style.RESET_ALL}")
        print(f"  Daemon: {Fore.GREEN}OK Active{Style.RESET_ALL}" if self.is_daemon_running() else f"  Daemon: {Fore.RED}FAIL Stopped{Style.RESET_ALL}")
        
        # Current data
        data = self.load_current_data()
        if data:
            print(f"\n{Fore.YELLOW}>> Current Session:{Style.RESET_ALL}")
            print(f"  Model: {Fore.LIGHTCYAN_EX}{self._format_model_name(data['primary_model'])}{Style.RESET_ALL}")
            print(f"  Messages: {Fore.LIGHTGREEN_EX}{data['message_count']}{Style.RESET_ALL}")
            print(f"  Tokens: {Fore.LIGHTYELLOW_EX}{self._format_tokens(data['tokens'])}{Style.RESET_ALL}")
            print(f"  Cost: {Fore.LIGHTRED_EX}${data['cost']:.2f}{Style.RESET_ALL}")
            print(f"  Duration: {Fore.LIGHTBLUE_EX}{self._format_duration(data['session_duration_minutes'])}{Style.RESET_ALL}")
            print(f"  Status: {self._format_status(data['status'])}")
        
        # Statusline preview
        theme_name, theme_system = self.get_current_theme()
        print(f"\n{Fore.YELLOW}>> Theme Preview ({theme_name}):{Style.RESET_ALL}")
        statusline = self.get_statusline()
        print(f"  {statusline}")
    
    def _format_model_name(self, model):
        """Format model name"""
        if 'sonnet-4' in model.lower():
            return 'Sonnet-4'
        elif 'sonnet' in model.lower():
            return 'Sonnet'
        elif 'haiku' in model.lower():
            return 'Haiku'
        elif 'opus' in model.lower():
            return 'Opus'
        return 'Claude'
    
    def _format_tokens(self, tokens):
        """Format token count"""
        if tokens >= 1000000:
            return f"{tokens/1000000:.1f}M"
        elif tokens >= 1000:
            return f"{tokens/1000:.1f}K"
        return str(tokens)
    
    def _format_duration(self, minutes):
        """Format duration"""
        if minutes >= 60:
            hours = int(minutes // 60)
            mins = int(minutes % 60)
            return f"{hours}h{mins}m"
        return f"{minutes}m"
    
    def _format_status(self, status):
        """Format status"""
        if status == 'ACTIVE':
            return f"{Fore.GREEN}[*] Active{Style.RESET_ALL}"
        elif status == 'COMPLETED':
            return f"{Fore.BLUE}[+] Completed{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}[-] Inactive{Style.RESET_ALL}"

# Global instance
DAEMON_MANAGER = DaemonManager()

def get_statusline():
    """Main entry point for Claude Code"""
    return DAEMON_MANAGER.get_statusline()

def main():
    """CLI entry point"""
    manager = DaemonManager()
    manager.status_command()

if __name__ == "__main__":
    main()