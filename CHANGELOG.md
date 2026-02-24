# Anubis — Changelog

All notable changes to Anubis are documented here.

---

## [v6.3] — 2026-02-24
### Added
- Deployed to AWS EC2 (Ubuntu 24.04, t3.micro)
- First successful cloud run: 2,191 unique threats, 33 active sources
- Resource Health Report with detailed per-source status breakdown

### Fixed
- Working directory permission issue on EC2 resolved
- Postfix email relay configuration for cloud deployment

---

## [v6.1 → v6.2]
### Changed
- GreyNoise replaced with free ip-api.com (geo + ASN + proxy detection)
- URLScan.io free tier query fallback chain added
- NCSC UK RSS feed (404) replaced with CISA advisories XML as CERT_EU primary

### Fixed
- CISA ICS endpoint updated (HTTP 403 on old paths)
- CSO Online RSS path corrected (`/index.rss` → `/feed/`)
- SC Magazine RSS path updated

---

## [v6.0]
### Added
- 11-source concurrent security news feed (BleepingComputer, TheHackerNews, SecurityAffairs, DarkReading, SecurityWeek, InfoSecurity, HackRead, and more)
- Hybrid Analysis public malware feed
- CAPE Sandbox fallback
- OpenPhish replacing dead PhishTank

### Fixed
- snort.org removed from Talos URLs (serves HTML login, never IP list)
- PacketStorm scraper blocking handled gracefully

---

## [v5.8]
### Added
- SSLBL (Abuse.ch SSL IP Blacklist)
- CERT/NCSC threat reports feed
- Hybrid Analysis integration
- Missing URL constants added (caused NameError on previous versions)

### Fixed
- intel_feed task key fix (was mapped to snyk incorrectly)
- AbuseIPDB cache TTL system (6h cache, prevents rate limiting)

---

## [v5.7]
### Added
- PowerBI-optimised export sheet in Excel output
- Interactive HTML dashboard generation (~2MB rich report)
- Security news cross-correlation map (CVE mentions in news)
- AttackerKB per-CVE enrichment in process_threats()
- ZDI cross-correlation map (CVE ID + product keyword fallback)

---

## [v5.6]
### Added
- LeakIX exposed RDP and vulnerable host feeds
- Censys search integration
- URLScan.io malicious URL feed

---

## [v5.3 → v5.5]
### Added
- EPSS v5.1 scoring (KEV-priority, multi-batch up to 500 CVEs)
- NVD CVE detail enrichment for high-priority CVEs (CWE + refs + exploit signals)
- MSF module CVE coverage (Rapid7 official GitHub, 24h cache)
- Multi-source accuracy validation pass

### Fixed
- naive/aware datetime comparison TypeError on Python <3.11
- Excel schema guard — auto-backup and fresh start on column mismatch

---

## [v5.0 → v5.2]
### Added
- Zero Day Initiative (ZDI) published advisories feed
- AttackerKB topics feed
- SANS ISC threat diary
- Firewall vendor advisories: Fortinet, Palo Alto, Cisco, CheckPoint, Juniper, F5, Citrix, SonicWall, WatchGuard, Sophos, Aruba, Zyxel, Barracuda, pfSense
- Excel AutoFilter + Dashboard sheet with charts
- Email delivery system (replaced Zoho Cliq webhooks)
- Base64 key obfuscation system with env var override

---

## [v4.x and earlier]
- Core threat feed integration (NVD, CISA KEV, Exploit-DB, MalwareBazaar, URLHaus, AlienVault OTX, ThreatFox, Shodan, AbuseIPDB)
- MITRE ATT&CK mapping (CWE + keyword based)
- Risk scoring engine (CVSS + likelihood + impact)
- Excel output with color-coded severity
- Concurrent fetch mode (ThreadPoolExecutor)
- Last-run tracking (1h interval guard)
