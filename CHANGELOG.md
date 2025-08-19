# Changelog

All notable changes to Claude Statusline will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2025-08-19

### 🎨 Major Theme System Overhaul
- **80+ Unique Themes** - Massive collection of professional statusline templates
- **Enhanced Existing Themes** - All templates now show git info, system stats, battery, folder name, session number
- **Colored Terminal Output** - Beautiful colored statusline display with cross-platform support
- **Customizable Color Schemes** - Configure colors for each statusline element

### 🖥️ Developer Themes
- **VSCode**, **IntelliJ**, **Sublime**, **Atom**, **Neovim**, **Emacs** styles
- Full system integration with git branch, CPU/RAM usage, battery status
- Professional IDE-style layouts with comprehensive information

### 🎮 Gaming Themes  
- **Minecraft** - Complete survival mode with health/hunger bars, items, biomes
- **Cyberpunk** - Neural interface with glitch effects, corp names, system monitoring
- **Retro**, **Arcade**, **RPG** - Immersive gaming interfaces with scores and stats

### 💰 Financial/Trading Themes (NEW)
- **Trading** - Stock market terminal with tickers, trends, volume
- **Crypto** - Cryptocurrency exchange with blockchain data, mining info
- **Stock Market** - Bloomberg-style terminal with P/E ratios, 52-week data
- **Banking** - Secure banking interface with account numbers, transactions

### 🚀 Space/Science Themes (NEW)
- **NASA** - Mission Control with altitude, velocity, fuel, communications
- **Space Station** - ISS operations with orbit data, solar power, experiments
- **Alien Contact** - Xenotech interface with coordinates, energy levels
- **Laboratory** - Scientific research with samples, pH levels, temperature

### 🏥 Medical/Health Themes (NEW)
- **Medical** - Healthcare system with patient ID, vital signs, billing
- **Hospital** - Hospital management with room numbers, bed capacity
- **Pharmacy** - Prescription system with RX numbers, inventory

### 🚗 Transportation Themes (NEW)
- **Aviation** - Air traffic control with flight numbers, altitude, heading
- **Railway** - Train dispatch with platforms, speed, passenger count
- **Automotive** - Vehicle diagnostics with VIN, odometer, fuel level
- **Maritime** - Harbor control with vessel names, coordinates, cargo

### 🎬 Entertainment Themes (NEW)
- **Cinema** - Movie theater with showtimes, ratings, seat capacity
- **Music Studio** - Recording studio with BPM, musical keys, track numbers
- **Sports** - Stadium broadcast with scores, plays, revenue
- **News** - Broadcast newsroom with breaking news, ratings, stories

### 🔧 Visual Theme Builder (NEW)
- **Interactive Theme Creator** - Build custom themes with live preview
- **Drag-and-Drop Interface** - Easy field selection and reordering
- **40+ Configurable Fields** - Choose any combination of data to display
- **Color Presets** - 7 professional color schemes (Ocean, Forest, Sunset, etc.)
- **Quick Templates** - Pre-built configurations (Minimal, Developer, Detailed, etc.)
- **Save & Apply** - Save custom themes and apply instantly

### 📊 Advanced Analytics System (NEW)
- **Usage Analytics** - Comprehensive productivity metrics and insights
- **Behavioral Analysis** - Usage patterns, peak hours, session clustering
- **Cost Forecasting** - Predict future costs based on usage trends
- **Optimization Recommendations** - Smart suggestions for efficiency improvements
- **Export Functionality** - Generate JSON/CSV reports for external analysis
- **Model Performance Comparison** - Analyze cost efficiency across models

### 💰 Budget Management System (NEW)
- **Budget Limits** - Set daily, weekly, monthly, yearly spending limits
- **Model-Specific Limits** - Control spending per model type
- **Project Budgets** - Track costs for specific projects
- **Alert System** - Warning at 80%, critical at 95% of budget
- **Spending Trends** - Visual spending patterns over time
- **Budget Recommendations** - Smart daily limits based on monthly budget

### 🎯 Enhanced CLI
- **Interactive Theme Manager** - Browse, search, and preview all themes  
- **Visual Builder Command** - `claude-statusline visual-builder`
- **Theme Categories** - Organized theme browsing by profession/interest
- **Search Functionality** - Find themes by name, category, or description
- **Analytics Commands** - `claude-analytics` for usage insights
- **Budget Commands** - `claude-budget` for financial management

### 🔧 Technical Improvements
- **System Information** - Real-time CPU, memory, battery monitoring
- **Git Integration** - Branch names, repository status, modification indicators
- **Enhanced Data Pipeline** - More efficient data extraction and formatting
- **Cross-Platform Compatibility** - Improved Windows, macOS, Linux support
- **Theme Count** - Increased from 80+ to 86 total themes (66 colored, 20 standard)

### Changed
- **formatter.py** - Enhanced with color support while maintaining backward compatibility
- **requirements.txt** - Added colorama>=0.4.6 as a dependency
- **Default template** - Set to 'compact' for optimal colored display
- **Theme Preview** - Now shows after selection, not immediately in list

### Fixed
- **Theme Selection Bug** - Fixed unpacking error with RPG and mono themes
- **Import Errors** - Fixed duplicate imports in analytics and budget modules
- **Console Utils** - Added `print_colored()` function for color output

## [1.3.3] - 2025-08-14

### Fixed
- **All import-time file operations** - Fixed check_current.py and check_session_data.py
- All file operations now happen in main() functions
- No files are read during module import

## [1.3.2] - 2025-08-14

### Fixed
- **Import-time file reading errors** - Fixed modules that were reading files during import
- Database file checks now happen at runtime, not import time
- Added proper error messages when database doesn't exist

## [1.3.1] - 2025-08-14

### Removed
- **Short alias `cs`** - Removed the short command alias to avoid conflicts with other tools
- All references to `cs` command in documentation

### Changed
- Updated all documentation to use full `claude-statusline` command
- Cleaned up CLI help text

## [1.3.0] - 2025-08-14

### Added
- **Python package structure** - Fully packaged as `claude-statusline`
- **Console entry points** - Direct commands like `claude-status`
- **Unified CLI interface** - Single command interface for all tools
- **Package installation support** - Install via pip with `pip install claude-statusline`
- **Development mode** - Support for editable installation with `pip install -e .`
- **Build configuration** - Modern packaging with `setup.py` and `pyproject.toml`
- **20+ customizable statusline templates** - Various display styles
- **Template selector tool** - Interactive preview and selection
- **Template gallery documentation** - TEMPLATES.md with all formats
- **Automatic price updates** - Fetch latest model pricing from official source
- **Comprehensive CLI documentation** - Full command reference in CLI.md
- **Claude Code integration guide** - CLAUDE_CODE_SETUP.md

### Changed
- **Complete project restructuring** - All modules moved to `claude_statusline/` package
- **Import system** - Updated to use relative imports throughout
- **CLI architecture** - Refactored from subprocess to direct module calls
- **Formatter system** - Now uses modular template system
- **Documentation** - Updated for package installation and usage
- **Configuration** - Improved config file handling and locations
- **Error handling** - Removed sys.stdout/stderr overrides for better compatibility

### Fixed
- **Windows encoding issues** - Removed problematic Unicode character handling
- **Import errors** - Fixed all relative imports for package structure
- **CLI I/O errors** - Resolved file handle issues in package mode
- **Database filtering** - Skip synthetic model messages

## [1.2.0] - 2025-08-14

### Changed
- Significantly reduced statusline length from 60+ to ~44 characters
- Improved readability with balanced formatting
- Removed excessive brackets for cleaner display
- Optimized model name display (e.g., "Opus 4.1" remains readable)
- Simplified time display format
- Made cost display more intelligent (adjusts decimal places based on amount)

### Fixed
- Windows console Unicode character compatibility issues
- Replaced Unicode symbols with ASCII alternatives

## [1.1.0] - 2025-08-13

### Added
- Visual statusline formatter with improved display
- Statusline rotation system for variety
- Support for multiple model tracking
- Session end time display
- Automatic daemon management
- Database persistence for sessions
- Cost tracking with configurable precision

### Changed
- Improved session data synchronization
- Enhanced error handling and fallback displays
- Optimized performance for faster statusline generation

### Fixed
- Session expiration time calculations
- Database update synchronization

## [1.0.0] - 2025-08-12

### Added
- Initial release of Claude Statusline
- Basic session tracking functionality
- Model identification and display
- Message count tracking
- Token usage monitoring
- Cost calculation and display
- Session timer with 5-hour duration
- Configuration file support
- Windows and Unix compatibility
- Daemon process management
- JSONL file parsing for Claude Code sessions

### Known Issues
- Some Unicode characters may not display correctly on Windows terminals
- Session tracking may occasionally miss updates during rapid interactions

## [0.1.0] - 2025-08-10 (Pre-release)

### Added
- Proof of concept implementation
- Basic JSONL parsing
- Simple statusline output
- Initial project structure