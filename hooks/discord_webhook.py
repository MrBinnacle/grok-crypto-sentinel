import os
import requests

def send(signal, persona):
    url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not url:
        raise EnvironmentError("DISCORD_WEBHOOK_URL environment variable is not set.")
    payload = {
        "content": f"Signal: {signal}\nPersona: {persona}"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to send Discord webhook: {e}") from e
