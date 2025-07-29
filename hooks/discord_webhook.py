import os
import requests

def send(payload):
    url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not url:
        raise EnvironmentError("DISCORD_WEBHOOK_URL environment variable is not set.")
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to send Discord webhook: {e}") from e
