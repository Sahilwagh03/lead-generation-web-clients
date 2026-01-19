from datetime import datetime, timezone
from app.db.database import get_db_connection

def save_leads(leads: list):
    conn = get_db_connection()
    cursor = conn.cursor()

    now = datetime.now(timezone.utc).isoformat()

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
            full_name,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            now
        )
        for lead in leads
    ])

    conn.commit()
    conn.close()
