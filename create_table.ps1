# =============================================
# Docker Postgres Table Setup Script (FINAL)
# =============================================

$CONTAINER = "leads_postgres"
$DB = "leads_db"
$USER = "admin"

$sql = @'
-- =========================
-- 1. ENUM TYPE
-- =========================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'lead_status_enum') THEN
        CREATE TYPE lead_status_enum AS ENUM (
            'NEW',
            'CONTACTED',
            'REMINDER',
            'RETARGET',
            'INTERESTED',
            'MEETING',
            'NEGOTIATION',
            'ACCEPTED',
            'REJECTED',
            'INVALID',
            'BLOCKED'
        );
    END IF;
END
$$;


-- =========================
-- 2. USERS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- 3. SCRAPING BATCHES
-- (added user reference)
-- =========================
CREATE TABLE IF NOT EXISTS scraping_batches (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    hashtag VARCHAR(100) NOT NULL,
    lead_count INTEGER DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- 4. LEADS
-- (added user_id + profile_url + username)
-- =========================
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    batch_id INTEGER NOT NULL,

    original_id BIGINT,

    followers INTEGER DEFAULT 0,
    following INTEGER DEFAULT 0,
    posts INTEGER DEFAULT 0,

    bio TEXT,
    website TEXT,

    email VARCHAR(255),
    phone VARCHAR(50),
    whatsapp TEXT,

    is_verified BOOLEAN DEFAULT FALSE,
    is_business BOOLEAN DEFAULT FALSE,

    category TEXT,
    full_name TEXT,

    lead_type TEXT,
    platform_detected VARCHAR(100),

    website_phones JSONB DEFAULT '[]'::jsonb,
    tags JSONB DEFAULT '[]'::jsonb,

    pitch_angle TEXT,

    -- NEW FIELDS (missing earlier)
    profile_url TEXT DEFAULT '',
    username TEXT DEFAULT '',

    status lead_status_enum DEFAULT 'NEW',

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMPTZ,

    CONSTRAINT fk_leads_batch
        FOREIGN KEY (batch_id)
        REFERENCES scraping_batches(id)
        ON DELETE CASCADE
);


-- =========================
-- 5. INDEXES
-- =========================
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE INDEX IF NOT EXISTS idx_batches_user_id ON scraping_batches(user_id);

CREATE INDEX IF NOT EXISTS idx_leads_user_id ON leads(user_id);
CREATE INDEX IF NOT EXISTS idx_leads_batch_id ON leads(batch_id);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_original_id ON leads(original_id);


-- =========================
-- 6. NOTIFICATIONS
-- =========================
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(30) DEFAULT 'SUMMARY',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_notifications_user_read
ON notifications(user_id, is_read);
'@


docker exec -i $CONTAINER psql `
    -U $USER `
    -d $DB `
    -v ON_ERROR_STOP=1 `
    -c "$sql"

Write-Host "✅ Tables & indexes created successfully"
