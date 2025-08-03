"""Business outcome tracking for McKinsey-in-a-box validation"""

from typing import Dict, List
from datetime import datetime, timedelta
import json


class BusinessOutcomeTracker:
    def __init__(self):
        self.outcome_file = "validation/business_outcomes.json"
        self.frameworks_tested = [
            "value_chain_analysis",
            "porter_five_forces",
            "bcg_growth_share_matrix",
            "mckinsey_7s_framework",
        ]

    def create_public_case_study(
        self, business_profile: Dict, problem: str, framework_used: str
    ) -> str:
        """Create trackable public case study"""
        case_id = f"case_{datetime.now().strftime('%Y%m%d_%H%M')}"

        case_study = {
            "case_id": case_id,
            "business_profile": {
                "industry": business_profile["industry"],
                "revenue_range": business_profile["revenue_range"],
                "employee_count": business_profile["employee_count"],
                "location": business_profile.get("location", "undisclosed"),
            },
            "problem_statement": problem,
            "framework_applied": framework_used,
            "recommendations": self._generate_framework_recommendations(
                problem, framework_used
            ),
            "baseline_metrics": business_profile.get("baseline_metrics", {}),
            "start_date": datetime.now().isoformat(),
            "tracking_period": "90_days",
            "public_url": f"https://mckinsey-in-a-box.com/case-studies/{case_id}",
            "status": "active",
        }

        self._save_case_study(case_study)
        return case_id

    def track_outcome_metrics(self, case_id: str, actual_results: Dict) -> Dict:
        """Track actual business outcomes vs predictions"""
        case_study = self._load_case_study(case_id)

        if not case_study:
            return {"error": "Case study not found"}

        # Calculate outcome accuracy
        predictions = case_study["recommendations"]["predicted_outcomes"]
        accuracy_scores = {}

        for metric, predicted_value in predictions.items():
            actual_value = actual_results.get(metric, 0)
            if predicted_value != 0:
                accuracy = 1 - abs(predicted_value - actual_value) / abs(
                    predicted_value
                )
                accuracy_scores[metric] = max(
                    0, accuracy
                )  # Cap at 0 for negative accuracy

        overall_accuracy = (
            sum(accuracy_scores.values()) / len(accuracy_scores)
            if accuracy_scores
            else 0
        )

        outcome_data = {
            "case_id": case_id,
            "completion_date": datetime.now().isoformat(),
            "predicted_outcomes": predictions,
            "actual_outcomes": actual_results,
            "accuracy_scores": accuracy_scores,
            "overall_accuracy": overall_accuracy,
            "framework_effectiveness": self._assess_framework_effectiveness(
                overall_accuracy
            ),
            "public_verification": True,
        }

        case_study["outcome_data"] = outcome_data
        case_study["status"] = "completed"
        self._save_case_study(case_study)

        return outcome_data

    def generate_credibility_report(self) -> Dict:
        """Generate public credibility report"""
        all_cases = self._load_all_case_studies()
        completed_cases = [case for case in all_cases if case["status"] == "completed"]

        if not completed_cases:
            return {"error": "No completed cases for analysis"}

        # Calculate aggregate metrics
        accuracy_scores = [
            case["outcome_data"]["overall_accuracy"] for case in completed_cases
        ]
        avg_accuracy = sum(accuracy_scores) / len(accuracy_scores)

        framework_performance = {}
        for case in completed_cases:
            framework = case["framework_applied"]
            accuracy = case["outcome_data"]["overall_accuracy"]

            if framework not in framework_performance:
                framework_performance[framework] = []
            framework_performance[framework].append(accuracy)

        # Calculate framework averages
        framework_averages = {
            framework: sum(scores) / len(scores)
            for framework, scores in framework_performance.items()
        }

        return {
            "report_date": datetime.now().isoformat(),
            "total_cases_completed": len(completed_cases),
            "overall_accuracy": avg_accuracy,
            "framework_performance": framework_averages,
            "credibility_score": self._calculate_credibility_score(
                avg_accuracy, len(completed_cases)
            ),
            "public_verification_url": "https://mckinsey-in-a-box.com/validation-report",
            "third_party_audit": "Available upon request",
        }

    def _generate_framework_recommendations(self, problem: str, framework: str) -> Dict:
        """Generate specific recommendations based on framework"""
        recommendations = {
            "value_chain_analysis": {
                "actions": [
                    "Analyze cost structure by activity",
                    "Identify value-adding vs non-value-adding activities",
                    "Benchmark against industry standards",
                ],
                "predicted_outcomes": {
                    "cost_reduction_pct": 15,
                    "efficiency_improvement_pct": 25,
                    "timeline_days": 90,
                },
            },
            "porter_five_forces": {
                "actions": [
                    "Assess competitive rivalry intensity",
                    "Evaluate supplier/buyer power",
                    "Identify barriers to entry",
                ],
                "predicted_outcomes": {
                    "market_position_improvement": 20,
                    "pricing_power_increase_pct": 10,
                    "timeline_days": 120,
                },
            },
        }

        return recommendations.get(
            framework,
            {
                "actions": ["Framework-specific analysis"],
                "predicted_outcomes": {"improvement_pct": 10, "timeline_days": 90},
            },
        )

    def _assess_framework_effectiveness(self, accuracy: float) -> str:
        """Assess framework effectiveness based on accuracy"""
        if accuracy >= 0.8:
            return "HIGHLY_EFFECTIVE"
        elif accuracy >= 0.6:
            return "EFFECTIVE"
        elif accuracy >= 0.4:
            return "MODERATELY_EFFECTIVE"
        else:
            return "NEEDS_IMPROVEMENT"

    def _calculate_credibility_score(self, avg_accuracy: float, case_count: int) -> int:
        """Calculate overall credibility score (0-100)"""
        accuracy_score = min(avg_accuracy * 80, 80)  # Max 80 points for accuracy
        sample_size_score = min(case_count * 2, 20)  # Max 20 points for sample size

        return int(accuracy_score + sample_size_score)

    def _save_case_study(self, case_study: Dict):
        """Save case study to file"""
        all_cases = self._load_all_case_studies()

        # Update existing or add new
        updated = False
        for i, case in enumerate(all_cases):
            if case["case_id"] == case_study["case_id"]:
                all_cases[i] = case_study
                updated = True
                break

        if not updated:
            all_cases.append(case_study)

        with open(self.outcome_file, "w") as f:
            json.dump({"case_studies": all_cases}, f, indent=2)

    def _load_case_study(self, case_id: str) -> Dict:
        """Load specific case study"""
        all_cases = self._load_all_case_studies()
        for case in all_cases:
            if case["case_id"] == case_id:
                return case
        return {}

    def _load_all_case_studies(self) -> List[Dict]:
        """Load all case studies"""
        try:
            with open(self.outcome_file, "r") as f:
                data = json.load(f)
                return data.get("case_studies", [])
        except FileNotFoundError:
            return []
