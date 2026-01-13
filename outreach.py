"""
Lead Outreach AI Generator (Ollama Python SDK)
---------------------------------------------
Reads ALL processed lead JSON files and generates
human-like outreach messages using Qwen 2.5 : 3B

Flow:
processed_leads/*.json → Analysis print → Ollama → AI message
"""

import json
import os
import sys
import ollama

# -----------------------------
# CONFIG
# -----------------------------
MODEL_NAME = "qwen2.5:3b"
PROCESSED_DIR = "processed_leads"
SAVE_OUTPUT = True
OUTPUT_FILE = "ai_outreach_messages.json"


# -----------------------------
# Ollama health check
# -----------------------------
def check_ollama():
    try:
        ollama.list()
    except Exception:
        print("❌ Ollama is not running or not installed.")
        print("👉 Start it using: ollama serve")
        sys.exit(1)


# -----------------------------
# Outreach channel decision
# -----------------------------
def decide_outreach_channel(profile):
    if profile.get("email"):
        return "email"
    if profile.get("whatsapp"):
        return "whatsapp"
    if profile.get("phone"):
        return "phone"
    return "instagram_dm"


# -----------------------------
# Prompt builder (LEAD-TYPE AWARE)
# -----------------------------
def build_prompt(profile, channel):
    lead_type = profile.get("lead_type")

    if lead_type == "cost_reduction_potential_client":
        pitch = (
            "Offer reducing their website running cost to around Rs.600/month by redesigning "
            "their site with a new brand identity, improved UI/UX, and adding AI-based order "
            "management to reduce manual work."
        )

    else:  # needs website + low priority
        pitch = (
            "Offer a complete website to digitize their business, help them get more orders, "
            "build a strong brand identity with high-quality UI/UX, and include an AI system "
            "that handles customer communication and order management automatically."
        )

    return f"""
You are a professional sales copywriter.

Write a short, friendly, non-pushy outreach message.

Business details:
- Instagram username: @{profile.get("username")}
- Lead type: {lead_type}
- Website platform: {profile.get("platform_detected")}
- Outreach channel: {channel}

Pitch to use:
{pitch}

Rules:
- Max 3 short sentences
- No emojis
- No marketing buzzwords
- Sound human and confident
- Do not mention scraping, data collection, or automation
- Do not sound like a sales ad

Message:
""".strip()


# -----------------------------
# Generate message via Ollama SDK
# -----------------------------
def generate_message(prompt):
    try:
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                "temperature": 0.4,
                "top_p": 0.9
            }
        )
        return response["response"].strip()
    except Exception as e:
        return f"⚠️ Generation failed: {e}"


# -----------------------------
# Load ALL processed lead files
# -----------------------------
def load_all_processed_leads():
    all_leads = []

    if not os.path.exists(PROCESSED_DIR):
        print(f"❌ Directory not found: {PROCESSED_DIR}")
        return all_leads

    files = [
        f for f in os.listdir(PROCESSED_DIR)
        if f.endswith("_processed.json")
    ]

    if not files:
        print("❌ No processed JSON files found.")
        return all_leads

    print(f"\n📂 Found {len(files)} processed files:\n")
    for f in files:
        print(f"   • {f}")

    for file in files:
        path = os.path.join(PROCESSED_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            all_leads.extend(json.load(f))

    return all_leads


# -----------------------------
# Main execution
# -----------------------------
def main():
    print("🔍 Checking Ollama...")
    check_ollama()

    leads = load_all_processed_leads()
    if not leads:
        return

    print(f"\n🚀 Generating outreach messages for {len(leads)} leads\n")

    output_data = []

    for idx, lead in enumerate(leads, start=1):
        channel = decide_outreach_channel(lead)

        # ---- PRINT ANALYSIS FIRST ----
        print("\n" + "=" * 60)
        print(f"{idx}. ANALYSIS")
        print(f"   Username      : @{lead.get('username')}")
        print(f"   Lead Type     : {lead.get('lead_type')}")
        print(f"   Platform      : {lead.get('platform_detected')}")
        print(f"   Contact Via   : {channel.upper()}")


        prompt = build_prompt(lead, channel)
        message = generate_message(prompt)

        record = {
            "username": lead.get("username"),
            "lead_type": lead.get("lead_type"),
            "platform": lead.get("platform_detected"),
            "contact_channel": channel,
            "generated_message": message
        }

        output_data.append(record)

    if SAVE_OUTPUT:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"\n📁 Saved AI messages → {OUTPUT_FILE}")

    print("\n🎉 OUTREACH GENERATION COMPLETE")


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    main()