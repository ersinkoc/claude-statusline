# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Statusline is a Python package that provides real-time session tracking and analytics for Claude Code usage. It processes JSONL log files from Claude Code, maintains a session database, and displays usage metrics in a compact statusline format.

## Build and Development Commands

### Installation
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"

# Build the package
python -m build
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=claude_statusline

# Run specific test file
pytest tests/test_statusline.py

# Test the statusline output directly
python -m claude_statusline.statusline

# Test current session detection
python tests/test_current_detect.py
```

### Code Quality
```bash
# Format code with black
black claude_statusline/

# Check code style with flake8
flake8 claude_statusline/

# Type checking with mypy
mypy claude_statusline/
```

### Package Distribution
```bash
# Build distribution packages
python -m build

# Check package integrity
twine check dist/*

# Upload to PyPI (when ready)
twine upload dist/*
```

## Architecture Overview

### Core Data Flow
1. **Claude Code** writes conversation logs to `~/.claude/projects/*/` as JSONL files
2. **Daemon** (`daemon.py`) runs continuously, calling rebuild every 60 seconds
3. **Rebuild** processes JSONL files, extracting tokens and grouping into 5-hour sessions
4. **Database** (`smart_sessions_db.json`) stores processed session data
5. **Statusline** reads database and formats output for Claude Code display

### Key Components

#### Entry Points
- `statusline.py`: Main entry called by Claude Code for status display
- `cli.py`: Unified CLI interface for all commands
- `daemon.py`: Background processor managing data updates

#### Data Processing
- `rebuild.py`: Core database builder processing JSONL files
- Token extraction path: `message.content[0].usage.{input_tokens, output_tokens, cache_*_tokens}`
- Sessions are 5-hour work blocks with automatic detection of active sessions

#### Utilities
- `instance_manager.py`: PID-based single instance enforcement using psutil
- `data_directory_utils.py`: Consistent path resolution to `~/.claude/data-statusline/`
- `safe_file_operations.py`: Atomic file operations with temp file writes
- `formatter.py`: Status formatting with model name resolution and cost calculation

#### Analytics Tools
- `session_analyzer.py`: Detailed session-by-session analysis
- `cost_analyzer.py`: Cost breakdown by time period and model
- `daily_report.py`: Daily usage summaries
- `activity_heatmap.py`: Visual activity patterns
- `model_usage.py`: Model-specific statistics

### Data Storage
All data is stored in `~/.claude/data-statusline/`:
- `smart_sessions_db.json`: Main session database
- `daemon_status.json`: Daemon health status
- `file_tracking.json`: JSONL file processing state
- `.unified_daemon.lock`: PID lock file

### Configuration Files
- `config.json`: Display templates, rotation settings, session duration
- `prices.json`: Model pricing data (auto-updated from remote source)

## Key Design Patterns

### Session Management
- Sessions are 5-hour blocks for typical work periods
- New session starts if gap > 5 hours between messages
- Active session detected when current time < session_end
- All timestamps in UTC for consistency

### Error Handling
- Graceful degradation: returns defaults if data unavailable
- Atomic writes prevent partial file corruption
- Stale lock detection and cleanup
- Malformed JSON skipped with logging

### Performance Optimizations
- Incremental JSONL processing (not fully loaded)
- File position tracking prevents reprocessing
- 60-second update interval balances freshness vs performance
- Efficient datetime comparisons for session grouping

## Common Development Tasks

### Adding New Analytics Command
1. Create new module in `claude_statusline/`
2. Add entry point in `cli.py` using click decorators
3. Read data from `smart_sessions_db.json`
4. Use `console_utils.py` for formatted output

### Modifying Token Extraction
Token paths are in `rebuild.py`:
- Look for `_extract_tokens_from_message()` function
- Tokens nested in: `message['content'][0]['usage']`

### Adding New Display Template
1. Edit `templates.py` to add template definition
2. Update `formatter.py` if new formatting needed
3. Add to template selector in `template_selector.py`

### Debugging Session Detection
- Check `check_current.py` for current session logic
- Session boundaries in `rebuild.py` `_should_start_new_session()`
- Live detection uses 5-hour window from session start

## External Dependencies
- **psutil**: Process management and PID checking (only external dependency)
- Python 3.8+ required
- Access to `~/.claude/` directory with Claude Code data

## Testing Approach
- Unit tests in `tests/` directory using pytest
- Test files start with `test_`
- Mock Claude Code data for testing
- Coverage target: maintain above 80%