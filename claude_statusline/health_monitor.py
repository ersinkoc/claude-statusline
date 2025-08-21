#!/usr/bin/env python3
"""
Health Monitor for Claude Statusline
System health monitoring and diagnostics
"""

import json
import psutil
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any
import subprocess
import sys

from .data_directory_utils import resolve_data_directory
from .safe_file_operations import safe_json_read


class HealthMonitor:
    """Monitor system health and Claude Statusline components"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.daemon_status_file = self.data_dir / "daemon_status.json"
        self.lock_file = self.data_dir / ".unified_daemon.lock"
    
    def run_comprehensive_health_check(self):
        """Run comprehensive health check of all components"""
        print("\n" + "="*80)
        print("🏥 CLAUDE STATUSLINE HEALTH CHECK")
        print("="*80 + "\n")
        
        all_healthy = True
        
        # Check daemon status
        daemon_healthy = self._check_daemon_health()
        all_healthy &= daemon_healthy
        
        # Check database integrity
        db_healthy = self._check_database_health()
        all_healthy &= db_healthy
        
        # Check file system health
        fs_healthy = self._check_filesystem_health()
        all_healthy &= fs_healthy
        
        # Check system resources
        sys_healthy = self._check_system_resources()
        all_healthy &= sys_healthy
        
        # Check data freshness
        data_healthy = self._check_data_freshness()
        all_healthy &= data_healthy
        
        # Overall status
        print("\n" + "="*60)
        if all_healthy:
            print("✅ OVERALL STATUS: HEALTHY")
        else:
            print("⚠️ OVERALL STATUS: ISSUES DETECTED")
        print("="*60)
        
        return all_healthy
    
    def _check_daemon_health(self) -> bool:
        """Check daemon health status"""
        print("🔧 DAEMON HEALTH")
        print("-" * 40)
        
        try:
            # Check if daemon is running
            if self.lock_file.exists():
                with open(self.lock_file, 'r') as f:
                    content = f.read().strip()
                    try:
                        # Try JSON format first
                        lock_data = json.loads(content)
                        pid = lock_data.get('pid')
                    except json.JSONDecodeError:
                        # Fallback to plain PID
                        pid = int(content)
                
                if psutil.pid_exists(pid):
                    print("✅ Daemon is running (PID: {})".format(pid))
                    
                    # Check daemon status file
                    if self.daemon_status_file.exists():
                        status = safe_json_read(self.daemon_status_file)
                        last_update = status.get('last_update', 'Unknown')
                        print(f"✅ Last update: {last_update}")
                        
                        # Check if updates are recent (within 2 minutes)
                        try:
                            # Parse ISO format without timezone info (assuming local time)
                            last_update_time = datetime.fromisoformat(last_update)
                            time_diff = datetime.now() - last_update_time
                            
                            if time_diff < timedelta(minutes=2):
                                print("✅ Daemon is actively updating")
                                return True
                            else:
                                print(f"⚠️ Daemon hasn't updated in {time_diff}")
                                return False
                        except:
                            print("⚠️ Cannot parse last update time")
                            return False
                    else:
                        print("⚠️ Daemon status file missing")
                        return False
                else:
                    print(f"❌ Daemon PID {pid} not found")
                    return False
            else:
                print("❌ Daemon not running (no lock file)")
                return False
        except Exception as e:
            print(f"❌ Daemon check failed: {e}")
            return False
    
    def _check_database_health(self) -> bool:
        """Check database integrity"""
        print("\n💾 DATABASE HEALTH")
        print("-" * 40)
        
        try:
            if not self.db_file.exists():
                print("❌ Database file missing")
                return False
            
            db = safe_json_read(self.db_file)
            if not db:
                print("❌ Database file corrupted or empty")
                return False
            
            # Check required sections
            required_sections = ['work_sessions', 'hourly_statistics', 'build_info']
            missing_sections = [s for s in required_sections if s not in db]
            
            if missing_sections:
                print(f"⚠️ Missing sections: {', '.join(missing_sections)}")
                return False
            
            # Check data counts
            sessions = len(db.get('work_sessions', {}))
            hourly_stats = len(db.get('hourly_statistics', {}))
            
            print(f"✅ Database loaded successfully")
            print(f"✅ Work sessions: {sessions}")
            print(f"✅ Hourly statistics: {hourly_stats} days")
            
            # Check build info
            build_info = db.get('build_info', {})
            total_files = build_info.get('total_files_processed', 0)
            total_messages = build_info.get('total_messages_in_tracking', 0)
            
            print(f"✅ Files processed: {total_files}")
            print(f"✅ Messages tracked: {total_messages:,}")
            
            return True
            
        except Exception as e:
            print(f"❌ Database check failed: {e}")
            return False
    
    def _check_filesystem_health(self) -> bool:
        """Check filesystem and permissions"""
        print("\n📁 FILESYSTEM HEALTH")
        print("-" * 40)
        
        try:
            # Check data directory
            if not self.data_dir.exists():
                print("❌ Data directory missing")
                return False
            
            print(f"✅ Data directory: {self.data_dir}")
            
            # Check permissions
            test_file = self.data_dir / ".health_check_test"
            try:
                test_file.write_text("test")
                test_file.unlink()
                print("✅ Write permissions OK")
            except Exception as e:
                print(f"❌ Write permission failed: {e}")
                return False
            
            # Check Claude projects directory
            claude_dir = Path.home() / ".claude"
            projects_dir = claude_dir / "projects"
            
            if not claude_dir.exists():
                print("⚠️ Claude directory not found")
                return False
            
            if not projects_dir.exists():
                print("⚠️ Claude projects directory not found")
                return False
            
            # Count JSONL files
            jsonl_files = list(projects_dir.glob("**/*.jsonl"))
            print(f"✅ Claude projects: {projects_dir}")
            print(f"✅ JSONL files found: {len(jsonl_files)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Filesystem check failed: {e}")
            return False
    
    def _check_system_resources(self) -> bool:
        """Check system resources (CPU, memory, disk)"""
        print("\n💻 SYSTEM RESOURCES")
        print("-" * 40)
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            print(f"CPU Usage: {cpu_percent:.1f}%")
            
            # Memory usage
            memory = psutil.virtual_memory()
            print(f"Memory Usage: {memory.percent:.1f}% ({memory.used // 1024**3}GB / {memory.total // 1024**3}GB)")
            
            # Disk space for data directory
            disk = psutil.disk_usage(str(self.data_dir))
            disk_percent = (disk.used / disk.total) * 100
            disk_free_gb = disk.free // 1024**3
            
            print(f"Disk Usage: {disk_percent:.1f}% (Free: {disk_free_gb}GB)")
            
            # Check if resources are healthy
            resource_issues = []
            if cpu_percent > 90:
                resource_issues.append("High CPU usage")
            if memory.percent > 90:
                resource_issues.append("High memory usage")
            if disk_percent > 95:
                resource_issues.append("Low disk space")
            
            if resource_issues:
                print(f"⚠️ Resource issues: {', '.join(resource_issues)}")
                return False
            else:
                print("✅ System resources healthy")
                return True
                
        except Exception as e:
            print(f"❌ System resource check failed: {e}")
            return False
    
    def _check_data_freshness(self) -> bool:
        """Check if data is fresh and being updated"""
        print("\n🕐 DATA FRESHNESS")
        print("-" * 40)
        
        try:
            if not self.db_file.exists():
                print("❌ Database file missing")
                return False
            
            # Check file modification time
            mod_time = datetime.fromtimestamp(self.db_file.stat().st_mtime)
            time_diff = datetime.now() - mod_time
            
            print(f"Last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Time since update: {time_diff}")
            
            # Data should be updated within last 5 minutes for active daemon
            if time_diff > timedelta(minutes=5):
                print("⚠️ Database not recently updated")
                return False
            else:
                print("✅ Database is fresh")
                return True
                
        except Exception as e:
            print(f"❌ Data freshness check failed: {e}")
            return False
    
    def generate_diagnostic_report(self):
        """Generate detailed diagnostic report"""
        print("\n" + "="*80)
        print("🔍 DIAGNOSTIC REPORT")
        print("="*80 + "\n")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self._collect_system_info(),
            'database_info': self._collect_database_info(),
            'daemon_info': self._collect_daemon_info(),
            'errors': self._collect_errors()
        }
        
        # Save report
        report_file = self.data_dir / f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print("📊 SYSTEM INFORMATION")
        print("-" * 40)
        print(f"Python Version: {report['system_info']['python_version']}")
        print(f"Platform: {report['system_info']['platform']}")
        print(f"CPU Cores: {report['system_info']['cpu_cores']}")
        print(f"Memory: {report['system_info']['memory_gb']:.1f}GB")
        
        print("\n💾 DATABASE INFORMATION")
        print("-" * 40)
        print(f"Database Size: {report['database_info']['size_mb']:.1f}MB")
        print(f"Sessions: {report['database_info']['sessions']}")
        print(f"Days of Data: {report['database_info']['days']}")
        
        if report['errors']:
            print("\n❌ ERRORS DETECTED")
            print("-" * 40)
            for error in report['errors']:
                print(f"  • {error}")
        
        print(f"\n📋 Full report saved to: {report_file}")
        return str(report_file)
    
    def _collect_system_info(self) -> Dict:
        """Collect system information"""
        return {
            'python_version': sys.version,
            'platform': sys.platform,
            'cpu_cores': psutil.cpu_count(),
            'memory_gb': psutil.virtual_memory().total / 1024**3,
            'disk_gb': psutil.disk_usage(str(self.data_dir)).total / 1024**3
        }
    
    def _collect_database_info(self) -> Dict:
        """Collect database information"""
        try:
            db = safe_json_read(self.db_file) if self.db_file.exists() else {}
            size_mb = self.db_file.stat().st_size / 1024**2 if self.db_file.exists() else 0
            
            return {
                'size_mb': size_mb,
                'sessions': len(db.get('work_sessions', {})),
                'days': len(db.get('hourly_statistics', {})),
                'build_info': db.get('build_info', {})
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _collect_daemon_info(self) -> Dict:
        """Collect daemon information"""
        try:
            if self.daemon_status_file.exists():
                return safe_json_read(self.daemon_status_file)
            else:
                return {'status': 'No daemon status file'}
        except Exception as e:
            return {'error': str(e)}
    
    def _collect_errors(self) -> List[str]:
        """Collect any errors or warnings"""
        errors = []
        
        try:
            # Check for stale lock files
            if self.lock_file.exists():
                with open(self.lock_file, 'r') as f:
                    pid = int(f.read().strip())
                if not psutil.pid_exists(pid):
                    errors.append(f"Stale lock file detected (PID {pid} not running)")
            
            # Check database size
            if self.db_file.exists():
                size_mb = self.db_file.stat().st_size / 1024**2
                if size_mb > 100:  # Large database
                    errors.append(f"Large database file ({size_mb:.1f}MB)")
            
            # Check for missing files
            required_files = ['prices.json']
            for filename in required_files:
                filepath = Path(__file__).parent / filename
                if not filepath.exists():
                    errors.append(f"Missing required file: {filename}")
        
        except Exception as e:
            errors.append(f"Error during error collection: {e}")
        
        return errors
    
    def quick_status_check(self):
        """Quick status check for all components"""
        print("\n🚀 QUICK STATUS CHECK")
        print("-" * 40)
        
        # Daemon
        daemon_ok = self._check_daemon_health()
        status_icon = "✅" if daemon_ok else "❌"
        print(f"{status_icon} Daemon")
        
        # Database
        db_ok = self.db_file.exists() and bool(safe_json_read(self.db_file))
        status_icon = "✅" if db_ok else "❌"
        print(f"{status_icon} Database")
        
        # Data directory
        data_ok = self.data_dir.exists() and self.data_dir.is_dir()
        status_icon = "✅" if data_ok else "❌"
        print(f"{status_icon} Data Directory")
        
        # Claude directory
        claude_ok = (Path.home() / ".claude").exists()
        status_icon = "✅" if claude_ok else "❌"
        print(f"{status_icon} Claude Data")
        
        return all([daemon_ok, db_ok, data_ok, claude_ok])
    
    def monitor_performance(self, duration: int = 60):
        """Monitor performance for specified duration"""
        print(f"\n⏱️ PERFORMANCE MONITORING ({duration}s)")
        print("-" * 50)
        
        start_time = datetime.now()
        samples = []
        
        print("Monitoring... (Press Ctrl+C to stop)")
        
        try:
            while (datetime.now() - start_time).seconds < duration:
                sample = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu': psutil.cpu_percent(),
                    'memory': psutil.virtual_memory().percent,
                    'processes': len(psutil.pids())
                }
                samples.append(sample)
                
                # Print current stats
                print(f"\r{datetime.now().strftime('%H:%M:%S')} - CPU: {sample['cpu']:5.1f}% | Memory: {sample['memory']:5.1f}% | Processes: {sample['processes']}", end="")
                
                # Wait 1 second
                import time
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
        
        print(f"\n\n📊 PERFORMANCE SUMMARY")
        print("-" * 40)
        
        if samples:
            avg_cpu = sum(s['cpu'] for s in samples) / len(samples)
            avg_memory = sum(s['memory'] for s in samples) / len(samples)
            max_cpu = max(s['cpu'] for s in samples)
            max_memory = max(s['memory'] for s in samples)
            
            print(f"Average CPU: {avg_cpu:.1f}%")
            print(f"Average Memory: {avg_memory:.1f}%")
            print(f"Peak CPU: {max_cpu:.1f}%")
            print(f"Peak Memory: {max_memory:.1f}%")
            print(f"Samples collected: {len(samples)}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='System health monitoring')
    parser.add_argument('--full', action='store_true', help='Run comprehensive health check')
    parser.add_argument('--quick', action='store_true', help='Quick status check')
    parser.add_argument('--monitor', type=int, metavar='SECONDS', help='Monitor performance for N seconds')
    parser.add_argument('--diagnostic', action='store_true', help='Generate diagnostic report')
    
    args = parser.parse_args()
    
    monitor = HealthMonitor()
    
    if args.full:
        monitor.run_comprehensive_health_check()
    elif args.quick:
        monitor.quick_status_check()
    elif args.monitor:
        monitor.monitor_performance(args.monitor)
    elif args.diagnostic:
        monitor.generate_diagnostic_report()
    else:
        monitor.quick_status_check()


if __name__ == "__main__":
    main()