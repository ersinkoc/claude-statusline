# Claude Statusline CLI Reference

Complete command-line interface documentation for Claude Statusline.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Structure](#command-structure)
- [Core Commands](#core-commands)
- [Analyticlaude-statusline Commands](#analyticlaude-statusline-commands)
- [Verification Commands](#verification-commands)
- [Management Commands](#management-commands)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Installation

```bash
# Install from package
pip install claude-statusline

# Install from source
git clone https://github.com/ersinkoc/claude-statusline.git
cd claude-statusline
pip install -e .

# Install from built wheel
pip install dist/claude_statusline-1.3.0-py3-none-any.whl
```

## Quick Start

```bash
# Show help
claude-statusline --help

# View current status
claude-status  # Direct statusline display
claude-statusline status

# Start background daemon
claude-statusline daemon --start

# Generate daily report
claude-statusline daily
```

## Command Structure

The package provides multiple entry points:

```bash
# Main CLI interface
claude-statusline <command> [options]

# Direct commands
claude-status           # Statusline display
claude-daemon          # Daemon management
claude-rebuild         # Database rebuild
claude-template        # Template selector
```

## Core Commands

Essential commands for basic functionality.

### `status`
Display current Claude Code session status.

```bash
claude-statusline status
```

**Output Examples:**
```
[Opus 4.1] LIVE ~17:00 | 727msg 65.9M $139.99
[Sonnet 4] OFF | 1234msg 12.3M $45.67
```

### `daemon`
Manage the background daemon that processes JSONL files.

```bash
# Start daemon
claude-statusline daemon --start
claude-daemon --start

# Check daemon status
claude-statusline daemon --status

# Stop daemon
claude-statusline daemon --stop

# Restart daemon
claude-statusline daemon --restart
```

**Options:**
- `--start`: Start the daemon
- `--stop`: Stop the daemon
- `--restart`: Restart the daemon
- `--status`: Check daemon status

### `rebuild`
Rebuild the database from JSONL files.

```bash
claude-statusline rebuild
claude-rebuild

# Rebuild with verbose output
claude-statusline rebuild --verbose
```

**Options:**
- `--verbose`: Show detailed progress
- `--force`: Force rebuild even if recent
- `--days N`: Process last N days only

## Analyticlaude-statusline Commands

Generate reports and analyze usage patterns.

### `sessions`
Analyze session details and patterns.

```bash
claude-statusline sessions

# Show only today's sessions
claude-statusline sessions --today

# Show last N sessions
claude-statusline sessions --last 10

# Export to JSON
claude-statusline sessions --export sessions.json
```

**Options:**
- `--today`: Today's sessions only
- `--last N`: Last N sessions
- `--model MODEL`: Filter by model
- `--export FILE`: Export to file

### `costs`
Analyze costs by model and time period.

```bash
claude-statusline costs

# Today's costs
claude-statusline costs --today

# This week's costs
claude-statusline costs --week

# This month's costs
claude-statusline costs --month

# By model breakdown
claude-statusline costs --by-model
```

**Options:**
- `--today`: Today's costs
- `--week`: This week's costs
- `--month`: This month's costs
- `--by-model`: Breakdown by model
- `--export FILE`: Export to CSV

### `daily`
Generate daily usage report.

```bash
claude-statusline daily

# Specific date
claude-statusline daily --date 2025-08-14

# Export to file
claude-statusline daily --export report.txt
```

**Options:**
- `--date YYYY-MM-DD`: Specific date
- `--timezone TZ`: Timezone (default: local)
- `--export FILE`: Export to file

### `heatmap`
Show activity heatmap visualization.

```bash
claude-statusline heatmap

# Last 30 days
claude-statusline heatmap --days 30

# Hourly breakdown
claude-statusline heatmap --hourly
```

**Options:**
- `--days N`: Last N days
- `--hourly`: Hourly breakdown
- `--weekly`: Weekly pattern

### `summary`
Generate summary statisticlaude-statusline.

```bash
claude-statusline summary

# All-time summary
claude-statusline summary --all

# This month
claude-statusline summary --month

# Export to JSON
claude-statusline summary --export summary.json
```

**Options:**
- `--all`: All-time statisticlaude-statusline
- `--month`: This month only
- `--week`: This week only
- `--export FILE`: Export to file

### `models`
Show model usage statisticlaude-statusline.

```bash
claude-statusline models

# With cost breakdown
claude-statusline models --costs

# Sort by usage
claude-statusline models --sort usage
```

**Options:**
- `--costs`: Include cost breakdown
- `--sort`: Sort by (usage|cost|count)
- `--top N`: Show top N models

## Verification Commands

Check and verify data integrity.

### `check-costs`
Verify cost calculations.

```bash
claude-statusline check-costs

# Check specific session
claude-statusline check-costs --session 123

# Recalculate all
claude-statusline check-costs --recalculate
```

**Options:**
- `--session ID`: Check specific session
- `--recalculate`: Recalculate all costs
- `--fix`: Fix discrepancies

### `verify`
Verify database integrity.

```bash
claude-statusline verify

# Full verification
claude-statusline verify --full

# Fix issues
claude-statusline verify --fix
```

**Options:**
- `--full`: Complete verification
- `--fix`: Attempt to fix issues
- `--report`: Generate report

### `current`
Check current session detection.

```bash
claude-statusline current

# Verbose output
claude-statusline current --verbose
```

**Options:**
- `--verbose`: Detailed output
- `--debug`: Debug information

### `session-data`
Check session data parsing.

```bash
claude-statusline session-data

# Check specific file
claude-statusline session-data --file conversation.jsonl

# Validate all files
claude-statusline session-data --validate-all
```

**Options:**
- `--file FILE`: Check specific file
- `--validate-all`: Validate all files
- `--fix`: Fix parsing issues

## Management Commands

Configuration and system management.

### `template`
Select statusline display template.

```bash
# Interactive selector
claude-statusline template
claude-template

# Set specific template
claude-statusline template minimal
claude-statusline template vim
claude-statusline template matrix

# List all templates
claude-statusline template --list
```

**Available Templates:**
- `compact`: Default compact format
- `minimal`: Minimal information
- `vim`: Vim-style statusline
- `terminal`: Terminal prompt style
- `matrix`: Matrix-style display
- `emoji`: With emoji indicators
- And 15+ more...

**Options:**
- `--list`: List all templates
- `--preview`: Preview all templates
- `--set TEMPLATE`: Set specific template

### `update-prices`
Update model pricing data.

```bash
claude-statusline update-prices
claude-update-prices

# Force update
claude-statusline update-prices --force

# From specific URL
claude-statusline update-prices --url https://...
```

**Options:**
- `--force`: Force update
- `--url URL`: Custom price source
- `--verify`: Verify prices

### `rotate`
Enable/disable statusline rotation.

```bash
claude-statusline rotate

# Enable rotation
claude-statusline rotate --enable

# Disable rotation
claude-statusline rotate --disable

# Set interval
claude-statusline rotate --interval 10
```

**Options:**
- `--enable`: Enable rotation
- `--disable`: Disable rotation
- `--interval N`: Rotation interval (seconds)

## Configuration

### Configuration File Location

- Default: `~/.claude/data-statusline/config.json`
- Package: `claude_statusline/config.json`

### Configuration Structure

```json
{
  "display": {
    "template": "compact",
    "enable_rotation": false,
    "rotation_interval": 10,
    "time_format": "%H:%M"
  },
  "monitoring": {
    "session_duration_hours": 5,
    "live_update_interval": 15,
    "db_update_interval": 300
  },
  "paths": {
    "claude_projects": "~/.claude/projects",
    "data_directory": ".claude/data-statusline"
  }
}
```

### Environment Variables

```bash
# Override data directory
export CLAUDE_DATA_DIR=/custom/path

# Set template
export CLAUDE_TEMPLATE=minimal

# Enable debug mode
export CLAUDE_DEBUG=1
```

## Examples

### Basic Usage

```bash
# Start monitoring
claude-statusline daemon --start
claude-statusline status

# Daily workflow
claude-statusline daily
claude-statusline costs --today
claude-statusline sessions --today
```

### Advanced Analyticlaude-statusline

```bash
# Weekly report
claude-statusline summary --week
claude-statusline heatmap --days 7
claude-statusline costs --week --by-model

# Export data
claude-statusline sessions --export sessions.json
claude-statusline costs --export costs.claude-statuslinev
claude-statusline summary --all --export summary.json
```

### Maintenance

```bash
# Regular maintenance
claude-statusline rebuild
claude-statusline verify --full
claude-statusline check-costs --recalculate

# Update configuration
claude-statusline template vim
claude-statusline update-prices
claude-statusline rotate --enable --interval 15
```

### Debugging

```bash
# Check system
claude-statusline daemon --status
claude-statusline current --verbose
claude-statusline session-data --validate-all

# Fix issues
claude-statusline rebuild --force
claude-statusline verify --fix
claude-statusline check-costs --fix
```

## Troubleshooting

### Common Issues

#### No Data Showing
```bash
# Check data exists
ls ~/.claude/projects/

# Rebuild database
claude-statusline rebuild --force

# Check daemon
claude-statusline daemon --status
claude-statusline daemon --restart
```

#### Incorrect Costs
```bash
# Update prices
claude-statusline update-prices --force

# Verify calculations
claude-statusline check-costs --recalculate

# Check specific session
claude-statusline session-data --file conversation.jsonl
```

#### Package Not Found
```bash
# Reinstall package
pip uninstall claude-statusline
pip install dist/claude_statusline-*.whl

# Development mode
pip install -e .
```

#### Template Not Working
```bash
# Reset to default
claude-statusline template compact

# List available
claude-statusline template --list

# Preview all
claude-statusline template --preview
```

### Debug Mode

```bash
# Enable debug output
export CLAUDE_DEBUG=1
claude-statusline status

# Check logs
cat ~/.claude/data-statusline/daemon.log
```

### Getting Help

```bash
# Command help
claude-statusline --help
claude-statusline status --help
claude-statusline costs --help

# Version information
claude-statusline --version
claude-statusline --version
```

## See Also

- [README.md](README.md) - Project overview
- [TEMPLATES.md](TEMPLATES.md) - Template gallery
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md) - Claude Code integration
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guide

---

**Version**: 1.3.0 | **Package**: `claude-statusline` | **Updated**: 2025-08-14