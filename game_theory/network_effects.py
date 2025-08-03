"""Network effects and viral growth mechanisms"""

from typing import Dict, List


class NetworkEffectsEngine:
    def __init__(self):
        self.viral_coefficients = {
            "referral_bonus": 0.3,  # 30% of subscription
            "accuracy_multiplier": 2.0,  # Higher accuracy = higher referral value
            "network_threshold": 100,  # Users needed for network effects
        }

    def calculate_network_value(self, total_users: int, avg_accuracy: float) -> Dict:
        """Calculate increasing value as network grows"""
        base_value = 100

        # Metcalfe's Law: Value proportional to n²
        network_multiplier = min((total_users / 100) ** 1.5, 10)  # Cap at 10x

        # Quality multiplier based on collective accuracy
        quality_multiplier = 1 + (avg_accuracy - 0.5) * 2  # 50% baseline

        network_value = base_value * network_multiplier * quality_multiplier

        return {
            "total_users": total_users,
            "base_value": base_value,
            "network_multiplier": network_multiplier,
            "quality_multiplier": quality_multiplier,
            "total_network_value": network_value,
            "value_per_user": network_value / max(total_users, 1),
        }

    def design_referral_system(
        self, referrer_accuracy: float, referee_tier: str
    ) -> Dict:
        """Design referral system that rewards quality users"""
        base_bonus = 30  # $30 base referral bonus

        # Accuracy bonus: Higher performing users get better referral rewards
        accuracy_bonus = (referrer_accuracy - 0.5) * 100  # $50 max bonus

        # Tier bonus: Referring higher-tier users pays more
        tier_bonuses = {"bronze": 1.0, "silver": 1.5, "gold": 2.0}
        tier_multiplier = tier_bonuses.get(referee_tier, 1.0)

        total_bonus = (base_bonus + accuracy_bonus) * tier_multiplier

        return {
            "referrer_accuracy": referrer_accuracy,
            "referee_tier": referee_tier,
            "base_bonus": base_bonus,
            "accuracy_bonus": accuracy_bonus,
            "tier_multiplier": tier_multiplier,
            "total_referral_bonus": total_bonus,
            "viral_coefficient": total_bonus / 100,  # Percentage of subscription value
        }

    def create_exclusive_communities(
        self, user_tier: str, user_accuracy: float
    ) -> Dict:
        """Create tier-based exclusive communities"""
        communities = {
            "bronze": {
                "name": "Crypto Scouts",
                "access_level": "basic",
                "features": ["Daily signals", "Basic analytics"],
            },
            "silver": {
                "name": "Signal Operators",
                "access_level": "advanced",
                "features": [
                    "Priority signals",
                    "Performance analytics",
                    "Community chat",
                ],
            },
            "gold": {
                "name": "Alpha Council",
                "access_level": "elite",
                "features": [
                    "Exclusive signals",
                    "Direct analyst access",
                    "Private Discord",
                    "Early feature access",
                ],
            },
        }

        user_community = communities.get(user_tier, communities["bronze"])

        # Special recognition for high performers
        if user_accuracy >= 0.80:
            user_community["special_status"] = "Verified Alpha Trader"
        elif user_accuracy >= 0.70:
            user_community["special_status"] = "Proven Performer"

        return {
            "tier": user_tier,
            "community": user_community,
            "exclusivity_value": len(communities)
            - list(communities.keys()).index(user_tier),
            "social_status": user_community.get("special_status", "Member"),
        }

    def implement_information_cascades(
        self, signal_confidence: float, user_tier_distribution: Dict
    ) -> Dict:
        """Create information cascades where higher-tier users influence lower tiers"""
        cascade_strength = 0

        # Gold tier users create strongest cascades
        gold_influence = user_tier_distribution.get("gold", 0) * 3.0
        silver_influence = user_tier_distribution.get("silver", 0) * 1.5
        bronze_influence = user_tier_distribution.get("bronze", 0) * 0.5

        total_influence = gold_influence + silver_influence + bronze_influence
        cascade_strength = min(total_influence / 100, 2.0)  # Cap at 2x

        # Higher confidence signals get amplified more
        amplified_confidence = signal_confidence * (1 + cascade_strength)

        return {
            "original_confidence": signal_confidence,
            "cascade_strength": cascade_strength,
            "amplified_confidence": min(amplified_confidence, 1.0),
            "tier_influence": {
                "gold": gold_influence,
                "silver": silver_influence,
                "bronze": bronze_influence,
            },
            "network_effect": (
                "Strong"
                if cascade_strength > 1.0
                else "Moderate" if cascade_strength > 0.5 else "Weak"
            ),
        }
