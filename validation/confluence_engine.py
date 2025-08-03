"""Multi-factor confluence engine for signal validation"""
from typing import Dict, List
from crypto_data.price_feeds import PriceFeed

class ConfluenceEngine:
    def __init__(self, config: Dict):
        self.price_feed = PriceFeed()
        self.min_factors = 3  # Require 3+ confirmations
        self.cooldown_hours = 24
        self.signal_history = {}
    
    def validate_signal(self, symbol: str, signal_type: str) -> Dict:
        """Validate signal using multi-factor confluence"""
        factors = []
        
        # Factor 1: Price breakout
        price_factor = self._check_price_breakout(symbol)
        if price_factor["valid"]:
            factors.append(price_factor)
        
        # Factor 2: Volume spike
        volume_factor = self._check_volume_spike(symbol)
        if volume_factor["valid"]:
            factors.append(volume_factor)
        
        # Factor 3: Timing (market hours)
        timing_factor = self._check_timing()
        if timing_factor["valid"]:
            factors.append(timing_factor)
        
        # Factor 4: Cooldown check
        cooldown_factor = self._check_cooldown(symbol, signal_type)
        if cooldown_factor["valid"]:
            factors.append(cooldown_factor)
        
        confluence_score = len(factors)
        signal_valid = confluence_score >= self.min_factors
        
        return {
            "valid": signal_valid,
            "confluence_score": confluence_score,
            "factors": factors,
            "symbol": symbol,
            "signal_type": signal_type
        }
    
    def _check_price_breakout(self, symbol: str) -> Dict:
        """Check if price shows breakout pattern"""
        try:
            volume_data = self.price_feed.get_volume_data(symbol, days=1)
            prices = [p[1] for p in volume_data["prices"]]
            
            if len(prices) < 10:
                return {"valid": False, "reason": "Insufficient price data"}
            
            recent_high = max(prices[-5:])
            previous_resistance = max(prices[-20:-5])
            
            breakout = recent_high > previous_resistance * 1.02  # 2% breakout
            
            return {
                "valid": breakout,
                "factor": "price_breakout",
                "current_high": recent_high,
                "resistance": previous_resistance
            }
        except Exception:
            return {"valid": False, "reason": "Price data error"}
    
    def _check_volume_spike(self, symbol: str) -> Dict:
        """Check for volume spike confirmation"""
        try:
            volume_data = self.price_feed.get_volume_data(symbol, days=1)
            volumes = [v[1] for v in volume_data["volumes"]]
            
            if len(volumes) < 10:
                return {"valid": False, "reason": "Insufficient volume data"}
            
            recent_volume = volumes[-1]
            avg_volume = sum(volumes[-10:-1]) / 9
            
            spike_pct = ((recent_volume - avg_volume) / avg_volume) * 100
            volume_spike = spike_pct > 30  # 30% volume increase
            
            return {
                "valid": volume_spike,
                "factor": "volume_spike",
                "spike_percentage": spike_pct
            }
        except Exception:
            return {"valid": False, "reason": "Volume data error"}
    
    def _check_timing(self) -> Dict:
        """Check if timing is appropriate for signal"""
        from datetime import datetime
        current_hour = datetime.now().hour
        
        # Prefer signals during active trading hours (9 AM - 4 PM ET)
        active_hours = 9 <= current_hour <= 16
        
        return {
            "valid": active_hours,
            "factor": "timing",
            "current_hour": current_hour
        }
    
    def _check_cooldown(self, symbol: str, signal_type: str) -> Dict:
        """Check if signal is not in cooldown period"""
        from datetime import datetime, timedelta
        
        key = f"{symbol}_{signal_type}"
        last_signal = self.signal_history.get(key)
        
        if not last_signal:
            self.signal_history[key] = datetime.now()
            return {"valid": True, "factor": "cooldown", "status": "first_signal"}
        
        time_since = datetime.now() - last_signal
        cooldown_expired = time_since >= timedelta(hours=self.cooldown_hours)
        
        if cooldown_expired:
            self.signal_history[key] = datetime.now()
        
        return {
            "valid": cooldown_expired,
            "factor": "cooldown",
            "hours_since_last": time_since.total_seconds() / 3600
        }