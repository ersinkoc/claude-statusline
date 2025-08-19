# PyPI Publishing Instructions for Claude Statusline v1.4.0

## 🎉 New Features in v1.4.0
- Colored terminal output for better visibility
- Cross-platform color support via colorama
- Customizable color schemes in config.json
- Full backward compatibility (colors can be disabled)

## 📦 Package Files Ready
✅ `claude_statusline-1.4.0.tar.gz` - Source distribution
✅ `claude_statusline-1.4.0-py3-none-any.whl` - Wheel distribution
✅ All checks passed with twine

## 🚀 Publishing to PyPI

### 1. Test PyPI (Recommended First)
```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/claude_statusline-1.4.0*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ claude-statusline==1.4.0
```

### 2. Production PyPI
```bash
# Upload to PyPI
twine upload dist/claude_statusline-1.4.0*

# You'll be prompted for:
# Username: __token__
# Password: <your-pypi-api-token>
```

### 3. Using API Token (Recommended)
Create a `.pypirc` file in your home directory:
```ini
[pypi]
  username = __token__
  password = pypi-<your-api-token>
```

Then upload:
```bash
twine upload dist/claude_statusline-1.4.0*
```

## 🔑 PyPI API Token Setup
1. Go to https://pypi.org/manage/account/token/
2. Create a new API token
3. Set scope to "Entire account" or specific to "claude-statusline"
4. Save the token securely

## ✅ Post-Publication Checklist
- [ ] Verify package page at https://pypi.org/project/claude-statusline/
- [ ] Test installation: `pip install claude-statusline==1.4.0`
- [ ] Test colored output: `claude-status`
- [ ] Update GitHub release with v1.4.0 tag
- [ ] Announce on social media/forums

## 📝 Package Details
- **Name**: claude-statusline
- **Version**: 1.4.0
- **Author**: Ersin Koç
- **License**: MIT
- **Dependencies**: psutil>=5.9.0, colorama>=0.4.6
- **Python**: >=3.8

## 🧪 Testing After Publication
```bash
# Fresh install
pip install claude-statusline==1.4.0

# Test statusline
claude-status

# Test CLI
claude-statusline --help

# Test colored output
claude-statusline template  # Interactive template selector
```

## 🔄 Rollback Instructions (if needed)
```bash
# Yank the version (marks as broken, doesn't delete)
# This must be done from PyPI web interface
# https://pypi.org/manage/project/claude-statusline/releases/

# Users can still install previous version
pip install claude-statusline==1.3.5
```

## 📊 Expected Output After Publishing
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading claude_statusline-1.4.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 95.2/95.2 kB • 00:00 • 2.1 MB/s
Uploading claude_statusline-1.4.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 89.3/89.3 kB • 00:00 • 1.8 MB/s

View at:
https://pypi.org/project/claude-statusline/1.4.0/
```

## 🎨 New Color Features Demo
After installation, users can enjoy:
- 🟢 Green LIVE status indicators
- 🔵 Cyan model names
- 🟡 Yellow costs and time
- 🟣 Magenta token counts
- Customizable color schemes via config.json

Good luck with the publication! 🚀