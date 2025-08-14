# Changelog

All notable changes to Claude Statusline will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-08-14

### Added
- 20+ customizable statusline templates
- Template selector tool with interactive preview
- Template gallery documentation (TEMPLATES.md)
- CLI command for template management
- Support for different styles: vim, terminal, matrix, discord, github, etc.

### Changed
- Refactored formatter to use template system
- Updated CLI with template management commands
- Enhanced documentation with template examples

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