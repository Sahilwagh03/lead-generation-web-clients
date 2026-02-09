import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
BASE_URL = os.getenv("WHATSAPP_BASE_URL")


class WhatsAppService:
    def __init__(self):
        self.url = f"{BASE_URL}/{PHONE_ID}/messages"
        self.headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        }

    # -------------------------
    # Send template message (LEGAL way)
    # -------------------------
    def send_template(self, phone: str, template: str, params: list[str]):
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "template",
            "template": {
                "name": template,
                "language": {"code": "en"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": str(p)} for p in params
                        ],
                    }
                ],
            },
        }

        response = requests.post(self.url, headers=self.headers, json=payload)

        return response.json()
