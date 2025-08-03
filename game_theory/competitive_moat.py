"""Competitive moat through game-theoretic mechanisms"""

from typing import Dict, List


class CompetitiveMoat:
    def __init__(self):
        self.switching_costs = {
            "data_lock_in": 0.3,  # Historical performance data
            "learning_curve": 0.2,  # Persona calibration
            "social_capital": 0.4,  # Community status
            "sunk_costs": 0.1,  # Time investment
        }

    def calculate_switching_costs(
        self, user_tenure_months: int, user_tier: str, community_status: str
    ) -> Dict:
        """Calculate psychological and economic switching costs"""
        base_switching_cost = 50  # Base cost in dollars

        # Tenure multiplier: Longer users have higher switching costs
        tenure_multiplier = 1 + (user_tenure_months * 0.1)  # 10% per month

        # Tier multiplier: Higher tiers have more to lose
        tier_multipliers = {"bronze": 1.0, "silver": 1.5, "gold": 2.5}
        tier_multiplier = tier_multipliers.get(user_tier, 1.0)

        # Status multiplier: Community recognition creates lock-in
        status_multipliers = {
            "Member": 1.0,
            "Proven Performer": 1.3,
            "Verified Alpha Trader": 2.0,
            "Top 10% performer": 2.5,
        }
        status_multiplier = status_multipliers.get(community_status, 1.0)

        total_switching_cost = (
            base_switching_cost
            * tenure_multiplier
            * tier_multiplier
            * status_multiplier
        )

        return {
            "base_cost": base_switching_cost,
            "tenure_months": user_tenure_months,
            "tier": user_tier,
            "status": community_status,
            "total_switching_cost": total_switching_cost,
            "retention_probability": min(
                total_switching_cost / 200, 0.95
            ),  # Max 95% retention
        }

    def create_data_network_effects(
        self, total_signals: int, user_feedback_count: int
    ) -> Dict:
        """Create data advantages that improve with scale"""
        # More signals = better pattern recognition
        signal_advantage = min(total_signals / 1000, 5.0)  # Cap at 5x advantage

        # User feedback improves signal quality
        feedback_advantage = min(user_feedback_count / 500, 3.0)  # Cap at 3x advantage

        # Combined data moat strength
        data_moat_strength = signal_advantage + feedback_advantage

        return {
            "total_signals": total_signals,
            "user_feedback_count": user_feedback_count,
            "signal_advantage": signal_advantage,
            "feedback_advantage": feedback_advantage,
            "data_moat_strength": data_moat_strength,
            "competitive_advantage": (
                "Strong"
                if data_moat_strength > 5
                else "Moderate" if data_moat_strength > 2 else "Developing"
            ),
        }

    def implement_anti_competitive_features(self, competitor_count: int) -> Dict:
        """Features that become stronger as competition increases"""

        # Exclusive data sources (harder to replicate with more competitors)
        exclusivity_value = min(competitor_count * 0.2, 2.0)

        # Brand differentiation through scarcity
        scarcity_premium = min(competitor_count * 0.1, 1.5)

        # Network effects defense
        network_defense = min(competitor_count * 0.15, 1.8)

        total_defense_strength = exclusivity_value + scarcity_premium + network_defense

        return {
            "competitor_count": competitor_count,
            "exclusivity_value": exclusivity_value,
            "scarcity_premium": scarcity_premium,
            "network_defense": network_defense,
            "total_defense_strength": total_defense_strength,
            "moat_sustainability": (
                "High"
                if total_defense_strength > 4
                else "Medium" if total_defense_strength > 2 else "Low"
            ),
        }

    def design_winner_take_most_dynamics(
        self, market_share: float, performance_rank: int
    ) -> Dict:
        """Design mechanisms that create winner-take-most outcomes"""

        # Performance-based market concentration
        if performance_rank == 1:
            market_gravity = 2.5  # Top performer attracts disproportionate users
        elif performance_rank <= 3:
            market_gravity = 1.5  # Top 3 get significant advantage
        elif performance_rank <= 10:
            market_gravity = 1.1  # Top 10 get slight advantage
        else:
            market_gravity = 0.8  # Others lose market share

        # Network effects amplification
        network_amplification = 1 + (
            market_share * 2
        )  # Higher share = stronger effects

        # Combined winner-take-most strength
        wtm_strength = market_gravity * network_amplification

        return {
            "current_market_share": market_share,
            "performance_rank": performance_rank,
            "market_gravity": market_gravity,
            "network_amplification": network_amplification,
            "winner_take_most_strength": wtm_strength,
            "market_position": (
                "Dominant"
                if wtm_strength > 3
                else (
                    "Strong"
                    if wtm_strength > 2
                    else "Competitive" if wtm_strength > 1 else "Weak"
                )
            ),
        }
