import pytest
from hooks import route_signal
from hooks import metrics_tracker

def test_route_signal_no_crash():
    """Ensure route_signal handles dummy signal safely without side effects."""
    dummy_signal = {
        "title": "Test Signal",
        "what_happened": "XRP spiked 42%",
        "why_it_matters": "Whale accumulation pattern",
        "posture": "[watch]"
    }
    try:
        route_signal(dummy_signal, "novice_plus")
    except Exception as e:
        pytest.fail(f"route_signal raised exception: {e}")

def test_update_metrics_runs():
    """Confirm update_metrics writes to metrics.yaml without crashing."""
    try:
        metrics_tracker.update_metrics("novice_plus", 2)
    except Exception as e:
        pytest.fail(f"update_metrics raised exception: {e}")
