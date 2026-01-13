"""
Lead Post Processor
-------------------
Processes Instagram scraper JSON data and classifies leads based on:
1. Website presence & REAL platform detection (supports custom domains)
2. Phone / WhatsApp availability

Outputs:
- Enriched JSON with sales-ready tags
- Saved into a common output folder
"""

import json
import os
import requests

# -----------------------------
# HTTP config
# -----------------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# -----------------------------
# HTML platform fingerprints
# -----------------------------
HTML_SIGNATURES = {
    "shopify": [
        "cdn.shopify.com",
        "shopify-section",
        "shopify-features",
        "window.shopify"
    ],
    "wix": [
        "wixsite.com",
        "wixstatic.com",
        "wix-dropdown-menu",
        "wix-code"
    ],
    "framer": [
        "framer-motion",
        "data-framer-name",
        "framer-appear"
    ],
    "webflow": [
        "webflow.js",
        "data-wf-page",
        "data-wf-site"
    ],
    "wordpress": [
        "wp-content",
        "wp-includes",
        "wp-emoji-release.min.js"
    ]
}

# -----------------------------
# SORT PRIORITIES (NEW)
# -----------------------------
LEAD_PRIORITY_ORDER = {
    "cost_reduction_potential_client": 0,
    "needs_website_outreach_client": 1,
    "low_priority": 2
}

PLATFORM_PRIORITY_ORDER = {
    "shopify": 0,      # highest priority
    "wix": 1,
    "webflow": 2,
    "framer": 3,
    "wordpress": 4,
    None: 5,
    "custom_coded": 6,
    "custom_coded_or_unknown": 7
}

# -----------------------------
# Platform detection
# -----------------------------
def detect_platform(website_url: str) -> str:
    """
    Detect website platform using HTML fingerprinting.
    Works even on custom domains.
    """
    if not website_url:
        return None

    try:
        response = requests.get(
            website_url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )

        if response.status_code != 200:
            return "custom_coded_or_unknown"

        html = response.text.lower()

        # Meta generator check
        if "name=\"generator\"" in html:
            if "wordpress" in html:
                return "wordpress"
            if "shopify" in html:
                return "shopify"
            if "wix" in html:
                return "wix"

        # Asset / JS fingerprint detection
        for platform, signatures in HTML_SIGNATURES.items():
            for sig in signatures:
                if sig in html:
                    return platform

        return "custom_coded"

    except Exception:
        return "custom_coded_or_unknown"


# -----------------------------
# Lead classification
# -----------------------------
def classify_lead(profile: dict) -> dict:
    website = profile.get("website", "").strip()
    phone = profile.get("phone", "").strip()
    whatsapp = profile.get("whatsapp", "").strip()

    lead_type = None
    platform = None
    tags = []
    pitch_angle = None

    # CASE 1: Website exists → cost reduction pitch
    if website:
        platform = detect_platform(website)
        lead_type = "cost_reduction_potential_client"

        if platform in ["shopify", "wix", "framer", "webflow", "wordpress"]:
            pitch_angle = (
                "Paying monthly for platform & apps → offer custom-coded website to reduce costs"
            )
        else:
            pitch_angle = (
                "Custom site → audit performance, hosting & infra to cut ongoing costs"
            )

        tags.extend([
            "has_website",
            platform,
            "high_intent",
            "cost_cutting_pitch"
        ])

    # CASE 2: No website but contact exists → needs website
    elif phone or whatsapp:
        lead_type = "needs_website_outreach_client"
        pitch_angle = (
            "Instagram-only business → offer website to increase trust & inbound leads"
        )

        tags.extend([
            "no_website",
            "has_contact",
            "website_needed",
            "warm_outreach"
        ])

    # CASE 3: Low intent
    else:
        lead_type = "low_priority"
        pitch_angle = "No website and no direct contact info"
        tags.append("low_intent")

    return {
        **profile,
        "lead_type": lead_type,
        "platform_detected": platform,
        "tags": tags,
        "pitch_angle": pitch_angle
    }


# -----------------------------
# Process JSON
# -----------------------------
def process_json(input_file: str, output_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    processed = []
    stats = {
        "total": 0,
        "cost_reduction_clients": 0,
        "needs_website_clients": 0,
        "low_priority": 0
    }

    for profile in data:
        stats["total"] += 1
        enriched = classify_lead(profile)
        processed.append(enriched)

        if enriched["lead_type"] == "cost_reduction_potential_client":
            stats["cost_reduction_clients"] += 1
        elif enriched["lead_type"] == "needs_website_outreach_client":
            stats["needs_website_clients"] += 1
        else:
            stats["low_priority"] += 1

    # -----------------------------
    # SORT OUTPUT (NEW)
    # -----------------------------
    processed.sort(
        key=lambda p: (
            LEAD_PRIORITY_ORDER.get(p.get("lead_type"), 99),
            PLATFORM_PRIORITY_ORDER.get(p.get("platform_detected"), 99)
        )
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

    print("📊 Summary:")
    for k, v in stats.items():
        print(f"   {k}: {v}")
    print(f"📁 Saved → {output_file}")


# -----------------------------
# Entry point (PROCESS ALL JSON FILES)
# -----------------------------
if __name__ == "__main__":

    BASE_DIR = os.getcwd()
    OUTPUT_DIR = os.path.join(BASE_DIR, "processed_leads")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    json_files = [
        f for f in os.listdir(BASE_DIR)
        if f.endswith(".json") and not f.endswith("_processed.json")
    ]

    if not json_files:
        print("❌ No JSON files found to process.")
        exit(0)

    print(f"\n📂 Found {len(json_files)} JSON files to process:\n")
    for f in json_files:
        print(f"   • {f}")

    for input_file in json_files:
        output_file = os.path.join(
            OUTPUT_DIR,
            input_file.replace(".json", "_processed.json")
        )

        print(f"\n{'='*60}")
        print(f"🚀 Processing: {input_file}")
        print(f"{'='*60}")

        try:
            process_json(input_file, output_file)
        except Exception as e:
            print(f"❌ Failed to process {input_file}: {e}")

    print(f"\n🎉 ALL FILES PROCESSED")
    print(f"📁 All outputs saved in: {OUTPUT_DIR}")