# Claude Statusline CLI Reference

Complete command-line interface documentation for Claude Statusline.

## Table of Contents

- [Quick Start](#quick-start)
- [Command Structure](#command-structure)
- [Core Commands](#core-commands)
- [Reports & Analytics](#reports--analytics)
- [Management Commands](#management-commands)
- [Debugging Commands](#debugging-commands)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Show help
python claude_statusline.py help

# View current status
python claude_statusline.py status

# Start background daemon
python claude_statusline.py daemon --daemon

# Generate daily report
python claude_statusline.py daily
```

## Command Structure

All commands follow this pattern:
```bash
python claude_statusline.py <category> <command> [options]
```

Or use shortcuts for common commands:
```bash
python claude_statusline.py <shortcut> [options]
```

### Available Shortcuts

| Shortcut | Full Command | Description |
|----------|-------------|-------------|
| `status` | `core status` | Show current session status |
| `daemon` | `core daemon` | Manage background daemon |
| `rebuild` | `core rebuild` | Rebuild database |
| `costs` | `reports costs` | Cost analysis report |
| `daily` | `reports daily` | Daily usage report |
| `sessions` | `reports sessions` | Session analysis |
| `update-prices` | `manage update-prices` | Update model prices |

## Core Commands

Essential commands for basic functionality.

### `core status`
Display current Claude Code session status in compact format.

```bash
python claude_statusline.py core status
```

**Output Format:**
```
[Model] LIVE/OFF ~HH:MM | XXXmsg XX.XM $XXX.XX
```

**Components:**
- `[Model]`: Current model (Opus 4.1, Sonnet 4, etc.)
- `LIVE/OFF`: Session active status
- `~HH:MM`: Session end time
- `XXXmsg`: Message count
- `XX.XM`: Token usage (M=millions, k=thousands)
- `$XXX.XX`: Total cost in USD

### `core daemon`
Manage the background daemon that processes JSONL files.

```bash
# Start daemon
python claude_statusline.py core daemon --daemon

# Check daemon status
python claude_statusline.py core daemon --status

# Stop daemon
python claude_statusline.py core daemon --stop

# Restart daemon
python claude_statusline.py core daemon --restart
```

**Options:**
- `--daemon`: Start daemon in background
- `--status`: Show daemon status
- `--stop`: Stop running daemon
- `--restart`: Restart daemon
- `--data-dir PATH`: Custom data directory

### `core rebuild`
Rebuild the session database from all JSONL files.

```bash
python claude_statusline.py core rebuild
```

**What it does:**
1. Scans all Claude Code project directories
2. Processes JSONL conversation files
3. Rebuilds session database
4. Updates cost calculations
5. Detects active sessions

**When to use:**
- After manual JSONL file changes
- To fix corrupted database
- When historical data is missing

## Reports & Analytics

Generate various reports and analytics from session data.

### `reports sessions`
Detailed analysis of individual sessions.

```bash
python claude_statusline.py reports sessions

# Options
python claude_statusline.py reports sessions --last 5
python claude_statusline.py reports sessions --date 2025-01-14
python claude_statusline.py reports sessions --model opus
```

**Options:**
- `--last N`: Show last N sessions
- `--date YYYY-MM-DD`: Sessions on specific date
- `--model MODEL`: Filter by model type
- `--export FILE`: Export to JSON file

### `reports costs`
Cost analysis breakdown by model and time period.

```bash
python claude_statusline.py reports costs

# Options
python claude_statusline.py reports costs --period week
python claude_statusline.py reports costs --by-model
python claude_statusline.py reports costs --detailed
```

**Options:**
- `--period [day|week|month|all]`: Time period
- `--by-model`: Group costs by model
- `--detailed`: Show detailed breakdown
- `--currency [USD|EUR|GBP]`: Currency display

### `reports daily`
Daily usage summary report.

```bash
python claude_statusline.py reports daily

# Options
python claude_statusline.py reports daily --days 7
python claude_statusline.py reports daily --format table
```

**Output includes:**
- Sessions per day
- Messages sent
- Tokens used
- Daily costs
- Model distribution

### `reports heatmap`
Visual activity heatmap showing usage patterns.

```bash
python claude_statusline.py reports heatmap

# Options
python claude_statusline.py reports heatmap --period month
python claude_statusline.py reports heatmap --by hour
```

**Displays:**
- Hour-by-hour activity
- Day-of-week patterns
- Peak usage times
- Session distribution

### `reports models`
Model usage statistics and comparison.

```bash
python claude_statusline.py reports models

# Options
python claude_statusline.py reports models --compare
python claude_statusline.py reports models --efficiency
```

**Shows:**
- Model usage frequency
- Average session length per model
- Cost efficiency metrics
- Token/message ratios

### `reports summary`
High-level summary of all usage.

```bash
python claude_statusline.py reports summary

# Options
python claude_statusline.py reports summary --format json
python claude_statusline.py reports summary --export summary.txt
```

## Management Commands

System management and maintenance commands.

### `manage update-prices`
Update model pricing from official repository.

```bash
# Update prices
python claude_statusline.py manage update-prices

# Verify current prices
python claude_statusline.py manage update-prices --verify

# Force update
python claude_statusline.py manage update-prices --force

# Custom source
python claude_statusline.py manage update-prices --source URL
```

**Options:**
- `--verify`: Check price validity
- `--force`: Update even if unchanged
- `--no-backup`: Skip backup creation
- `--source URL`: Custom price source

### `manage test`
Run system tests and diagnostics.

```bash
python claude_statusline.py manage test

# Options
python claude_statusline.py manage test --verbose
python claude_statusline.py manage test --component statusline
```

## Debugging Commands

Commands for troubleshooting and verification.

### `check current`
Verify current session detection.

```bash
python claude_statusline.py check current
```

**Checks:**
- Active session detection
- Session timing accuracy
- Live data updates
- File tracking

### `check costs`
Verify cost calculation accuracy.

```bash
python claude_statusline.py check costs

# Options
python claude_statusline.py check costs --session SESSION_ID
python claude_statusline.py check costs --recalculate
```

### `check verify`
Comprehensive verification of all components.

```bash
python claude_statusline.py check verify
```

**Verifies:**
- Database integrity
- Price configuration
- Session consistency
- Cost calculations

### `check session`
Check session data integrity.

```bash
python claude_statusline.py check session

# Options
python claude_statusline.py check session --fix
python claude_statusline.py check session --session SESSION_ID
```

## Configuration

### config.json
Main configuration file for display and behavior.

```json
{
  "display": {
    "enable_rotation": false,
    "status_format": "compact",
    "show_git_branch": true,
    "time_format": "%H:%M"
  },
  "monitoring": {
    "session_duration_hours": 5,
    "live_update_interval": 15
  },
  "reporting": {
    "cost_precision": 2,
    "default_timezone": "UTC"
  }
}
```

### prices.json
Model pricing configuration (auto-updated).

```json
{
  "models": {
    "claude-opus-4-1-20250805": {
      "input": 15.0,
      "output": 75.0,
      "name": "Opus 4.1"
    }
  }
}
```

## Examples

### Daily Workflow

```bash
# Morning: Check yesterday's usage
python claude_statusline.py daily --days 1

# Start work: Ensure daemon is running
python claude_statusline.py daemon --status
python claude_statusline.py daemon --daemon  # If not running

# During work: Monitor current session
python claude_statusline.py status

# End of day: Generate reports
python claude_statusline.py reports summary
python claude_statusline.py reports costs
```

### Weekly Analysis

```bash
# Weekly cost report
python claude_statusline.py costs --period week

# Model efficiency comparison
python claude_statusline.py reports models --compare

# Activity patterns
python claude_statusline.py reports heatmap --period week
```

### Maintenance Tasks

```bash
# Weekly price update
python claude_statusline.py update-prices

# Monthly database rebuild
python claude_statusline.py rebuild

# Verify system health
python claude_statusline.py check verify
```

## Troubleshooting

### No Data Showing

```bash
# Check Claude Code data exists
ls ~/.claude/projects/

# Rebuild database
python claude_statusline.py rebuild

# Check daemon status
python claude_statusline.py daemon --status
```

### Incorrect Costs

```bash
# Update prices
python claude_statusline.py update-prices

# Verify cost calculations
python claude_statusline.py check costs

# Rebuild with fresh data
python claude_statusline.py rebuild
```

### Daemon Issues

```bash
# Check daemon status
python claude_statusline.py daemon --status

# View daemon logs
cat ~/.claude/data-statusline/daemon_status.json

# Restart daemon
python claude_statusline.py daemon --restart
```

### Session Detection Problems

```bash
# Check current session detection
python claude_statusline.py check current

# Verify session data
python claude_statusline.py check session

# Force rebuild
python claude_statusline.py rebuild
```

## Advanced Usage

### Custom Scripts

You can still run individual scripts directly:

```bash
# Direct script execution
python statusline.py
python unified_daemon.py --daemon
python cost_analyzer.py --detailed
```

### Integration with Other Tools

```bash
# Pipe status to other commands
python claude_statusline.py status | grep LIVE

# Export data for external processing
python claude_statusline.py reports sessions --export data.json

# Use in scripts
if python claude_statusline.py daemon --status | grep -q "running"; then
    echo "Daemon is active"
fi
```

### Cron Jobs

```bash
# Add to crontab for automated tasks
# Update prices daily at 3 AM
0 3 * * * /usr/bin/python /path/to/claude_statusline.py update-prices

# Generate daily report at 6 PM
0 18 * * * /usr/bin/python /path/to/claude_statusline.py daily

# Ensure daemon is running every hour
0 * * * * /usr/bin/python /path/to/claude_statusline.py daemon --daemon
```

## Environment Variables

```bash
# Custom data directory
export CLAUDE_DATA_DIR=~/.claude/custom-data

# Custom config path
export CLAUDE_CONFIG=/path/to/config.json

# Debug mode
export CLAUDE_DEBUG=1
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Missing dependencies |
| 3 | Configuration error |
| 4 | Data not found |
| 5 | Daemon error |
| 130 | Interrupted (Ctrl+C) |

## Getting Help

```bash
# General help
python claude_statusline.py help

# Category help
python claude_statusline.py reports

# Command help
python claude_statusline.py reports costs --help

# Version info
python claude_statusline.py --version
```

---

For more information, see the [main README](README.md) or visit the [GitHub repository](https://github.com/ersinkoc/claude-statusline).