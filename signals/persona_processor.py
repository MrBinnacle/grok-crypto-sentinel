"""Persona-based signal filtering and formatting"""
import yaml
from typing import Dict, List, Optional

class PersonaProcessor:
    def __init__(self):
        with open("persona_presets.yaml", "r") as f:
            self.personas = yaml.safe_load(f)
    
    def filter_signals(self, signals: List[Dict], persona: str) -> List[Dict]:
        """Filter signals based on persona preferences"""
        if persona not in self.personas:
            return signals
            
        persona_config = self.personas[persona]
        max_insights = persona_config.get("max_insights_per_day", 3)
        entry_radar = persona_config.get("entry_radar", "active")
        
        # Filter based on entry radar sensitivity
        if entry_radar == "hyper":
            filtered = signals  # Show all signals
        elif entry_radar == "active":
            filtered = [s for s in signals if s.get("volume_spike", 0) > 30]
        else:  # filtered
            filtered = [s for s in signals if s.get("volume_spike", 0) > 50]
        
        # Limit to max insights per day
        return filtered[:max_insights]
    
    def format_output(self, signals: List[Dict], persona: str) -> str:
        """Format signals according to persona tone"""
        if not signals:
            return "🟢 No critical signals today. Stay the course.\n\n📈 Entry Radar Status: None triggered\n🧠 Daily Reflection: Let others chase the obvious."
        
        persona_config = self.personas.get(persona, {})
        tone = persona_config.get("tone", "explanatory")
        
        output = []
        for signal in signals:
            if tone == "terse":
                output.append(f"• 🔍 {signal['what_happened']}\n🎯 {signal['suggested_posture']}")
            else:
                output.append(f"• 🔍 {signal['what_happened']}\n📉 {signal['why_it_matters']}\n🎯 Posture: [{signal['suggested_posture']}]")
        
        return "\n\n".join(output)