# Contributing to Claude Statusline

First off, thank you for considering contributing to Claude Statusline! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and expected**
- **Include screenshots if possible**
- **Include your configuration** (config.json)
- **Note your operating system and Python version**
- **Package version** (`pip show claude-statusline`)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Provide specific examples to demonstrate the enhancement**
- **Describe the current behavior and expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repo and create your branch from `main`:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. Make your changes and ensure:
   - The code follows the existing style
   - You've added tests if applicable
   - Documentation is updated
   - Your changes don't break existing functionality

3. Commit your changes using clear commit messages:
   ```bash
   git commit -m "Add amazing feature that does X"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```

5. Open a Pull Request

## Development Setup

### Package Development

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/claude-statusline.git
   cd claude-statusline
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   pip install -e ".[dev]"  # Development dependencies
   ```

4. Run tests:
   ```bash
   pytest
   pytest --cov=claude_statusline  # With coverage
   ```

### Project Structure

```
claude-statusline/
├── claude_statusline/      # Main package
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # CLI interface
│   ├── statusline.py      # Core statusline
│   ├── daemon.py          # Background daemon
│   ├── templates.py       # Template system
│   └── ...                # Other modules
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_statusline.py
│   └── ...
├── docs/                  # Documentation
├── setup.py              # Package setup
├── pyproject.toml        # Modern packaging
└── README.md
```

### Code Style Guidelines

- **Python**: Follow PEP 8
- **Line length**: 100 characters maximum
- **Imports**: Use relative imports within package
- **Docstrings**: Use Google style docstrings
- **Type hints**: Use when beneficial for clarity

Example:
```python
from typing import Dict, Any, Optional

def format_statusline(self, data: Dict[str, Any]) -> str:
    """Format session data into statusline string.
    
    Args:
        data: Session data dictionary
        
    Returns:
        Formatted statusline string
    """
    # Implementation
```

### Testing

#### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_statusline.py

# Run with coverage
pytest --cov=claude_statusline

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_statusline.py::test_format_compact
```

#### Writing Tests

Place tests in the `tests/` directory. Test files should be named `test_*.py`:

```python
# tests/test_templates.py
import pytest
from claude_statusline.templates import StatuslineTemplates

def test_compact_format():
    templates = StatuslineTemplates()
    data = {
        'primary_model': 'Opus 4.1',
        'message_count': 100,
        'tokens': 1000000,
        'cost': 10.50
    }
    result = templates.compact_format(data)
    assert 'Opus 4.1' in result
    assert '100' in result
```

### Building and Publishing

#### Building the Package

```bash
# Install build tools
pip install build twine

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build

# Check the package
twine check dist/*
```

#### Testing Package Installation

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from wheel
pip install dist/claude_statusline-*.whl

# Test commands
claude-status
claude-statusline --help
```

#### Publishing to PyPI

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ claude-statusline

# If everything works, upload to PyPI
twine upload dist/*
```

### Adding New Features

#### Adding a New Template

1. Add template method to `templates.py`:
```python
def my_new_format(self, data: Dict[str, Any]) -> str:
    """My new format description"""
    # Implementation
    return formatted_string
```

2. Register in template dictionary:
```python
self.templates = {
    # ...
    'my_new': self.my_new_format,
}
```

3. Update documentation in `TEMPLATES.md`

4. Add tests in `tests/test_templates.py`

#### Adding a New CLI Command

1. Add module in `claude_statusline/`:
```python
# claude_statusline/my_command.py
def main():
    """Main entry point"""
    # Implementation
```

2. Update `cli.py`:
```python
from . import my_command

TOOLS = {
    'category': {
        'commands': {
            'my-command': {
                'module': my_command,
                'help': 'Description'
            }
        }
    }
}
```

3. Update documentation in `CLI.md`

### Documentation

- Update `README.md` for user-facing changes
- Update `CLI.md` for new commands or options
- Update `CHANGELOG.md` following [Keep a Changelog](https://keepachangelog.com/)
- Add docstrings to all functions and classes
- Include examples in documentation

### Debugging Tips

```bash
# Enable debug mode
export CLAUDE_DEBUG=1

# Check package structure
pip show -f claude-statusline

# Run in verbose mode
claude-statusline status --verbose

# Check import issues
python -c "import claude_statusline; print(claude_statusline.__version__)"

# Test specific module
python -m claude_statusline.statusline
```

## Release Process

1. Update version in:
   - `setup.py`
   - `pyproject.toml`
   - `claude_statusline/__init__.py`
   - `README.md`

2. Update `CHANGELOG.md`

3. Create git tag:
   ```bash
   git tag -a v1.3.0 -m "Version 1.3.0"
   git push origin v1.3.0
   ```

4. Build and publish to PyPI

5. Create GitHub release

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Claude Statusline! 🎉