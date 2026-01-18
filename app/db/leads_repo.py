from app.db.database import get_db_connection

from app.db.database import get_db_connection

def save_leads(leads: list):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO leads (
            followers,
            following,
            posts,
            bio,
            website,
            email,
            phone,
            whatsapp,
            is_verified,
            is_business,
            category,
            full_name
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            lead.get("followers"),
            lead.get("following"),
            lead.get("posts"),
            lead.get("bio"),
            lead.get("website"),
            lead.get("email"),
            lead.get("phone"),
            lead.get("whatsapp"),
            int(lead.get("is_verified", False)),
            int(lead.get("is_business", False)),
            lead.get("category"),
            lead.get("full_name"),
        )
        for lead in leads
    ])

    conn.commit()
    conn.close()

def normalize_lead(lead: dict) -> dict:
    return {
        "followers": lead.get("followers") or lead.get("followers_count"),
        "following": lead.get("following") or lead.get("following_count"),
        "posts": lead.get("posts") or lead.get("posts_count"),

        "bio": lead.get("bio"),
        "website": lead.get("website"),
        "email": lead.get("email"),
        "phone": lead.get("phone"),
        "whatsapp": lead.get("whatsapp"),

        "is_verified": lead.get("is_verified", lead.get("isVerified", False)),
        "is_business": lead.get("is_business", lead.get("isBusiness", False)),

        "category": lead.get("category"),
        "full_name": lead.get("full_name") or lead.get("fullName"),
    }
