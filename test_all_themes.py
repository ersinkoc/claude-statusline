#!/usr/bin/env python3
"""
Test all themes to ensure they work correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_statusline.colored_templates import ColoredTemplates
from claude_statusline.templates import StatuslineTemplates
import traceback

def test_all_themes():
    """Test all available themes"""
    
    # Sample data for testing
    test_data = {
        'primary_model': 'claude-opus-4-1-20250805',
        'model': 'claude-opus-4-1-20250805',
        'active': True,
        'session_number': 42,
        'session_end_time': '15:30',
        'message_count': 123,
        'tokens': 4567890,
        'total_tokens': 4567890,
        'cost': 12.34,
        'total_cost': 12.34,
        'remaining_seconds': 3600
    }
    
    print("="*80)
    print("TESTING ALL THEMES")
    print("="*80)
    
    # Test colored templates
    colored = ColoredTemplates()
    colored_themes = list(colored.templates.keys())
    
    print(f"\n📊 Testing {len(colored_themes)} Colored Themes:")
    print("-"*60)
    
    errors = []
    success = 0
    
    for i, theme_name in enumerate(colored_themes, 1):
        try:
            formatter = colored.templates[theme_name]
            result = formatter(test_data)
            print(f"✅ {i:3}. {theme_name:20} OK - Sample: {result[:60]}...")
            success += 1
        except Exception as e:
            error_msg = f"❌ {i:3}. {theme_name:20} FAILED - {str(e)}"
            print(error_msg)
            errors.append((theme_name, str(e)))
            # Print full traceback for debugging
            traceback.print_exc()
    
    # Test standard templates
    standard = StatuslineTemplates()
    standard_themes = standard.list_templates()
    
    print(f"\n📊 Testing {len(standard_themes)} Standard Themes:")
    print("-"*60)
    
    for i, theme_name in enumerate(standard_themes, 1):
        try:
            result = standard.format(theme_name, test_data)
            print(f"✅ {i:3}. {theme_name:20} OK - Sample: {result[:60]}...")
            success += 1
        except Exception as e:
            error_msg = f"❌ {i:3}. {theme_name:20} FAILED - {str(e)}"
            print(error_msg)
            errors.append((theme_name, str(e)))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    total_themes = len(colored_themes) + len(standard_themes)
    print(f"✅ Success: {success}/{total_themes}")
    print(f"❌ Failed:  {len(errors)}/{total_themes}")
    
    if errors:
        print("\n🔴 Failed Themes:")
        for theme, error in errors:
            print(f"   - {theme}: {error}")
    else:
        print("\n🎉 All themes passed!")
    
    return len(errors) == 0


if __name__ == "__main__":
    success = test_all_themes()
    sys.exit(0 if success else 1)