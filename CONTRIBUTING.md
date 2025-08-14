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

1. Clone your fork:
   ```bash
   git clone https://github.com/ersinkoc/claude-statusline.git
   cd claude-statusline
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example Code Style

```python
def format_statusline(session_data: Dict[str, Any]) -> str:
    """
    Format session data into a compact statusline string.
    
    Args:
        session_data: Dictionary containing session information
        
    Returns:
        Formatted statusline string
    """
    # Implementation here
    pass
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Use descriptive test names

Example test:
```python
def test_format_statusline_with_active_session():
    """Test statusline formatting for an active session."""
    session_data = {
        'model': 'Opus 4.1',
        'active': True,
        'message_count': 100
    }
    result = format_statusline(session_data)
    assert 'LIVE' in result
    assert 'Opus 4.1' in result
```

### Documentation

- Update README.md if you change functionality
- Add docstrings to new functions/classes
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/)
- Comment complex logic

## Project Structure

```
claude-statusline/
├── statusline.py           # Main entry point
├── config.json            # Configuration file
├── prices.json            # Model pricing data
├── requirements.txt       # Dependencies
├── tests/                 # Test files
│   ├── test_statusline.py
│   └── test_formatter.py
├── docs/                  # Documentation
└── utils/                 # Utility modules
```

## Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Formatting, missing semi colons, etc
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding missing tests
- **chore**: Changes to the build process or auxiliary tools

## Review Process

1. A maintainer will review your PR
2. They may request changes or ask questions
3. Once approved, your PR will be merged
4. Your contribution will be noted in the changelog

## Community

- Join discussions in [GitHub Discussions](https://github.com/ersinkoc/claude-statusline/discussions)
- Ask questions in issues with the "question" label
- Help others by answering questions
- Share your use cases and configurations

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- The contributors page

Thank you for contributing to Claude Statusline! 🎉