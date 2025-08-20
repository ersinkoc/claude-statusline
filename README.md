# Claude Statusline

Real-time session tracking and analytics for Claude Code, displaying usage metrics in a compact statusline format.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Version](https://img.shields.io/badge/version-1.4.0-green.svg)

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
- 🎨 **86+ Display Templates** - Massive collection of themed statuslines
- 🌈 **Colored Output** - Rich terminal colors with customizable schemes
- 🔧 **Visual Theme Builder** - Interactive theme creator with live preview
- 🎯 **Custom Themes** - Create and save your own statusline designs

### Analytics & Reporting (NEW v1.4.0)
- 📈 **Advanced Usage Analytics** - Comprehensive productivity metrics and insights
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
# Developer Themes
◈ Opus 4.1 ● LIVE #3 ⎇ main 📁 MyProject Ln 51, Col 4.3M $10.15 ⏰ 1h20m 🖥️ 11% 🧠 52% 🔋85% UTF-8  # VSCode
🧠 Opus 4.1  LIVE  📁 MyProject ⚡ main ↕ 533 msgs ∑ 46.2M tokens $ 98.778 ⏱️ 1h20m 🖥️ CPU: 21% RAM: 52% Session #3 | 23:42  # IntelliJ

# Gaming Themes  
🏹 [Opus 4.1] 🌍 MyProject Biome Day 3 ♥♥♥♥♥ 🍖🍖🍖🍖🍖 XP: 51 💎 4.3M ⛃ 10 Coins ⏰ 1h20m  # Minecraft
◢NEURAL◤ [Opus 4.1] ⟦ONLINE⟧ CORP: MYPROJ RAM: 51GB CPU: 4.3MGHz €$ 10.2K SYS: 21% 52% NET: main TIME: 1h20m▒ ◢#003◤  # Cyberpunk

# Professional Themes
🚀 NASA HOUSTON [Opus 4.1 MISSION CONTROL] GO/NO-GO: LIVE MISSION: CLAUDE-03 ALT: 5100km VEL: 7846m/s FUEL: 2% COMMS: 533 T- 1h20m | 23:42 UTC 🌍 EARTH ORBIT  # NASA
₿ MYPC [Opus 4.1 BLOCKCHAIN] ● $98.778780 24H: 46.2M VOL: 533B MCAP: $52649090K MINING: 13% 53% ⛏️ #3 | 1h20m  # Crypto
🏥 MEDICAL CENTER [DR. Opus 4.1] ● STABLE ID: PT-0003 ♥ 73BPM VISITS: 533 RECORDS: 46.2M BILL: $98.78 ⏰ 1h20m | 23:42 🚑 WARD-MyP  # Medical
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
pip install dist/claude_statusline-1.4.0-py3-none-any.whl

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

# Analytics & Reporting (NEW!)
claude-statusline costs           # Cost analysis
claude-statusline daily           # Daily report
claude-statusline sessions        # Session details
claude-statusline heatmap         # Activity heatmap
claude-statusline summary         # Summary statistics
claude-analytics dashboard        # Comprehensive usage analytics (NEW!)
claude-analytics productivity     # Productivity metrics (NEW!)
claude-analytics patterns         # Usage pattern analysis (NEW!)
claude-analytics export           # Export analytics data (NEW!)

# Budget Management (NEW!)
claude-budget dashboard           # Budget overview & alerts
claude-budget set <period> <amt>  # Set budget limits
claude-budget model-limit         # Set model-specific limits
claude-budget project <name> <$>  # Project budget tracking
claude-budget export              # Export budget reports

# Configuration and Themes
claude-statusline theme           # Interactive theme manager
claude-statusline visual-builder  # Visual theme builder with live preview
claude-statusline template        # Select display template
claude-statusline update-prices   # Update model prices
claude-statusline rotate          # Toggle statusline rotation
```

📖 **[Full CLI Documentation](CLI.md)** - Complete command reference with all options and examples

### Usage Examples

#### 📊 Analytics Dashboard
```bash
# View comprehensive analytics for last 30 days
claude-analytics dashboard --days 30

# Get productivity metrics with recommendations
claude-analytics productivity --days 7

# Analyze usage patterns and behaviors
claude-analytics patterns --days 30

# Export detailed analytics report
claude-analytics export --days 30 --format json
```

#### 💰 Budget Management
```bash
# Set monthly budget with alerts
claude-budget set monthly 500

# Set daily limit for specific model
claude-budget model-limit claude-3-5-sonnet 10.0 --monthly 300

# View budget status with spending trends
claude-budget dashboard

# Set project-specific budget
claude-budget project "MyApp Development" 1000 --start 2025-01-01 --end 2025-03-31

# Export budget report
claude-budget export --format csv
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

Claude Statusline offers **80+ unique themes** across multiple categories:

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
claude-statusline visual-builder          # Create custom themes
claude-statusline theme apply vscode      # Apply specific theme
claude-statusline theme search developer  # Search themes
```

---

**Current Version**: 1.4.0 | **Last Updated**: 2025-08-19 | **Package**: `claude-statusline`
