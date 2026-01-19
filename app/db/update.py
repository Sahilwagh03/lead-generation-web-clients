from database import get_db_connection

def backfill_created_at():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE leads
        SET created_at = datetime('now')
        WHERE created_at IS NULL
    """)

    conn.commit()
    conn.close()
    print("✅ created_at updated with current date for old leads")

backfill_created_at()