from app.db.database import get_db_connection

def get_all_leads(
    limit: int = 50,
    offset: int = 0,
    is_verified: bool | None = None,
    is_business: bool | None = None
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM leads WHERE 1=1"
    params = []

    if is_verified is not None:
        query += " AND is_verified = ?"
        params.append(1 if is_verified else 0)

    if is_business is not None:
        query += " AND is_business = ?"
        params.append(1 if is_business else 0)

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]