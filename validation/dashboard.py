"""Performance dashboard for validation and credibility"""
import json
from datetime import datetime
from typing import Dict
from validation.performance_tracker import PerformanceTracker

class ValidationDashboard:
    def __init__(self):
        self.tracker = PerformanceTracker()
    
    def generate_report(self) -> str:
        """Generate performance validation report"""
        stats = self.tracker.get_performance_stats()
        
        report = f"""
=== GROK CRYPTO SENTINEL - PERFORMANCE VALIDATION ===
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M ET')}

SIGNAL PERFORMANCE:
• Total Signals Evaluated: {stats['total_signals']}
• Accuracy Rate: {stats['accuracy']:.1%}
• Average Return: {stats['avg_return']:.1f}%

VALIDATION STATUS:
• Minimum Accuracy Target: 65% {'PASS' if stats['accuracy'] >= 0.65 else 'FAIL'}
• Minimum Avg Return Target: 8% {'PASS' if stats['avg_return'] >= 8 else 'FAIL'}
• Signal Quality: {'HIGH' if stats['accuracy'] >= 0.65 and stats['avg_return'] >= 8 else 'DEVELOPING'}

COMPETITIVE BENCHMARK:
• vs Random (50%): {'+' if stats['accuracy'] > 0.5 else '-'}{abs(stats['accuracy'] - 0.5):.1%}
• vs Market Average (8%): {'+' if stats['avg_return'] > 8 else '-'}{abs(stats['avg_return'] - 8):.1f}%

CREDIBILITY SCORE: {self._calculate_credibility_score(stats)}/100
        """
        
        return report.strip()
    
    def export_validation_data(self) -> Dict:
        """Export validation data for external audit"""
        performance_data = self.tracker._load_performance_data()
        stats = self.tracker.get_performance_stats()
        
        return {
            "validation_timestamp": datetime.now().isoformat(),
            "performance_stats": stats,
            "signal_count": len(performance_data.get("signals", {})),
            "methodology": {
                "evaluation_period": "24 hours",
                "profit_threshold": "2%",
                "data_source": "CoinGecko API"
            },
            "competitive_position": {
                "accuracy_vs_random": stats['accuracy'] - 0.5,
                "return_vs_market": stats['avg_return'] - 8.0
            }
        }
    
    def _calculate_credibility_score(self, stats: Dict) -> int:
        """Calculate credibility score (0-100)"""
        score = 0
        
        # Accuracy component (40 points max)
        if stats['accuracy'] >= 0.65:
            score += 40
        elif stats['accuracy'] >= 0.55:
            score += 20
        
        # Return component (40 points max)
        if stats['avg_return'] >= 8:
            score += 40
        elif stats['avg_return'] >= 4:
            score += 20
        
        # Sample size component (20 points max)
        if stats['total_signals'] >= 50:
            score += 20
        elif stats['total_signals'] >= 20:
            score += 10
        
        return min(score, 100)

if __name__ == "__main__":
    dashboard = ValidationDashboard()
    print(dashboard.generate_report())