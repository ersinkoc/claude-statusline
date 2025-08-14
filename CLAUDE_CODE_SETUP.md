# Claude Code Integration Setup

## Installation Options

### Option 1: Using the Wrapper Script (Recommended)
If you're using claude-statusline from the source directory:

```json
{
  "statusline": {
    "command": "python",
    "args": ["C:\\Sync\\Codebox\\claudecode\\ClaudeStatusline\\statusline.py"]
  }
}
```

### Option 2: After Package Installation
If you've installed the package via pip:

```bash
pip install dist/claude_statusline-1.3.0-py3-none-any.whl
```

Then in Claude Code settings.json:

```json
{
  "statusline": {
    "command": "claude-status"
  }
}
```

Or using Python module directly:

```json
{
  "statusline": {
    "command": "python",
    "args": ["-m", "claude_statusline.statusline"]
  }
}
```

### Option 3: Development Mode Installation
For development, install in editable mode:

```bash
pip install -e .
```

Then use any of the above configurations.

## Available Commands After Installation

Once the package is installed, these commands become available:

- `claude-statusline` - Main CLI interface
- `claude-status` - Direct statusline display (for Claude Code)
- `claude-daemon` - Daemon management
- `claude-rebuild` - Database rebuild
- `claude-template` - Template selector

## Configuration File

The configuration file is located at:
- Development: `claude_statusline/config.json`
- After installation: Check `~/.claude/data-statusline/config.json`

## Testing the Setup

1. Test the statusline display:
```bash
python statusline.py
```

2. Test the CLI:
```bash
python -m claude_statusline.cli --help
```

3. Test daemon start:
```bash
python -m claude_statusline.daemon --start
```

## Troubleshooting

If you encounter import errors:
1. Ensure you're in the correct directory
2. Check that all dependencies are installed: `pip install psutil`
3. For development, use the wrapper script (`statusline.py`) in the root directory