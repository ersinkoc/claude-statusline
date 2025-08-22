#!/usr/bin/env python3
"""Test statusline functionality"""

import pytest
from claude_statusline.formatter import SimpleVisualFormatter

def test_formatter_basic():
    """Test basic formatter functionality"""
    formatter = SimpleVisualFormatter('aesthetic')
    test_data = {
        'primary_model': 'claude-sonnet-4-20250514',
        'message_count': 42,
        'tokens': 12500,
        'cost': 15.3
    }
    
    result = formatter.format_statusline(test_data)
    assert 'Sonnet-4' in result
    assert '42' in result
    assert '12.5K' in result

def test_aesthetic_themes():
    """Test aesthetic themes work without errors"""
    from claude_statusline.aesthetic_themes import AestheticThemes
    aesthetic = AestheticThemes()
    
    test_data = {
        'primary_model': 'claude-sonnet-4-20250514',
        'message_count': 42,
        'tokens': 12500,
        'cost': 15.3
    }
    
    # Test a few themes
    themes_to_test = ['aesthetic', 'rainbow_line', 'powerline_pro']
    for theme_name in themes_to_test:
        result = aesthetic.get_theme(theme_name, test_data)
        assert isinstance(result, str)
        assert len(result) > 0

def test_token_formatting():
    """Test token formatting"""
    formatter = SimpleVisualFormatter()
    
    # Test various token counts
    assert '500 tok' in formatter._format_tokens(500)
    assert '1.2k' in formatter._format_tokens(1200) 
    assert '1.5M' in formatter._format_tokens(1500000)