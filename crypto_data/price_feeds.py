"""Crypto price data ingestion from CoinGecko API"""
import requests
from typing import Dict, List

class PriceFeed:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
    
    def get_current_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Get current prices for crypto symbols"""
        ids = ",".join(symbols).lower()
        try:
            response = requests.get(
                f"{self.base_url}/simple/price",
                params={"ids": ids, "vs_currencies": "usd"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Price feed failed: {e}") from e
    
    def get_volume_data(self, symbol: str, days: int = 1) -> Dict:
        """Get volume data for breakout detection"""
        try:
            response = requests.get(
                f"{self.base_url}/coins/{symbol.lower()}/market_chart",
                params={"vs_currency": "usd", "days": days},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return {
                "prices": data["prices"],
                "volumes": data["total_volumes"]
            }
        except requests.RequestException as e:
            raise RuntimeError(f"Volume data failed: {e}") from e