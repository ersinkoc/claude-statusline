#!/usr/bin/env python3
"""
Advanced Usage Analytics for Claude Statusline
Comprehensive usage insights, productivity metrics, and optimization recommendations
"""

import json
import math
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict, Counter
import statistics

from .data_directory_utils import resolve_data_directory
from .safe_file_operations import safe_json_read
from .console_utils import print_colored


class UsageAnalytics:
    """Advanced usage analytics and insights system"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = resolve_data_directory(data_dir)
        self.db_file = self.data_dir / "smart_sessions_db.json"
        self.prices_file = Path(__file__).parent / "prices.json"
        
        self.db = safe_json_read(self.db_file) if self.db_file.exists() else {}
        self.prices = safe_json_read(self.prices_file) if self.prices_file.exists() else {}
        
        # Cache for expensive calculations
        self._cache = {}
    
    def get_session_productivity_metrics(self, days: int = 30) -> Dict[str, Any]:
        """Calculate comprehensive productivity metrics"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        metrics = {
            'period': {'days': days, 'start': start_date.isoformat(), 'end': end_date.isoformat()},
            'sessions': {'total': 0, 'active_hours': 0, 'avg_duration': 0},
            'productivity': {},
            'efficiency': {},
            'patterns': {},
            'models': {},
            'recommendations': []
        }
        
        sessions_data = []
        hourly_stats = self.db.get('hourly_statistics', {})
        
        # Collect session data
        for date_str, hours in hourly_stats.items():
            try:
                session_date = datetime.strptime(date_str, "%Y-%m-%d")
                if start_date <= session_date <= end_date:
                    for hour, hour_data in hours.items():
                        if hour_data.get('message_count', 0) > 0:
                            sessions_data.append({
                                'date': session_date,
                                'hour': int(hour),
                                'messages': hour_data.get('message_count', 0),
                                'tokens': hour_data.get('tokens', 0),
                                'cost': hour_data.get('cost', 0.0),
                                'model': hour_data.get('primary_model', 'unknown'),
                                'duration': 60  # Assuming 1 hour sessions
                            })
            except ValueError:
                continue
        
        if not sessions_data:
            return metrics
        
        # Basic session metrics
        metrics['sessions']['total'] = len(sessions_data)
        metrics['sessions']['active_hours'] = len(sessions_data)
        total_messages = sum(s['messages'] for s in sessions_data)
        total_tokens = sum(s['tokens'] for s in sessions_data)
        total_cost = sum(s['cost'] for s in sessions_data)
        
        # Productivity metrics
        messages_per_hour = total_messages / len(sessions_data) if sessions_data else 0
        tokens_per_message = total_tokens / total_messages if total_messages > 0 else 0
        cost_per_message = total_cost / total_messages if total_messages > 0 else 0
        cost_per_token = total_cost / total_tokens if total_tokens > 0 else 0
        
        metrics['productivity'] = {
            'messages_per_hour': round(messages_per_hour, 2),
            'tokens_per_message': round(tokens_per_message, 0),
            'cost_per_message': round(cost_per_message, 4),
            'cost_per_token': round(cost_per_token, 6),
            'total_messages': total_messages,
            'total_tokens': total_tokens,
            'total_cost': round(total_cost, 2)
        }
        
        # Efficiency analysis
        daily_activity = defaultdict(list)
        for session in sessions_data:
            date_key = session['date'].strftime('%Y-%m-%d')
            daily_activity[date_key].append(session)
        
        daily_productivity = []
        for date, day_sessions in daily_activity.items():
            day_messages = sum(s['messages'] for s in day_sessions)
            day_hours = len(day_sessions)
            day_cost = sum(s['cost'] for s in day_sessions)
            
            if day_hours > 0:
                daily_productivity.append({
                    'date': date,
                    'messages_per_hour': day_messages / day_hours,
                    'cost_efficiency': day_messages / day_cost if day_cost > 0 else 0,
                    'total_hours': day_hours,
                    'total_messages': day_messages,
                    'total_cost': day_cost
                })
        
        if daily_productivity:
            avg_daily_messages = statistics.mean([d['messages_per_hour'] for d in daily_productivity])
            cost_efficiency_scores = [d['cost_efficiency'] for d in daily_productivity if d['cost_efficiency'] > 0]
            avg_cost_efficiency = statistics.mean(cost_efficiency_scores) if cost_efficiency_scores else 0
            
            metrics['efficiency'] = {
                'avg_daily_messages_per_hour': round(avg_daily_messages, 2),
                'avg_cost_efficiency': round(avg_cost_efficiency, 2),
                'productivity_trend': self._calculate_productivity_trend(daily_productivity),
                'best_day': max(daily_productivity, key=lambda x: x['messages_per_hour']),
                'most_efficient_day': max(daily_productivity, key=lambda x: x['cost_efficiency']) if cost_efficiency_scores else None
            }
        
        # Usage patterns
        hourly_patterns = defaultdict(list)
        daily_patterns = defaultdict(list)
        
        for session in sessions_data:
            hourly_patterns[session['hour']].append(session['messages'])
            daily_patterns[session['date'].strftime('%A')].append(session['messages'])
        
        peak_hours = sorted(hourly_patterns.items(), key=lambda x: statistics.mean(x[1]) if x[1] else 0, reverse=True)[:3]
        peak_days = sorted(daily_patterns.items(), key=lambda x: statistics.mean(x[1]) if x[1] else 0, reverse=True)[:3]
        
        metrics['patterns'] = {
            'peak_hours': [{'hour': h, 'avg_messages': round(statistics.mean(msgs), 1)} for h, msgs in peak_hours],
            'peak_days': [{'day': d, 'avg_messages': round(statistics.mean(msgs), 1)} for d, msgs in peak_days],
            'session_distribution': self._analyze_session_distribution(sessions_data)
        }
        
        # Model analysis
        model_usage = defaultdict(lambda: {'sessions': 0, 'messages': 0, 'tokens': 0, 'cost': 0.0})
        
        for session in sessions_data:
            model = session['model']
            model_usage[model]['sessions'] += 1
            model_usage[model]['messages'] += session['messages']
            model_usage[model]['tokens'] += session['tokens']
            model_usage[model]['cost'] += session['cost']
        
        model_stats = []
        for model, stats in model_usage.items():
            model_name = self._format_model_name(model)
            avg_cost_per_message = stats['cost'] / stats['messages'] if stats['messages'] > 0 else 0
            
            model_stats.append({
                'model': model_name,
                'sessions': stats['sessions'],
                'messages': stats['messages'],
                'avg_cost_per_message': round(avg_cost_per_message, 4),
                'total_cost': round(stats['cost'], 2),
                'cost_percentage': round((stats['cost'] / total_cost) * 100, 1) if total_cost > 0 else 0
            })
        
        metrics['models'] = sorted(model_stats, key=lambda x: x['total_cost'], reverse=True)
        
        # Generate recommendations
        metrics['recommendations'] = self._generate_usage_recommendations(metrics)
        
        return metrics
    
    def get_cost_breakdown_analysis(self, days: int = 30) -> Dict[str, Any]:
        """Detailed cost breakdown and analysis"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        analysis = {
            'period': {'days': days, 'start': start_date.isoformat(), 'end': end_date.isoformat()},
            'total_cost': 0.0,
            'breakdown': {
                'by_model': {},
                'by_day': {},
                'by_hour': {},
                'by_token_type': {}
            },
            'trends': {},
            'projections': {},
            'cost_insights': []
        }
        
        hourly_stats = self.db.get('hourly_statistics', {})
        daily_costs = []
        
        for date_str, hours in hourly_stats.items():
            try:
                session_date = datetime.strptime(date_str, "%Y-%m-%d")
                if start_date <= session_date <= end_date:
                    day_cost = 0.0
                    for hour, hour_data in hours.items():
                        cost = hour_data.get('cost', 0.0)
                        day_cost += cost
                        analysis['total_cost'] += cost
                        
                        # By model
                        model = hour_data.get('primary_model', 'unknown')
                        model_name = self._format_model_name(model)
                        if model_name not in analysis['breakdown']['by_model']:
                            analysis['breakdown']['by_model'][model_name] = 0.0
                        analysis['breakdown']['by_model'][model_name] += cost
                        
                        # By hour
                        hour_key = f"{int(hour):02d}:00"
                        if hour_key not in analysis['breakdown']['by_hour']:
                            analysis['breakdown']['by_hour'][hour_key] = 0.0
                        analysis['breakdown']['by_hour'][hour_key] += cost
                    
                    # By day
                    analysis['breakdown']['by_day'][date_str] = day_cost
                    daily_costs.append({'date': session_date, 'cost': day_cost})
                    
            except ValueError:
                continue
        
        # Calculate trends
        if len(daily_costs) > 7:
            recent_week = daily_costs[-7:]
            previous_week = daily_costs[-14:-7] if len(daily_costs) >= 14 else daily_costs[:-7]
            
            recent_avg = statistics.mean([d['cost'] for d in recent_week])
            previous_avg = statistics.mean([d['cost'] for d in previous_week]) if previous_week else recent_avg
            
            trend_percentage = ((recent_avg - previous_avg) / previous_avg * 100) if previous_avg > 0 else 0
            
            analysis['trends'] = {
                'daily_average': round(recent_avg, 2),
                'trend_percentage': round(trend_percentage, 1),
                'trend_direction': 'increasing' if trend_percentage > 5 else 'decreasing' if trend_percentage < -5 else 'stable'
            }
        
        # Cost projections
        if daily_costs:
            avg_daily_cost = statistics.mean([d['cost'] for d in daily_costs])
            analysis['projections'] = {
                'weekly': round(avg_daily_cost * 7, 2),
                'monthly': round(avg_daily_cost * 30, 2),
                'yearly': round(avg_daily_cost * 365, 2)
            }
        
        # Generate insights
        analysis['cost_insights'] = self._generate_cost_insights(analysis)
        
        return analysis
    
    def get_usage_patterns_report(self, days: int = 30) -> Dict[str, Any]:
        """Detailed usage patterns and behavior analysis"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        patterns = {
            'period': {'days': days, 'start': start_date.isoformat(), 'end': end_date.isoformat()},
            'temporal_patterns': {},
            'session_patterns': {},
            'interaction_patterns': {},
            'behavioral_insights': []
        }
        
        sessions_data = []
        hourly_stats = self.db.get('hourly_statistics', {})
        
        # Collect all session data
        for date_str, hours in hourly_stats.items():
            try:
                session_date = datetime.strptime(date_str, "%Y-%m-%d")
                if start_date <= session_date <= end_date:
                    for hour, hour_data in hours.items():
                        if hour_data.get('message_count', 0) > 0:
                            sessions_data.append({
                                'datetime': session_date.replace(hour=int(hour)),
                                'date': session_date,
                                'hour': int(hour),
                                'day_of_week': session_date.strftime('%A'),
                                'messages': hour_data.get('message_count', 0),
                                'tokens': hour_data.get('tokens', 0),
                                'cost': hour_data.get('cost', 0.0),
                                'model': hour_data.get('primary_model', 'unknown')
                            })
            except ValueError:
                continue
        
        if not sessions_data:
            return patterns
        
        # Temporal patterns
        hourly_activity = defaultdict(list)
        daily_activity = defaultdict(list)
        weekly_activity = defaultdict(list)
        
        for session in sessions_data:
            hourly_activity[session['hour']].append(session['messages'])
            daily_activity[session['day_of_week']].append(session['messages'])
            week_num = session['date'].isocalendar()[1]
            weekly_activity[week_num].append(session['messages'])
        
        patterns['temporal_patterns'] = {
            'hourly_distribution': {
                hour: {
                    'avg_messages': round(statistics.mean(messages), 1),
                    'total_sessions': len(messages),
                    'peak_activity': max(messages) if messages else 0
                }
                for hour, messages in hourly_activity.items()
            },
            'daily_distribution': {
                day: {
                    'avg_messages': round(statistics.mean(messages), 1),
                    'total_sessions': len(messages),
                    'consistency_score': round(1.0 - (statistics.stdev(messages) / statistics.mean(messages)), 2) if len(messages) > 1 and statistics.mean(messages) > 0 else 1.0
                }
                for day, messages in daily_activity.items()
            },
            'peak_hours': sorted(
                [(hour, round(statistics.mean(messages), 1)) for hour, messages in hourly_activity.items()],
                key=lambda x: x[1], reverse=True
            )[:5],
            'peak_days': sorted(
                [(day, round(statistics.mean(messages), 1)) for day, messages in daily_activity.items()],
                key=lambda x: x[1], reverse=True
            )
        }
        
        # Session patterns
        session_lengths = []
        gaps_between_sessions = []
        
        sorted_sessions = sorted(sessions_data, key=lambda x: x['datetime'])
        for i, session in enumerate(sorted_sessions):
            if i > 0:
                gap = (session['datetime'] - sorted_sessions[i-1]['datetime']).total_seconds() / 3600
                gaps_between_sessions.append(gap)
        
        patterns['session_patterns'] = {
            'avg_session_gap_hours': round(statistics.mean(gaps_between_sessions), 1) if gaps_between_sessions else 0,
            'session_frequency_per_day': round(len(sessions_data) / days, 1),
            'longest_streak': self._calculate_longest_streak(sessions_data),
            'session_clustering': self._analyze_session_clustering(sessions_data)
        }
        
        # Interaction patterns
        message_patterns = [s['messages'] for s in sessions_data]
        token_patterns = [s['tokens'] for s in sessions_data]
        
        patterns['interaction_patterns'] = {
            'message_distribution': {
                'avg_per_session': round(statistics.mean(message_patterns), 1),
                'median_per_session': round(statistics.median(message_patterns), 1),
                'std_deviation': round(statistics.stdev(message_patterns), 1) if len(message_patterns) > 1 else 0,
                'typical_range': f"{round(statistics.median(message_patterns) - statistics.stdev(message_patterns) if len(message_patterns) > 1 else 0, 1)}-{round(statistics.median(message_patterns) + statistics.stdev(message_patterns) if len(message_patterns) > 1 else statistics.median(message_patterns), 1)}"
            },
            'token_efficiency': {
                'avg_tokens_per_message': round(statistics.mean([t/m for s in sessions_data for t, m in [(s['tokens'], s['messages'])] if m > 0]), 0),
                'token_variability': round(statistics.stdev(token_patterns), 0) if len(token_patterns) > 1 else 0,
                'efficiency_trend': self._calculate_efficiency_trend(sessions_data)
            },
            'model_switching_behavior': self._analyze_model_switching(sessions_data)
        }
        
        # Generate behavioral insights
        patterns['behavioral_insights'] = self._generate_behavioral_insights(patterns, sessions_data)
        
        return patterns
    
    def display_comprehensive_usage_report(self, days: int = 30):
        """Display comprehensive usage analytics dashboard"""
        print("\n" + "="*100)
        print_colored("📊 COMPREHENSIVE USAGE ANALYTICS DASHBOARD", "cyan", bold=True)
        print("="*100)
        
        # Get all analytics data
        productivity = self.get_session_productivity_metrics(days)
        cost_analysis = self.get_cost_breakdown_analysis(days)
        usage_patterns = self.get_usage_patterns_report(days)
        
        # 1. Executive Summary
        print_colored(f"\n📋 EXECUTIVE SUMMARY (Last {days} days)", "blue", bold=True)
        print("-" * 60)
        
        total_sessions = productivity.get('sessions', {}).get('total', 0)
        total_cost = productivity.get('productivity', {}).get('total_cost', 0.0)
        total_messages = productivity.get('productivity', {}).get('total_messages', 0)
        avg_daily_cost = cost_analysis.get('projections', {}).get('monthly', 0) / 30 if cost_analysis.get('projections', {}).get('monthly') else 0
        
        print(f"  🎯 Total Sessions:        {total_sessions:,}")
        print(f"  💬 Total Messages:        {total_messages:,}")
        print(f"  💰 Total Cost:           ${total_cost:,.2f}")
        print(f"  📈 Daily Average Cost:    ${avg_daily_cost:.2f}")
        print(f"  ⚡ Messages/Hour:         {productivity.get('productivity', {}).get('messages_per_hour', 0)}")
        print(f"  💎 Cost/Message:         ${productivity.get('productivity', {}).get('cost_per_message', 0):.4f}")
        
        # 2. Productivity Metrics
        print_colored(f"\n🚀 PRODUCTIVITY METRICS", "green", bold=True)
        print("-" * 60)
        
        efficiency = productivity.get('efficiency', {})
        if efficiency:
            trend = efficiency.get('productivity_trend', 'stable')
            trend_color = "green" if trend == "improving" else "red" if trend == "declining" else "yellow"
            
            print(f"  📊 Productivity Trend:    ", end="")
            print_colored(f"{trend.upper()}", trend_color)
            print(f"  🏆 Best Day Messages/Hr:  {efficiency.get('best_day', {}).get('messages_per_hour', 'N/A')}")
            print(f"  💡 Cost Efficiency Score: {efficiency.get('avg_cost_efficiency', 0):.2f}")
        
        # 3. Usage Patterns
        print_colored(f"\n⏰ USAGE PATTERNS", "magenta", bold=True)
        print("-" * 60)
        
        peak_hours = usage_patterns.get('temporal_patterns', {}).get('peak_hours', [])[:3]
        peak_days = usage_patterns.get('temporal_patterns', {}).get('peak_days', [])
        
        print("  🕐 Peak Hours:")
        for i, (hour, avg_msgs) in enumerate(peak_hours, 1):
            print(f"     {i}. {hour:02d}:00 - {avg_msgs} msgs/hour")
        
        print("  📅 Most Active Days:")
        for day, avg_msgs in peak_days:
            print(f"     {day}: {avg_msgs} average messages")
        
        # 4. Cost Analysis
        print_colored(f"\n💰 COST BREAKDOWN", "yellow", bold=True)
        print("-" * 60)
        
        model_costs = cost_analysis.get('breakdown', {}).get('by_model', {})
        sorted_models = sorted(model_costs.items(), key=lambda x: x[1], reverse=True)[:5]
        
        print("  🤖 Top Models by Cost:")
        for model, cost in sorted_models:
            percentage = (cost / total_cost * 100) if total_cost > 0 else 0
            print(f"     {model}: ${cost:.2f} ({percentage:.1f}%)")
        
        # 5. Projections
        projections = cost_analysis.get('projections', {})
        if projections:
            print_colored(f"\n🔮 COST PROJECTIONS", "cyan", bold=True)
            print("-" * 60)
            print(f"  📅 Weekly:   ${projections.get('weekly', 0):.2f}")
            print(f"  📅 Monthly:  ${projections.get('monthly', 0):.2f}")
            print(f"  📅 Yearly:   ${projections.get('yearly', 0):,.2f}")
        
        # 6. Recommendations
        recommendations = productivity.get('recommendations', [])
        if recommendations:
            print_colored(f"\n💡 OPTIMIZATION RECOMMENDATIONS", "blue", bold=True)
            print("-" * 60)
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        
        # 7. Session Quality Analysis
        print_colored(f"\n🎯 SESSION QUALITY ANALYSIS", "green", bold=True)
        print("-" * 60)
        
        interaction_patterns = usage_patterns.get('interaction_patterns', {})
        msg_dist = interaction_patterns.get('message_distribution', {})
        
        print(f"  📊 Avg Messages/Session:  {msg_dist.get('avg_per_session', 0)}")
        print(f"  📈 Median Messages:       {msg_dist.get('median_per_session', 0)}")
        print(f"  📋 Typical Range:         {msg_dist.get('typical_range', 'N/A')}")
        
        token_eff = interaction_patterns.get('token_efficiency', {})
        print(f"  🔤 Tokens per Message:    {token_eff.get('avg_tokens_per_message', 0)}")
        
        # 8. Insights & Patterns
        behavioral_insights = usage_patterns.get('behavioral_insights', [])
        if behavioral_insights:
            print_colored(f"\n🧠 BEHAVIORAL INSIGHTS", "magenta", bold=True)
            print("-" * 60)
            for insight in behavioral_insights[:5]:
                print(f"  • {insight}")
    
    def export_usage_report(self, days: int = 30, format: str = 'json') -> str:
        """Export comprehensive usage report"""
        report_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'period_days': days,
                'report_type': 'comprehensive_usage_analytics'
            },
            'productivity_metrics': self.get_session_productivity_metrics(days),
            'cost_analysis': self.get_cost_breakdown_analysis(days),
            'usage_patterns': self.get_usage_patterns_report(days)
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"usage_analytics_{timestamp}.{format}"
        output_path = self.data_dir / output_file
        
        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2)
        elif format == 'csv':
            # Export key metrics to CSV
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Productivity summary
                writer.writerow(['Metric', 'Value'])
                prod_metrics = report_data['productivity_metrics']['productivity']
                for key, value in prod_metrics.items():
                    writer.writerow([key.replace('_', ' ').title(), value])
                
                writer.writerow([])  # Empty row
                writer.writerow(['Model', 'Cost', 'Percentage'])
                
                # Model breakdown
                for model_data in report_data['productivity_metrics']['models']:
                    writer.writerow([
                        model_data['model'],
                        model_data['total_cost'],
                        f"{model_data['cost_percentage']}%"
                    ])
        
        print_colored(f"✅ Usage analytics report exported to: {output_path}", "green")
        return str(output_path)
    
    # Helper methods for calculations
    def _format_model_name(self, model: str) -> str:
        """Format model name for display"""
        if 'claude-3-5-sonnet' in model:
            return 'Claude 3.5 Sonnet'
        elif 'claude-3-opus' in model:
            return 'Claude 3 Opus'
        elif 'claude-3-haiku' in model:
            return 'Claude 3 Haiku'
        elif 'opus-4' in model or 'claude-opus-4' in model:
            return 'Claude Opus 4.1'
        else:
            return model.replace('-', ' ').title()
    
    def _calculate_productivity_trend(self, daily_data: List[Dict]) -> str:
        """Calculate productivity trend over time"""
        if len(daily_data) < 7:
            return "insufficient_data"
        
        # Compare first half vs second half
        mid_point = len(daily_data) // 2
        first_half = daily_data[:mid_point]
        second_half = daily_data[mid_point:]
        
        first_avg = statistics.mean([d['messages_per_hour'] for d in first_half])
        second_avg = statistics.mean([d['messages_per_hour'] for d in second_half])
        
        change = (second_avg - first_avg) / first_avg if first_avg > 0 else 0
        
        if change > 0.1:
            return "improving"
        elif change < -0.1:
            return "declining"
        else:
            return "stable"
    
    def _analyze_session_distribution(self, sessions_data: List[Dict]) -> Dict:
        """Analyze distribution of session characteristics"""
        message_counts = [s['messages'] for s in sessions_data]
        
        if not message_counts:
            return {}
        
        quartiles = [
            statistics.quantiles(message_counts, n=4)[0],
            statistics.median(message_counts),
            statistics.quantiles(message_counts, n=4)[2]
        ]
        
        return {
            'q1_messages': round(quartiles[0], 1),
            'median_messages': round(quartiles[1], 1),
            'q3_messages': round(quartiles[2], 1),
            'outlier_threshold': round(quartiles[2] + 1.5 * (quartiles[2] - quartiles[0]), 1),
            'high_activity_sessions': len([m for m in message_counts if m > quartiles[2] + 1.5 * (quartiles[2] - quartiles[0])])
        }
    
    def _generate_usage_recommendations(self, metrics: Dict) -> List[str]:
        """Generate actionable usage recommendations"""
        recommendations = []
        
        productivity = metrics.get('productivity', {})
        efficiency = metrics.get('efficiency', {})
        patterns = metrics.get('patterns', {})
        models = metrics.get('models', [])
        
        # Cost optimization recommendations
        if models:
            expensive_model = models[0]  # Most expensive model
            if expensive_model['cost_percentage'] > 60:
                recommendations.append(f"Consider using {expensive_model['model']} more strategically - it accounts for {expensive_model['cost_percentage']:.1f}% of your costs")
        
        # Productivity recommendations
        messages_per_hour = productivity.get('messages_per_hour', 0)
        if messages_per_hour < 10:
            recommendations.append("Low messages per hour detected. Consider preparing questions in advance or using longer, more detailed prompts")
        elif messages_per_hour > 50:
            recommendations.append("High message frequency detected. Consider consolidating related questions into single, comprehensive prompts")
        
        # Time-based recommendations
        peak_hours = patterns.get('peak_hours', [])
        if len(peak_hours) >= 2:
            best_hour = peak_hours[0]['hour']
            recommendations.append(f"Your most productive hour is {best_hour:02d}:00. Consider scheduling complex tasks during this time")
        
        # Efficiency recommendations  
        trend = efficiency.get('productivity_trend', 'stable')
        if trend == 'declining':
            recommendations.append("Productivity trend is declining. Consider taking breaks or varying your interaction patterns")
        elif trend == 'improving':
            recommendations.append("Great! Your productivity is improving. Keep up the current workflow patterns")
        
        cost_per_message = productivity.get('cost_per_message', 0)
        if cost_per_message > 0.05:
            recommendations.append("High cost per message. Consider asking more comprehensive questions to get more value per interaction")
        
        return recommendations[:6]  # Limit to top 6 recommendations
    
    def _generate_cost_insights(self, analysis: Dict) -> List[str]:
        """Generate cost-related insights"""
        insights = []
        
        total_cost = analysis['total_cost']
        breakdown = analysis.get('breakdown', {})
        trends = analysis.get('trends', {})
        
        # Model cost insights
        by_model = breakdown.get('by_model', {})
        if by_model:
            most_expensive = max(by_model.items(), key=lambda x: x[1])
            insights.append(f"Most expensive model: {most_expensive[0]} (${most_expensive[1]:.2f})")
            
            if len(by_model) > 1:
                cost_concentration = most_expensive[1] / total_cost if total_cost > 0 else 0
                if cost_concentration > 0.8:
                    insights.append(f"High cost concentration: {cost_concentration*100:.1f}% on single model")
        
        # Trend insights
        trend_direction = trends.get('trend_direction', 'stable')
        trend_percentage = trends.get('trend_percentage', 0)
        
        if trend_direction != 'stable':
            insights.append(f"Cost trend: {trend_direction} by {abs(trend_percentage):.1f}% week-over-week")
        
        # Daily pattern insights
        by_day = breakdown.get('by_day', {})
        if by_day:
            daily_costs = list(by_day.values())
            if daily_costs:
                avg_daily = statistics.mean(daily_costs)
                max_daily = max(daily_costs)
                
                if max_daily > avg_daily * 2:
                    insights.append(f"Cost variability detected: highest day ${max_daily:.2f} vs average ${avg_daily:.2f}")
        
        return insights
    
    def _calculate_longest_streak(self, sessions_data: List[Dict]) -> int:
        """Calculate longest consecutive days streak"""
        if not sessions_data:
            return 0
        
        dates = set(s['date'].date() for s in sessions_data)
        sorted_dates = sorted(dates)
        
        longest_streak = 1
        current_streak = 1
        
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i] - sorted_dates[i-1]).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
        
        return longest_streak
    
    def _analyze_session_clustering(self, sessions_data: List[Dict]) -> Dict:
        """Analyze how sessions cluster in time"""
        if not sessions_data:
            return {}
        
        sorted_sessions = sorted(sessions_data, key=lambda x: x['datetime'])
        gaps = []
        
        for i in range(1, len(sorted_sessions)):
            gap_hours = (sorted_sessions[i]['datetime'] - sorted_sessions[i-1]['datetime']).total_seconds() / 3600
            gaps.append(gap_hours)
        
        if not gaps:
            return {}
        
        avg_gap = statistics.mean(gaps)
        short_gaps = len([g for g in gaps if g <= 2])  # Within 2 hours
        long_gaps = len([g for g in gaps if g >= 24])  # More than a day
        
        return {
            'avg_gap_hours': round(avg_gap, 1),
            'clustered_sessions_pct': round((short_gaps / len(gaps)) * 100, 1) if gaps else 0,
            'isolated_sessions_pct': round((long_gaps / len(gaps)) * 100, 1) if gaps else 0,
            'clustering_pattern': 'highly_clustered' if short_gaps / len(gaps) > 0.6 else 'spread_out' if long_gaps / len(gaps) > 0.4 else 'mixed'
        }
    
    def _calculate_efficiency_trend(self, sessions_data: List[Dict]) -> str:
        """Calculate token efficiency trend over time"""
        if len(sessions_data) < 10:
            return "insufficient_data"
        
        sorted_sessions = sorted(sessions_data, key=lambda x: x['datetime'])
        
        # Calculate token efficiency for each session
        efficiencies = []
        for session in sorted_sessions:
            if session['messages'] > 0:
                efficiency = session['tokens'] / session['messages']
                efficiencies.append(efficiency)
        
        if len(efficiencies) < 5:
            return "insufficient_data"
        
        # Compare first third vs last third
        third = len(efficiencies) // 3
        first_third = efficiencies[:third]
        last_third = efficiencies[-third:]
        
        first_avg = statistics.mean(first_third)
        last_avg = statistics.mean(last_third)
        
        change = (last_avg - first_avg) / first_avg if first_avg > 0 else 0
        
        if change > 0.1:
            return "improving"
        elif change < -0.1:
            return "declining"
        else:
            return "stable"
    
    def _analyze_model_switching(self, sessions_data: List[Dict]) -> Dict:
        """Analyze model switching behavior"""
        if not sessions_data:
            return {}
        
        sorted_sessions = sorted(sessions_data, key=lambda x: x['datetime'])
        switches = 0
        model_sequence = []
        
        current_model = None
        for session in sorted_sessions:
            model = session['model']
            if current_model and model != current_model:
                switches += 1
            current_model = model
            model_sequence.append(model)
        
        unique_models = len(set(model_sequence))
        switch_rate = switches / len(sessions_data) if sessions_data else 0
        
        return {
            'total_switches': switches,
            'switch_rate': round(switch_rate, 3),
            'models_used': unique_models,
            'switching_behavior': 'frequent' if switch_rate > 0.3 else 'occasional' if switch_rate > 0.1 else 'stable'
        }
    
    def _generate_behavioral_insights(self, patterns: Dict, sessions_data: List[Dict]) -> List[str]:
        """Generate behavioral insights from usage patterns"""
        insights = []
        
        temporal = patterns.get('temporal_patterns', {})
        session_patterns = patterns.get('session_patterns', {})
        interaction = patterns.get('interaction_patterns', {})
        
        # Time-based insights
        peak_hours = temporal.get('peak_hours', [])
        if peak_hours:
            peak_hour = peak_hours[0][0]
            if 9 <= peak_hour <= 17:
                insights.append("Primary usage during business hours suggests work-related activities")
            elif 18 <= peak_hour <= 23:
                insights.append("Evening usage pattern suggests personal projects or learning")
            elif 0 <= peak_hour <= 6:
                insights.append("Night owl usage pattern detected - consider sleep schedule impact")
        
        # Session frequency insights
        freq_per_day = session_patterns.get('session_frequency_per_day', 0)
        if freq_per_day > 8:
            insights.append("High session frequency suggests intensive usage - monitor for efficiency")
        elif freq_per_day < 1:
            insights.append("Low session frequency - consider more regular engagement for better results")
        
        # Consistency insights
        daily_dist = temporal.get('daily_distribution', {})
        if daily_dist:
            consistency_scores = [day_data.get('consistency_score', 0) for day_data in daily_dist.values()]
            avg_consistency = statistics.mean(consistency_scores) if consistency_scores else 0
            
            if avg_consistency > 0.8:
                insights.append("High usage consistency - excellent habit formation")
            elif avg_consistency < 0.5:
                insights.append("Irregular usage patterns - consider establishing routine")
        
        # Message pattern insights
        msg_dist = interaction.get('message_distribution', {})
        avg_messages = msg_dist.get('avg_per_session', 0)
        median_messages = msg_dist.get('median_per_session', 0)
        
        if avg_messages > median_messages * 1.5:
            insights.append("Some sessions with very high activity - suggests batch processing approach")
        
        # Model switching insights
        model_behavior = interaction.get('model_switching_behavior', {})
        switching = model_behavior.get('switching_behavior', 'stable')
        
        if switching == 'frequent':
            insights.append("Frequent model switching suggests experimentation or task-specific optimization")
        elif switching == 'stable':
            insights.append("Consistent model usage suggests found preferred workflow")
        
        return insights


def main():
    """CLI entry point for usage analytics"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Statusline Usage Analytics')
    subparsers = parser.add_subparsers(dest='command', help='Analytics commands')
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Show comprehensive usage dashboard')
    dashboard_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze')
    
    # Productivity command
    prod_parser = subparsers.add_parser('productivity', help='Show productivity metrics')
    prod_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze')
    
    # Cost analysis command
    cost_parser = subparsers.add_parser('costs', help='Show cost breakdown analysis')
    cost_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze')
    
    # Patterns command
    patterns_parser = subparsers.add_parser('patterns', help='Show usage patterns')
    patterns_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export usage analytics report')
    export_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze')
    export_parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Export format')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    analytics = UsageAnalytics()
    
    if args.command == 'dashboard':
        analytics.display_comprehensive_usage_report(args.days)
    elif args.command == 'productivity':
        metrics = analytics.get_session_productivity_metrics(args.days)
        print(json.dumps(metrics, indent=2))
    elif args.command == 'costs':
        cost_analysis = analytics.get_cost_breakdown_analysis(args.days)
        print(json.dumps(cost_analysis, indent=2))
    elif args.command == 'patterns':
        patterns = analytics.get_usage_patterns_report(args.days)
        print(json.dumps(patterns, indent=2))
    elif args.command == 'export':
        analytics.export_usage_report(args.days, args.format)


if __name__ == "__main__":
    main()