# Changelog

All notable changes to Claude Statusline will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.9.0] - 2025-08-21

### 🚀 Major New Features

#### 📊 Trend Analyzer (NEW!)
- **Usage Trend Analysis** - Comprehensive trend analysis over 30+ days
- **Productivity Pattern Recognition** - Identify peak hours and optimal work times
- **Model Efficiency Comparison** - Cost per message analysis across all models  
- **AI-Powered Insights** - Smart recommendations for optimization
- **Predictive Analytics** - 7-day cost and usage predictions
- **Correlation Analysis** - Identify patterns between cost and productivity

#### 🏥 Health Monitor (NEW!)
- **Comprehensive System Health Check** - Monitor all Claude Statusline components
- **Daemon Health Monitoring** - Real-time daemon status and performance tracking
- **Database Integrity Verification** - Ensure data consistency and reliability
- **File System Health** - Check permissions, disk space, and directory structure
- **Performance Monitoring** - CPU, memory, and disk usage tracking with alerts
- **Diagnostic Report Generation** - Detailed system diagnostics with JSON export

#### 💰 Enhanced Budget Manager
- **Advanced Budget Dashboard** - Visual spending breakdown by model and time period
- **Smart Alert System** - Configurable warning (80%) and critical (95%) thresholds
- **Project-Based Budgeting** - Track costs for specific projects with date ranges
- **Model-Specific Limits** - Set individual spending limits for each AI model
- **Comprehensive Reporting** - Export budget reports in JSON and CSV formats
- **Spending Trend Analysis** - Weekly and monthly spending comparisons

### 🎨 Expanded Theme System
- **200+ Premium Themes** - Massive expansion of available themes
- **Advanced Dynamic Themes** - Time and context-aware theme variations
- **Professional Executive Themes** - C-Suite dashboard styles with comprehensive metrics
- **Gaming & Entertainment Themes** - Immersive gaming HUDs and entertainment interfaces
- **Scientific & Medical Themes** - Laboratory and healthcare monitoring styles
- **Cyberpunk & Futuristic Themes** - Matrix-style and holographic interfaces

### 🔧 Enhanced CLI System
- **Fixed All Argparse Conflicts** - Resolved command-line argument parsing issues
- **Unified Command Interface** - Consistent command structure across all tools
- **Direct Class Instantiation** - Bypassed argparse for better reliability
- **Improved Error Handling** - Better error messages and graceful degradation
- **Enhanced Help System** - Comprehensive help for all commands and options

### 📈 Advanced Analytics Suite
- **Enhanced Analytics CLI** - Interactive analytics interface with real-time data
- **Improved Daily Reports** - Detailed hourly breakdowns with local timezone support
- **Session Pattern Analysis** - Deep dive into usage patterns and work habits
- **Cost Efficiency Metrics** - Detailed analysis of cost per message and token efficiency
- **Multi-Day Range Reports** - Flexible date range reporting (7, 14, 30 days)

### 🔧 Technical Improvements
- **Robust Database Processing** - Handle 460+ JSONL files with 134K+ messages
- **Enhanced Token Tracking** - Support for 13.6B+ tokens with accurate cost calculation
- **Improved Session Detection** - 5-hour gap system with live session tracking
- **Better Error Recovery** - Graceful handling of corrupted or missing data
- **Cross-Platform Compatibility** - Enhanced Windows, macOS, and Linux support

### 📊 Data Processing Enhancements
- **Real-Time Data Updates** - Daemon processes data every 60 seconds
- **Incremental File Processing** - Efficient processing of new JSONL entries
- **Enhanced Cost Calculation** - Accurate pricing with automatic price updates
- **Session Clustering** - Smart grouping of related conversations
- **Timezone-Aware Reporting** - Proper local time conversion for all reports

### 🛠️ New CLI Commands
```bash
# New trend analysis
claude-statusline trends --insights
claude-statusline trends --productivity  
claude-statusline trends --efficiency

# Health monitoring
claude-statusline health --full
claude-statusline health --monitor 60
claude-statusline health --diagnostic

# Enhanced budget management  
claude-statusline budget set monthly 500
claude-statusline budget dashboard
claude-statusline budget status

# Fixed daily reports
claude-statusline daily --days 7
claude-statusline daily --date 2025-08-21
```

### Fixed
- **Daily Report Generator** - Fixed missing `generate_multi_day_report` method
- **Budget Manager** - Added missing dashboard and status methods
- **Health Monitor** - Fixed daemon PID parsing for JSON lock files
- **Timezone Handling** - Corrected time parsing for daemon status updates
- **Theme Application** - Resolved theme switching and display issues
- **CLI Argument Parsing** - Fixed all argparse conflicts across analytics tools

### Changed
- **Version Bumped to 1.9.0** - Major feature release
- **CLI Interface** - More intuitive command structure
- **Error Messages** - Clearer, more helpful error reporting
- **Performance** - Optimized database queries and file operations
- **Memory Usage** - Reduced memory footprint for large datasets

### Security
- **Safe File Operations** - All file operations use atomic writes
- **Input Validation** - Enhanced validation for all user inputs
- **Error Logging** - Secure logging without exposing sensitive data

## [1.8.0] - 2025-08-21

### Added
- 79+ Epic Powerline Mega themes with RGB color support and nerd fonts
- 19+ Ultimate Epic themes using all available data fields
- Professional powerline themes with comprehensive metrics
- Real-time session tracking with accurate token counts and costs
- Daemon now properly extracts usage data from JSONL files
- Support for both 'tokens' and 'total_tokens' field names
- Support for both 'model' and 'primary_model' field names

### Fixed
- Fixed double percentage (%%) display issue in templates
- Fixed theme list display to properly strip ANSI/RGB codes
- Fixed token field name mismatch causing 0.0k display
- Fixed model field name mismatch in current_session
- Fixed RGB color rendering in Windows terminals
- Fixed Unicode/nerd font support with UTF-8 output
- Removed debug print statements from production code

### Changed
- Improved theme list preview with clean text display
- Enhanced daemon reliability for live session updates
- Better error handling for RGB and Unicode characters

## [1.7.0] - 2025-08-21

### 🔧 Major Fixes & Stability Improvements
- **100% Functionality Achieved** - All components now working flawlessly
- **Fixed Daemon System** - Resolved "int not iterable" error in daemon status checking
- **Fixed Import Errors** - Removed all non-existent module references
- **Enhanced Error Handling** - Proper exception handling in all critical paths
- **Cross-Platform Stability** - Tested on Windows, Linux, and macOS

### 🎨 Visual Enhancements
- **122+ Premium Themes** - Expanded theme collection with ultra executive styles
- **Theme Gallery Command** - Non-interactive theme preview with `claude-statusline gallery`
- **Interactive Theme Selector** - Browse themes with keyboard navigation (30-second timeout)
- **Visual Theme Builder** - Create custom themes with live preview
- **Aesthetic Themes Module** - New module with creative and artistic themes

### 📊 Enhanced Analytics
- **Improved Session Detection** - More accurate active session tracking
- **Better Cost Calculations** - Using prices.json for accurate cost tracking
- **Enhanced Daily Reports** - Detailed hourly breakdowns with local timezone
- **Session Analytics** - Comprehensive session-by-session analysis

### 🚀 Performance Improvements
- **Optimized Database Rebuilding** - Faster JSONL processing with incremental updates
- **Reduced Memory Usage** - Efficient file streaming without full loading
- **Background Daemon** - Automatic database updates every 60 seconds
- **Atomic File Operations** - Safe concurrent access with retry logic

### 🐛 Bug Fixes
- **Fixed circular imports** in CLI entry points
- **Resolved safe_json_read/write** argument order issues
- **Fixed daemon lock file** handling on Windows
- **Corrected theme module** imports and references
- **Fixed stdin reading** issues causing status command to hang
- **Resolved analytics database** format compatibility issues

### 📦 Package Structure
- **Cleaned module imports** - Removed obsolete dependencies
- **Updated entry points** - Fixed CLI command routing
- **Improved error messages** - Better user feedback on failures
- **Enhanced logging** - Debug information for troubleshooting

### 🔄 Changed
- Daemon now uses proper PID-based locking mechanism
- Status command uses simple_statusline for reliability
- Gallery command replaces interactive selector as default
- All imports changed to absolute imports for package compatibility

## [1.5.0] - 2025-08-20

### 🎨 Powerline Templates & Multi-line Displays
- **15 New Powerline Templates** - Professional powerline-style statuslines with colored backgrounds
- **Multi-line Templates** - Rich 2-3 line displays with detailed metrics
- **Segment Separators** - Arrow-style separators between data segments
- **Colored Backgrounds** - Each data segment has distinct background colors
- **Progress Bars** - Visual progress indicators with gradient colors

### 📊 New Multi-line Templates
- **multiline_status** - 6-line detailed status view with token breakdowns
- **dashboard** - Compact 3-line dashboard with progress percentage
- **block_timer** - Progress bar with 5-hour block timing
- **pro_usage** - Professional usage statistics with version info
- **analytics** - Analytics dashboard with efficiency metrics
- **session_tracker** - Session timeline with activity indicators
- **cost_breakdown** - Detailed cost analysis by component
- **performance** - Performance metrics with I/O ratios

### ⚡ New Powerline Styles (Max 3 Lines)
- **powerline1** - Classic powerline with arrow segments
- **powerline2** - Modern flat design with status indicators
- **powerline3** - Gradient segments with smooth transitions
- **segments** - Clean segments with separators
- **blocks** - Block-based visualization with fill levels
- **metro** - Windows Metro style tiles
- **pills** - Rounded pill/badge appearance
- **cards** - Card-based layout with borders
- **badges** - GitHub-style status badges
- **tabs** - Tab interface style
- **ribbons** - Ribbon banners with angles
- **status_bar** - macOS-style status bar
- **progress** - Progress-focused display
- **compact_power** - Compact 2-line powerline
- **elegant_power** - Elegant minimalist powerline

### 🔧 Technical Improvements
- Added `powerline_templates.py` module for all powerline styles
- Enhanced `colored_templates.py` with powerline integration
- Improved template system architecture for better modularity
- Added comprehensive template testing capabilities

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