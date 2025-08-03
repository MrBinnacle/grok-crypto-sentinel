import os
import requests
import json
from datetime import datetime


def send(signal, persona):
    """
    Sends a signal to Notion.

    Args:
        signal (dict): Signal dictionary containing title and posture.
        persona (str): Active persona.

    Raises:
        ValueError: If NOTION_TOKEN environment variable is not set.
    """

    # Get Notion token and database ID from environment variables
    notion_token = os.getenv("NOTION_TOKEN")
    notion_db_id = os.getenv("NOTION_DB_ID")

    # Check if required environment variables are set
    if notion_token is None:
        raise ValueError("NOTION_TOKEN environment variable is not set")
    if notion_db_id is None:
        raise ValueError("NOTION_DB_ID environment variable is not set")

    # Set up headers and payload
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    payload = {
        "parent": {"database_id": notion_db_id},
        "properties": {
            "Date": {"date": {"start": datetime.utcnow().isoformat()}},
            "Signal": {"title": [{"text": {"content": signal["title"]}}]},
            "Action": {"rich_text": [{"text": {"content": signal["posture"]}}]},
        },
    }

    # Send request to Notion API
    url = "https://api.notion.com/v1/pages"
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Notion webhook failed: {e}") from e
