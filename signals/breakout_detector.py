"""Breakout signal detection using volume and price analysis.

This module provides functionality to detect breakout patterns in cryptocurrency prices
based on volume spikes and price levels.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, TypedDict, Literal

from crypto_data.price_feeds import PriceFeed

# Constants
HOURS_IN_DAY = 24
MIN_VOLUME_DATA_POINTS = 2

# Type definitions
class BreakoutSignal(TypedDict):
    """Structure of a breakout signal."""
    what_happened: str
    why_it_matters: str
    suggested_posture: Literal["accumulate", "hold", "reduce"]
    current_price: float
    volume_spike: float

class ConfigurationError(Exception):
    """Raised when there's an error in the configuration."""
    pass


class BreakoutDetector:
    """Detects breakout patterns in cryptocurrency prices based on volume and price levels.
    
    Args:
        config: Dictionary containing configuration parameters including:
            - codex.breakout_watch.support_floor: Price floor for support
            - codex.breakout_watch.breakout_zone: Price level for breakout
            - codex.onchain_signal.volume_spike_pct: Minimum volume spike percentage
    
    Raises:
        ConfigurationError: If required configuration is missing or invalid
    """
    
    def __init__(self, config: Dict):
        """Initialize the BreakoutDetector with configuration."""
        self.price_feed = PriceFeed()
        
        try:
            self.support_floor = float(config.get("codex", {}).get("breakout_watch", {}).get("support_floor"))
            self.breakout_zone = float(config.get("codex", {}).get("breakout_watch", {}).get("breakout_zone"))
            self.volume_threshold = float(config.get("codex", {}).get("onchain_signal", {}).get("volume_spike_pct"))
        except (TypeError, ValueError) as e:
            raise ConfigurationError("Invalid configuration values") from e
    
    def _get_volume_spike_percentage(self, volumes: List[float]) -> float:
        """Calculate the percentage increase of the current volume compared to average.
        
        Args:
            volumes: List of volume values
            
        Returns:
            float: Percentage increase of current volume compared to average
            
        Raises:
            ValueError: If insufficient data points are provided
        """
        if len(volumes) < MIN_VOLUME_DATA_POINTS:
            raise ValueError(f"At least {MIN_VOLUME_DATA_POINTS} data points required")
            
        previous_volumes = volumes[:-1]
        current_volume = volumes[-1]
        avg_volume = sum(previous_volumes) / len(previous_volumes)
        
        if avg_volume == 0:
            return float('inf')
            
        return ((current_volume - avg_volume) / avg_volume) * 100

    def detect_breakout(self, symbol: str) -> Optional[BreakoutSignal]:
        """Detect breakout signals based on price and volume.
        
        Args:
            symbol: Cryptocurrency symbol to check for breakouts
            
        Returns:
            Optional[BreakoutSignal]: Breakout signal if conditions are met, None otherwise
            
        Raises:
            RuntimeError: If there's an error during breakout detection
            ConfigurationError: If the detector is not properly configured
        """
        try:
            # Get current price and volume data
            price_data = self.price_feed.get_current_prices([symbol])
            volume_data = self.price_feed.get_volume_data(symbol)
            
            # Validate price data
            if not price_data or not isinstance(price_data, dict):
                return None
                
            symbol_data = price_data.get(symbol)
            if not isinstance(symbol_data, dict):
                return None
                
            current_price = symbol_data.get("usd")
            if current_price is None:
                return None
            
            # Process volume data
            if not isinstance(volume_data, dict) or not isinstance(volume_data.get("volumes"), list):
                return None
                
            recent_volumes = [float(v[1]) for v in volume_data["volumes"][-HOURS_IN_DAY:] if len(v) > 1]
            
            if len(recent_volumes) < MIN_VOLUME_DATA_POINTS:
                return None
            
            # Calculate volume spike
            try:
                volume_spike_pct = self._get_volume_spike_percentage(recent_volumes)
            except (ValueError, ZeroDivisionError):
                return None
            
            # Check breakout conditions
            if (current_price > self.breakout_zone and 
                volume_spike_pct > self.volume_threshold):
                
                return {
                    "what_happened": f"{symbol.upper()} broke resistance at ${self.breakout_zone:.2f}",
                    "why_it_matters": f"Volume spike +{volume_spike_pct:.0f}% signals strong momentum",
                    "suggested_posture": "accumulate",
                    "current_price": current_price,
                    "volume_spike": volume_spike_pct
                }
            
            return None
            
        except (KeyError, TypeError, ValueError) as e:
            # Handle expected errors
            return None
        except Exception as e:
            # Log unexpected errors and re-raise
            raise RuntimeError(f"Breakout detection failed for {symbol}") from e