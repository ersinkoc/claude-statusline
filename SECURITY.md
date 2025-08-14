# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | :white_check_mark: |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :x:                |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Claude Statusline seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT:
- Open a public GitHub issue for the vulnerability
- Post about the vulnerability on social media
- Exploit the vulnerability for malicious purposes

### Please DO:
- Email us at: security@claude-statusline.dev (or create a private security advisory on GitHub)
- Include the following information:
  - Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
  - Full paths of source file(s) related to the manifestation of the issue
  - The location of the affected source code (tag/branch/commit or direct URL)
  - Any special configuration required to reproduce the issue
  - Step-by-step instructions to reproduce the issue
  - Proof-of-concept or exploit code (if possible)
  - Impact of the issue, including how an attacker might exploit it

### What to expect:
- **Initial Response**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Assessment**: We will investigate and validate the reported vulnerability within 7 days
- **Resolution Timeline**: 
  - Critical vulnerabilities: Fixed within 7 days
  - High severity: Fixed within 14 days
  - Medium severity: Fixed within 30 days
  - Low severity: Fixed in the next regular release
- **Disclosure**: We will coordinate with you on the disclosure timeline

## Security Considerations

### Data Privacy
Claude Statusline processes session data locally and does not transmit any information to external servers. However, users should be aware that:

- Session data is stored locally in JSON files
- Cost and usage information is calculated based on local JSONL files
- No authentication tokens or API keys are stored or transmitted

### File System Access
The application requires read/write access to:
- Claude Code session files (JSONL format)
- Local database files for session tracking
- Configuration files

### Daemon Processes
The background daemon processes:
- Run with the same privileges as the user
- Do not accept network connections
- Communicate only through local file system

### Best Practices for Users

1. **File Permissions**: Ensure appropriate file permissions on the data directory
   ```bash
   chmod 700 ~/.claude/data-statusline  # Unix/Linux/macOS
   ```

2. **Regular Updates**: Keep the software updated to receive security patches
   ```bash
   git pull origin main
   pip install -r requirements.txt --upgrade
   ```

3. **Configuration Security**: 
   - Do not share your config.json file if it contains sensitive paths
   - Review configuration changes before applying them

4. **Data Cleanup**: Regularly clean old session data
   ```bash
   python cleanup.py --older-than 90
   ```

## Known Security Limitations

1. **No Encryption**: Session data is stored in plain text JSON files
2. **No Authentication**: The statusline does not implement user authentication
3. **Local Access**: Anyone with file system access can read session data
4. **No Network Security**: The tool is designed for local use only

## Security Features

### Input Validation
- All file paths are validated before access
- JSON parsing includes error handling
- Command injection prevention in subprocess calls

### Resource Limits
- Maximum file size limits for JSONL processing
- Memory usage caps for daemon processes
- Timeout limits for file operations

### Error Handling
- Sensitive information is not included in error messages
- Stack traces are sanitized in production mode
- Failed operations fail safely without exposing system details

## Compliance

This project aims to comply with:
- OWASP secure coding practices
- Python security best practices
- OS-specific security guidelines

## Security Updates

Security updates will be released as:
- Patch versions for non-breaking security fixes
- Minor versions for security improvements requiring changes
- Security advisories for critical issues

Subscribe to security updates:
- Watch the GitHub repository for releases
- Enable security alerts in your GitHub settings
- Follow our security advisory feed

## Contact

For security concerns, contact:
- Email: security@claude-statusline.dev
- GitHub Security Advisories: [Create private advisory](https://github.com/ersinkoc/claude-statusline/security/advisories/new)

## Attribution

We appreciate responsible disclosure and will acknowledge security researchers who:
- Follow responsible disclosure practices
- Give us reasonable time to address issues
- Do not exploit vulnerabilities maliciously

Security researchers will be credited in:
- Security advisories
- Release notes
- Hall of Fame (if desired)

---

Last updated: 2025-08-14
Next review: 2025-02-14