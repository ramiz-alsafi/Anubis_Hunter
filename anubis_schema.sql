-- ============================================================
-- Anubis v6.3 — PostgreSQL Schema
-- Phase 5: Persistent Database Backend
-- ============================================================

-- Create dedicated database user and database
-- (Run as postgres superuser first, then connect to anubis_db)

-- DROP TABLE IF EXISTS threats CASCADE;
-- DROP TABLE IF EXISTS runs CASCADE;

-- ============================================================
-- RUN TRACKING TABLE
-- Logs every Anubis execution for history and analytics
-- ============================================================
CREATE TABLE IF NOT EXISTS runs (
    id              SERIAL PRIMARY KEY,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at     TIMESTAMPTZ,
    total_threats   INTEGER DEFAULT 0,
    new_threats     INTEGER DEFAULT 0,
    updated_threats INTEGER DEFAULT 0,
    sources_active  INTEGER DEFAULT 0,
    sources_failed  INTEGER DEFAULT 0,
    status          VARCHAR(20) DEFAULT 'running',  -- running | completed | failed
    notes           TEXT
);

-- ============================================================
-- MAIN THREATS TABLE
-- One row per unique threat (upsert on ID)
-- ============================================================
CREATE TABLE IF NOT EXISTS threats (

    -- === IDENTITY ===
    id                  VARCHAR(255) PRIMARY KEY,   -- Anubis unique ID (CVE-xxxx, EXPLOIT-xxx, etc.)
    threat_type         VARCHAR(50),                -- cve, exploit, malware, urlhaus, phish, ip, ioc, news...
    title               TEXT,                       -- Short title / CVE ID / malware name
    description         TEXT,                       -- Full description

    -- === SEVERITY & SCORING ===
    cvss_score          NUMERIC(4,1) DEFAULT 0.0,
    cvss_severity       VARCHAR(20),                -- CRITICAL, HIGH, MEDIUM, LOW
    epss_score          NUMERIC(8,6) DEFAULT 0.0,   -- 0.000000 → 1.000000
    epss_percentile     NUMERIC(8,6) DEFAULT 0.0,
    risk_score          INTEGER DEFAULT 0,          -- Anubis composite risk score (1-9)
    priority            VARCHAR(10),                -- P1, P2, P3, P4
    attackerkb_score    NUMERIC(4,2) DEFAULT 0.0,
    confidence_score    VARCHAR(30),                -- e.g. "HIGH (85%)"

    -- === EXPLOIT & PATCH STATUS ===
    exploit_status      VARCHAR(50) DEFAULT 'NONE', -- NONE, POC, WEAPONIZED, IN_THE_WILD
    fix_available       VARCHAR(50) DEFAULT 'NONE', -- NONE, PATCH, WORKAROUND, VENDOR_ADVISORY
    in_cisa_kev         BOOLEAN DEFAULT FALSE,      -- In CISA Known Exploited Vulnerabilities
    has_msf_module      BOOLEAN DEFAULT FALSE,      -- Has Metasploit exploit module
    zdi_advisory        VARCHAR(255) DEFAULT 'NONE',-- ZDI advisory ID if available

    -- === SOURCE INTELLIGENCE ===
    source              VARCHAR(100),               -- Primary source (nvd, exploit-db, etc.)
    source_count        INTEGER DEFAULT 1,          -- How many sources reported this threat
    intel_url           TEXT DEFAULT 'NONE',        -- Primary reference URL
    news_coverage       TEXT,                       -- Related security news headlines

    -- === MITRE ATT&CK ===
    mitre_techniques    TEXT,                       -- e.g. "T1190,T1059" comma-separated
    mitre_tactics       TEXT,                       -- e.g. "Initial Access,Execution"
    cwe_id              VARCHAR(50),                -- e.g. CWE-79, CWE-89

    -- === AFFECTED PRODUCTS ===
    affected_product    TEXT,                       -- Vendor + product name
    affected_versions   TEXT,                       -- Version range
    vendor              VARCHAR(100),               -- Vendor name (Microsoft, Apache, etc.)

    -- === IOC FIELDS (for IP/URL/hash threats) ===
    ioc_type            VARCHAR(30),                -- ip, url, hash, domain, email
    ioc_value           TEXT,                       -- The actual IOC
    ioc_country         VARCHAR(5),                 -- ISO country code
    ioc_asn             VARCHAR(100),               -- ASN info
    ioc_tags            TEXT,                       -- Comma-separated tags

    -- === DATES ===
    published_at        TIMESTAMPTZ,                -- When the threat was published/disclosed
    patched_at          TIMESTAMPTZ,                -- When patch was released (if known)

    -- === PHASE 6 DASHBOARD METADATA ===
    -- These columns power the future web dashboard
    first_seen_at       TIMESTAMPTZ DEFAULT NOW(),  -- When Anubis first detected this
    last_seen_at        TIMESTAMPTZ DEFAULT NOW(),  -- When Anubis last updated this
    run_count           INTEGER DEFAULT 1,          -- How many Anubis runs have seen this
    is_trending         BOOLEAN DEFAULT FALSE,      -- Flagged as trending (multiple sources + news)
    is_active           BOOLEAN DEFAULT TRUE,       -- Still active / not resolved
    dashboard_tags      TEXT[],                     -- Array of tags for dashboard filtering
    severity_changed    BOOLEAN DEFAULT FALSE,      -- CVSS/priority changed since first seen
    last_run_id         INTEGER REFERENCES runs(id),-- Which run last touched this record

    -- === RAW DATA ===
    raw_data            JSONB,                      -- Full raw threat dict for future use

    -- === AUDIT ===
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- INDEXES — optimized for Phase 6 dashboard queries
-- ============================================================

-- Priority filtering (most common dashboard query)
CREATE INDEX IF NOT EXISTS idx_threats_priority
    ON threats (priority);

-- Severity filtering
CREATE INDEX IF NOT EXISTS idx_threats_cvss_severity
    ON threats (cvss_severity);

-- Type filtering
CREATE INDEX IF NOT EXISTS idx_threats_type
    ON threats (threat_type);

-- CISA KEV flag (critical threats dashboard)
CREATE INDEX IF NOT EXISTS idx_threats_kev
    ON threats (in_cisa_kev) WHERE in_cisa_kev = TRUE;

-- MSF module flag
CREATE INDEX IF NOT EXISTS idx_threats_msf
    ON threats (has_msf_module) WHERE has_msf_module = TRUE;

-- Time-based queries (trending, historical)
CREATE INDEX IF NOT EXISTS idx_threats_first_seen
    ON threats (first_seen_at DESC);

CREATE INDEX IF NOT EXISTS idx_threats_last_seen
    ON threats (last_seen_at DESC);

-- EPSS score range queries
CREATE INDEX IF NOT EXISTS idx_threats_epss
    ON threats (epss_score DESC);

-- Risk score range queries
CREATE INDEX IF NOT EXISTS idx_threats_risk
    ON threats (risk_score DESC);

-- Source filtering
CREATE INDEX IF NOT EXISTS idx_threats_source
    ON threats (source);

-- Trending flag
CREATE INDEX IF NOT EXISTS idx_threats_trending
    ON threats (is_trending) WHERE is_trending = TRUE;

-- Full-text search on title + description
CREATE INDEX IF NOT EXISTS idx_threats_fts
    ON threats USING GIN (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(description,'')));

-- JSONB raw data queries
CREATE INDEX IF NOT EXISTS idx_threats_raw
    ON threats USING GIN (raw_data);

-- ============================================================
-- AUTO-UPDATE updated_at TRIGGER
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS threats_updated_at ON threats;
CREATE TRIGGER threats_updated_at
    BEFORE UPDATE ON threats
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- USEFUL VIEWS FOR PHASE 6 DASHBOARD
-- ============================================================

-- Critical threats view (P1 + P2 only)
CREATE OR REPLACE VIEW critical_threats AS
SELECT * FROM threats
WHERE priority IN ('P1', 'P2')
  AND is_active = TRUE
ORDER BY risk_score DESC, epss_score DESC;

-- KEV threats view
CREATE OR REPLACE VIEW kev_threats AS
SELECT * FROM threats
WHERE in_cisa_kev = TRUE
  AND is_active = TRUE
ORDER BY cvss_score DESC;

-- Trending threats view
CREATE OR REPLACE VIEW trending_threats AS
SELECT * FROM threats
WHERE is_trending = TRUE
  AND is_active = TRUE
ORDER BY last_seen_at DESC;

-- Threat summary stats (for dashboard counters)
CREATE OR REPLACE VIEW threat_stats AS
SELECT
    COUNT(*)                                            AS total_threats,
    COUNT(*) FILTER (WHERE priority = 'P1')             AS p1_count,
    COUNT(*) FILTER (WHERE priority = 'P2')             AS p2_count,
    COUNT(*) FILTER (WHERE in_cisa_kev = TRUE)          AS kev_count,
    COUNT(*) FILTER (WHERE has_msf_module = TRUE)       AS msf_count,
    COUNT(*) FILTER (WHERE is_trending = TRUE)          AS trending_count,
    COUNT(*) FILTER (WHERE epss_score >= 0.5)           AS high_epss_count,
    COUNT(*) FILTER (WHERE exploit_status = 'IN_THE_WILD') AS in_wild_count,
    COUNT(*) FILTER (WHERE first_seen_at >= NOW() - INTERVAL '24 hours') AS new_24h,
    COUNT(*) FILTER (WHERE first_seen_at >= NOW() - INTERVAL '7 days')   AS new_7d,
    ROUND(AVG(cvss_score)::numeric, 2)                  AS avg_cvss,
    ROUND(AVG(epss_score)::numeric, 4)                  AS avg_epss,
    MAX(last_seen_at)                                   AS last_updated
FROM threats
WHERE is_active = TRUE;

-- ============================================================
-- DONE
-- ============================================================
\echo 'Anubis schema created successfully'
\echo 'Tables: threats, runs'
\echo 'Views:  critical_threats, kev_threats, trending_threats, threat_stats'
