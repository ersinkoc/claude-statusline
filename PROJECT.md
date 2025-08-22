# Claude Statusline v1.8.0

## 🚀 Professional Real-time Session Tracking for Claude Code

A powerful Python package that provides comprehensive session tracking, cost analytics, and beautiful statusline displays for Claude Code users.

## ✨ Key Features

### 🎨 100+ Epic Powerline Themes
- Professional powerline-style themes with nerd fonts
- Advanced RGB color support with smooth gradients
- Unified theme management system
- Custom theme builder with live preview

### 📊 Real-time Analytics
- Live session tracking with accurate token counts
- Input/Output token breakdown
- Cache efficiency monitoring
- Cost tracking with official pricing

### 💼 Professional Tools
- Background daemon for automatic updates
- Comprehensive CLI with 20+ commands
- Budget management and alerts
- Usage pattern analysis
- Export reports in JSON/CSV

### 🛠️ Technical Excellence
- Cross-platform support (Windows/macOS/Linux)
- Minimal dependencies (only psutil)
- Atomic file operations for data safety
- Efficient JSONL processing
- Smart session detection (5-hour blocks)

## 📦 Installation

```bash
# From PyPI
pip install claude-statusline

# From source
pip install dist/claude_statusline-1.8.0-py3-none-any.whl
```

## 🎯 Quick Start

```bash
# View current status
claude-status

# Browse themes
claude-statusline theme

# View analytics
claude-statusline costs
claude-statusline daily
claude-statusline sessions
```

## 🏗️ Architecture

```
Claude Code (JSONL) → Daemon → Database → Statusline Display
                       ↓
                   Analytics
                   Reports
                   Themes
```

## 📂 Project Structure

```
claude-statusline/
├── claude_statusline/          # Core package
│   ├── statusline.py          # Main display logic
│   ├── daemon.py              # Background processor
│   ├── rebuild.py             # Database builder
│   ├── unified_theme_system.py # Theme management
│   ├── epic_powerline_mega_themes.py # 79+ themes
│   ├── ultimate_epic_themes.py # 19+ advanced themes
│   └── professional_powerline.py # Professional themes
├── tests/                     # Test suite
├── dist/                      # Package distributions
└── docs/                      # Documentation

Data Storage:
~/.claude/data-statusline/
├── smart_sessions_db.json     # Session database
├── daemon_status.json         # Daemon health
└── custom_themes.json         # User themes
```

## 🎨 Theme Examples

```
⚡ Opus 4.1 LIVE ● 533 msgs ⟨16.6M/16.6M⟩ $98.78 ▶ 1h20m
🔥 [Opus-4.1] ⚡ACTIVE #3 📊 533↕ 💰$98.78 ⏱1:20 🔋85%
🌊 Opus 4.1 ≋ LIVE ≋ 533 messages ≋ 16.6M tokens ≋ $98.78
```

## 🔧 Development

```bash
# Install in dev mode
pip install -e .

# Run tests
pytest

# Build package
python -m build
```

## 📈 What's New in v1.8.0

- ✅ 100+ epic powerline themes with RGB colors
- ✅ Fixed all Unicode/ANSI display issues
- ✅ Real-time token tracking with I/O breakdown
- ✅ Cache efficiency monitoring
- ✅ Fixed field name compatibility issues
- ✅ All content now in English
- ✅ Improved theme list display
- ✅ Enhanced daemon reliability

## 🤝 Contributing

Contributions welcome! The codebase is clean, well-documented, and ready for enhancements.

## 📄 License

MIT License - Free for personal and commercial use.

## 🔗 Links

- [GitHub Repository](https://github.com/ersinkoc/claude-statusline)
- [PyPI Package](https://pypi.org/project/claude-statusline/)
- [Documentation](https://github.com/ersinkoc/claude-statusline/wiki)

---

**Built with ❤️ for the Claude Code community**