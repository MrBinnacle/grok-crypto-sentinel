"""Breakout signal detection using volume and price analysis"""
from typing import Dict, Optional
from crypto_data.price_feeds import PriceFeed

class BreakoutDetector:
    def __init__(self, config: Dict):
        self.price_feed = PriceFeed()
        self.support_floor = config["codex"]["breakout_watch"]["support_floor"]
        self.breakout_zone = config["codex"]["breakout_watch"]["breakout_zone"]
        self.volume_threshold = config["codex"]["onchain_signal"]["volume_spike_pct"]
    
    def detect_breakout(self, symbol: str) -> Optional[Dict]:
        """Detect breakout signals based on price and volume"""
        try:
            # Get current price and volume data
            price_data = self.price_feed.get_current_prices([symbol])
            volume_data = self.price_feed.get_volume_data(symbol)
            
            current_price = price_data[symbol]["usd"]
            recent_volumes = [v[1] for v in volume_data["volumes"][-24:]]  # Last 24 hours
            
            if len(recent_volumes) < 2:
                return None
                
            # Calculate volume spike
            avg_volume = sum(recent_volumes[:-1]) / len(recent_volumes[:-1])
            current_volume = recent_volumes[-1]
            volume_spike_pct = ((current_volume - avg_volume) / avg_volume) * 100
            
            # Check breakout conditions
            if (current_price > self.breakout_zone and 
                volume_spike_pct > self.volume_threshold):
                
                return {
                    "what_happened": f"{symbol.upper()} broke resistance at ${self.breakout_zone}",
                    "why_it_matters": f"Volume spike +{volume_spike_pct:.0f}% signals strong momentum",
                    "suggested_posture": "accumulate",
                    "current_price": current_price,
                    "volume_spike": volume_spike_pct
                }
            
            return None
            
        except Exception as e:
            raise RuntimeError(f"Breakout detection failed for {symbol}: {e}") from e