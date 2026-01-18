import json
import os
import re
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
load_dotenv()

def init_cerebras():
    api_key = os.getenv("CEREBRAS_API_KEY")
    if not api_key:
        print("⚠️ Cerebras API key not found")
        return None
    client = Cerebras(
        api_key=api_key,
    )
    return client

def validate_and_clean_json(raw_response):
    """
    Extracts and returns clean JSON from LLM response.
    Does NOT validate fields - just returns properly formatted JSON.
    
    Args:
        raw_response: Raw text response from Cerebras
        
    Returns:
        dict: Cleaned JSON object or None if parsing fails
    """
    if not raw_response:
        return None
    
    try:
        # Remove end-of-sequence tokens like <|im_end|>
        cleaned = re.sub(r'<\|im_end\|>.*$', '', raw_response)
        cleaned = re.sub(r'<\|.*?\|>', '', cleaned)
        
        # Remove markdown code blocks
        cleaned = re.sub(r'```json\s*', '', cleaned)
        cleaned = re.sub(r'```\s*', '', cleaned)
        
        # Extract JSON object (everything between first { and last })
        # This handles cases where LLM adds text before/after JSON
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned, re.DOTALL)
        
        if not json_match:
            print(f"  ⚠️ No JSON object found in response")
            return None
        
        json_str = json_match.group(0)
        
        # Parse and return JSON
        data = json.loads(json_str)
        return data
        
    except json.JSONDecodeError as e:
        print(f"  ⚠️ JSON parsing error: {e}")
        print(f"  Raw response: {raw_response[:300]}...")
        return None
    except Exception as e:
        print(f"  ⚠️ Unexpected error: {e}")
        return None

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
            max_tokens=1000,
            temperature=0.0,
        )
        raw_text = response.choices[0].text
        validated_json = validate_and_clean_json(raw_text)
        
        if validated_json:
            print(f"  ✅ Successfully parsed profile for @{username}")
            return validated_json
        else:
            print(f"  ❌ Failed to validate JSON for @{username}")
            return None
        
    except Exception as e:
        print(f"  ⚠️ Cerebras failed for @{username}: {e}")
        return None