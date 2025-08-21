#!/usr/bin/env python3
"""
Trend Analyzer for Claude Statusline
Analyzes usage trends, patterns, and predictions
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import statistics

from .data_directory_utils import resolve_data_directory
from .safe_file_operations import safe_json_read


class TrendAnalyzer:
    """Analyze usage trends and make predictions"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.db = safe_json_read(self.db_file) if self.db_file.exists() else {}
    
    def analyze_usage_trends(self, days: int = 30):
        """Analyze usage trends over specified days"""
        print("\n" + "="*80)
        print("📈 USAGE TREND ANALYSIS")
        print("="*80 + "\n")
        
        # Get daily statistics
        daily_stats = self._get_daily_stats(days)
        
        if not daily_stats:
            print("❌ No data available for trend analysis")
            return
        
        # Calculate trends
        dates = sorted(daily_stats.keys())
        messages = [daily_stats[date]['messages'] for date in dates]
        costs = [daily_stats[date]['cost'] for date in dates]
        tokens = [daily_stats[date]['tokens'] for date in dates]
        
        print("📊 TREND SUMMARY")
        print("-" * 60)
        
        # Message trends
        msg_trend = self._calculate_trend(messages)
        print(f"Messages Trend: {self._format_trend(msg_trend)}")
        
        # Cost trends  
        cost_trend = self._calculate_trend(costs)
        print(f"Cost Trend:     {self._format_trend(cost_trend)}")
        
        # Token trends
        token_trend = self._calculate_trend(tokens)
        print(f"Token Trend:    {self._format_trend(token_trend)}")
        
        # Show weekly comparisons
        self._show_weekly_comparison(daily_stats)
        
        # Predictions
        self._show_predictions(daily_stats)
        
        # Efficiency metrics
        self._analyze_efficiency_trends(daily_stats)
    
    def analyze_productivity_patterns(self):
        """Analyze productivity patterns and optimal work times"""
        print("\n" + "="*80)
        print("🏆 PRODUCTIVITY PATTERN ANALYSIS")
        print("="*80 + "\n")
        
        hourly_stats = self.db.get('hourly_statistics', {})
        
        # Analyze by hour of day
        hour_productivity = defaultdict(lambda: {'messages': 0, 'sessions': 0, 'cost': 0.0})
        
        for date_str, hours in hourly_stats.items():
            for hour_str, hour_data in hours.items():
                hour = int(hour_str.split(':')[0])
                messages = hour_data.get('messages', 0)
                cost = hour_data.get('cost', 0.0)
                
                hour_productivity[hour]['messages'] += messages
                hour_productivity[hour]['cost'] += cost
                hour_productivity[hour]['sessions'] += 1 if messages > 0 else 0
        
        # Find peak hours
        print("⏰ PEAK PRODUCTIVITY HOURS")
        print("-" * 40)
        
        sorted_hours = sorted(
            hour_productivity.items(),
            key=lambda x: x[1]['messages'],
            reverse=True
        )
        
        for hour, stats in sorted_hours[:5]:
            efficiency = stats['messages'] / stats['cost'] if stats['cost'] > 0 else 0
            print(f"{hour:02d}:00 - {stats['messages']:,} messages, ${stats['cost']:.2f}, {efficiency:.1f} msg/$")
        
        # Analyze by day of week
        self._analyze_weekly_productivity(hourly_stats)
        
        # Show recommendations
        self._show_productivity_recommendations(hour_productivity, sorted_hours)
    
    def analyze_model_efficiency(self):
        """Analyze efficiency of different models"""
        print("\n" + "="*80)
        print("🤖 MODEL EFFICIENCY ANALYSIS")
        print("="*80 + "\n")
        
        hourly_stats = self.db.get('hourly_statistics', {})
        model_stats = defaultdict(lambda: {'messages': 0, 'cost': 0.0, 'tokens': 0, 'sessions': 0})
        
        for date_str, hours in hourly_stats.items():
            for hour_data in hours.values():
                model = hour_data.get('primary_model', 'Unknown')
                messages = hour_data.get('messages', 0)
                cost = hour_data.get('cost', 0.0)
                tokens = hour_data.get('total_tokens', 0)
                
                model_stats[model]['messages'] += messages
                model_stats[model]['cost'] += cost
                model_stats[model]['tokens'] += tokens
                model_stats[model]['sessions'] += 1 if messages > 0 else 0
        
        print("💰 COST EFFICIENCY (Messages per Dollar)")
        print("-" * 60)
        
        efficiency_ranking = []
        for model, stats in model_stats.items():
            if stats['cost'] > 0:
                efficiency = stats['messages'] / stats['cost']
                cost_per_msg = stats['cost'] / stats['messages'] if stats['messages'] > 0 else 0
                token_per_dollar = stats['tokens'] / stats['cost'] if stats['cost'] > 0 else 0
                
                efficiency_ranking.append({
                    'model': model,
                    'efficiency': efficiency,
                    'cost_per_msg': cost_per_msg,
                    'token_per_dollar': token_per_dollar,
                    'stats': stats
                })
        
        # Sort by efficiency
        efficiency_ranking.sort(key=lambda x: x['efficiency'], reverse=True)
        
        for rank, data in enumerate(efficiency_ranking, 1):
            print(f"{rank}. {data['model']}")
            print(f"   Messages/$ : {data['efficiency']:.1f}")
            print(f"   Cost/msg   : ${data['cost_per_msg']:.3f}")
            print(f"   Tokens/$   : {data['token_per_dollar']:,.0f}")
            print(f"   Total cost : ${data['stats']['cost']:.2f}")
            print()
    
    def generate_insights_report(self):
        """Generate comprehensive insights and recommendations"""
        print("\n" + "="*80)
        print("💡 INSIGHTS & RECOMMENDATIONS")
        print("="*80 + "\n")
        
        daily_stats = self._get_daily_stats(30)
        
        if not daily_stats:
            print("❌ Insufficient data for insights")
            return
        
        insights = []
        
        # Usage pattern insights
        dates = sorted(daily_stats.keys())
        recent_avg = statistics.mean([daily_stats[d]['cost'] for d in dates[-7:]])
        overall_avg = statistics.mean([daily_stats[d]['cost'] for d in dates])
        
        if recent_avg > overall_avg * 1.2:
            insights.append("📈 Your usage has increased significantly in the last week")
        elif recent_avg < overall_avg * 0.8:
            insights.append("📉 Your usage has decreased in the last week")
        
        # Efficiency insights
        costs = [daily_stats[d]['cost'] for d in dates if daily_stats[d]['messages'] > 0]
        messages = [daily_stats[d]['messages'] for d in dates if daily_stats[d]['messages'] > 0]
        
        if costs and messages:
            efficiency_trend = self._calculate_correlation(costs, messages)
            if efficiency_trend > 0.7:
                insights.append("💰 Strong correlation between cost and message volume - consistent pricing")
            elif efficiency_trend < 0.3:
                insights.append("⚠️ Inconsistent cost patterns - review model selection")
        
        # Peak time insights
        hourly_stats = self.db.get('hourly_statistics', {})
        peak_hours = self._find_peak_hours(hourly_stats)
        if peak_hours:
            insights.append(f"🕐 Most productive hours: {', '.join(f'{h}:00' for h in peak_hours[:3])}")
        
        # Display insights
        if insights:
            print("🔍 KEY INSIGHTS")
            print("-" * 40)
            for insight in insights:
                print(f"  • {insight}")
            print()
        
        # Recommendations
        recommendations = self._generate_recommendations(daily_stats, hourly_stats)
        if recommendations:
            print("💡 RECOMMENDATIONS")
            print("-" * 40)
            for rec in recommendations:
                print(f"  • {rec}")
            print()
    
    def _get_daily_stats(self, days: int) -> Dict[str, Dict]:
        """Get daily statistics for the specified number of days"""
        daily_stats = {}
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        hourly_stats = self.db.get('hourly_statistics', {})
        
        for date_str, hours in hourly_stats.items():
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if start_date <= date <= end_date:
                    total_messages = sum(h.get('messages', 0) for h in hours.values())
                    total_cost = sum(h.get('cost', 0.0) for h in hours.values())
                    total_tokens = sum(h.get('total_tokens', 0) for h in hours.values())
                    
                    daily_stats[date_str] = {
                        'messages': total_messages,
                        'cost': total_cost,
                        'tokens': total_tokens,
                        'sessions': len([h for h in hours.values() if h.get('messages', 0) > 0])
                    }
            except ValueError:
                continue
        
        return daily_stats
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend direction (-1 to 1)"""
        if len(values) < 2:
            return 0.0
        
        # Simple linear regression slope
        n = len(values)
        x = list(range(n))
        
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(xi * xi for xi in x)
        
        if n * sum_x2 - sum_x * sum_x == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        return slope / max(values) if max(values) != 0 else 0.0
    
    def _format_trend(self, trend: float) -> str:
        """Format trend value as readable string"""
        if trend > 0.1:
            return f"📈 Increasing ({trend:.2f})"
        elif trend < -0.1:
            return f"📉 Decreasing ({trend:.2f})"
        else:
            return f"📊 Stable ({trend:.2f})"
    
    def _show_weekly_comparison(self, daily_stats: Dict):
        """Show weekly comparison"""
        print("\n📅 WEEKLY COMPARISON")
        print("-" * 40)
        
        dates = sorted(daily_stats.keys())
        if len(dates) < 14:
            print("Insufficient data for weekly comparison")
            return
        
        # Compare last week vs previous week
        recent_week = dates[-7:]
        previous_week = dates[-14:-7]
        
        recent_cost = sum(daily_stats[d]['cost'] for d in recent_week)
        previous_cost = sum(daily_stats[d]['cost'] for d in previous_week)
        
        recent_msgs = sum(daily_stats[d]['messages'] for d in recent_week)
        previous_msgs = sum(daily_stats[d]['messages'] for d in previous_week)
        
        cost_change = ((recent_cost - previous_cost) / previous_cost * 100) if previous_cost > 0 else 0
        msg_change = ((recent_msgs - previous_msgs) / previous_msgs * 100) if previous_msgs > 0 else 0
        
        print(f"Last Week     : ${recent_cost:.2f}, {recent_msgs:,} messages")
        print(f"Previous Week : ${previous_cost:.2f}, {previous_msgs:,} messages")
        print(f"Change        : {cost_change:+.1f}% cost, {msg_change:+.1f}% messages")
    
    def _show_predictions(self, daily_stats: Dict):
        """Show usage predictions"""
        print("\n🔮 PREDICTIONS (Next 7 Days)")
        print("-" * 40)
        
        dates = sorted(daily_stats.keys())
        if len(dates) < 7:
            print("Insufficient data for predictions")
            return
        
        recent_costs = [daily_stats[d]['cost'] for d in dates[-7:]]
        recent_msgs = [daily_stats[d]['messages'] for d in dates[-7:]]
        
        avg_daily_cost = statistics.mean(recent_costs)
        avg_daily_msgs = statistics.mean(recent_msgs)
        
        predicted_weekly_cost = avg_daily_cost * 7
        predicted_weekly_msgs = avg_daily_msgs * 7
        
        print(f"Predicted Cost     : ${predicted_weekly_cost:.2f}")
        print(f"Predicted Messages : {predicted_weekly_msgs:,.0f}")
        print(f"Daily Average      : ${avg_daily_cost:.2f}, {avg_daily_msgs:.0f} messages")
    
    def _analyze_efficiency_trends(self, daily_stats: Dict):
        """Analyze efficiency trends over time"""
        print("\n⚡ EFFICIENCY TRENDS")
        print("-" * 40)
        
        dates = sorted(daily_stats.keys())
        efficiencies = []
        
        for date in dates:
            stats = daily_stats[date]
            if stats['cost'] > 0:
                efficiency = stats['messages'] / stats['cost']
                efficiencies.append(efficiency)
        
        if not efficiencies:
            print("No efficiency data available")
            return
        
        current_efficiency = efficiencies[-1] if efficiencies else 0
        avg_efficiency = statistics.mean(efficiencies)
        
        print(f"Current Efficiency : {current_efficiency:.1f} messages/$")
        print(f"Average Efficiency : {avg_efficiency:.1f} messages/$")
        
        if current_efficiency > avg_efficiency * 1.1:
            print("✅ Your efficiency is above average")
        elif current_efficiency < avg_efficiency * 0.9:
            print("⚠️ Your efficiency is below average")
        else:
            print("📊 Your efficiency is stable")
    
    def _analyze_weekly_productivity(self, hourly_stats: Dict):
        """Analyze productivity by day of week"""
        print("\n📅 WEEKLY PRODUCTIVITY PATTERNS")
        print("-" * 40)
        
        day_stats = defaultdict(lambda: {'messages': 0, 'cost': 0.0})
        
        for date_str, hours in hourly_stats.items():
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                day_name = date.strftime("%A")
                
                daily_messages = sum(h.get('messages', 0) for h in hours.values())
                daily_cost = sum(h.get('cost', 0.0) for h in hours.values())
                
                day_stats[day_name]['messages'] += daily_messages
                day_stats[day_name]['cost'] += daily_cost
            except ValueError:
                continue
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days:
            stats = day_stats[day]
            if stats['cost'] > 0:
                efficiency = stats['messages'] / stats['cost']
                print(f"{day:<9}: {stats['messages']:>6,} messages, ${stats['cost']:>7.2f}, {efficiency:>5.1f} msg/$")
    
    def _show_productivity_recommendations(self, hour_productivity: Dict, sorted_hours: List):
        """Show productivity recommendations"""
        print("\n💡 PRODUCTIVITY RECOMMENDATIONS")
        print("-" * 50)
        
        if not sorted_hours:
            print("No data available for recommendations")
            return
        
        # Find peak and low productivity hours
        peak_hours = [h for h, _ in sorted_hours[:3]]
        low_hours = [h for h, _ in sorted_hours[-3:]]
        
        print(f"🏆 Focus on hours: {', '.join(f'{h:02d}:00' for h in peak_hours)}")
        print(f"⏰ Consider avoiding: {', '.join(f'{h:02d}:00' for h in low_hours)}")
        
        # Efficiency recommendations
        total_messages = sum(stats['messages'] for stats in hour_productivity.values())
        total_cost = sum(stats['cost'] for stats in hour_productivity.values())
        
        if total_cost > 0:
            overall_efficiency = total_messages / total_cost
            print(f"📊 Current overall efficiency: {overall_efficiency:.1f} messages/$")
    
    def _find_peak_hours(self, hourly_stats: Dict) -> List[int]:
        """Find peak productivity hours"""
        hour_totals = defaultdict(int)
        
        for hours in hourly_stats.values():
            for hour_str, hour_data in hours.items():
                hour = int(hour_str.split(':')[0])
                hour_totals[hour] += hour_data.get('messages', 0)
        
        sorted_hours = sorted(hour_totals.items(), key=lambda x: x[1], reverse=True)
        return [hour for hour, _ in sorted_hours[:5]]
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate correlation coefficient between two lists"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)
        
        denominator = ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5
        
        if denominator == 0:
            return 0.0
        
        return (n * sum_xy - sum_x * sum_y) / denominator
    
    def _generate_recommendations(self, daily_stats: Dict, hourly_stats: Dict) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        if not daily_stats:
            return recommendations
        
        dates = sorted(daily_stats.keys())
        recent_costs = [daily_stats[d]['cost'] for d in dates[-7:]]
        
        # Cost management recommendations
        avg_cost = statistics.mean(recent_costs) if recent_costs else 0
        if avg_cost > 50:
            recommendations.append("Consider setting daily cost limits to manage spending")
        
        # Usage pattern recommendations
        peak_hours = self._find_peak_hours(hourly_stats)
        if peak_hours:
            recommendations.append(f"Schedule important work during peak hours: {peak_hours[0]:02d}:00-{peak_hours[0]+2:02d}:00")
        
        # Model efficiency recommendations
        if avg_cost > 0:
            recommendations.append("Review model efficiency analysis to optimize cost per message")
        
        return recommendations


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze usage trends and patterns')
    parser.add_argument('--days', type=int, default=30, help='Number of days to analyze')
    parser.add_argument('--trends', action='store_true', help='Show usage trends')
    parser.add_argument('--productivity', action='store_true', help='Show productivity patterns')  
    parser.add_argument('--efficiency', action='store_true', help='Show model efficiency')
    parser.add_argument('--insights', action='store_true', help='Generate insights report')
    parser.add_argument('--all', action='store_true', help='Show all analyses')
    
    args = parser.parse_args()
    
    analyzer = TrendAnalyzer()
    
    if args.all or not any([args.trends, args.productivity, args.efficiency, args.insights]):
        analyzer.analyze_usage_trends(args.days)
        analyzer.analyze_productivity_patterns()
        analyzer.analyze_model_efficiency()
        analyzer.generate_insights_report()
    else:
        if args.trends:
            analyzer.analyze_usage_trends(args.days)
        if args.productivity:
            analyzer.analyze_productivity_patterns()
        if args.efficiency:
            analyzer.analyze_model_efficiency()
        if args.insights:
            analyzer.generate_insights_report()


if __name__ == "__main__":
    main()