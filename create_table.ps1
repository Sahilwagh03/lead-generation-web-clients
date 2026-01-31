# PowerShell script to create tables in Docker Postgres

$CONTAINER = "leads_postgres"
$DB = "leads_db"
$USER = "admin"

$sql = @"
-- Table 1: Scraping batches
CREATE TABLE IF NOT EXISTS scraping_batches (
    id SERIAL PRIMARY KEY,
    hashtag VARCHAR(100) NOT NULL,
    lead_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Leads
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    batch_id INTEGER NOT NULL,
    
    original_id BIGINT,
    followers INTEGER DEFAULT 0,
    following INTEGER DEFAULT 0,
    posts INTEGER DEFAULT 0,
    bio TEXT,
    website VARCHAR(500),
    email VARCHAR(255),
    phone VARCHAR(50),
    whatsapp VARCHAR(50),
    is_verified BOOLEAN DEFAULT FALSE,
    is_business BOOLEAN DEFAULT FALSE,
    category VARCHAR(100),
    full_name VARCHAR(255),
    
    lead_type VARCHAR(50),
    platform_detected VARCHAR(50),
    website_phones JSONB DEFAULT '[]'::jsonb,
    tags JSONB DEFAULT '[]'::jsonb,
    pitch_angle TEXT,
    
    status VARCHAR(20) DEFAULT 'scraped',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMPTZ,
    
    CONSTRAINT fk_leads_batch
        FOREIGN KEY (batch_id)
        REFERENCES scraping_batches(id)
        ON DELETE CASCADE
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_leads_batch_id ON leads(batch_id);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_original_id ON leads(original_id);
"@

# Execute SQL inside Docker container
docker exec -i $CONTAINER psql `
    -U $USER `
    -d $DB `
    -v ON_ERROR_STOP=1 `
    -c "$sql"

Write-Host "✅ Tables & indexes created successfully"
