# Anubis — Changelog

---

## [v6.3] — 2026-02-25 🎉
### Phase 5 Complete — PostgreSQL Backend
- **PostgreSQL integration** via `anubis_db.py` module
- **`threats` table** — 40+ columns, full threat data + Phase 6 dashboard metadata
- **`runs` table** — every Anubis execution logged with stats
- **Upsert logic** — `ON CONFLICT DO UPDATE` refreshes existing threats each run
- **Run tracking** — `run_count`, `severity_changed`, `first_seen_at`, `last_seen_at` per threat
- **13 indexes** — priority, severity, EPSS, KEV, full-text search (GIN), JSONB
- **4 views** — `critical_threats`, `kev_threats`, `trending_threats`, `threat_stats`
- **Deployed to AWS EC2** (Ubuntu 24.04, t3.micro) — first cloud run: 2,191 threats
- **Postfix + Gmail relay** configured and operational
- **GitHub repo** structured with README, CHANGELOG, .gitignore, LICENSE

### Fixed
- EC2 working directory permissions for Excel/HTML output
- Postfix `sasl_passwd.db` missing (postmap not run)
- Postfix `generic.db` missing
- EC2 IPv6 outbound blocked → forced `inet_protocols = ipv4`
- PostgreSQL schema file permissions (copied to /tmp for postgres user access)

---

## [v6.1 → v6.2] — 2026-02
### Changed
- GreyNoise replaced with free ip-api.com (geo + ASN + proxy detection)
- URLScan.io free tier query fallback chain added
- NCSC UK RSS (404) replaced with CISA advisories XML

### Fixed
- CISA ICS endpoint updated (HTTP 403 on old paths)
- CSO Online RSS path corrected
- SC Magazine RSS path updated

---

## [v6.0]
### Added
- 11-source concurrent security news feed
- Hybrid Analysis public malware feed
- OpenPhish replacing dead PhishTank

### Fixed
- snort.org removed from Talos URLs (serves HTML login page)
- PacketStorm scraper blocking handled gracefully

---

## [v5.8]
### Added
- SSLBL (Abuse.ch SSL IP Blacklist)
- CERT/NCSC threat reports feed
- Hybrid Analysis integration
- Missing URL constants fixed (caused NameError)
- AbuseIPDB 6h cache system

---

## [v5.7]
### Added
- PowerBI-optimised export sheet
- Interactive HTML dashboard (~2MB)
- Security news cross-correlation map
- AttackerKB per-CVE enrichment
- ZDI cross-correlation map

---

## [v5.6]
### Added
- LeakIX exposed RDP and vulnerable host feeds
- URLScan.io malicious URL feed

---

## [v5.3 → v5.5]
### Added
- EPSS v5.1 scoring (KEV-priority, multi-batch)
- NVD CVE detail enrichment for high-priority CVEs
- MSF module CVE coverage (Rapid7 official, 24h cache)
- Multi-source accuracy validation pass

### Fixed
- naive/aware datetime comparison TypeError on Python <3.11
- Excel schema guard with auto-backup on column mismatch

---

## [v5.0 → v5.2]
### Added
- ZDI published advisories
- AttackerKB topics feed
- SANS ISC threat diary
- Firewall vendor advisories (Fortinet, Palo Alto, Cisco, CheckPoint, Juniper, F5, Citrix, SonicWall, WatchGuard, Sophos, Aruba, Zyxel, Barracuda, pfSense)
- Excel AutoFilter + Dashboard sheet with charts
- Email delivery system (replaced Zoho Cliq)
- Base64 key obfuscation with env var override

---

## [v4.x and earlier]
- Core threat feed integration (NVD, CISA KEV, Exploit-DB, MalwareBazaar, URLHaus, OTX, ThreatFox, Shodan, AbuseIPDB)
- MITRE ATT&CK mapping (CWE + keyword)
- Risk scoring engine
- Excel output with color-coded severity
- Concurrent fetch mode (ThreadPoolExecutor)
- Last-run tracking (1h interval guard)
