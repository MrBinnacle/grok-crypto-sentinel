"""Game-theoretic incentive alignment system"""
from typing import Dict, List
import json

class IncentiveEngine:
    def __init__(self):
        self.user_tiers = {
            "bronze": {"accuracy_threshold": 0.55, "max_signals": 1, "price": 50},
            "silver": {"accuracy_threshold": 0.65, "max_signals": 2, "price": 100}, 
            "gold": {"accuracy_threshold": 0.75, "max_signals": 3, "price": 200}
        }
    
    def calculate_dynamic_pricing(self, user_id: str, current_accuracy: float) -> Dict:
        """Dynamic pricing based on delivered performance"""
        base_price = 100
        
        if current_accuracy >= 0.75:
            multiplier = 1.5
        elif current_accuracy >= 0.65:
            multiplier = 1.0
        elif current_accuracy >= 0.55:
            multiplier = 0.7
        else:
            multiplier = 0.5
        
        return {
            "user_id": user_id,
            "accuracy": current_accuracy,
            "final_price": base_price * multiplier,
            "tier_eligible": self._get_eligible_tier(current_accuracy)
        }
    
    def implement_scarcity_mechanism(self, total_users: int) -> Dict:
        """Implement artificial scarcity to increase value perception"""
        max_users = {"bronze": 1000, "silver": 500, "gold": 100}
        current_capacity = sum(max_users.values())
        waitlist_size = max(0, total_users - current_capacity)
        
        return {
            "total_capacity": current_capacity,
            "waitlist_size": waitlist_size,
            "scarcity_multiplier": 1 + (waitlist_size / current_capacity),
            "exclusivity_score": min(waitlist_size / 100, 5.0)
        }
    
    def create_user_competition(self, user_performances: List[Dict]) -> Dict:
        """Create competitive leaderboard to drive engagement"""
        sorted_users = sorted(user_performances, key=lambda x: x["accuracy"], reverse=True)
        
        leaderboard = []
        for i, user in enumerate(sorted_users[:10]):
            leaderboard.append({
                "rank": i + 1,
                "user_id": user["user_id"][:8] + "...",
                "accuracy": user["accuracy"],
                "tier": self._get_eligible_tier(user["accuracy"])
            })
        
        return {
            "leaderboard": leaderboard,
            "total_participants": len(user_performances),
            "competition_incentive": "Top 10 users get 50% discount next month"
        }
    
    def implement_social_proof(self, user_accuracy: float) -> Dict:
        """Generate social proof mechanisms"""
        percentile = self._calculate_percentile(user_accuracy)
        
        social_signals = []
        if percentile >= 90:
            social_signals.append("Top 10% performer")
        elif percentile >= 75:
            social_signals.append("Above average performer")
        
        if user_accuracy >= 0.70:
            social_signals.append("Verified high-accuracy signals")
        
        return {
            "user_percentile": percentile,
            "social_proof_badges": social_signals,
            "referral_value": int(user_accuracy * 100),
            "testimonial_eligible": user_accuracy >= 0.65
        }
    
    def _get_eligible_tier(self, accuracy: float) -> str:
        """Determine highest tier user qualifies for"""
        for tier, requirements in reversed(list(self.user_tiers.items())):
            if accuracy >= requirements["accuracy_threshold"]:
                return tier
        return "bronze"
    
    def _calculate_percentile(self, user_accuracy: float) -> float:
        """Calculate user's performance percentile"""
        if user_accuracy >= 0.75:
            return 95
        elif user_accuracy >= 0.65:
            return 75
        elif user_accuracy >= 0.55:
            return 50
        else:
            return 25