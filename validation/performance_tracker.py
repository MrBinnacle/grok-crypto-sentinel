"""Signal performance tracking and validation system"""
import json
from datetime import datetime, timedelta
from typing import Dict, TypedDict, Literal, Any, Union

from crypto_data.price_feeds import PriceFeed
from signals.breakout_detector import BreakoutSignal

# Type definitions for signals
class EnrichedBreakoutSignal(BreakoutSignal):
    """Extended signal type with additional metadata."""
    symbol: str
    confluence_score: float

class PerformanceTracker:
    def __init__(self):
        self.price_feed = PriceFeed()
        self.performance_file = "validation/signal_performance.json"
        
    def log_signal(self, signal: Union[Dict[str, Any], EnrichedBreakoutSignal], persona: str) -> str:
        """Log signal for performance tracking
        
        Args:
            signal: The signal to log, either as a dictionary or EnrichedBreakoutSignal
            persona: The persona this signal is for
            
        Returns:
            str: Unique identifier for the logged signal
            
        Raises:
            ValueError: If the signal is missing required fields
        """
        try:
            # Handle both dict and EnrichedBreakoutSignal
            symbol = signal.get('symbol', 'unknown') if isinstance(signal, dict) else signal['symbol']
            current_price = signal.get('current_price') if isinstance(signal, dict) else signal['current_price']
            
            signal_id = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M')}"
            
            performance_data = self._load_performance_data()
            performance_data.setdefault("signals", {})[signal_id] = {
                "timestamp": datetime.now().isoformat(),
                "signal": dict(signal) if not isinstance(signal, dict) else signal,
                "persona": persona,
                "entry_price": current_price,
                "status": "active"
            }
            
            self._save_performance_data(performance_data)
            return signal_id
            
        except (KeyError, AttributeError) as e:
            raise ValueError(f"Invalid signal format: {e}") from e
    
    def evaluate_signals(self) -> Dict[str, float]:
        """Evaluate 24h performance of active signals.
        
        Returns:
            Dict containing:
                - evaluated (int): Number of signals evaluated
                - winners (int): Number of profitable signals
                - accuracy (float): Ratio of winners to evaluated signals (0.0 to 1.0)
        """
        performance_data = self._load_performance_data()
        evaluated_count = 0
        winners_count = 0
        
        for signal_id, data in performance_data["signals"].items():
            if data.get("status") == "active":
                try:
                    signal_time = datetime.fromisoformat(data["timestamp"])
                    if datetime.now() - signal_time >= timedelta(hours=24):
                        outcome = self._evaluate_signal_outcome(data)
                        data["status"] = "evaluated"
                        data["outcome"] = outcome
                        
                        evaluated_count += 1
                        if outcome.get("profitable", False):
                            winners_count += 1
                except (KeyError, ValueError) as e:
                    # Skip signals with invalid timestamps
                    continue
        
        # Calculate accuracy as a float between 0.0 and 1.0
        accuracy = float(winners_count) / evaluated_count if evaluated_count > 0 else 0.0
        
        return {
            "evaluated": evaluated_count,
            "winners": winners_count,
            "accuracy": accuracy
        }
        
        self._save_performance_data(performance_data)
        return results
    
    def get_performance_stats(self) -> Dict:
        """Get overall performance statistics"""
        performance_data = self._load_performance_data()
        evaluated_signals = [s for s in performance_data["signals"].values() if s["status"] == "evaluated"]
        
        if not evaluated_signals:
            return {"total_signals": 0, "accuracy": 0, "avg_return": 0}
        
        profitable = [s for s in evaluated_signals if s.get("outcome", {}).get("profitable", False)]
        returns = [s.get("outcome", {}).get("return_pct", 0) for s in evaluated_signals]
        
        return {
            "total_signals": len(evaluated_signals),
            "accuracy": len(profitable) / len(evaluated_signals),
            "avg_return": sum(returns) / len(returns) if returns else 0
        }
    
    def _evaluate_signal_outcome(self, signal_data: Dict) -> Dict:
        """Evaluate if signal was profitable after 24h"""
        try:
            entry_price = signal_data.get("entry_price", 0)
            if not entry_price:
                return {"profitable": False, "return_pct": 0, "error": "No entry price"}
            
            # Simulate outcome for validation (replace with real price check)
            import random
            return_pct = random.uniform(-5, 10)  # Temporary simulation
            
            return {
                "return_pct": return_pct,
                "profitable": return_pct > 2.0,
                "evaluated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "profitable": False, "return_pct": 0}
    
    def _load_performance_data(self) -> Dict:
        """Load performance data from file"""
        try:
            with open(self.performance_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"signals": {}, "created": datetime.now().isoformat()}
    
    def _save_performance_data(self, data: Dict):
        """Save performance data to file"""
        with open(self.performance_file, "w") as f:
            json.dump(data, f, indent=2)