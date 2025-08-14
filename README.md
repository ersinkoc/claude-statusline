# Claude Statusline

Real-time session tracking and analytics for Claude Code, displaying usage metrics in a compact statusline format.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## Features

- 📊 **Real-time Monitoring** - Track active sessions with live updates
- 💰 **Cost Tracking** - Accurate cost calculation based on official pricing
- 📈 **Analytics** - Detailed reports on usage patterns and trends
- 🤖 **Multi-Model Support** - Track Opus, Sonnet, and Haiku models
- ⚡ **Lightweight** - Minimal dependencies (only psutil)
- 🎯 **Unified CLI** - Single command interface for all features

## Quick Start

```bash
# Clone and install
git clone https://github.com/ersinkoc/claude-statusline.git
cd claude-statusline
pip install -r requirements.txt

# View current status
python claude_statusline.py status

# Start background daemon
python claude_statusline.py daemon --daemon

# Generate daily report
python claude_statusline.py daily
```

**Example Output:**
```
[Opus 4.1] LIVE ~17:00 | 727msg 65.9M $139
```

## Installation

### Prerequisites
- Python 3.8+
- Claude Code installed
- Access to `~/.claude` directory

### Setup
1. Clone the repository
2. Install dependencies: `pip install psutil`
3. Run: `python claude_statusline.py status`

## Usage

### Common Commands

```bash
# Core functionality
python claude_statusline.py status        # Current session status
python claude_statusline.py daemon        # Manage background daemon
python claude_statusline.py rebuild       # Rebuild database

# Analytics
python claude_statusline.py costs         # Cost analysis
python claude_statusline.py daily         # Daily report
python claude_statusline.py sessions      # Session details

# Management
python claude_statusline.py update-prices # Update model prices
```

📖 **[Full CLI Documentation](CLI.md)** - Complete command reference with all options and examples

## How It Works

1. **Data Collection**: Reads Claude Code's JSONL conversation logs
2. **Processing**: Background daemon processes and aggregates data
3. **Storage**: Maintains a local database of sessions and metrics
4. **Display**: Formats data into a compact, readable statusline

```
Claude Code → JSONL Files → Daemon → Database → Statusline
```

## Configuration

### Basic Settings (`config.json`)

```json
{
  "display": {
    "enable_rotation": false,
    "status_format": "compact"
  },
  "monitoring": {
    "session_duration_hours": 5
  }
}
```

### Pricing Updates

Model prices are automatically updated from the official repository:

```bash
python claude_statusline.py update-prices
```

## Project Structure

```
claude-statusline/
├── claude_statusline.py    # Main CLI interface
├── statusline.py           # Core statusline display
├── unified_daemon.py       # Background processor
├── config.json            # Configuration
├── prices.json            # Model pricing
├── CLI.md                 # Full CLI documentation
└── requirements.txt       # Dependencies
```

## Data Files

- **Source**: `~/.claude/projects/*/` - Claude Code JSONL files
- **Database**: `~/.claude/data-statusline/` - Processed data
  - `smart_sessions_db.json` - Session database
  - `live_session.json` - Current session
  - `daemon_status.json` - Daemon status

## Troubleshooting

### No Data Showing
```bash
# Check Claude Code data exists
ls ~/.claude/projects/

# Rebuild database
python claude_statusline.py rebuild

# Ensure daemon is running
python claude_statusline.py daemon --status
```

### Incorrect Costs
```bash
# Update prices
python claude_statusline.py update-prices

# Verify calculations
python claude_statusline.py check costs
```

### More Help
- Run `python claude_statusline.py help` for command help
- See [CLI.md](CLI.md) for detailed documentation
- Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development

```bash
# Run tests
python claude_statusline.py manage test

# Check code style
flake8 .

# Build documentation
cd docs && make html
```

## Documentation

- [CLI Reference](CLI.md) - Complete command documentation
- [Architecture](ARCHITECTURE.md) - System design and data flow
- [Contributing](CONTRIBUTING.md) - Contribution guidelines
- [Changelog](CHANGELOG.md) - Version history
- [Security](SECURITY.md) - Security policy

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Claude Code team for the excellent development environment
- Contributors and testers from the community
- Built with ❤️ for the Claude Code community

## Support

- **Issues**: [GitHub Issues](https://github.com/ersinkoc/claude-statusline/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ersinkoc/claude-statusline/discussions)
- **Documentation**: [Full CLI Reference](CLI.md)

---

**Current Version**: 1.2.0 | **Last Updated**: 2025-08-14