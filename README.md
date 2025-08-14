# Claude Statusline

Real-time session tracking and analytics for Claude Code, displaying usage metrics in a compact statusline format.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Version](https://img.shields.io/badge/version-1.3.0-green.svg)

## Features

- 📊 **Real-time Monitoring** - Track active sessions with live updates
- 💰 **Cost Tracking** - Accurate cost calculation based on official pricing
- 📈 **Analytics** - Detailed reports on usage patterns and trends
- 🤖 **Multi-Model Support** - Track Opus, Sonnet, and Haiku models
- 🎨 **20+ Display Templates** - Choose from various statusline formats
- ⚡ **Lightweight** - Minimal dependencies (only psutil)
- 📦 **Easy Installation** - Available as a Python package
- 🎯 **Unified CLI** - Single command interface for all features

## Quick Start

### Install from Package

```bash
# Install the package
pip install claude-statusline

# View current status
claude-status

# Use the CLI
claude-statusline --help
```

### Install from Source

```bash
# Clone repository
git clone https://github.com/ersinkoc/claude-statusline.git
cd claude-statusline

# Install in development mode
pip install -e .

# Or build and install the package
python -m build
pip install dist/claude_statusline-*.whl
```

**Example Outputs:**
```
[Opus 4.1] LIVE ~17:00 | 727msg 65.9M $139     # Compact (default)
O4.1 456m $90                                   # Minimal
claude@O4.1:~$ 456 msgs | $89.99               # Terminal
--INSERT-- O4.1 456L $90.0 [utf-8]             # Vim style
```

📖 **[See all 20+ templates](TEMPLATES.md)** - Choose your favorite style!

## Installation

### Prerequisites
- Python 3.8+
- Claude Code installed
- Access to `~/.claude` directory

### Package Installation

```bash
# Install from PyPI (when published)
pip install claude-statusline

# Install from local wheel
pip install dist/claude_statusline-1.3.0-py3-none-any.whl

# Development installation
git clone https://github.com/ersinkoc/claude-statusline.git
cd claude-statusline
pip install -e .
```

### Claude Code Integration

Add to your Claude Code `settings.json`:

```json
{
  "statusline": {
    "command": "claude-status"
  }
}
```

Or if using from source:

```json
{
  "statusline": {
    "command": "python",
    "args": ["path/to/claude-statusline/statusline.py"]
  }
}
```

## Usage

### Command Line Interface

```bash
# Main CLI
claude-statusline <command> [options]

# Direct statusline display
claude-status
```

### Common Commands

```bash
# Core functionality
claude-statusline status          # Current session status
claude-statusline daemon          # Manage background daemon
claude-statusline rebuild         # Rebuild database

# Analytics
claude-statusline costs           # Cost analysis
claude-statusline daily           # Daily report
claude-statusline sessions        # Session details
claude-statusline heatmap         # Activity heatmap
claude-statusline summary         # Summary statistics

# Configuration
claude-statusline template        # Select display template
claude-statusline update-prices   # Update model prices
claude-statusline rotate          # Toggle statusline rotation
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
    "template": "compact",      // Choose from 20+ templates
    "enable_rotation": false,
    "status_format": "compact"
  },
  "monitoring": {
    "session_duration_hours": 5
  }
}
```

### Template Selection

```bash
# Interactive template selector with preview
claude-statusline template

# Quick template change
claude-statusline template minimal
claude-statusline template vim
```

📖 **[Template Gallery](TEMPLATES.md)** - Preview all available statusline formats

### Pricing Updates

Model prices are automatically updated from the official repository:

```bash
claude-statusline update-prices
```

## Project Structure

```
claude-statusline/
├── claude_statusline/      # Package directory
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # Main CLI interface
│   ├── statusline.py      # Core statusline display
│   ├── daemon.py          # Background processor
│   ├── templates.py       # Template definitions
│   ├── config.json        # Configuration
│   └── prices.json        # Model pricing
├── tests/                 # Test suite
├── docs/                  # Documentation
├── setup.py              # Package setup
├── pyproject.toml        # Modern package config
└── README.md             # This file
```

## Data Files

- **Source**: `~/.claude/projects/*/` - Claude Code JSONL files
- **Database**: `~/.claude/data-statusline/` - Processed data
  - `smart_sessions_db.json` - Session database
  - `live_session.json` - Current session
  - `daemon_status.json` - Daemon status

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/ersinkoc/claude-statusline.git
cd claude-statusline

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run test suite
pytest

# Run with coverage
pytest --cov=claude_statusline

# Run specific test
pytest tests/test_statusline.py
```

### Building the Package

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI (when ready)
twine upload dist/*
```

## Troubleshooting

### No Data Showing
```bash
# Check Claude Code data exists
ls ~/.claude/projects/

# Rebuild database
claude-statusline rebuild

# Ensure daemon is running
claude-statusline daemon --status
```

### Incorrect Costs
```bash
# Update prices
claude-statusline update-prices

# Verify calculations
claude-statusline verify
```

### Package Issues
```bash
# Reinstall package
pip uninstall claude-statusline
pip install dist/claude_statusline-*.whl

# Check installation
pip show claude-statusline
```

### More Help
- Run `claude-statusline --help` for command help
- See [CLI.md](CLI.md) for detailed documentation
- Check [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md) for Claude Code integration
- Report issues on [GitHub](https://github.com/ersinkoc/claude-statusline/issues)

## Documentation

- [CLI Reference](CLI.md) - Complete command documentation
- [Template Gallery](TEMPLATES.md) - All 20+ statusline formats
- [Architecture](ARCHITECTURE.md) - System design and data flow
- [Claude Code Setup](CLAUDE_CODE_SETUP.md) - Integration guide
- [Contributing](CONTRIBUTING.md) - Contribution guidelines
- [Changelog](CHANGELOG.md) - Version history
- [Security](SECURITY.md) - Security policy

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

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

**Current Version**: 1.3.0 | **Last Updated**: 2025-08-14 | **Package**: `claude-statusline`