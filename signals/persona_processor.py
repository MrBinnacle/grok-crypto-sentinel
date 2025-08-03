"""Persona-based signal filtering and formatting"""

import yaml
from typing import Dict, List, Union, Any, TypeVar, Optional

from signals.breakout_detector import BreakoutSignal

# Create a type variable that can be either a dict or EnrichedBreakoutSignal
EnrichedSignal = TypeVar("EnrichedSignal", Dict[str, Any], "EnrichedBreakoutSignal")


class EnrichedBreakoutSignal(BreakoutSignal):
    """Extended signal type with additional metadata."""

    symbol: str
    confluence_score: float


class PersonaProcessor:
    def __init__(self):
        with open("persona_presets.yaml", "r") as f:
            self.personas = yaml.safe_load(f)

    def filter_signals(
        self, signals: List[EnrichedSignal], persona: str
    ) -> List[EnrichedSignal]:
        """Filter signals based on persona preferences

        Args:
            signals: List of signals to filter, either as dicts or EnrichedBreakoutSignal
            persona: The persona to filter for

        Returns:
            Filtered list of signals matching persona preferences
        """
        if not signals:
            return []

        if persona not in self.personas:
            return signals

        persona_config = self.personas[persona]
        max_insights = persona_config.get("max_insights_per_day", 3)
        entry_radar = persona_config.get("entry_radar", "active")

        # Helper function to get volume spike from either dict or EnrichedBreakoutSignal
        def get_volume_spike(signal: EnrichedSignal) -> float:
            if isinstance(signal, dict):
                return signal.get("volume_spike", 0.0)
            return getattr(signal, "volume_spike", 0.0)

        # Filter based on entry radar sensitivity
        if entry_radar == "hyper":
            filtered = signals  # Show all signals
        elif entry_radar == "active":
            filtered = [s for s in signals if get_volume_spike(s) > 30.0]
        else:  # filtered
            filtered = [s for s in signals if get_volume_spike(s) > 50.0]

        # Limit to max insights per day
        return filtered[:max_insights]

    def format_output(self, signals: List[EnrichedSignal], persona: str) -> str:
        """Format signals according to persona tone

        Args:
            signals: List of signals to format, either as dicts or EnrichedBreakoutSignal
            persona: The persona to format for

        Returns:
            Formatted string representation of the signals
        """
        if not signals:
            return "🟢 No critical signals today. Stay the course.\n\n📈 Entry Radar Status: None triggered\n🧠 Daily Reflection: Let others chase the obvious."

        persona_config = self.personas.get(persona, {})
        tone = persona_config.get("tone", "explanatory")

        output = []
        for signal in signals:
            # Extract fields from either dict or EnrichedBreakoutSignal
            if isinstance(signal, dict):
                what_happened = signal.get("what_happened", "")
                why_it_matters = signal.get("why_it_matters", "")
                suggested_posture = signal.get("suggested_posture", "")
            else:
                what_happened = getattr(signal, "what_happened", "")
                why_it_matters = getattr(signal, "why_it_matters", "")
                suggested_posture = getattr(signal, "suggested_posture", "")

            if tone == "terse":
                output.append(f"• 🔍 {what_happened}\n🎯 {suggested_posture}")
            else:
                output.append(
                    f"• 🔍 {what_happened}\n📉 {why_it_matters}\n🎯 Posture: [{suggested_posture}]"
                )

        return "\n\n".join(output)
