import yaml
import datetime
from typing import Dict, Any

METRICS_FILE = "metrics.yaml"

def load_metrics() -> Dict[str, Any]:
    try:
        with open(METRICS_FILE, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {
            "signals_triggered_today": 0,
            "average_signals_per_day": 0,
            "persona_uptime": {},
            "last_updated": ""
        }

def update_metrics(persona_used: str, signals_triggered: int) -> None:
    metrics = load_metrics()
    today = datetime.date.today().isoformat()

    # Track signal triggers
    metrics["signals_triggered_today"] = signals_triggered
    metrics["last_updated"] = f"{today}T09:15:00Z"

    # Update persona uptime counter
    if persona_used not in metrics["persona_uptime"]:
        metrics["persona_uptime"][persona_used] = 0
    metrics["persona_uptime"][persona_used] += 1

    # TODO: calculate rolling average
    with open(METRICS_FILE, "w") as f:
        yaml.dump(metrics, f)

if __name__ == "__main__":
    # EXAMPLE USAGE
    update_metrics(persona_used="novice_plus", signals_triggered=2)