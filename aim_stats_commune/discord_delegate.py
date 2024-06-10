import requests
import os

from dotenv import load_dotenv


load_dotenv()
webhook_id = os.getenv("WEBHOOK_ID")
webhook_token = os.getenv("WEBHOOK_TOKEN")
webhook_url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"


def send_message(message: str):
    payload = {
        "content": message,
        "username": "AIM stats commune"
    }

    print(message)
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(f"Response: {response.text}")
