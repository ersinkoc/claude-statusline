# Claude Statusline Architecture Documentation

## Overview

Claude Statusline is a comprehensive monitoring system for Claude Code usage. It processes JSONL log files from Claude Code, maintains a session database, and provides real-time status and analytics tools.

## Core Components

### 1. Main Entry Point

#### **statusline.py**
- **Purpose**: Main entry point called by Claude Code to display current status
- **Key Functions**:
  - Starts the daemon if not running
  - Reads session data from `smart_sessions_db.json`
  - Formats and outputs statusline in format: `[Model] [Status] [Time] [Messages] [Tokens] [Cost]`
  - Uses `simple_visual_formatter.py` for formatting
- **Dependencies**: `unified_daemon.py`, `simple_visual_formatter.py`
- **Output**: Single line status string to stdout

### 2. Data Processing Core

#### **unified_daemon.py**
- **Purpose**: Background daemon that continuously processes Claude Code JSONL files
- **Key Functions**:
  - Runs three concurrent threads:
    1. **Database Updater**: Rebuilds database every 60 seconds
    2. **Live Tracker**: Updates live session data (currently disabled)
    3. **Status Writer**: Writes daemon status to `daemon_status.json`
  - Manages PID-based locking to ensure single instance
  - Handles graceful shutdown on SIGTERM/SIGINT
- **Files Created/Updated**:
  - `smart_sessions_db.json` - Main session database
  - `daemon_status.json` - Daemon health status
  - `live_session.json` - Live session tracking
  - `.unified_daemon.lock` - PID lock file

#### **rebuild_database.py**
- **Purpose**: Core database builder that processes all JSONL files
- **Key Functions**:
  - Scans `~/.claude/projects/*/` for JSONL files
  - Extracts token usage from nested message structure
  - Groups messages into 5-hour sessions
  - Calculates costs based on `prices.json`
  - Detects and tracks current active session
  - Maintains file position tracking in `file_tracking.json`
- **Session Logic**:
  - Sessions are 5-hour blocks
  - New session starts if gap > 5 hours between messages
  - Active session detected if current time < session_end
- **Token Extraction Path**: 
  ```
  message.content[0].usage.input_tokens
  message.content[0].usage.output_tokens
  message.content[0].usage.cache_creation_input_tokens
  message.content[0].usage.cache_read_input_tokens
  ```

### 3. Utility Modules

#### **instance_manager.py**
- **Purpose**: Manages single-instance enforcement using PID locks
- **Key Functions**:
  - `ensure_single_instance()` - Prevents multiple daemon instances
  - `_is_process_running()` - Uses psutil to check if PID exists
  - Handles stale lock cleanup
- **External Dependencies**: `psutil`

#### **data_directory_utils.py**
- **Purpose**: Resolves data directory paths consistently
- **Key Functions**:
  - `resolve_data_directory()` - Returns `~/.claude/data-statusline/`
  - Ensures directory exists
  - Provides single source of truth for data location

#### **safe_file_operations.py**
- **Purpose**: Provides safe file I/O operations with error handling
- **Key Functions**:
  - `safe_json_read()` - Reads JSON with fallback to empty dict
  - `safe_json_write()` - Atomic write with temp file
  - Handles file locks and permissions

#### **console_utils.py**
- **Purpose**: Console output formatting utilities
- **Key Functions**:
  - Color output support detection
  - Box drawing for reports
  - Progress indicators
  - Cross-platform console handling

#### **simple_visual_formatter.py**
- **Purpose**: Formats session data for statusline display
- **Key Functions**:
  - `format_status()` - Main formatting entry point
  - `_format_model()` - Model name resolution from prices.json
  - `_format_tokens()` - Human-readable token counts (12.3M)
  - `_format_cost()` - Currency formatting ($123.45)
  - `_format_time()` - Session time formatting

### 4. Analytics Tools

#### **session_analyzer.py**
- **Purpose**: Detailed session-by-session analysis
- **Key Functions**:
  - Lists all sessions with start/end times
  - Shows message count, token usage, costs per session
  - Calculates session duration and gaps
  - Provides daily/weekly/monthly summaries
- **Output**: Formatted table with session details

#### **cost_analyzer.py**
- **Purpose**: Cost analysis and breakdown by time period
- **Key Functions**:
  - Daily/weekly/monthly cost aggregation
  - Model-specific cost breakdown
  - Cost trends and projections
  - Budget tracking and alerts
- **Output**: Cost reports with trends

#### **daily_report.py**
- **Purpose**: Day-by-day usage summary
- **Key Functions**:
  - Daily message/token/cost totals
  - Session count per day
  - Average session metrics
  - Peak usage identification
- **Output**: Daily summary table

#### **activity_heatmap.py**
- **Purpose**: Visual activity patterns over time
- **Key Functions**:
  - Hour-of-day usage patterns
  - Day-of-week patterns
  - Monthly activity calendar
  - Peak usage time detection
- **Output**: ASCII heatmap visualization

#### **model_usage.py**
- **Purpose**: Model-specific usage statistics
- **Key Functions**:
  - Token usage per model
  - Cost per model
  - Model preference trends
  - Efficiency metrics (tokens per message)
- **Output**: Model comparison table

#### **summary_report.py**
- **Purpose**: High-level executive summary
- **Key Functions**:
  - Total usage statistics
  - Average daily/weekly costs
  - Most active periods
  - Key insights and recommendations
- **Output**: Executive summary report

#### **verify_costs.py**
- **Purpose**: Validates cost calculations
- **Key Functions**:
  - Recalculates costs from raw data
  - Compares with stored values
  - Identifies discrepancies
  - Audit trail generation

### 5. Testing/Debug Tools

#### **test_statusline.py**
- **Purpose**: Tests statusline output and model detection
- **Usage**: `python test_statusline.py`
- **Tests**: Database reading, model formatting, session detection

#### **test_current_detect.py**
- **Purpose**: Tests current session detection logic
- **Usage**: `python test_current_detect.py`
- **Tests**: Active session identification, time calculations

#### **check_costs.py**
- **Purpose**: Quick cost verification from database
- **Usage**: `python check_costs.py`
- **Output**: Total costs from all sessions

#### **check_current.py**
- **Purpose**: Debug current session detection
- **Usage**: `python check_current.py`
- **Output**: Current session details if active

### 6. Configuration Files

#### **prices.json**
```json
{
  "models": {
    "claude-opus-4-1-20250805": {
      "input": 15.0,          // $ per 1M tokens
      "output": 75.0,         // $ per 1M tokens
      "cache_write_5m": 18.75,// $ per 1M tokens
      "cache_read": 1.5,      // $ per 1M tokens
      "name": "Opus 4.1"      // Display name
    }
  }
}
```

#### **config.json**
```json
{
  "session_duration_hours": 5,
  "daemon_update_interval": 60,
  "max_jsonl_size_mb": 100,
  "timezone": "UTC"
}
```

## Data Flow

```
1. Claude Code writes JSONL → ~/.claude/projects/*/
                                      ↓
2. unified_daemon.py (every 60s) → Calls rebuild_database.py
                                      ↓
3. rebuild_database.py → Processes JSONL files
                         → Extracts tokens/costs
                         → Groups into sessions
                         → Updates smart_sessions_db.json
                                      ↓
4. statusline.py → Reads smart_sessions_db.json
                 → Formats with simple_visual_formatter.py
                 → Outputs status line
                                      ↓
5. Analytics tools → Read smart_sessions_db.json
                   → Generate reports
```

## File Structure

```
~/.claude/
├── projects/           # Claude Code JSONL files
│   └── project-xxx/
│       └── *.jsonl
└── data-statusline/    # Statusline data
    ├── smart_sessions_db.json    # Main database
    ├── file_tracking.json        # JSONL processing state
    ├── daemon_status.json        # Daemon health
    ├── live_session.json         # Current session
    └── .unified_daemon.lock      # PID lock
```

## Database Schema

### smart_sessions_db.json
```json
{
  "work_sessions": {
    "2024-11-14": [
      {
        "session_start": "2024-11-14T09:00:00Z",
        "session_end": "2024-11-14T14:00:00Z",
        "messages": [],
        "message_count": 234,
        "total_cost": 45.67,
        "input_tokens": 1234567,
        "output_tokens": 234567,
        "cache_creation_tokens": 12345,
        "cache_read_tokens": 2345,
        "primary_model": "claude-opus-4-1-20250805"
      }
    ]
  },
  "current_session": {
    "session_number": 1,
    "model": "claude-opus-4-1-20250805",
    "message_count": 45,
    "total_cost": 12.34,
    "input_tokens": 234567,
    "output_tokens": 45678
  },
  "file_positions": {},
  "last_update": "2024-11-14T13:45:00Z"
}
```

## Key Design Decisions

1. **5-Hour Sessions**: Chosen to represent typical work blocks
2. **UTC Timezone**: Ensures consistency across timezones
3. **Daemon Architecture**: Allows real-time updates without blocking
4. **File Tracking**: Remembers position to avoid reprocessing
5. **PID Locking**: Prevents data corruption from multiple instances
6. **Atomic Writes**: Uses temp files to prevent partial writes
7. **Graceful Degradation**: Returns defaults if data unavailable

## Performance Considerations

- JSONL files are processed incrementally (not fully loaded)
- Database updates every 60 seconds (configurable)
- File tracking prevents reprocessing of old data
- Token extraction optimized for nested structure
- Session grouping uses efficient datetime comparisons

## Error Handling

- Missing files return empty/default values
- Malformed JSON is skipped with logging
- Stale locks are detected and cleaned
- Daemon crashes are recoverable
- Cost calculation errors fall back to 0

## Future Improvements

1. **Live Session Tracking**: Currently disabled, needs WebSocket integration
2. **Multi-Model Support**: Expand beyond Opus 4.1
3. **Export Functionality**: CSV/JSON export for external analysis
4. **Web Dashboard**: HTML-based real-time dashboard
5. **Alerting**: Cost/usage threshold notifications
6. **Backup/Restore**: Database backup functionality
7. **Performance Metrics**: Track processing time and efficiency