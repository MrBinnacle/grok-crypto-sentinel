"""Executive Information Noise Filter"""

from typing import Dict, List


class ExecutiveNoiseFilter:
    def __init__(self):
        self.noise_patterns = [
            "synergy",
            "leverage",
            "paradigm shift",
            "disruptive innovation",
            "best practices",
            "low-hanging fruit",
            "move the needle",
            "circle back",
            "deep dive",
            "boil the ocean",
        ]

        self.signal_indicators = [
            "revenue impact",
            "cost reduction",
            "market share",
            "customer retention",
            "competitive advantage",
            "regulatory change",
            "technology shift",
        ]

    def filter_executive_content(self, content: str, executive_role: str) -> Dict:
        """Filter noise from executive communications"""

        # Count buzzwords vs actionable content
        noise_score = sum(
            1 for pattern in self.noise_patterns if pattern in content.lower()
        )
        signal_score = sum(
            1 for indicator in self.signal_indicators if indicator in content.lower()
        )

        # Calculate signal-to-noise ratio
        total_words = len(content.split())
        noise_ratio = noise_score / max(total_words / 100, 1)  # Per 100 words
        signal_ratio = signal_score / max(total_words / 100, 1)

        # Determine content quality
        if signal_ratio > noise_ratio * 2:
            quality = "HIGH_SIGNAL"
        elif signal_ratio > noise_ratio:
            quality = "MODERATE_SIGNAL"
        else:
            quality = "HIGH_NOISE"

        return {
            "content_quality": quality,
            "noise_score": noise_score,
            "signal_score": signal_score,
            "signal_to_noise_ratio": signal_ratio / max(noise_ratio, 0.1),
            "recommendation": self._get_recommendation(quality),
            "filtered_insights": self._extract_insights(content, executive_role),
        }

    def prioritize_executive_inputs(
        self, inputs: List[Dict], executive_role: str
    ) -> List[Dict]:
        """Prioritize information inputs for executive attention"""

        priority_weights = {
            "ceo": {
                "strategic": 3.0,
                "competitive": 2.5,
                "financial": 2.0,
                "operational": 1.0,
            },
            "cfo": {
                "financial": 3.0,
                "regulatory": 2.5,
                "operational": 2.0,
                "strategic": 1.5,
            },
            "coo": {
                "operational": 3.0,
                "financial": 2.0,
                "strategic": 1.5,
                "competitive": 1.0,
            },
        }

        role_weights = priority_weights.get(executive_role, priority_weights["ceo"])

        # Score each input
        for input_item in inputs:
            category = input_item.get("category", "operational")
            urgency = input_item.get("urgency", 1)  # 1-5 scale
            impact = input_item.get("impact", 1)  # 1-5 scale

            base_weight = role_weights.get(category, 1.0)
            priority_score = base_weight * urgency * impact

            input_item["priority_score"] = priority_score
            input_item["executive_relevance"] = self._assess_relevance(
                input_item, executive_role
            )

        # Sort by priority score
        return sorted(inputs, key=lambda x: x["priority_score"], reverse=True)

    def generate_executive_summary(
        self, filtered_inputs: List[Dict], max_items: int = 3
    ) -> Dict:
        """Generate concise executive summary"""

        top_items = filtered_inputs[:max_items]

        summary = {
            "total_inputs_processed": len(filtered_inputs),
            "high_priority_items": len(
                [i for i in filtered_inputs if i["priority_score"] > 10]
            ),
            "top_decisions_needed": [],
            "key_risks": [],
            "opportunities": [],
        }

        for item in top_items:
            if item.get("requires_decision", False):
                summary["top_decisions_needed"].append(
                    {
                        "decision": item.get("title", "Unknown"),
                        "deadline": item.get("deadline", "ASAP"),
                        "impact": item.get("impact", 1),
                    }
                )

            if item.get("category") == "risk":
                summary["key_risks"].append(item.get("title", "Unknown risk"))

            if item.get("category") == "opportunity":
                summary["opportunities"].append(
                    item.get("title", "Unknown opportunity")
                )

        return summary

    def _get_recommendation(self, quality: str) -> str:
        """Get recommendation based on content quality"""
        recommendations = {
            "HIGH_SIGNAL": "Priority read - contains actionable insights",
            "MODERATE_SIGNAL": "Review when time permits - mixed value",
            "HIGH_NOISE": "Skip - mostly buzzwords and fluff",
        }
        return recommendations.get(quality, "Review content quality")

    def _extract_insights(self, content: str, executive_role: str) -> List[str]:
        """Extract key insights relevant to executive role"""
        insights = []

        # Simple keyword-based extraction (would be ML in production)
        if executive_role == "ceo" and any(
            word in content.lower() for word in ["market", "competition", "strategy"]
        ):
            insights.append("Strategic market intelligence detected")

        if executive_role == "cfo" and any(
            word in content.lower() for word in ["cost", "revenue", "margin", "cash"]
        ):
            insights.append("Financial impact information identified")

        if executive_role == "coo" and any(
            word in content.lower() for word in ["process", "efficiency", "operations"]
        ):
            insights.append("Operational improvement opportunity found")

        return insights

    def _assess_relevance(self, input_item: Dict, executive_role: str) -> str:
        """Assess relevance of input to specific executive role"""
        category = input_item.get("category", "")

        relevance_map = {
            "ceo": ["strategic", "competitive", "market"],
            "cfo": ["financial", "regulatory", "risk"],
            "coo": ["operational", "process", "efficiency"],
        }

        role_keywords = relevance_map.get(executive_role, [])

        if any(keyword in category.lower() for keyword in role_keywords):
            return "HIGH"
        elif input_item.get("impact", 1) >= 4:
            return "MEDIUM"
        else:
            return "LOW"
