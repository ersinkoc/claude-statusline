#!/usr/bin/env python3
"""
Model Session Statistics

Extracts and displays session-by-session statistics for each model from the smart_sessions_db.json file.
Shows detailed breakdown of messages, tokens, and costs per model per session.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict

from .data_directory_utils import get_default_data_directory
from .console_utils import console, print_info, print_success, print_warning, print_error


def load_model_prices(data_dir: Path = None) -> Dict[str, Any]:
    """
    Load model pricing data from prices.json.

    Args:
        data_dir: Optional data directory override

    Returns:
        Dictionary containing pricing data
    """
    if data_dir is None:
        data_dir = get_default_data_directory()

    prices_file = data_dir / "prices.json"

    if not prices_file.exists():
        print_warning(f"Prices file not found: {prices_file}")
        return {}

    try:
        with open(prices_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print_error(f"Error loading prices: {e}")
        return {}


def get_model_prices(prices_data: Dict[str, Any], model: str) -> Dict[str, float]:
    """
    Get pricing for a specific model.

    Args:
        prices_data: Pricing data dictionary
        model: Model name

    Returns:
        Dictionary with pricing information
    """
    models = prices_data.get('models', {})

    # Try exact match first
    if model in models:
        return models[model]

    # Try partial match
    for model_key, prices in models.items():
        if model_key in model or model in model_key:
            return prices

    # Return fallback pricing
    return prices_data.get('fallback_pricing', {
        'input': 15.0,
        'output': 75.0,
        'cache_write_5m': 18.75,
        'cache_read': 1.5
    })


def calculate_cost(model: str, tokens: Dict[str, int], prices_data: Dict[str, Any]) -> float:
    """
    Calculate cost for given model and token usage.

    Args:
        model: Model name
        tokens: Token usage dictionary
        prices_data: Pricing data

    Returns:
        Total cost in USD
    """
    # Skip cost calculation for non-Claude models with zero pricing
    if model.startswith('glm-'):
        return 0.0

    model_prices = get_model_prices(prices_data, model)

    input_tokens = tokens.get('input_tokens', 0)
    output_tokens = tokens.get('output_tokens', 0)
    cache_creation = tokens.get('cache_creation_input_tokens', 0)
    cache_read = tokens.get('cache_read_input_tokens', 0)

    input_cost = (input_tokens / 1_000_000) * model_prices.get('input', 15.0)
    output_cost = (output_tokens / 1_000_000) * model_prices.get('output', 75.0)
    cache_cost = (cache_creation / 1_000_000) * model_prices.get('cache_write_5m', 18.75)
    cache_read_cost = (cache_read / 1_000_000) * model_prices.get('cache_read', 1.5)

    total_cost = input_cost + output_cost + cache_cost + cache_read_cost

    return total_cost


def load_sessions_data(data_dir: Path = None) -> Dict[str, Any]:
    """
    Load sessions data from smart_sessions_db.json.

    Args:
        data_dir: Optional data directory override

    Returns:
        Dictionary containing sessions data
    """
    if data_dir is None:
        data_dir = get_default_data_directory()

    db_file = data_dir / "smart_sessions_db.json"

    if not db_file.exists():
        print_error(f"Database file not found: {db_file}")
        return {}

    try:
        with open(db_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print_error(f"Error loading database: {e}")
        return {}


def extract_model_session_stats(sessions_data: Dict[str, Any], data_dir: Path = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract model-specific session statistics from work sessions.

    Args:
        sessions_data: Database content
        data_dir: Optional data directory override

    Returns:
        Dictionary mapping model names to list of session statistics
    """
    work_sessions = sessions_data.get('work_sessions', {})
    model_sessions = defaultdict(list)

    # Load pricing data for accurate cost calculation
    prices_data = load_model_prices(data_dir)

    for date_str, sessions in work_sessions.items():
        for session_idx, session in enumerate(sessions):
            session_start = datetime.fromisoformat(session['session_start'].replace('Z', '+00:00'))
            session_end = datetime.fromisoformat(session['session_end'].replace('Z', '+00:00'))

            # For each model in this session, extract statistics
            # Note: Current structure only has aggregate session data, not per-model breakdown
            # We'll distribute tokens proportionally among models based on hourly statistics

            # Get hourly data for this session period to find model usage
            date_data = sessions_data.get('hourly_statistics', {}).get(date_str.split('T')[0], {})

            # Calculate model statistics for this session
            session_duration = (session_end - session_start).total_seconds() / 3600  # hours
            start_hour = session_start.hour
            end_hour = session_end.hour

            # Collect hourly data for this session period
            hourly_models = defaultdict(lambda: {
                'messages': 0,
                'input_tokens': 0,
                'output_tokens': 0,
                'cache_creation_input_tokens': 0,
                'cache_read_input_tokens': 0,
                'total_tokens': 0,
                'cost': 0.0,
                'hours': []
            })

            # Extract hourly statistics for the session period
            for hour in range(start_hour, min(end_hour + 1, 24)):
                hour_key = f"{hour:02d}:00"
                if hour_key in date_data:
                    hour_data = date_data[hour_key]
                    for model_name, model_stats in hour_data.get('models', {}).items():
                        hourly_models[model_name]['messages'] += model_stats['messages']
                        hourly_models[model_name]['input_tokens'] += model_stats['input_tokens']
                        hourly_models[model_name]['output_tokens'] += model_stats['output_tokens']
                        hourly_models[model_name]['cache_creation_input_tokens'] += model_stats['cache_creation_input_tokens']
                        hourly_models[model_name]['cache_read_input_tokens'] += model_stats['cache_read_input_tokens']
                        hourly_models[model_name]['total_tokens'] += model_stats['total_tokens']
                        hourly_models[model_name]['cost'] += model_stats['cost']
                        hourly_models[model_name]['hours'].append(hour)

            # Create session entry for each model used
            for model_name, model_stats in hourly_models.items():
                # Only include Claude models (skip GLM and other non-Claude models)
                if not model_name.startswith('claude-'):
                    continue

                session_entry = {
                    'date': date_str,
                    'session_index': session_idx + 1,
                    'session_start': session['session_start'],
                    'session_end': session['session_end'],
                    'duration_hours': session_duration,
                    'messages': model_stats['messages'],
                    'input_tokens': model_stats['input_tokens'],
                    'output_tokens': model_stats['output_tokens'],
                    'cache_creation_input_tokens': model_stats['cache_creation_input_tokens'],
                    'cache_read_input_tokens': model_stats['cache_read_input_tokens'],
                    'total_tokens': model_stats['total_tokens'],
                    'cost': model_stats['cost'],  # Use database cost (already correctly calculated)
                    'active_hours': model_stats['hours']
                }
                model_sessions[model_name].append(session_entry)

    return dict(model_sessions)


def display_model_session_stats(model_sessions: Dict[str, List[Dict[str, Any]]],
                              model_filter: str = None, limit: int = None):
    """
    Display model session statistics in a formatted table.

    Args:
        model_sessions: Model-specific session data
        model_filter: Optional model name filter
        limit: Optional limit for number of sessions to show
    """
    if not model_sessions:
        print_warning("No session data found.")
        return

    models_to_show = [model_filter] if model_filter and model_filter in model_sessions else list(model_sessions.keys())

    for model_name in models_to_show:
        if model_name not in model_sessions:
            print_warning(f"Model '{model_name}' not found in session data.")
            continue

        sessions = model_sessions[model_name]
        if limit:
            sessions = sessions[-limit:]  # Show most recent sessions

        print_success(f"\n📊 {model_name} - Session Statistics ({len(sessions)} sessions)")
        print("=" * 120)

        # Table header
        header = f"{'Date':<12} {'Session':<8} {'Duration':<10} {'Messages':<8} {'Input':<10} {'Output':<10} {'Cache R':<10} {'Total':<12} {'Cost':<10}"
        print(header)
        print("-" * 120)

        # Session rows
        total_messages = 0
        total_input = 0
        total_output = 0
        total_cache_read = 0
        total_tokens = 0
        total_cost = 0.0

        for session in sessions:
            date_short = session['date'].split('T')[0]
            duration_str = f"{session['duration_hours']:.1f}h"

            row = (f"{date_short:<12} "
                   f"{session['session_index']:<8} "
                   f"{duration_str:<10} "
                   f"{session['messages']:<8} "
                   f"{session['input_tokens']:<10,} "
                   f"{session['output_tokens']:<10,} "
                   f"{session['cache_read_input_tokens']:<10,} "
                   f"{session['total_tokens']:<12,} "
                   f"${session['cost']:<9.2f}")
            print(row)

            total_messages += session['messages']
            total_input += session['input_tokens']
            total_output += session['output_tokens']
            total_cache_read += session['cache_read_input_tokens']
            total_tokens += session['total_tokens']
            total_cost += session['cost']

        # Summary row
        print("-" * 120)
        summary = (f"{'TOTAL':<12} "
                  f"{len(sessions):<8} "
                  f"{'':<10} "
                  f"{total_messages:<8} "
                  f"{total_input:<10,} "
                  f"{total_output:<10,} "
                  f"{total_cache_read:<10,} "
                  f"{total_tokens:<12,} "
                  f"${total_cost:<9.2f}")
        print(summary)

        # Additional statistics
        avg_duration = sum(s['duration_hours'] for s in sessions) / len(sessions)
        avg_tokens = total_tokens // len(sessions)
        avg_cost = total_cost / len(sessions)

        print(f"\n📈 Additional Statistics:")
        print(f"  Average session duration: {avg_duration:.1f} hours")
        print(f"  Average tokens per session: {avg_tokens:,}")
        print(f"  Average cost per session: ${avg_cost:.2f}")
        print(f"  Most active hours: {get_most_active_hours(sessions)}")


def get_most_active_hours(sessions: List[Dict[str, Any]]) -> str:
    """
    Find the most active hours from session data.

    Args:
        sessions: List of session dictionaries

    Returns:
        String with most active hours
    """
    hour_counts = defaultdict(int)

    for session in sessions:
        for hour in session.get('active_hours', []):
            hour_counts[hour] += 1

    if not hour_counts:
        return "N/A"

    sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
    top_hours = [f"{h:02d}:00" for h, _ in sorted_hours[:3]]

    return ", ".join(top_hours)


def list_available_models(sessions_data: Dict[str, Any]) -> List[str]:
    """
    List all available Claude models from the sessions data.

    Args:
        sessions_data: Database content

    Returns:
        List of Claude model names
    """
    models = set()
    hourly_stats = sessions_data.get('hourly_statistics', {})

    for date_data in hourly_stats.values():
        for hour_data in date_data.values():
            # Only include Claude models
            for model_name in hour_data.get('models', {}).keys():
                if model_name.startswith('claude-'):
                    models.add(model_name)

    return sorted(list(models))


def main():
    """Main entry point for model session statistics."""
    import argparse

    parser = argparse.ArgumentParser(description="Show model-specific session statistics")
    parser.add_argument("--model", "-m", help="Filter by specific model name")
    parser.add_argument("--limit", "-l", type=int, help="Limit number of sessions to show")
    parser.add_argument("--list-models", action="store_true", help="List all available models")
    parser.add_argument("--data-dir", help="Override data directory path")

    args = parser.parse_args()

    # Load sessions data
    data_dir = Path(args.data_dir) if args.data_dir else None
    sessions_data = load_sessions_data(data_dir)
    if not sessions_data:
        return

    # List models if requested
    if args.list_models:
        models = list_available_models(sessions_data)
        print_info("Available Claude models:")
        for model in models:
            print(f"  • {model}")
        return

    # Extract and display model session statistics
    model_sessions = extract_model_session_stats(sessions_data, data_dir)
    display_model_session_stats(model_sessions, args.model, args.limit)


if __name__ == "__main__":
    main()