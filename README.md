# Claude Statusline

Real-time session tracking and analytics for Claude Code with 100+ powerline themes and comprehensive analytics.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Version](https://img.shields.io/badge/version-1.9.8-green.svg)

## Features

### Core Features
- 📊 **Real-time Monitoring** - Track active sessions with live updates
- 💰 **Cost Tracking** - Accurate cost calculation based on official pricing
- 🤖 **Multi-Model Support** - Track Opus, Sonnet, and Haiku models
- 📁 **Git Integration** - Shows branch info and repository status
- 💻 **System Info** - CPU, memory, and folder information
- ⚡ **Lightweight** - Minimal dependencies (only psutil)
- 📦 **Easy Installation** - Available as a Python package

### Powerline Themes (v1.9.1 - NEW!)
- 🎨 **100 Professional Themes** - Carefully designed powerline themes with logical widget grouping
- 🌈 **Advanced RGB Colors** - True color output with soft, pleasant color schemes
- 🔧 **Interactive Theme Browser** - Navigate themes with live preview and search
- 🎯 **Custom Theme Builder** - Create and save your own powerline designs
- ⚡ **Real-time Data** - Live token counts, cache efficiency, and session metrics
- 📱 **Smart Widget Organization** - Related widgets grouped together (tokens, time, etc.)
- 📊 **Two-Line Display** - Progress bar on second line showing session completion (◼◻)
- ⧂ **Visual Enhancements** - Refined Unicode characters for softer appearance

### Analytics & Reporting
- 📈 **Advanced Usage Analytics** - Comprehensive productivity metrics and insights
- 📊 **Trend Analysis** - Usage trends, productivity patterns, and optimization recommendations
- 🏥 **Health Monitoring** - System health diagnostics and performance monitoring
- 💹 **Budget Management** - Set spending limits and track budget compliance
- 📊 **Usage Patterns Analysis** - Behavioral insights and optimization recommendations
- 📉 **Cost Forecasting** - Predict future costs based on usage trends
- 📋 **Export Reports** - Generate detailed reports for external analysis
- 🚨 **Smart Alerts** - Budget warnings and usage anomaly detection
- 🎯 **Unified CLI** - Single command interface for all features

## Quick Start

### Install from PyPI

```bash
# Install the package
pip install claude-statusline

# View current status
claude-statusline status

# Browse themes interactively
claude-statusline theme

# Start background daemon
claude-statusline daemon --start

# View analytics
claude-statusline analytics
```

### Commands Overview

```bash
# Core Commands
claude-statusline status          # Show current session status
claude-statusline daemon --start  # Start background monitoring
claude-statusline theme          # Interactive theme browser
claude-statusline rebuild        # Rebuild database from logs

# Analytics Commands
claude-statusline analytics      # Advanced usage analytics
claude-statusline trends         # Usage trends and patterns
claude-statusline health         # System health monitoring
claude-statusline budget         # Budget management
claude-statusline sessions       # Session analysis
claude-statusline model-sessions # Model-specific session statistics
claude-statusline costs          # Cost analysis
claude-statusline daily          # Daily reports
claude-statusline heatmap        # Activity heatmaps
claude-statusline summary        # Summary statistics

# Utilities
claude-statusline update-prices  # Update model pricing
claude-statusline verify         # Verify cost calculations
claude-statusline rotate         # Theme rotation settings
```

## Theme System

The powerline theme system provides 100 professionally designed themes with:

- **Smart Widget Grouping** - Related widgets (tokens, time, etc.) are consecutive
- **Pleasant Color Schemes** - Soft, eye-friendly RGB colors instead of harsh tones
- **Nerd Font Icons** - Creative, diverse icons for each widget type
- **Live Preview** - See real data in themes before applying
- **Custom Themes** - Build and save your own designs
- **Interactive Browser** - Navigate with simple commands (n/p for next/previous)

### Theme Browser Commands

```
n/j = Next theme        p/k = Previous theme     ENTER = Apply theme
r   = Random theme      g   = Go to number       q     = Quit
+10 = Jump forward     -10 = Jump back           /     = Search
b   = Theme builder
```

## Analytics Features

### Model Session Analytics (v1.9.3 - NEW!)
- **Session-by-Session Breakdown** - Detailed statistics for each model per session
- **Token-Level Analysis** - Input, output, cache creation, and cache read tokens
- **Accurate Cost Calculation** - Precise cost tracking based on official model pricing
- **Model Filtering** - Focus on specific Claude models (Sonnet, Opus, Haiku)
- **Performance Metrics** - Session duration, message count, and most active hours

### Trend Analysis
- Usage patterns over time
- Productivity insights
- Model efficiency analysis
- Peak usage hours identification
- Seasonal trends detection

### Health Monitoring
- System performance metrics
- Database health checks
- Daemon status monitoring
- Performance bottleneck detection

### Budget Management
- Set monthly/weekly spending limits
- Real-time budget tracking
- Overspend warnings
- Cost projection alerts

## Installation

### From PyPI (Recommended)
```bash
pip install claude-statusline
```

### From Source
```bash
git clone https://github.com/yourusername/claude-statusline.git
cd claude-statusline
pip install -e .
```

## Configuration

The tool automatically creates configuration in `~/.claude/data-statusline/`:

- `smart_sessions_db.json` - Session database
- `theme_config.json` - Current theme settings
- `daemon_status.json` - Background daemon status
- `config.json` - General configuration
- `prices.json` - Model pricing data

## Requirements

- Python 3.8+
- Claude Code (for session data)
- psutil (automatically installed)

## Architecture

```
Claude Code → JSONL Logs → Database Builder → Analytics Tools
                    ↓
               Session Database ← Background Daemon
                    ↓
            Statusline Display ← Theme System
```

## Data Privacy

- All data stays local on your machine
- No network requests except for price updates
- Session data derived only from Claude Code logs
- No telemetry or tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Changelog

### v1.9.8 (Latest) - Rebuild Function Bug Fix (HOTFIX)
- **FIXED**: Database rebuild command now correctly returns success/failure status
- **FIXED**: CLI shows "[OK] Database rebuild completed" on successful rebuild
- **FIXED**: Missing return value in `rebuild_database()` method resolved

### v1.9.7 - Architecture Improvement - Centralized Model Management
- **NEW**: Centralized `model_utils.py` with unified model display functions
- **NEW**: Dynamic model names loaded from prices.json with tier-based emojis (🧠🎭⚡🔮)
- **IMPROVED**: Consistent model display across all analytics and statusline modules
- **IMPROVED**: Smart model classification (flagship, balanced, fast, special)
- **TECHNICAL**: Eliminated duplicate code across 8+ files using DRY principles
- **TECHNICAL**: Enhanced extensibility for adding new models without multiple updates

### v1.9.6 - CLI Version Display Fix (HOTFIX)
- **FIXED**: CLI --version command now shows correct version instead of hard-coded v1.9.0
- **FIXED**: Version output now dynamically reads from __version__ variable
- **IMPROVED**: Automatic synchronization between CLI version and package version

### v1.9.5 - Version Synchronization Fix
- **FIXED**: Version display inconsistency between CLI output and package version
- **FIXED**: Synchronized version numbers across all package files
- **IMPROVED**: Package consistency for clean PyPI publishing
- **TECHNICAL**: Version coordination and metadata accuracy

### v1.9.4 - Model Session Analytics (Fixed)
- **NEW**: `model-sessions` command for detailed session-by-session statistics
- **NEW**: Model-specific cost calculation with accurate pricing data
- **NEW**: Token-level breakdown (input, output, cache creation, cache read)
- **NEW**: Performance metrics per session (duration, messages, active hours)
- **NEW**: Model filtering - focus only on Claude models (excludes GLM)
- **IMPROVED**: Accurate cost calculation using official model pricing
- **FIXED**: Removed non-Claude models from analytics for cleaner data
- **FIXED**: Correct cost calculation using official model pricing database
- **FIXED**: Proper model filtering showing only Claude models (Sonnet, Opus, Haiku)

### v1.9.3 - Model Session Analytics
- **NEW**: Initial model session statistics implementation
- **NEW**: Session-by-session breakdown for each model

### v1.9.2 - Model Filtering Enhancement
- **IMPROVED**: Exclusive Claude model support in data processing
- **IMPROVED**: Comprehensive filtering at all levels of data processing
- **IMPROVED**: Clean data integrity with only Claude model usage

### v1.9.1 - Visual Enhancements
- **NEW**: Two-line powerline display with progress bar
- **NEW**: Session progress tracking with visual indicators
- **IMPROVED**: Enhanced visual presentation

### v1.9.0 - Powerline Theme System
- **NEW**: 100 professional powerline themes with smart widget grouping
- **NEW**: Interactive theme browser with live preview and search
- **NEW**: Custom theme builder for creating personalized designs
- **NEW**: Advanced RGB color system with soft, pleasant color schemes
- **NEW**: Comprehensive trend analysis and productivity insights
- **NEW**: System health monitoring and diagnostics
- **IMPROVED**: Unified powerline system replaces all previous theme systems
- **IMPROVED**: Token widgets now grouped together logically
- **IMPROVED**: Cleaned up codebase by removing 16 obsolete files
- **FIXED**: Better Unicode and nerd font support across platforms
- **FIXED**: Improved theme organization and consistency

### v1.8.0
- Advanced analytics and budget management
- Multi-model cost tracking improvements
- Enhanced session detection
- Performance optimizations

## Support

For issues, feature requests, or questions:
- Create an issue on GitHub
- Check the documentation in the `/docs` folder
- Review the CLI help with `claude-statusline --help`