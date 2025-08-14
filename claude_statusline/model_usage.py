#!/usr/bin/env python3
"""
Model Usage Analyzer for Claude Statusline
Analyzes usage patterns across different Claude models
"""

import json
import sys
import io

from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

from .data_directory_utils import resolve_data_directory
from .safe_file_operations import safe_json_read


class ModelUsageAnalyzer:
    """Analyze Claude model usage patterns"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.prices_file = Path(__file__).parent / "prices.json"
        
        self.db = safe_json_read(self.db_file) if self.db_file.exists() else {}
        self.prices = safe_json_read(self.prices_file) if self.prices_file.exists() else {}
    
    def analyze_model_usage(self):
        """Comprehensive model usage analysis"""
        print("\n" + "="*80)
        print("🤖 MODEL USAGE ANALYSIS")
        print("="*80 + "\n")
        
        model_totals = defaultdict(lambda: {
            'messages': 0,
            'input_tokens': 0,
            'output_tokens': 0,
            'cache_tokens': 0,
            'total_tokens': 0,
            'cost': 0.0,
            'days_used': set(),
            'sessions': 0
        })
        
        # Analyze hourly statistics
        hourly_stats = self.db.get('hourly_statistics', {})
        
        for date_str, hours in hourly_stats.items():
            for hour, hour_data in hours.items():
                models = hour_data.get('models', {})
                
                if isinstance(models, dict):
                    for model, stats in models.items():
                        if stats.get('messages', 0) > 0:
                            model_totals[model]['messages'] += stats.get('messages', 0)
                            model_totals[model]['input_tokens'] += stats.get('input_tokens', 0)
                            model_totals[model]['output_tokens'] += stats.get('output_tokens', 0)
                            model_totals[model]['cache_tokens'] += stats.get('cache_creation_input_tokens', 0)
                            model_totals[model]['total_tokens'] += stats.get('total_tokens', 0)
                            model_totals[model]['cost'] += stats.get('cost', 0.0)
                            model_totals[model]['days_used'].add(date_str)
        
        # Count sessions per model
        work_sessions = self.db.get('work_sessions', {})
        for date_str, sessions in work_sessions.items():
            for session in sessions:
                if isinstance(session, dict):
                    model = session.get('primary_model', 'unknown')
                    model_totals[model]['sessions'] += 1
        
        if not model_totals:
            print("❌ No model usage data found!")
            return
        
        # Sort by cost
        sorted_models = sorted(model_totals.items(), key=lambda x: x[1]['cost'], reverse=True)
        
        # Print detailed statistics
        print("📊 DETAILED MODEL STATISTICS")
        print("-" * 80)
        
        for model, stats in sorted_models:
            model_name = self._get_model_display_name(model)
            days_active = len(stats['days_used'])
            
            print(f"\n{model_name}")
            print("  " + "-" * 60)
            print(f"  Total Messages     : {stats['messages']:,}")
            print(f"  Total Sessions     : {stats['sessions']}")
            print(f"  Days Active        : {days_active}")
            print(f"  Total Cost         : ${stats['cost']:,.2f}")
            print(f"  Input Tokens       : {stats['input_tokens']:,}")
            print(f"  Output Tokens      : {stats['output_tokens']:,}")
            print(f"  Cache Tokens       : {stats['cache_tokens']:,}")
            print(f"  Total Tokens       : {stats['total_tokens']:,}")
            
            if stats['messages'] > 0:
                avg_tokens = stats['total_tokens'] / stats['messages']
                avg_cost = stats['cost'] / stats['messages']
                print(f"  Avg Tokens/Message : {avg_tokens:,.0f}")
                print(f"  Avg Cost/Message   : ${avg_cost:.4f}")
            
            if days_active > 0:
                daily_cost = stats['cost'] / days_active
                print(f"  Avg Daily Cost     : ${daily_cost:.2f}")
        
        # Print comparison table
        self._print_model_comparison(sorted_models)
        
        # Calculate cost efficiency
        self._analyze_cost_efficiency(model_totals)
    
    def _print_model_comparison(self, sorted_models):
        """Print model comparison table"""
        print("\n" + "="*80)
        print("📈 MODEL COMPARISON")
        print("-" * 80)
        print(f"{'Model':<15} {'Messages':>10} {'Tokens':>15} {'Cost':>12} {'% of Total':>12}")
        print("-" * 80)
        
        total_cost = sum(stats['cost'] for _, stats in sorted_models)
        total_messages = sum(stats['messages'] for _, stats in sorted_models)
        total_tokens = sum(stats['total_tokens'] for _, stats in sorted_models)
        
        for model, stats in sorted_models:
            model_name = self._get_model_display_name(model)[:15]
            percentage = (stats['cost'] / total_cost * 100) if total_cost > 0 else 0
            
            print(f"{model_name:<15} {stats['messages']:>10,} {stats['total_tokens']:>15,} ${stats['cost']:>11,.2f} {percentage:>11.1f}%")
        
        print("-" * 80)
        print(f"{'TOTAL':<15} {total_messages:>10,} {total_tokens:>15,} ${total_cost:>11,.2f} {100:>11.1f}%")
    
    def _analyze_cost_efficiency(self, model_totals):
        """Analyze cost efficiency across models"""
        print("\n" + "="*80)
        print("💰 COST EFFICIENCY ANALYSIS")
        print("-" * 80)
        
        efficiencies = []
        
        for model, stats in model_totals.items():
            if stats['total_tokens'] > 0:
                cost_per_1k_tokens = (stats['cost'] / stats['total_tokens']) * 1000
                efficiencies.append({
                    'model': model,
                    'cost_per_1k': cost_per_1k_tokens,
                    'total_tokens': stats['total_tokens'],
                    'total_cost': stats['cost']
                })
        
        if efficiencies:
            efficiencies.sort(key=lambda x: x['cost_per_1k'])
            
            print(f"{'Model':<20} {'Cost/1K Tokens':>15} {'Total Tokens':>15} {'Total Cost':>12}")
            print("-" * 80)
            
            for eff in efficiencies:
                model_name = self._get_model_display_name(eff['model'])[:20]
                print(f"{model_name:<20} ${eff['cost_per_1k']:>14.4f} {eff['total_tokens']:>15,} ${eff['total_cost']:>11,.2f}")
            
            print("\n💡 INSIGHTS:")
            most_efficient = efficiencies[0]
            least_efficient = efficiencies[-1]
            
            print(f"  Most Efficient : {self._get_model_display_name(most_efficient['model'])} (${most_efficient['cost_per_1k']:.4f}/1K tokens)")
            print(f"  Least Efficient: {self._get_model_display_name(least_efficient['model'])} (${least_efficient['cost_per_1k']:.4f}/1K tokens)")
            
            ratio = least_efficient['cost_per_1k'] / most_efficient['cost_per_1k'] if most_efficient['cost_per_1k'] > 0 else 0
            print(f"  Cost Ratio     : {ratio:.1f}x difference")
    
    def analyze_model_trends(self, days: int = 30):
        """Analyze model usage trends over time"""
        print("\n" + "="*80)
        print(f"📈 MODEL USAGE TRENDS (Last {days} Days)")
        print("="*80 + "\n")
        
        end_date = datetime.now()
        daily_model_usage = defaultdict(lambda: defaultdict(lambda: {'messages': 0, 'cost': 0.0}))
        
        for i in range(days):
            date = end_date - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            hourly_data = self.db.get('hourly_statistics', {}).get(date_str, {})
            
            for hour, hour_data in hourly_data.items():
                models = hour_data.get('models', {})
                
                if isinstance(models, dict):
                    for model, stats in models.items():
                        if stats.get('messages', 0) > 0:
                            daily_model_usage[date_str][model]['messages'] += stats.get('messages', 0)
                            daily_model_usage[date_str][model]['cost'] += stats.get('cost', 0.0)
        
        if not daily_model_usage:
            print("❌ No trend data available!")
            return
        
        # Identify model preference changes
        model_preferences = []
        
        for date_str in sorted(daily_model_usage.keys()):
            day_data = daily_model_usage[date_str]
            if day_data:
                # Find primary model for the day
                primary_model = max(day_data.items(), key=lambda x: x[1]['cost'])
                model_preferences.append({
                    'date': date_str,
                    'model': primary_model[0],
                    'cost': primary_model[1]['cost'],
                    'messages': primary_model[1]['messages']
                })
        
        # Print trend summary
        if model_preferences:
            print("📅 DAILY PRIMARY MODEL USAGE")
            print("-" * 80)
            print(f"{'Date':<12} {'Primary Model':<20} {'Messages':>10} {'Cost':>12}")
            print("-" * 80)
            
            for pref in model_preferences[-10:]:  # Last 10 days
                model_name = self._get_model_display_name(pref['model'])[:20]
                print(f"{pref['date']:<12} {model_name:<20} {pref['messages']:>10,} ${pref['cost']:>11,.2f}")
            
            # Calculate model switching frequency
            switches = 0
            for i in range(1, len(model_preferences)):
                if model_preferences[i]['model'] != model_preferences[i-1]['model']:
                    switches += 1
            
            print(f"\n📊 Model switches in {days} days: {switches}")
            
            # Find most consistent model
            model_days = defaultdict(int)
            for pref in model_preferences:
                model_days[pref['model']] += 1
            
            if model_days:
                most_used = max(model_days.items(), key=lambda x: x[1])
                print(f"🏆 Most used model: {self._get_model_display_name(most_used[0])} ({most_used[1]} days)")
    
    def _get_model_display_name(self, model: str) -> str:
        """Get display name for model"""
        if 'opus-4-1' in model.lower():
            return '🧠 Opus 4.1'
        elif 'opus-4' in model.lower():
            return '🧠 Opus 4'
        elif 'opus' in model.lower():
            return '🧠 Opus 3'
        elif 'sonnet-4' in model.lower():
            return '🎭 Sonnet 4'
        elif 'sonnet-3-7' in model.lower():
            return '🎭 Sonnet 3.7'
        elif 'sonnet-3-5' in model.lower():
            return '🎭 Sonnet 3.5'
        elif 'sonnet' in model.lower():
            return '🎭 Sonnet'
        elif 'haiku-4' in model.lower():
            return '⚡ Haiku 4'
        elif 'haiku-3-5' in model.lower():
            return '⚡ Haiku 3.5'
        elif 'haiku' in model.lower():
            return '⚡ Haiku'
        else:
            return model[:20]


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze Claude model usage')
    parser.add_argument('--trends', type=int, help='Show trends for last N days', default=0)
    
    args = parser.parse_args()
    
    analyzer = ModelUsageAnalyzer()
    
    analyzer.analyze_model_usage()
    
    if args.trends > 0:
        analyzer.analyze_model_trends(args.trends)


if __name__ == "__main__":
    main()