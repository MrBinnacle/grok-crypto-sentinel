import requests
from datetime import datetime

headers = {
    "Authorization": "Bearer YOUR_NOTION_SECRET",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

payload = {
    "parent": { "database_id": "YOUR_DB_ID" },
    "properties": {
        "Date": { "date": { "start": datetime.utcnow().isoformat() } },
        "Signal": { "title": [{ "text": { "content": "Breakout Watch Triggered" } }] },
        "Action": { "rich_text": [{ "text": { "content": "Posture: Watch" } }] }
    }
}

requests.post("https://api.notion.com/v1/pages", json=payload, headers=headers)
