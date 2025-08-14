#!/usr/bin/env python3
"""
Cost Analyzer for Claude Statusline
Detailed cost analysis and projections
"""

import json
import sys
import io

from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import statistics

from .data_directory_utils import resolve_data_directory
from .safe_file_operations import safe_json_read


class CostAnalyzer:
    """Analyze costs and provide financial insights"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.prices_file = Path(__file__).parent / "prices.json"
        
        self.db = safe_json_read(self.db_file) if self.db_file.exists() else {}
        self.prices = safe_json_read(self.prices_file) if self.prices_file.exists() else {}
    
    def analyze_costs(self):
        """Comprehensive cost analysis"""
        print("\n" + "="*80)
        print("💰 COMPREHENSIVE COST ANALYSIS")
        print("="*80 + "\n")
        
        # Collect all cost data
        daily_costs = defaultdict(float)
        hourly_costs = defaultdict(float)
        model_costs = defaultdict(float)
        token_breakdown = defaultdict(lambda: {
            'input': 0, 'output': 0, 'cache': 0, 'cache_read': 0
        })
        
        hourly_stats = self.db.get('hourly_statistics', {})
        
        for date_str, hours in hourly_stats.items():
            for hour, hour_data in hours.items():
                cost = hour_data.get('cost', 0.0)
                
                if cost > 0:
                    daily_costs[date_str] += cost
                    hour_num = int(hour.split(':')[0])
                    hourly_costs[hour_num] += cost
                    
                    # Model breakdown
                    for model, stats in hour_data.get('models', {}).items():
                        model_costs[model] += stats.get('cost', 0.0)
                        token_breakdown[model]['input'] += stats.get('input_tokens', 0)
                        token_breakdown[model]['output'] += stats.get('output_tokens', 0)
                        token_breakdown[model]['cache'] += stats.get('cache_creation_input_tokens', 0)
                        token_breakdown[model]['cache_read'] += stats.get('cache_read_input_tokens', 0)
        
        if not daily_costs:
            print("❌ No cost data found!")
            return
        
        # Calculate statistics
        costs_list = list(daily_costs.values())
        total_cost = sum(costs_list)
        avg_daily_cost = statistics.mean(costs_list) if costs_list else 0
        median_daily_cost = statistics.median(costs_list) if costs_list else 0
        max_daily_cost = max(costs_list) if costs_list else 0
        min_daily_cost = min(costs_list) if costs_list else 0
        
        # Print summary statistics
        print("📊 COST SUMMARY")
        print("-" * 40)
        print(f"Total Spent         : ${total_cost:,.2f}")
        print(f"Days with Activity  : {len(daily_costs)}")
        print(f"Average Daily Cost  : ${avg_daily_cost:.2f}")
        print(f"Median Daily Cost   : ${median_daily_cost:.2f}")
        print(f"Highest Daily Cost  : ${max_daily_cost:.2f}")
        print(f"Lowest Daily Cost   : ${min_daily_cost:.2f}")
        
        if len(costs_list) > 1:
            std_dev = statistics.stdev(costs_list)
            print(f"Standard Deviation  : ${std_dev:.2f}")
        print()
        
        # Print projections
        self._print_cost_projections(avg_daily_cost)
        
        # Print token cost breakdown
        self._print_token_cost_breakdown(token_breakdown, model_costs)
        
        # Print most expensive days
        self._print_expensive_days(daily_costs)
        
        # Print hourly cost distribution
        self._print_hourly_distribution(hourly_costs)
    
    def _print_cost_projections(self, avg_daily_cost):
        """Print cost projections"""
        print("📈 COST PROJECTIONS (Based on Average)")
        print("-" * 40)
        print(f"Weekly Projection   : ${avg_daily_cost * 7:.2f}")
        print(f"Monthly Projection  : ${avg_daily_cost * 30:.2f}")
        print(f"Quarterly Projection: ${avg_daily_cost * 90:.2f}")
        print(f"Yearly Projection   : ${avg_daily_cost * 365:.2f}")
        print()
    
    def _print_token_cost_breakdown(self, token_breakdown, model_costs):
        """Print detailed token and cost breakdown"""
        print("🔍 TOKEN & COST BREAKDOWN BY MODEL")
        print("-" * 40)
        
        for model in sorted(model_costs.keys(), key=lambda x: model_costs[x], reverse=True):
            tokens = token_breakdown[model]
            cost = model_costs[model]
            
            if cost > 0:
                model_name = self._get_model_display_name(model)
                total_tokens = sum(tokens.values())
                
                print(f"\n{model_name}")
                print(f"  Total Cost      : ${cost:,.2f}")
                print(f"  Input Tokens    : {tokens['input']:,}")
                print(f"  Output Tokens   : {tokens['output']:,}")
                print(f"  Cache Tokens    : {tokens['cache']:,}")
                print(f"  Cache Read      : {tokens['cache_read']:,}")
                print(f"  Total Tokens    : {total_tokens:,}")
                
                # Calculate component costs
                model_prices = self._get_model_prices(model)
                if model_prices:
                    input_cost = (tokens['input'] / 1_000_000) * model_prices.get('input', 0)
                    output_cost = (tokens['output'] / 1_000_000) * model_prices.get('output', 0)
                    cache_cost = (tokens['cache'] / 1_000_000) * model_prices.get('cache_write_5m', 0)
                    cache_read_cost = (tokens['cache_read'] / 1_000_000) * model_prices.get('cache_read', 0)
                    
                    print(f"  Cost Breakdown:")
                    print(f"    Input    : ${input_cost:,.2f} ({input_cost/cost*100:.1f}%)")
                    print(f"    Output   : ${output_cost:,.2f} ({output_cost/cost*100:.1f}%)")
                    print(f"    Cache    : ${cache_cost:,.2f} ({cache_cost/cost*100:.1f}%)")
                    print(f"    Cache Read: ${cache_read_cost:,.2f} ({cache_read_cost/cost*100:.1f}%)")
    
    def _print_expensive_days(self, daily_costs):
        """Print most expensive days"""
        print("\n💸 TOP 5 MOST EXPENSIVE DAYS")
        print("-" * 40)
        print(f"{'Date':<12} {'Cost':>12} {'Day of Week':<12}")
        print("-" * 40)
        
        sorted_days = sorted(daily_costs.items(), key=lambda x: x[1], reverse=True)
        
        for date_str, cost in sorted_days[:5]:
            try:
                date = datetime.fromisoformat(date_str + "T00:00:00")
                weekday = date.strftime('%A')
            except:
                weekday = '?'
            
            print(f"{date_str:<12} ${cost:>11,.2f} {weekday:<12}")
    
    def _print_hourly_distribution(self, hourly_costs):
        """Print hourly cost distribution"""
        print("\n⏰ COST BY HOUR OF DAY (UTC)")
        print("-" * 40)
        
        max_cost = max(hourly_costs.values()) if hourly_costs else 0
        
        for hour in range(24):
            cost = hourly_costs.get(hour, 0)
            if cost > 0:
                bar_length = int((cost / max_cost) * 30) if max_cost > 0 else 0
                bar = '█' * bar_length
                print(f"{hour:02d}:00 ${cost:>8,.2f} {bar}")
    
    def analyze_cost_trends(self, days: int = 30):
        """Analyze cost trends over time"""
        print("\n" + "="*80)
        print(f"📈 COST TRENDS (Last {days} Days)")
        print("="*80 + "\n")
        
        end_date = datetime.now()
        costs_by_date = []
        
        for i in range(days):
            date = end_date - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            daily_cost = 0
            hourly_data = self.db.get('hourly_statistics', {}).get(date_str, {})
            
            for hour_data in hourly_data.values():
                daily_cost += hour_data.get('cost', 0.0)
            
            if daily_cost > 0:
                costs_by_date.append({
                    'date': date_str,
                    'cost': daily_cost,
                    'weekday': date.strftime('%a')
                })
        
        if not costs_by_date:
            print("❌ No trend data available!")
            return
        
        costs_by_date.reverse()
        
        # Calculate moving average
        window_size = min(7, len(costs_by_date))
        moving_avg = []
        
        for i in range(len(costs_by_date)):
            start = max(0, i - window_size + 1)
            window = costs_by_date[start:i+1]
            avg = sum(d['cost'] for d in window) / len(window)
            moving_avg.append(avg)
        
        # Print trend table
        print(f"{'Date':<12} {'Day':<5} {'Cost':>10} {'7-Day Avg':>10} {'Trend':>8}")
        print("-" * 55)
        
        for i, data in enumerate(costs_by_date):
            trend = ""
            if i > 0:
                diff = data['cost'] - costs_by_date[i-1]['cost']
                if diff > 0:
                    trend = f"+{diff:.2f}"
                else:
                    trend = f"{diff:.2f}"
            
            print(f"{data['date']:<12} {data['weekday']:<5} ${data['cost']:>9,.2f} ${moving_avg[i]:>9,.2f} {trend:>8}")
        
        # Calculate trend statistics
        if len(costs_by_date) > 1:
            first_half = costs_by_date[:len(costs_by_date)//2]
            second_half = costs_by_date[len(costs_by_date)//2:]
            
            first_half_avg = sum(d['cost'] for d in first_half) / len(first_half)
            second_half_avg = sum(d['cost'] for d in second_half) / len(second_half)
            
            trend_pct = ((second_half_avg - first_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0
            
            print("\n📊 TREND ANALYSIS")
            print("-" * 40)
            print(f"First Half Average  : ${first_half_avg:.2f}")
            print(f"Second Half Average : ${second_half_avg:.2f}")
            print(f"Trend               : {'+' if trend_pct > 0 else ''}{trend_pct:.1f}%")
            
            if trend_pct > 20:
                print("⚠️  Costs are increasing significantly!")
            elif trend_pct < -20:
                print("✅ Costs are decreasing nicely!")
            else:
                print("📊 Costs are relatively stable")
    
    def _get_model_prices(self, model: str) -> Dict:
        """Get pricing for a specific model"""
        models = self.prices.get('models', {})
        
        # Try exact match first
        if model in models:
            return models[model]
        
        # Try partial match
        for model_key, prices in models.items():
            if model_key in model or model in model_key:
                return prices
        
        # Return fallback pricing
        return self.prices.get('fallback_pricing', {})
    
    def _get_model_display_name(self, model: str) -> str:
        """Get display name for model"""
        if 'opus' in model.lower():
            return '🧠 Opus'
        elif 'sonnet' in model.lower():
            return '🎭 Sonnet'
        elif 'haiku' in model.lower():
            return '⚡ Haiku'
        else:
            return model[:20]


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze Claude usage costs')
    parser.add_argument('--trends', type=int, help='Show trends for last N days', default=0)
    
    args = parser.parse_args()
    
    analyzer = CostAnalyzer()
    
    analyzer.analyze_costs()
    
    if args.trends > 0:
        analyzer.analyze_cost_trends(args.trends)


if __name__ == "__main__":
    main()