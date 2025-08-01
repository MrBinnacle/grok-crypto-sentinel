"""Main task runner for 9:15 AM ET crypto signal generation"""
import yaml
from datetime import datetime
from signals.breakout_detector import BreakoutDetector
from signals.persona_processor import PersonaProcessor
from hooks.hooks import route_signal

class TaskRunner:
    def __init__(self):
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        
        self.breakout_detector = BreakoutDetector(self.config)
        self.persona_processor = PersonaProcessor()
        self.default_assets = ["bitcoin", "ethereum", "ripple"]
    
    def run_daily_scan(self, persona: str = "novice_plus") -> str:
        """Execute daily crypto signal scan"""
        print(f"[📆 {datetime.now().strftime('%Y-%m-%d – %H:%M ET')}]")
        
        all_signals = []
        
        # Scan each asset for breakout signals
        for asset in self.default_assets:
            try:
                signal = self.breakout_detector.detect_breakout(asset)
                if signal:
                    all_signals.append(signal)
                    # Route to webhooks
                    route_signal(signal, persona)
            except Exception as e:
                print(f"Error scanning {asset}: {e}")
        
        # Filter and format based on persona
        filtered_signals = self.persona_processor.filter_signals(all_signals, persona)
        output = self.persona_processor.format_output(filtered_signals, persona)
        
        return output
    
    def run(self):
        """Main entry point"""
        try:
            result = self.run_daily_scan()
            print(result)
            return result
        except Exception as e:
            print(f"Task runner failed: {e}")
            return None

if __name__ == "__main__":
    runner = TaskRunner()
    runner.run()