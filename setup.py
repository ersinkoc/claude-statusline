#!/usr/bin/env python3
"""
Setup configuration for claude-statusline package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().strip().split("\n")

setup(
    name="claude-statusline",
    version="1.3.0",
    author="Ersin Koç",
    author_email="ersinkoc@users.noreply.github.com",
    description="Real-time session tracking and analytics for Claude Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ersinkoc/claude-statusline",
    project_urls={
        "Bug Tracker": "https://github.com/ersinkoc/claude-statusline/issues",
        "Documentation": "https://github.com/ersinkoc/claude-statusline/blob/main/README.md",
        "Source Code": "https://github.com/ersinkoc/claude-statusline",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "claude_statusline": [
            "*.json",
            "*.md",
            "templates/*.json",
        ],
    },
    entry_points={
        "console_scripts": [
            "claude-statusline=claude_statusline.cli:main",
            "claude-status=claude_statusline.statusline:main",
            "claude-daemon=claude_statusline.daemon:main",
            "claude-rebuild=claude_statusline.rebuild:main",
            "claude-template=claude_statusline.template_selector:main",
        ],
    },
    keywords=[
        "claude",
        "claude-code",
        "statusline",
        "monitoring",
        "analytics",
        "ai",
        "anthropic",
        "session-tracking",
        "cost-tracking",
        "developer-tools",
    ],
    zip_safe=False,
)