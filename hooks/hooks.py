import os
from hooks import discord_webhook, notion_webhook

def route_signal(signal: dict, persona: str):
    """
    Routes a validated signal payload to appropriate outputs.

    Args:
        signal (dict): Parsed signal dictionary from Grok output
        persona (str): Active persona (e.g. "sniper", "novice_plus")
    """

    # Dispatch to Discord
    if os.getenv("DISCORD_WEBHOOK_URL"):
        discord_webhook.send(signal)

    # Dispatch to Notion
    if os.getenv("NOTION_TOKEN") and os.getenv("NOTION_DB_ID"):
        try:
            notion_webhook.send(signal, persona)
        except AttributeError:
            raise NotImplementedError("notion_webhook module must implement a 'send(signal, persona)' method.")

    # Extend with Slack, email, CSV, etc.
