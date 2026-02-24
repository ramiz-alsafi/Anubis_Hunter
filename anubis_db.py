"""
anubis_db.py — PostgreSQL Integration Module
Anubis v6.3 Phase 5: Persistent Database Backend
By Ramiz Alsafi

Drop this file in ~/Anubis/ alongside the main script.
Add two lines to Anubis_hunter_v6_3.py to activate (see bottom of this file).
"""

import os
import json
import psycopg2
import psycopg2.extras
from datetime import datetime
from typing import Optional

# ============================================================
# DATABASE CONNECTION CONFIG
# Set as environment variables or edit defaults below
# ============================================================
DB_HOST     = os.environ.get("ANUBIS_DB_HOST",     "localhost")
DB_PORT     = int(os.environ.get("ANUBIS_DB_PORT", "5432"))
DB_NAME     = os.environ.get("ANUBIS_DB_NAME",     "anubis_db")
DB_USER     = os.environ.get("ANUBIS_DB_USER",     "anubis")
DB_PASSWORD = os.environ.get("ANUBIS_DB_PASS",     "anubis_pass")  # change this!

# ============================================================
# CONNECTION MANAGEMENT
# ============================================================
_conn = None

def get_connection():
    """Get (or create) a persistent DB connection."""
    global _conn
    try:
        if _conn is None or _conn.closed:
            _conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=10,
            )
            _conn.autocommit = False
            print(f"✓ Connected to PostgreSQL: {DB_NAME}@{DB_HOST}")
    except Exception as e:
        print(f"✗ DB connection failed: {e}")
        _conn = None
    return _conn


def close_connection():
    """Close the DB connection cleanly."""
    global _conn
    if _conn and not _conn.closed:
        _conn.close()
        _conn = None


def test_connection():
    """Quick connectivity test — returns True if DB is reachable."""
    try:
        conn = get_connection()
        if conn is None:
            return False
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
        print("✓ PostgreSQL connection test passed")
        return True
    except Exception as e:
        print(f"✗ PostgreSQL connection test failed: {e}")
        return False


# ============================================================
# RUN TRACKING
# ============================================================
def start_run() -> Optional[int]:
    """Log the start of an Anubis run. Returns run_id."""
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO runs (started_at, status) VALUES (NOW(), 'running') RETURNING id"
            )
            run_id = cur.fetchone()[0]
            conn.commit()
            print(f"✓ DB run started (run_id={run_id})")
            return run_id
    except Exception as e:
        print(f"✗ Failed to start run log: {e}")
        conn.rollback()
        return None


def finish_run(run_id: int, total: int, new: int, updated: int,
               sources_active: int = 0, sources_failed: int = 0,
               status: str = 'completed'):
    """Log the completion of an Anubis run."""
    conn = get_connection()
    if not conn or not run_id:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE runs SET
                    finished_at     = NOW(),
                    total_threats   = %s,
                    new_threats     = %s,
                    updated_threats = %s,
                    sources_active  = %s,
                    sources_failed  = %s,
                    status          = %s
                WHERE id = %s
            """, (total, new, updated, sources_active, sources_failed, status, run_id))
            conn.commit()
            print(f"✓ DB run finished (run_id={run_id}, new={new}, updated={updated})")
    except Exception as e:
        print(f"✗ Failed to finish run log: {e}")
        conn.rollback()


# ============================================================
# THREAT FIELD MAPPING
# Maps Anubis threat dict keys → DB column names
# ============================================================
def _map_threat(t: dict, run_id: Optional[int] = None) -> dict:
    """
    Convert an Anubis threat dictionary to a DB-ready dict.
    Handles missing keys gracefully — every field has a safe default.
    """
    def safe_float(val, default=0.0):
        try:
            return float(val) if val not in (None, '', 'N/A', 'NONE') else default
        except (ValueError, TypeError):
            return default

    def safe_int(val, default=0):
        try:
            return int(val) if val not in (None, '', 'N/A', 'NONE') else default
        except (ValueError, TypeError):
            return default

    def safe_bool(val):
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.strip().upper() in ('TRUE', 'YES', '1', 'ACTIVE', 'CONFIRMED')
        return bool(val) if val else False

    def safe_str(val, default=''):
        if val is None:
            return default
        s = str(val).strip()
        return s if s not in ('None', 'nan', 'NaN', 'N/A') else default

    # --- Extract MITRE fields ---
    mitre_raw = t.get('MITRE_Techniques') or t.get('mitre_techniques') or ''
    mitre_techniques = safe_str(mitre_raw)
    mitre_tactics    = safe_str(t.get('MITRE_Tactics') or t.get('mitre_tactics') or '')

    # --- Determine is_trending ---
    source_count  = safe_int(t.get('Source_Count') or t.get('source_count'), 1)
    news_coverage = safe_str(t.get('News_Coverage') or t.get('news_coverage'))
    epss_score    = safe_float(t.get('EPSS_Score') or t.get('epss_score'))
    in_kev        = safe_bool(t.get('CISA_KEV') or t.get('in_cisa_kev'))
    is_trending   = (source_count >= 3) or (news_coverage != '') or (epss_score >= 0.3) or in_kev

    # --- Dashboard tags array ---
    tags = []
    priority = safe_str(t.get('Priority') or t.get('priority'))
    if priority in ('P1', 'P2'):
        tags.append('critical')
    if in_kev:
        tags.append('kev')
    if safe_bool(t.get('MSF_Module') or t.get('has_msf_module')):
        tags.append('exploitable')
    if epss_score >= 0.5:
        tags.append('high-epss')
    exploit_status = safe_str(t.get('Exploit_Status') or t.get('exploit_status'), 'NONE').upper()
    if exploit_status == 'IN_THE_WILD':
        tags.append('in-the-wild')
    if news_coverage:
        tags.append('in-news')

    # --- Parse published date ---
    published_at = None
    for date_field in ('Published', 'published_at', 'Date', 'date'):
        raw_date = t.get(date_field)
        if raw_date and str(raw_date) not in ('', 'None', 'nan', 'N/A'):
            try:
                if isinstance(raw_date, datetime):
                    published_at = raw_date
                else:
                    published_at = datetime.fromisoformat(str(raw_date).replace('Z', '+00:00'))
                break
            except Exception:
                pass

    return {
        'id':               safe_str(t.get('ID') or t.get('id')),
        'threat_type':      safe_str(t.get('Type') or t.get('threat_type')),
        'title':            safe_str(t.get('Title') or t.get('CVE_ID') or t.get('ID') or t.get('id')),
        'description':      safe_str(t.get('Description') or t.get('description')),
        'cvss_score':       safe_float(t.get('CVSS_Score') or t.get('cvss_score')),
        'cvss_severity':    safe_str(t.get('Severity') or t.get('cvss_severity')),
        'epss_score':       epss_score,
        'epss_percentile':  safe_float(t.get('EPSS_Percentile') or t.get('epss_percentile')),
        'risk_score':       safe_int(t.get('Risk_Score') or t.get('risk_score')),
        'priority':         priority,
        'attackerkb_score': safe_float(t.get('AttackerKB_Score') or t.get('attackerkb_score')),
        'confidence_score': safe_str(t.get('Confidence_Score') or t.get('confidence_score')),
        'exploit_status':   exploit_status,
        'fix_available':    safe_str(t.get('Fix_Available') or t.get('fix_available'), 'NONE'),
        'in_cisa_kev':      in_kev,
        'has_msf_module':   safe_bool(t.get('MSF_Module') or t.get('has_msf_module')),
        'zdi_advisory':     safe_str(t.get('ZDI_Advisory') or t.get('zdi_advisory'), 'NONE'),
        'source':           safe_str(t.get('Source') or t.get('source')),
        'source_count':     source_count,
        'intel_url':        safe_str(t.get('Intel_URL') or t.get('intel_url'), 'NONE'),
        'news_coverage':    news_coverage,
        'mitre_techniques': mitre_techniques,
        'mitre_tactics':    mitre_tactics,
        'cwe_id':           safe_str(t.get('CWE') or t.get('cwe_id')),
        'affected_product': safe_str(t.get('Affected_Product') or t.get('affected_product')),
        'affected_versions':safe_str(t.get('Affected_Versions') or t.get('affected_versions')),
        'vendor':           safe_str(t.get('Vendor') or t.get('vendor')),
        'ioc_type':         safe_str(t.get('IOC_Type') or t.get('ioc_type')),
        'ioc_value':        safe_str(t.get('IOC_Value') or t.get('ioc_value')),
        'ioc_country':      safe_str(t.get('Country') or t.get('ioc_country')),
        'ioc_asn':          safe_str(t.get('ASN') or t.get('ioc_asn')),
        'ioc_tags':         safe_str(t.get('Tags') or t.get('ioc_tags')),
        'published_at':     published_at,
        'is_trending':      is_trending,
        'is_active':        True,
        'dashboard_tags':   tags,
        'last_run_id':      run_id,
        'raw_data':         json.dumps(t, default=str),
    }


# ============================================================
# CORE UPSERT — the heart of Phase 5
# ============================================================
UPSERT_SQL = """
INSERT INTO threats (
    id, threat_type, title, description,
    cvss_score, cvss_severity, epss_score, epss_percentile,
    risk_score, priority, attackerkb_score, confidence_score,
    exploit_status, fix_available, in_cisa_kev, has_msf_module, zdi_advisory,
    source, source_count, intel_url, news_coverage,
    mitre_techniques, mitre_tactics, cwe_id,
    affected_product, affected_versions, vendor,
    ioc_type, ioc_value, ioc_country, ioc_asn, ioc_tags,
    published_at, is_trending, is_active, dashboard_tags, last_run_id, raw_data,
    first_seen_at, last_seen_at, run_count
)
VALUES (
    %(id)s, %(threat_type)s, %(title)s, %(description)s,
    %(cvss_score)s, %(cvss_severity)s, %(epss_score)s, %(epss_percentile)s,
    %(risk_score)s, %(priority)s, %(attackerkb_score)s, %(confidence_score)s,
    %(exploit_status)s, %(fix_available)s, %(in_cisa_kev)s, %(has_msf_module)s, %(zdi_advisory)s,
    %(source)s, %(source_count)s, %(intel_url)s, %(news_coverage)s,
    %(mitre_techniques)s, %(mitre_tactics)s, %(cwe_id)s,
    %(affected_product)s, %(affected_versions)s, %(vendor)s,
    %(ioc_type)s, %(ioc_value)s, %(ioc_country)s, %(ioc_asn)s, %(ioc_tags)s,
    %(published_at)s, %(is_trending)s, %(is_active)s, %(dashboard_tags)s, %(last_run_id)s,
    %(raw_data)s,
    NOW(), NOW(), 1
)
ON CONFLICT (id) DO UPDATE SET
    -- Always update these (may improve each run)
    cvss_score          = EXCLUDED.cvss_score,
    cvss_severity       = EXCLUDED.cvss_severity,
    epss_score          = EXCLUDED.epss_score,
    epss_percentile     = EXCLUDED.epss_percentile,
    risk_score          = EXCLUDED.risk_score,
    priority            = EXCLUDED.priority,
    attackerkb_score    = EXCLUDED.attackerkb_score,
    confidence_score    = EXCLUDED.confidence_score,
    exploit_status      = EXCLUDED.exploit_status,
    fix_available       = EXCLUDED.fix_available,
    in_cisa_kev         = EXCLUDED.in_cisa_kev,
    has_msf_module      = EXCLUDED.has_msf_module,
    zdi_advisory        = EXCLUDED.zdi_advisory,
    source_count        = GREATEST(threats.source_count, EXCLUDED.source_count),
    intel_url           = EXCLUDED.intel_url,
    news_coverage       = EXCLUDED.news_coverage,
    mitre_techniques    = EXCLUDED.mitre_techniques,
    mitre_tactics       = EXCLUDED.mitre_tactics,
    is_trending         = EXCLUDED.is_trending,
    is_active           = TRUE,
    dashboard_tags      = EXCLUDED.dashboard_tags,
    last_run_id         = EXCLUDED.last_run_id,
    raw_data            = EXCLUDED.raw_data,
    -- Track if severity changed since first seen
    severity_changed    = (threats.cvss_severity IS DISTINCT FROM EXCLUDED.cvss_severity),
    -- Increment run counter and update last seen
    last_seen_at        = NOW(),
    run_count           = threats.run_count + 1,
    updated_at          = NOW()
"""


def save_threats(threats: list, run_id: Optional[int] = None) -> tuple[int, int]:
    """
    Upsert a list of threat dicts into PostgreSQL.
    Returns (new_count, updated_count).
    """
    conn = get_connection()
    if not conn:
        print("✗ DB unavailable — skipping database write")
        return 0, 0

    if not threats:
        print("⚠️  No threats to save")
        return 0, 0

    new_count     = 0
    updated_count = 0
    errors        = 0
    batch_size    = 500

    print(f"\n💾 Saving {len(threats)} threats to PostgreSQL...")

    try:
        with conn.cursor() as cur:
            # Get existing IDs for counting new vs updated
            ids = [str(t.get('ID') or t.get('id') or '') for t in threats]
            ids = [i for i in ids if i]  # filter empty

            cur.execute(
                "SELECT id FROM threats WHERE id = ANY(%s)",
                (ids,)
            )
            existing_ids = {row[0] for row in cur.fetchall()}

        # Process in batches
        for i in range(0, len(threats), batch_size):
            batch = threats[i:i + batch_size]
            mapped = []
            for t in batch:
                try:
                    m = _map_threat(t, run_id)
                    if m['id']:  # skip threats with no ID
                        mapped.append(m)
                        if m['id'] in existing_ids:
                            updated_count += 1
                        else:
                            new_count += 1
                except Exception as e:
                    errors += 1
                    if errors <= 3:  # only log first few
                        print(f"  ⚠️  Mapping error for threat: {e}")

            if mapped:
                try:
                    with conn.cursor() as cur:
                        psycopg2.extras.execute_batch(cur, UPSERT_SQL, mapped, page_size=100)
                    conn.commit()
                    print(f"  ✓ Batch {i//batch_size + 1}: {len(mapped)} threats saved")
                except Exception as e:
                    print(f"  ✗ Batch {i//batch_size + 1} failed: {e}")
                    conn.rollback()

    except Exception as e:
        print(f"✗ DB save error: {e}")
        try:
            conn.rollback()
        except Exception:
            pass

    print(f"✓ DB complete: {new_count} new | {updated_count} updated | {errors} errors")
    return new_count, updated_count


# ============================================================
# QUICK STATS QUERY — for post-run summary
# ============================================================
def get_db_stats() -> dict:
    """Pull current DB stats for the run summary."""
    conn = get_connection()
    if not conn:
        return {}
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM threat_stats")
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception as e:
        print(f"⚠️  Could not fetch DB stats: {e}")
        return {}


def print_db_stats():
    """Print a formatted DB stats summary."""
    stats = get_db_stats()
    if not stats:
        return
    print("\n" + "=" * 60)
    print("🐘 POSTGRESQL DATABASE STATS")
    print("=" * 60)
    print(f"  Total threats in DB:    {stats.get('total_threats', 0):,}")
    print(f"  P1 Critical:            {stats.get('p1_count', 0):,}")
    print(f"  P2 High:                {stats.get('p2_count', 0):,}")
    print(f"  CISA KEV:               {stats.get('kev_count', 0):,}")
    print(f"  With MSF exploit:       {stats.get('msf_count', 0):,}")
    print(f"  Trending:               {stats.get('trending_count', 0):,}")
    print(f"  High EPSS (≥50%):       {stats.get('high_epss_count', 0):,}")
    print(f"  In the wild:            {stats.get('in_wild_count', 0):,}")
    print(f"  New last 24h:           {stats.get('new_24h', 0):,}")
    print(f"  New last 7 days:        {stats.get('new_7d', 0):,}")
    print(f"  Avg CVSS score:         {stats.get('avg_cvss', 0)}")
    print(f"  Last updated:           {stats.get('last_updated', 'N/A')}")
    print("=" * 60)


# ============================================================
# HOW TO INTEGRATE INTO Anubis_hunter_v6_3.py
# ============================================================
# Add these imports near the top of the main script:
#
#     from anubis_db import save_threats, start_run, finish_run, print_db_stats, test_connection
#
# In main(), after "all_threats = process_threats(...)":
#
#     # === PHASE 5: Save to PostgreSQL ===
#     run_id = start_run()
#     new_db, updated_db = save_threats(all_threats, run_id)
#     finish_run(run_id, len(all_threats), new_db, updated_db)
#     print_db_stats()
#
# That's it — 4 lines. Everything else stays the same.
# Excel + HTML generation continues as normal after this block.
# ============================================================
