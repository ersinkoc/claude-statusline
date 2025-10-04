#!/usr/bin/env python3
"""
Model utilities for Claude Statusline
Centralized model name resolution and display formatting
"""

import json
from pathlib import Path


def get_model_display_name(model: str, prices_data: dict = None) -> str:
    """
    Get display name for model using prices.json data

    Args:
        model: Model identifier string
        prices_data: Optional prices data dictionary. If None, tries to load from prices.json

    Returns:
        Formatted display name with appropriate emoji
    """
    # Load prices data if not provided
    if prices_data is None:
        prices_file = Path(__file__).parent / "prices.json"
        try:
            with open(prices_file, 'r', encoding='utf-8') as f:
                prices_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            prices_data = {}

    # First try to find exact match in prices.json
    model_info = prices_data.get('models', {}).get(model)
    if model_info and 'name' in model_info and 'tier' in model_info:
        tier = model_info['tier']
        name = model_info['name']

        # Add appropriate emoji based on tier and model type
        if 'glm' in model.lower():
            return f'🔮 {name}'
        elif tier == 'flagship':
            return f'🧠 {name}'
        elif tier == 'balanced':
            return f'🎭 {name}'
        elif tier == 'fast':
            return f'⚡ {name}'
        else:
            return name

    # Fallback to pattern matching for backward compatibility
    model_lower = model.lower()

    # Check for specific patterns first (more specific first)
    if 'opus-4-1' in model_lower:
        return '🧠 Opus 4.1'
    elif 'opus-4' in model_lower:
        return '🧠 Opus 4'
    elif 'sonnet-4-5' in model_lower:
        return '🎭 Sonnet 4.5'
    elif 'sonnet-4' in model_lower:
        return '🎭 Sonnet 4'
    elif 'sonnet-3-7' in model_lower:
        return '🎭 Sonnet 3.7'
    elif 'sonnet-3-5' in model_lower:
        return '🎭 Sonnet 3.5'
    elif 'haiku-4' in model_lower:
        return '⚡ Haiku 4'
    elif 'haiku-3-5' in model_lower:
        return '⚡ Haiku 3.5'

    # General patterns (less specific)
    elif 'opus' in model_lower:
        return '🧠 Opus 3'
    elif 'sonnet' in model_lower:
        return '🎭 Sonnet'
    elif 'haiku' in model_lower:
        return '⚡ Haiku'
    elif 'glm' in model_lower:
        return '🔮 GLM'
    else:
        return model[:20]


def get_model_tier(model: str, prices_data: dict = None) -> str:
    """
    Get model tier (flagship, balanced, fast) from prices.json

    Args:
        model: Model identifier string
        prices_data: Optional prices data dictionary

    Returns:
        Model tier string or 'unknown' if not found
    """
    # Load prices data if not provided
    if prices_data is None:
        prices_file = Path(__file__).parent / "prices.json"
        try:
            with open(prices_file, 'r', encoding='utf-8') as f:
                prices_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            prices_data = {}

    model_info = prices_data.get('models', {}).get(model)
    if model_info and 'tier' in model_info:
        return model_info['tier']

    # Fallback to pattern matching
    model_lower = model.lower()
    if 'opus' in model_lower:
        return 'flagship'
    elif 'sonnet' in model_lower:
        return 'balanced'
    elif 'haiku' in model_lower:
        return 'fast'
    else:
        return 'unknown'


def is_claude_model(model: str) -> bool:
    """
    Check if model is a Claude model (not GLM or other)

    Args:
        model: Model identifier string

    Returns:
        True if model is a Claude model
    """
    model_lower = model.lower()
    return 'claude-' in model_lower or any(
        claude_type in model_lower
        for claude_type in ['opus', 'sonnet', 'haiku']
    )