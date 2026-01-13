import google.generativeai as genai
import os
import json

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ Gemini API key not found")
        return None

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        generation_config={
            "temperature": 0.0,
            "response_mime_type": "application/json"
        }
    )

def process_with_gemini(content, username, gemini_model):
    if not gemini_model:
        return None

    prompt = f"""
Extract Instagram profile information from the text below.

Rules:
- Followers / Following / Posts are numbers
- Bio is descriptive text
- Website must be a real business website
- Ignore social media links
- WhatsApp must be extracted separately

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
        print(f"  🤖 Gemini processing @{username}...")
        response = gemini_model.generate_content(prompt)
        return json.loads(response.text)

    except Exception as e:
        print(f"  ⚠️ Gemini failed for @{username}: {e}")
        return None
