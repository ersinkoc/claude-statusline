# Changelog

All notable changes to Claude Statusline will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.9.5] - 2025-10-04

### 🐛 Version Synchronization Fix
- **Fixed Version Display** - Corrected version output to match actual package version
- **Updated Package Metadata** - Synchronized version numbers across all files
- **Package Consistency** - Ensured version consistency in setup.py, __init__.py, and CLI output
- **Release Preparation** - Clean version bump for PyPI publishing

### Technical Improvements
- **Version Coordination** - All version references now properly synchronized
- **Build Readiness** - Package prepared for clean PyPI publishing
- **Metadata Accuracy** - Correct version information in all package metadata

## [1.9.4] - 2025-10-04

### 📊 Model Session Analytics (FIXED)

#### Cost Calculation Corrections
- **Accurate Pricing Database** - Fixed cost calculation using official model pricing
- **Claude-Only Filtering** - Properly filters to show only Claude models (Sonnet, Opus, Haiku)
- **Database Cost Usage** - Uses pre-calculated costs from session database for accuracy
- **Model Exclusion** - GLM and other non-Claude models completely excluded from analytics

#### Fixed Issues
- **Cost Accuracy** - Corrected token cost calculations with proper pricing tiers
- **Model Filtering** - Ensures only Claude models appear in statistics
- **Data Integrity** - Clean session data without mixed model contamination
- **Pricing Consistency** - All models use correct per-million token pricing

### Technical Improvements
- **Price Data Integration** - Proper integration with prices.json for accurate calculations
- **Model Validation** - Robust model name filtering and validation
- **Cost Verification** - Cross-referenced with database-stored cost calculations

## [1.9.3] - 2025-10-04

### 📊 Model Session Analytics (NEW!)

#### Model-Specific Session Statistics
- **Session-by-Session Breakdown** - Detailed statistics for each model per session
- **Comprehensive Token Analysis** - Input, output, cache read, and total tokens per session
- **Cost Tracking** - Individual session costs and totals per model
- **Session Duration Analysis** - Track session length and active hours
- **Multi-Model Support** - Statistics available for all models: Claude, GLM, etc.

#### New CLI Command
- **`model-sessions` Command** - Complete model-specific session analytics
- **Filtering Options** - Filter by specific model or limit number of sessions
- **Model Listing** - List all available models in the database
- **Summary Statistics** - Average tokens, costs, and most active hours per model

#### Technical Features
- **Hourly Data Extraction** - Intelligent session statistics from hourly data
- **Smart Session Mapping** - Maps work sessions to hourly model usage
- **Performance Optimized** - Efficient data processing for large session histories
- **Console Safe Output** - Cross-platform Unicode and emoji support

### Usage Examples
```bash
# List all available models
claude-statusline model-sessions --list-models

# Show all sessions for specific model
claude-statusline model-sessions --model claude-sonnet-4-5-20250929

# Limit results to recent sessions
claude-statusline model-sessions --model glm-4.5 --limit 10

# Show all models and all sessions
claude-statusline model-sessions
```

## [1.9.2] - 2025-08-22

### 🔧 Model Filtering Enhancement

#### Claude-Only Processing
- **Exclusive Claude Model Support** - Now only processes models starting with "claude-"
- **Non-Claude Model Exclusion** - Automatically filters out GLM, synthetic, and other non-Claude models
- **Comprehensive Filtering** - Applied filtering at all levels: message processing, model statistics, session tracking, and work sessions
- **Clean Data Integrity** - Ensures database only contains Claude model usage data

### Technical Improvements
- **Enhanced Rebuild Process** - Complete model filtering in rebuild.py
- **Model Statistics Accuracy** - Only Claude models contribute to statistics and cost calculations
- **Session Management** - Work sessions created with only Claude model data
- **Primary Model Selection** - Automatically selects most used Claude model as primary

## [1.9.1] - 2025-08-22

### 🎨 Visual Enhancements

#### Two-Line Powerline Display (NEW!)
- **Progress Bar on Second Line** - Visual session progress with block characters
- **Session Progress Tracking** - Shows completion percentage (0-100%)
- **Time Display** - Elapsed time on left, remaining time on right of progress bar
- **Dynamic Colors** - Green (fresh), Yellow (mid), Orange (ending) based on progress
- **Unicode Block Characters** - Clean ◼ (filled) and ◻ (empty) blocks for progress

#### Refined Visual Elements
- **⧂ Starting Character** - Circle with small circle for softer line beginnings
- **❱ Chevron Separators** - Added directional flow indicators in progress bar
- **Model Name Fix** - "Opus-4" instead of "Op-4" for better clarity
- **Improved Time Formatting** - Consistent HH:MM format with zero padding

### Fixed
- **Session elapsed time formatting** - Added proper timezone handling
- **Progress calculation** - Fixed timezone issues in session progress
- **Multi-line output** - Proper handling of newlines in statusline display
- **Unicode output** - Better buffer handling for Windows terminals

### Technical Details
- Updated `unified_powerline_system.py` with `_render_progress_bar()` method
- Added `_calculate_session_progress()` for accurate progress tracking
- Modified statusline output to handle multi-line content correctly
- Enhanced Unicode character handling for cross-platform compatibility

## [1.9.0] - 2025-08-22

### 🚀 Major New Features

#### 🎨 Unified Powerline Theme System (NEW!)
- **100 Professional Powerline Themes** - Carefully designed themes with logical widget grouping
- **Interactive Theme Browser** - Navigate themes with live preview, search, and simple commands
- **Custom Theme Builder** - Create and save personalized powerline designs with color scheme selection
- **Advanced RGB Color System** - Soft, eye-friendly color schemes instead of harsh RGB values
- **Smart Widget Grouping** - Token widgets now grouped together consecutively for better organization
- **Real-time Data Integration** - Live token counts, cache efficiency, and session metrics
- **Nerd Font Icon System** - Creative, diverse icons for each widget type

#### 📊 Enhanced Analytics Suite
- **Comprehensive Trend Analysis** - Usage patterns, productivity insights, and optimization recommendations
- **System Health Monitoring** - Performance diagnostics and bottleneck detection
- **Advanced Budget Management** - Set spending limits and track budget compliance with alerts
- **Session Pattern Analysis** - Deep dive into usage patterns and work habits
- **Cost Efficiency Metrics** - Detailed analysis of cost per message and token efficiency
- **Multi-timeframe Reporting** - Flexible date range reporting (daily, weekly, monthly)

#### 🔧 Enhanced User Experience
- **Simplified Interactive UI** - Clean, functional theme browser without complex boxes
- **Live Preview System** - See actual powerline rendering with real data before applying
- **Theme Search & Navigation** - Search themes by name, jump to specific numbers, random selection
- **Folder Name Integration** - Display current working directory in statusline
- **Session End Time Display** - Shows when current session will end in local timezone
- **Git Branch Enhancement** - Dedicated git-specific icons for repository information

### 🎯 Smart Widget System
- **Logical Widget Organization** - Related widgets (tokens, time, etc.) are now consecutive
- **Intelligent Widget Selection** - Avoids redundant time widgets (only one per theme)
- **Enhanced Data Fields** - Folder name, session end time, improved session numbering
- **Priority Widget System** - Important widgets (git, folder) prioritized in theme generation
- **Token Widget Grouping** - Input/output/cache tokens grouped together for clarity

### 🎨 Theme Browser Features
- **Simple Navigation** - Commands: n/j (next), p/k (previous), r (random), q (quit)
- **Direct Number Access** - Type theme number (1-100) to jump directly
- **Search Functionality** - Search themes by name with "/" command
- **Live Data Preview** - Shows real session data in theme previews
- **Theme Builder Access** - Built-in custom theme creator with "b" command
- **Clean UI Design** - No complex boxes, just functional text interface

### 🔧 Technical Improvements
- **Codebase Cleanup** - Removed 16 obsolete files for cleaner architecture
- **Unified Architecture** - Single powerline system replaces multiple theme systems
- **Better Unicode Support** - Enhanced nerd font and Unicode character handling
- **Console Output Optimization** - Improved safe Unicode printing with UTF-8 support
- **Fixed Import System** - Resolved all broken imports after cleanup
- **Enhanced Error Handling** - Better error recovery in theme rendering

### 🛠️ New CLI Commands
```bash
# Interactive theme browser
claude-statusline theme

# Theme commands
claude-statusline theme build     # Custom theme builder
claude-statusline theme list      # List all themes  
claude-statusline theme apply     # Apply specific theme

# All existing analytics commands remain unchanged
claude-statusline analytics      # Advanced usage analytics
claude-statusline trends         # Usage trends and patterns
claude-statusline health         # System health monitoring
claude-statusline budget         # Budget management
```

### 🗂️ Removed Obsolete Files
- `epic_powerline_mega_themes.py` - Old theme system
- `epic_powerline_themes.py` - Old theme system
- `fixed_powerline_themes.py` - Old theme system
- `mega_widget_system.py` - Old widget system
- `modern_powerline_art.py` - Old theme system
- `powerline_themes.py` - Old theme system
- `professional_powerline.py` - Old theme system
- `pure_powerline_renderer.py` - Old renderer
- `theme_selector.py` - Replaced by interactive manager
- `ultimate_epic_themes.py` - Old theme system
- `ultimate_powerline_themes.py` - Old theme system
- `unified_status.py` - Old status system
- `unified_theme_system.py` - Replaced by unified powerline system
- `widget_system.py` - Old widget system
- `usage_analytics.py` - Duplicate functionality
- `fallback_renderer.py` - Old fallback system

### Fixed
- **Session Number Display** - Now shows "#2" instead of just "2" for better clarity
- **Timezone Handling** - Uses system timezone instead of hardcoded UTC+3
- **Theme Loading** - Removed dependency on obsolete theme systems
- **Import Errors** - Fixed broken imports after code cleanup
- **Widget Positioning** - Proper powerline triangle transitions between widgets
- **Icon Selection** - More diverse, creative icons instead of repetitive emojis
- **Unicode Output** - Better terminal compatibility across platforms
- **Theme Organization** - Token widgets properly grouped together

### Changed
- **Version Bumped to 1.9.0** - Major theme system overhaul
- **Architecture** - Single unified powerline system
- **Widget Logic** - Smart grouping and selection algorithms
- **Color System** - Soft, pleasant colors throughout all themes
- **Navigation** - Simplified command-based theme browser
- **File Organization** - Cleaner codebase with only essential files

### Technical Details
- Moved `safe_unicode_print` function to `console_utils.py`
- Updated `__init__.py` to reflect new architecture
- Fixed `__main__.py` import references
- Consolidated theme management under `unified_powerline_system.py`
- Enhanced CLI help documentation
- Improved error handling in theme rendering

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