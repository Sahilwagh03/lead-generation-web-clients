import json
import os
from cerebras.cloud.sdk import Cerebras

def init_cerebras():
    api_key = os.getenv("CEREBRAS_API_KEY")
    if not api_key:
        print("⚠️ Cerebras API key not found")
        return None
    client = Cerebras(
        api_key=api_key,
    )
    return client

def process_with_cerebras(content, username, cerebras_client):
    if not cerebras_client:
        return None

    prompt = f"""
    Extract Instagram profile information from the text below.

    Rules:
    - Followers / Following / Posts are numbers
    - Bio is all descriptive text
    - Website must be a real business website
    - Ignore Threads and Instagram internal links
    - ONLY extract actual business websites (company websites, e-commerce stores, landing pages, portfolios)
    - EXCLUDE all social media links like: Facebook, Twitter/X, LinkedIn, TikTok, YouTube, Pinterest, Snapchat, Telegram, etc.
    - INCLUDE WhatsApp links/numbers separately in the "whatsapp" field, NOT in website
    - If multiple URLs exist, prioritize the main business website
    - Common website patterns: company.com, mybrand.com, shop.example.com, www.business.co

    TEXT:
    {content}

    Return ONLY valid JSON:
    {{
    "followers_count": number or null,
    "following_count": number or null,
    "posts_count": number or null,
    "bio": string or null,
    "website": string or null,
    "email": string or null,
    "phone": string or null,
    "whatsapp": string or null,
    "is_verified": boolean,
    "is_business": boolean,
    "category": string or null,
    "full_name": string or null
    }}
    """.strip()
    
    try:
        print(f"  🤖 Cerebras processing @{username}...")
        response = cerebras_client.completions.create(
            prompt=prompt,
            model="qwen-3-32b",
            max_tokens=10000,
            temperature=0.0,
        )
        return json.loads(response.choices[0].text)
    except Exception as e:
        print(f"  ⚠️ Cerebras failed for @{username}: {e}")
        return None
