"""Main task runner for 9:15 AM ET crypto signal generation"""

import yaml
from datetime import datetime
from typing import Dict, TypedDict, Literal, Any

from signals.breakout_detector import BreakoutDetector, BreakoutSignal
from signals.persona_processor import PersonaProcessor
from hooks.hooks import route_signal
from validation.performance_tracker import PerformanceTracker
from validation.confluence_engine import ConfluenceEngine


class EnrichedBreakoutSignal(BreakoutSignal):
    """Extends BreakoutSignal with additional fields for processing."""

    symbol: str
    confluence_score: float


class TaskRunner:
    def __init__(self):
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)

        self.breakout_detector = BreakoutDetector(self.config)
        self.persona_processor = PersonaProcessor()
        self.performance_tracker = PerformanceTracker()
        self.confluence_engine = ConfluenceEngine(self.config)
        self.default_assets = ["bitcoin", "ethereum", "ripple"]

    def run_daily_scan(self, persona: str = "novice_plus") -> str:
        """Execute daily crypto signal scan.

        Args:
            persona: The user persona to generate signals for (default: "novice_plus")

        Returns:
            str: Formatted output string with signals for the specified persona
        """
        print(f"[📆 {datetime.now().strftime('%Y-%m-%d – %H:%M ET')}]")

        all_signals: list[EnrichedBreakoutSignal] = []

        # Scan each asset for breakout signals
        for asset in self.default_assets:
            try:
                # Get base signal from detector
                base_signal = self.breakout_detector.detect_breakout(asset)
                if not base_signal:
                    continue

                # Validate signal with confluence engine
                validation = self.confluence_engine.validate_signal(asset, "breakout")
                if not validation.get("valid", False):
                    continue

                # Create enriched signal with additional fields
                enriched_signal: EnrichedBreakoutSignal = {
                    **base_signal,  # Include all base signal fields
                    "symbol": asset,
                    "confluence_score": float(validation.get("confluence_score", 0.0)),
                }

                all_signals.append(enriched_signal)

                # Log for performance tracking
                signal_id = self.performance_tracker.log_signal(
                    enriched_signal, persona
                )

                # Route to webhooks
                route_signal(enriched_signal, persona)

            except Exception as e:
                print(f"Error scanning {asset}: {e}")

        # Filter and format based on persona
        filtered_signals = self.persona_processor.filter_signals(all_signals, persona)
        output = self.persona_processor.format_output(filtered_signals, persona)

        return output

    def run(self):
        """Main entry point"""
        try:
            # Evaluate previous signals
            evaluation_results = self.performance_tracker.evaluate_signals()
            if evaluation_results["evaluated"] > 0:
                print(
                    f"Evaluated {evaluation_results['evaluated']} signals, {evaluation_results['accuracy']:.1%} accuracy"
                )

            # Run daily scan
            result = self.run_daily_scan()
            print(result)
            return result
        except Exception as e:
            print(f"Task runner failed: {e}")
            return None


if __name__ == "__main__":
    runner = TaskRunner()
    runner.run()
