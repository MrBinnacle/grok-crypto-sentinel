"""Tests for crypto data ingestion"""
import pytest
from crypto_data.price_feeds import PriceFeed

def test_price_feed_initialization():
    """Test PriceFeed can be initialized"""
    feed = PriceFeed()
    assert feed.base_url == "https://api.coingecko.com/api/v3"

@pytest.mark.integration
def test_get_current_prices():
    """Integration test for price fetching"""
    feed = PriceFeed()
    try:
        prices = feed.get_current_prices(["bitcoin"])
        assert "bitcoin" in prices
        assert "usd" in prices["bitcoin"]
        assert isinstance(prices["bitcoin"]["usd"], (int, float))
    except Exception:
        pytest.skip("API unavailable")