# Claude Statusline

A comprehensive monitoring and analytics system for Claude Code usage, providing real-time session tracking, cost analysis, and detailed usage insights.

## What This Is

Claude Statusline is a powerful tool designed to help developers track and analyze their Claude Code AI assistant usage. It provides:

- **Real-time Session Monitoring**: Track active Claude Code sessions with live updates on message count, token usage, and costs
- **Comprehensive Analytics**: Analyze usage patterns, costs, and model performance across different time periods
- **Automatic Data Processing**: Background daemon that continuously processes Claude Code's JSONL log files
- **Visual Reports**: Generate heatmaps, cost breakdowns, and usage statistics
- **Model Cost Tracking**: Accurate cost calculation based on official Anthropic pricing

## What This Is NOT

- **Not a Claude Code replacement**: This tool monitors Claude Code usage, it doesn't replace or modify Claude Code itself
- **Not a cost limiter**: While it tracks costs, it doesn't prevent or limit Claude Code usage
- **Not official Anthropic software**: This is an independent open-source tool
- **Not a security tool**: It doesn't encrypt or secure your Claude Code data

## Features

### Core Components

1. **Statusline Display** (`statusline.py`)
   - Shows current session status in a compact format
   - Displays model name, session time, message count, tokens, and cost
   - Format: `[Model] [Status] [Time] [Messages] [Tokens] [Cost]`

2. **Unified Daemon** (`unified_daemon.py`)
   - Runs in background to process JSONL files
   - Updates session database every minute
   - Manages all data processing operations

3. **Database Builder** (`rebuild_database.py`)
   - Processes all Claude Code JSONL files
   - Builds comprehensive session database
   - Detects and tracks active sessions

### Analytics Tools

- **Session Analyzer** (`session_analyzer.py`): Detailed session breakdowns
- **Cost Analyzer** (`cost_analyzer.py`): Cost analysis by model and time period
- **Daily Report** (`daily_report.py`): Day-by-day usage summaries
- **Activity Heatmap** (`activity_heatmap.py`): Visual usage patterns
- **Model Usage** (`model_usage.py`): Model-specific statistics
- **Summary Report** (`summary_report.py`): High-level usage overview

## Installation

### Prerequisites

- Python 3.8 or higher
- Claude Code installed and configured
- Access to `~/.claude` directory

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ersinkoc/claude-statusline.git
cd claude-statusline
```

2. Install dependencies:
```bash
pip install -r requirements.txt  # Only psutil is required
```

3. Verify Claude Code data location:
```bash
ls ~/.claude/projects/  # Should contain project folders with JSONL files
```

## Usage

### Quick Start

1. **View current status:**
```bash
python statusline.py
```
Output: `[Opus 4.1] [LIVE] [ends 17:00] [234msg] [12.5M] [$45.67] [ClaudeStatus] [14:30]`

2. **Start the daemon (for automatic updates):**
```bash
python unified_daemon.py --daemon
```

3. **Rebuild database from JSONL files:**
```bash
python rebuild_database.py
```

### Running Analytics

Generate various reports:

```bash
# Session analysis
python session_analyzer.py

# Cost breakdown
python cost_analyzer.py

# Daily usage report
python daily_report.py

# Activity heatmap
python activity_heatmap.py

# Model usage statistics
python model_usage.py
```

## Data Structure

### File Locations

- **Claude Code Data**: `~/.claude/projects/*/` - Original JSONL files from Claude Code
- **Statusline Database**: `~/.claude/data-statusline/` - Processed data and analytics
  - `smart_sessions_db.json` - Main session database
  - `file_tracking.json` - Tracks processed JSONL files
  - `daemon_status.json` - Daemon status information
  - `live_session.json` - Current session data

### Session Structure

Sessions are tracked in 5-hour blocks:
- Each session contains: start time, end time, messages, tokens, cost, model information
- Active sessions are updated in real-time
- Historical sessions are preserved for analytics

## Configuration

### Pricing Configuration

Model prices are configured in `prices.json`:
```json
{
  "models": {
    "claude-opus-4-1-20250805": {
      "input": 15.0,
      "output": 75.0,
      "cache_write_5m": 18.75,
      "cache_read": 1.5,
      "name": "Opus 4.1"
    }
  }
}
```

### Session Duration

Default session duration is 5 hours. Modify in `rebuild_database.py`:
```python
self.session_duration = timedelta(hours=5)
```

## Architecture

```
┌─────────────────┐
│  Claude Code    │ ──> Writes JSONL files
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ ~/.claude/      │ ──> JSONL storage
│   projects/     │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ unified_daemon  │ ──> Processes JSONL files
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ smart_sessions  │ ──> Session database
│    _db.json     │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  statusline.py  │ ──> Display current status
│  & analytics    │ ──> Generate reports
└─────────────────┘
```

## Troubleshooting

### No data showing

1. Check if Claude Code data exists:
```bash
ls -la ~/.claude/projects/
```

2. Rebuild the database:
```bash
python rebuild_database.py
```

3. Check daemon status:
```bash
python unified_daemon.py --status
```

### Incorrect costs

1. Verify `prices.json` has correct pricing
2. Check model names match exactly
3. Rebuild database to recalculate

### Daemon issues

1. Stop existing daemon:
```bash
python unified_daemon.py --stop
```

2. Remove lock file if stuck:
```bash
rm ~/.claude/data-statusline/.unified_daemon.lock
```

3. Restart daemon:
```bash
python unified_daemon.py --restart
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built for the Claude Code community
- Uses official Anthropic pricing data
- Inspired by the need for better usage tracking

## Disclaimer

This tool is not affiliated with, endorsed by, or officially connected to Anthropic or Claude Code. It's an independent open-source project created by the community.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Provide JSONL samples (sanitized) when reporting bugs

---

**Note**: This tool reads Claude Code's local data files. It does not modify Claude Code or communicate with Anthropic's servers.