import os
import requests
import logging

def send(signal, persona):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        logging.error("DISCORD_WEBHOOK_URL environment variable is not set")
        raise EnvironmentError("DISCORD_WEBHOOK_URL environment variable is not set.")

    payload = {
        "content": f"Signal: {signal}\nPersona: {persona}"
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        logging.error(f"Discord webhook failed: {error}")
        raise RuntimeError(f"Failed to send Discord webhook: {error}") from error
