# Claude Statusline

Real-time session tracking and analytics for Claude Code, displaying usage metrics in a compact statusline format.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Version](https://img.shields.io/badge/version-1.9.0-green.svg)

## Features

### Core Features
- 📊 **Real-time Monitoring** - Track active sessions with live updates
- 💰 **Cost Tracking** - Accurate cost calculation based on official pricing
- 🤖 **Multi-Model Support** - Track Opus, Sonnet, and Haiku models
- 📁 **Git Integration** - Shows branch info and repository status
- 💻 **System Info** - CPU, memory, battery, and folder information
- ⚡ **Lightweight** - Minimal dependencies (only psutil and colorama)
- 📦 **Easy Installation** - Available as a Python package

### Visual & Themes
- 🎨 **100+ Epic Powerline Themes** - Professional powerline-style themes with nerd fonts and RGB colors
- 🌈 **Advanced RGB Support** - True color output with gradient effects and smooth transitions
- 🔧 **Unified Theme System** - Single management system for all themes and templates
- 🎯 **Custom Themes** - Create and save your own statusline designs
- ⚡ **Live Session Data** - Real-time token counts, cache efficiency, and I/O token tracking

### Analytics & Reporting
- 📈 **Advanced Usage Analytics** - Comprehensive productivity metrics and insights
- 📊 **Trend Analysis** - Usage trends, productivity patterns, and AI-powered insights (NEW!)
- 🏥 **Health Monitoring** - System health diagnostics and performance monitoring (NEW!)
- 💹 **Budget Management** - Set spending limits and track budget compliance
- 📊 **Usage Patterns Analysis** - Behavioral insights and optimization recommendations
- 📉 **Cost Forecasting** - Predict future costs based on usage trends
- 📋 **Export Reports** - Generate JSON/CSV reports for external analysis
- 🚨 **Smart Alerts** - Budget warnings and usage anomaly detection
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
```bash
# Epic Powerline Themes with RGB Colors
⚡ Opus 4.1 LIVE ● 533 msgs ⟨16.6M/16.6M⟩ $98.78 ▶ 1h20m  # ocean_tsunami_power
🔥 [Opus-4.1] ⚡ACTIVE #3 📊 533↕ 💰$98.78 ⏱1:20 🔋85%  # fire_king
🌊 Opus 4.1 ≋ LIVE ≋ 533 messages ≋ 16.6M tokens ≋ $98.78  # ocean_wave

# Professional Powerline with Nerd Fonts  
 Opus 4.1  LIVE  533 msgs  16.6M tok  $98.78  85%  # With RGB backgrounds
█ MODEL: Opus 4.1 █ STATUS: ACTIVE █ TOKENS: 16.6M █ COST: $98.78 █  # Block style
▌Opus-4.1▐ ⟨LIVE⟩ │533│ ⟨16.6M⟩ ⟨$98.78⟩ ⟨1:20⟩  # Bracket style

# Advanced Themes with All Fields
🎯 Opus 4.1 | LIVE | Msgs: 533 | I/O: 8.3M/8.3M | Cache: 95% | Cost: $98.78 | Session: 1h20m
💻 [OPUS-4.1] ▶ ACTIVE ▶ 533 messages ▶ 16.6M tokens (I:8.3M/O:8.3M) ▶ Cache efficiency: 95% ▶ $98.78
⚡ Opus 4.1 ┃ LIVE #3 ┃ 533↕ ┃ Input: 8.3M ┃ Output: 8.3M ┃ Cache: 2.1M/105K ┃ Eff: 95% ┃ $98.78 ┃ 1:20
```

📖 **[See all 80+ templates](#themes)** - Massive collection with professional themes!

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
pip install dist/claude_statusline-1.9.0-py3-none-any.whl

# Development installation
git clone https://github.com/ersinkoc/claude-statusline.git
cd claude-statusline
pip install -e .
```

### Claude Code Integration

Add to your Claude Code `settings.json`:

```json
{
  "statusLine": {
    "command": "claude-status"
  }
}
```

Or if using from source:

```json
{
  "statusLine": {
    "command": "python",
    "args": ["path/to/claude-statusline/claude_statusline/statusline.py"]
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

# Analytics & Reporting
claude-statusline costs           # Cost analysis
claude-statusline daily           # Daily report
claude-statusline sessions        # Session details
claude-statusline heatmap         # Activity heatmap
claude-statusline summary         # Summary statistics
claude-statusline models          # Model usage statistics
claude-statusline analytics       # Advanced usage analytics

# NEW v1.9.0 Features!
claude-statusline trends          # Comprehensive trend analysis
claude-statusline health          # System health monitoring

# Budget Management
claude-statusline budget          # Budget management and tracking

# Configuration and Themes
claude-statusline theme           # Interactive theme manager
claude-statusline visual-builder  # Visual theme builder with live preview
claude-statusline template        # Select display template
claude-statusline update-prices   # Update model prices
claude-statusline rotate          # Toggle statusline rotation
```

📖 **[Full CLI Documentation](CLI.md)** - Complete command reference with all options and examples

### Usage Examples

#### 📊 Advanced Analytics (NEW v1.9.0!)
```bash
# Comprehensive trend analysis
claude-statusline trends           # All trend analyses
claude-statusline trends --trends  # Usage trends only
claude-statusline trends --productivity  # Productivity patterns
claude-statusline trends --efficiency    # Model efficiency analysis
claude-statusline trends --insights      # AI-powered insights

# System health monitoring
claude-statusline health           # Quick health check
claude-statusline health --full    # Comprehensive health check
claude-statusline health --diagnostic  # Generate diagnostic report
claude-statusline health --monitor 120  # Monitor performance for 2 minutes
```

#### 📈 Usage Analytics
```bash
# Session analysis
claude-statusline sessions         # Analyze all sessions
claude-statusline sessions --patterns  # Usage patterns
claude-statusline sessions --top 10    # Top 10 sessions

# Cost analysis
claude-statusline costs            # Cost breakdown
claude-statusline costs --trends   # Cost trends analysis

# Daily and summary reports
claude-statusline daily            # Today's report
claude-statusline daily --days 7   # Last 7 days
claude-statusline summary --weekly # Weekly summary
claude-statusline summary --monthly # Monthly summary
```

#### 💰 Budget Management
```bash
# Budget dashboard and management
claude-statusline budget           # Budget dashboard
claude-statusline budget set monthly 500     # Set monthly budget
claude-statusline budget status    # Budget status
```

#### 🎨 Theme Selection
```bash
# Interactive theme browser with search
claude-statusline theme

# Quick theme changes
claude-statusline template cyberpunk
claude-statusline template nasa
claude-statusline template vscode

# Create custom theme
claude-statusline visual-builder
```

## How It Works

1. **Data Collection**: Reads Claude Code's JSONL conversation logs from `~/.claude/projects/*/`
2. **Processing**: Background daemon (`daemon.py`) processes data every 60 seconds
3. **Storage**: Maintains database in `~/.claude/data-statusline/smart_sessions_db.json`
4. **Display**: Unified theme system formats data with 100+ themes

```
Claude Code → JSONL Files → Daemon → Database → Theme System → Statusline
                              ↓
                          Rebuild.py
                     (Token extraction)
```

## Configuration

### Basic Settings (`config.json`)

```json
{
  "display": {
    "template": "pro",           // Template style
    "current_theme": "ocean_tsunami_power",  // Active theme
    "theme_system": "unified",   // Theme system
    "enable_rotation": false,
    "visual_mode": false
  },
  "monitoring": {
    "session_duration_hours": 5,  // Session block duration
    "db_update_interval": 60      // Daemon update interval
  }
}
```

### Theme Selection

```bash
# Interactive theme browser with live preview
claude-statusline theme

# List all available themes
claude-statusline theme list

# Apply a specific theme
claude-statusline theme apply ocean_tsunami_power
claude-statusline theme apply fire_king
claude-statusline theme apply matrix_rain
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
├── claude_statusline/              # Package directory
│   ├── __init__.py                # Package initialization
│   ├── __main__.py                # Package entry point
│   ├── cli.py                     # Unified CLI interface
│   ├── statusline.py              # Core statusline display
│   ├── daemon.py                  # Background processor
│   ├── rebuild.py                 # Database builder & token extraction
│   ├── unified_theme_system.py    # Theme management system
│   ├── unified_status.py          # Unified status display
│   ├── epic_powerline_mega_themes.py  # 79+ powerline themes
│   ├── ultimate_epic_themes.py    # 19+ advanced themes
│   ├── professional_powerline.py  # Professional themes
│   ├── config.json                # Configuration
│   └── prices.json                # Model pricing
├── tests/                         # Test suite
├── dist/                          # Built packages
├── setup.py                       # Package setup
├── pyproject.toml                 # Modern package config
└── README.md                      # This file
```

## Data Files

- **Source**: `~/.claude/projects/*/` - Claude Code JSONL conversation logs
- **Database**: `~/.claude/data-statusline/` - Processed data
  - `smart_sessions_db.json` - Main session database with hourly statistics
  - `daemon_status.json` - Daemon health status (PID, last update)
  - `file_tracking.json` - JSONL file processing state
  - `.unified_daemon.lock` - PID lock file for single instance
  - `custom_themes.json` - User-created themes

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
- [Template Gallery](TEMPLATES.md) - All 80+ statusline formats
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

## Themes

Claude Statusline offers **100+ epic powerline themes** with RGB colors and nerd fonts:

### 🖥️ Developer Themes
- **VSCode**, **IntelliJ**, **Sublime**, **Atom**, **Neovim**, **Emacs**
- Full system integration with git status, CPU/RAM, battery info

### 🎮 Gaming Themes  
- **Minecraft**, **Cyberpunk**, **Retro**, **RPG**, **Arcade**
- Immersive gaming interfaces with health bars, inventory, effects

### 💰 Financial/Trading Themes
- **Trading**, **Crypto**, **Stock Market**, **Banking**
- Professional trading terminal interfaces with real-time data

### 🚀 Space/Science Themes
- **NASA**, **Space Station**, **Alien Contact**, **Laboratory**
- Mission control and scientific research interfaces

### 🏥 Medical/Health Themes
- **Medical**, **Hospital**, **Pharmacy**
- Healthcare system interfaces with patient data

### 🚗 Transportation Themes
- **Aviation**, **Railway**, **Automotive**, **Maritime**
- Transportation control systems and dashboards

### 🎬 Entertainment Themes
- **Cinema**, **Music Studio**, **Sports**, **News**
- Broadcast and entertainment industry interfaces

### ⚡ Quick Theme Commands
```bash
claude-statusline theme                    # Interactive theme browser
claude-statusline theme list              # List all themes
claude-statusline theme apply <name>      # Apply specific theme
claude-statusline theme current           # Show current theme
```

---

**Current Version**: 1.9.0 | **Last Updated**: 2025-08-21 | **Package**: `claude-statusline`