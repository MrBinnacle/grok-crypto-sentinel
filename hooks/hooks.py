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
        try:
            discord_webhook.send(signal, persona)
        except Exception as e:
            print(f"Discord webhook failed: {e}")

    # Dispatch to Notion
    if os.getenv("NOTION_TOKEN") and os.getenv("NOTION_DB_ID"):
        try:
            notion_webhook.send(signal, persona)
        except (ImportError, ModuleNotFoundError) as e:
            raise ImportError("notion_webhook module or its 'send' method is missing.") from e
        except AttributeError as e:
            raise AttributeError("notion_webhook module must implement a 'send(signal, persona)' method.") from e

    # TODO: Add Slack, email, CSV integrations
