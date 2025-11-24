#!/usr/bin/env python3
"""Test statusline functionality"""

import pytest
from claude_statusline.model_utils import get_model_display_name, get_model_tier, is_claude_model
from claude_statusline.unified_powerline_system import UnifiedPowerlineSystem


def test_model_display_names():
    """Test model display name resolution"""
    # Test Opus 4.5
    assert 'Opus 4.5' in get_model_display_name('claude-opus-4-5-20251101')

    # Test Sonnet 4.5
    assert 'Sonnet 4.5' in get_model_display_name('claude-sonnet-4-5-20250929')

    # Test Opus 4.1
    assert 'Opus 4.1' in get_model_display_name('claude-opus-4-1-20250805')

    # Test fallback patterns
    assert 'Sonnet' in get_model_display_name('claude-sonnet-unknown')
    assert 'Haiku' in get_model_display_name('claude-haiku-unknown')


def test_model_tiers():
    """Test model tier classification"""
    assert get_model_tier('claude-opus-4-5-20251101') == 'flagship'
    assert get_model_tier('claude-sonnet-4-5-20250929') == 'balanced'
    assert get_model_tier('claude-haiku-4-20250514') == 'fast'


def test_is_claude_model():
    """Test Claude model detection"""
    assert is_claude_model('claude-opus-4-5-20251101') == True
    assert is_claude_model('claude-sonnet-4-5-20250929') == True
    assert is_claude_model('glm-4.5') == False


def test_unified_powerline_system():
    """Test unified powerline system initialization"""
    system = UnifiedPowerlineSystem()

    # Check themes are loaded
    themes = system.list_themes()
    assert len(themes) > 0

    # Check current theme exists
    current = system.get_current_theme()
    assert current is not None


def test_powerline_theme_rendering():
    """Test powerline theme rendering"""
    system = UnifiedPowerlineSystem()

    # Test rendering with current theme
    current_theme = system.get_current_theme()
    result = system.render_theme(current_theme)
    assert isinstance(result, str)
    assert len(result) > 0
