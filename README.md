# 🐺 Anubis — Threat Intelligence Hunter

**Automated threat intelligence aggregation platform collecting, enriching, and reporting from 40+ security feeds in real time. Persistent PostgreSQL backend, full host defense via Wazuh, and now live on the public internet.**

By **Ramiz Alsafi** | Deployed on **AWS EC2** | 🌐 **[anubispro.duckdns.org](https://anubispro.duckdns.org)**

---

## What is Anubis?

Anubis is a self-hosted threat intelligence platform that runs on a schedule and automatically:

- Pulls from **50+ threat intelligence sources** (NVD, CISA KEV, Exploit-DB, MalwareBazaar, URLHaus, AlienVault OTX, Shodan, AbuseIPDB, and more)
- Enriches **every single CVE** with **EPSS scores**, **MITRE ATT&CK mappings**, **NVD detail enrichment**, and **MSF module coverage** — no caps, full coverage
- Deduplicates and cross-correlates threats across all sources
- Risk-scores every threat using CVSS, EPSS, KEV status, exploit availability, and attacker activity
- Persists all threat data to **PostgreSQL** with full historical tracking and upsert logic
- Generates a formatted **Excel database** with color-coded severity and dashboard charts
- Generates an **interactive HTML dashboard** (~2MB rich report) served live at [anubispro.duckdns.org](https://anubispro.duckdns.org)
- Sends a full **threat report email** with both files attached via Postfix + Gmail relay
- Cleans up after itself — auto-deletes stale backups and syncs the latest dashboard to Nginx on every run
- Defends itself: the EC2 instance running Anubis is protected by a **Wazuh agent** with custom detection rules, FIM, and active response

---

## 📡 Data Sources (40+)

| Category | Sources |
|---|---|
| CVE / Vulnerability | NVD, CISA KEV, VulnCheck KEV, RedHat, GitHub Advisories, CIRCL, OSV.dev |
| Exploit Intelligence | Exploit-DB, ZDI, Metasploit (Rapid7), PacketStorm, Vulners |
| Malware / IOC | MalwareBazaar, ThreatFox, URLHaus, Hybrid Analysis, Abuse.ch SSLBL |
| IP Reputation | AbuseIPDB, Shodan InternetDB, Feodo Tracker, Talos, Emerging Threats, Blocklist.de, FireHOL L1+L2, IPsum, Tor Exit Nodes |
| Phishing | OpenPhish, URLScan.io |
| Threat Intel Platforms | AlienVault OTX, LeakIX, AttackerKB |
| Firewall / Vendor Advisories | Fortinet, Palo Alto, Cisco, CheckPoint, WatchGuard, Juniper, F5, Citrix, SonicWall, Sophos, Zyxel, Aruba, Barracuda, pfSense |
| News & Reports | SANS ISC, BleepingComputer, TheHackerNews, SecurityAffairs, DarkReading, SecurityWeek, InfoSecurity, HackRead |
| Microsoft | MSRC, Windows CVEs, Patch Tuesday |
| Other | MITRE ATT&CK (local CWE mapping), CERT/NCSC, CISA Ransomware, CISA ICS, Ubuntu Security |

---

## ⚙️ Architecture

```
Threat Feeds (40+)
       ↓
  Concurrent Fetch (ThreadPoolExecutor)
       ↓
  Normalization & Deduplication
       ↓
  Enrichment Layer
  ├── EPSS Scoring (FIRST.org) — ALL CVEs, batched
  ├── NVD CVE Detail Enrichment — ALL CVEs, priority ordered
  │   (KEV → CRITICAL → HIGH → remaining, with smart rate limiting)
  ├── MITRE ATT&CK Mapping (CWE + Keyword)
  ├── MSF Module Coverage (Rapid7)
  ├── IP Geo/ASN Enrichment (ip-api.com)
  └── News Cross-Correlation
       ↓
  Risk Scoring (CVSS + EPSS + KEV + Exploit + Attacker Activity)
       ↓
  ┌─────────────────────────────────────┐
  │           Output Layer              │
  ├── PostgreSQL DB (persistent/upsert) │
  ├── Excel Database (formatted)        │
  ├── Interactive HTML Dashboard        │ ← Full DB (all runs, not just latest)
  ├── Email Report (with attachments)   │
  └── Nginx Sync (auto-deploy to web)   │ ← New in v6.1
  └─────────────────────────────────────┘
       ↓
  ┌─────────────────────────────────────┐
  │       Post-Run Cleanup              │
  ├── Deletes stale backup files        │ ← New in v6.1
  └── Syncs dashboard │
  └─────────────────────────────────────┘
       ↓
  ┌─────────────────────────────────────┐
  │         Host Defense Layer          │
  │                                     │
  │  Wazuh Agent (EC2)                  │
  ├── Log Collection (auth, syslog,     │
  │   kernel, dpkg, apt, mail,          │
  │   cloud-init, postgresql, chrony,   │
  │   SSM, journald, dmesg, UFW)        │ ← UFW logs added in v6.1
  ├── File Integrity Monitoring         │
  │   (/etc, /bin, SSH keys, /Anubis)   │
  ├── Rootcheck & Syscollector          │
  ├── Custom Detection Rules            │
  │   (brute force, reverse shell,      │
  │   malware staging, off-hours SSH,   │
  │   privilege escalation, new users)  │
  └── Active Response (firewall-drop)   │
  └─────────────────────────────────────┘
       ↓
  Wazuh Manager
       ↓
  ┌─────────────────────────────────────┐
  │       Public Web Layer (NEW)        │
  │                                     │
  │  Nginx Reverse Proxy                │
  ├── HTTPS via Let's Encrypt (Certbot) │
  ├── DuckDNS — anubispro.duckdns.org   │
  ├── TLS 1.2 / 1.3 only                │
  ├── Sensitive file access blocked     │
  └── UFW — ports 80, 443, 1514,        │
             1515, 55000 (locked)       │
  └─────────────────────────────────────┘
```

---

## 🛡️ Host Defense

The EC2 instance running Anubis is monitored by a **Wazuh agent** deployed in full defense mode. This is not just a SIEM demo — it's actively protecting the platform that generates the threat intel.

**What's live right now:**

- Full log collection across auth, syslog, kernel, dpkg, apt, mail, cloud-init, postgresql, chrony, SSM, journald, dmesg, and **UFW firewall logs**
- File integrity monitoring on `/etc`, `/bin`, `/sbin`, SSH keys, and `/home/ubuntu/Anubis` in **realtime mode**
- Custom detection rules tuned for brute force, reverse shell attempts, malware staging, off-hours SSH, privilege escalation, and new user creation
- **Active response** enabled — firewall-drop fires automatically on confirmed brute force
- **VirusTotal integration** — file hashes from FIM alerts are checked against VT automatically
- **Email alerting** — Wazuh alert emails delivered in real time for Level 6+ events
- **UFW firewall** hardened — default deny inbound, SSH locked to authorized IPs, Wazuh ports restricted

Check the `screenshots/` directory for sanitized real alert examples captured live from the platform.

---

## 🌐 Public Deployment (New in v6.1)

Anubis is now live on the public internet. The interactive HTML dashboard auto-updates on every run.

**Stack:**
- **Nginx** reverse proxy serving static dashboard
- **Let's Encrypt** SSL certificate via Certbot
- **DuckDNS** free subdomain — `anubispro.duckdns.org`
- **UFW** firewall — hardened inbound rules, sensitive ports locked

**Security hardening on the public endpoint:**
- HTTPS only — HTTP redirects to 443
- TLS 1.2 / 1.3, strong cipher suite
- `.py`, `.log`, `.xlsx`, `.json`, `.sql`, `.db`, `.env` files blocked at Nginx level
- Hidden files and internal directories (`__pycache__`, `.git`, `venv`) denied
- No backend exposed — pure static file serving (Phase 6)
- Phase 7 FastAPI proxy already stubbed in config, one uncomment away

---

## 🗄️ Database Schema

PostgreSQL backend with:

- `threats` table — 40+ columns including Phase 6 dashboard metadata
- `runs` table — every Anubis execution logged with stats
- 13 indexes — optimized for priority, severity, EPSS, KEV, full-text search, and JSONB
- 4 views — `critical_threats`, `kev_threats`, `trending_threats`, `threat_stats`
- Upsert logic — existing threats updated with latest scores, `run_count` and `severity_changed` tracked
- `first_seen_at`, `last_seen_at`, `is_trending`, `dashboard_tags` — full historical tracking

**2,896+ threats in DB across multiple runs.**

---

## 🚀 Getting Started

**Requirements**

- Python 3.10+
- PostgreSQL 14+
- Nginx
- Certbot (`python3-certbot-nginx`)
- Postfix (for email delivery via Gmail relay)
- Linux (Ubuntu 22.04+ recommended)
- AWS EC2 t3.micro or equivalent (1GB RAM minimum)
- **10x NVD enrichment speed:**

---

## 🔥 UFW Firewall Rules

```
# SSH locked to your IP
# HTTP (redirects to HTTPS)
# HTTPS
# Wazuh agent comms
# Wazuh enrollment
# Wazuh API locked

```

---

## 🗺️ Roadmap

| Phase | Status | Description |
|---|---|---|
| Phase 1–4 | ✅ Complete | Core feeds, enrichment, Excel/HTML output, email alerts |
| Phase 5 | ✅ Complete | PostgreSQL backend — persistent storage, upsert, run tracking |
| Phase 6 | ✅ Complete | Wazuh SIEM + host defense + UFW + Nginx + HTTPS + public deployment |
| Phase 7 | 📋 Planned | Web dashboard (FastAPI + React + django) |
| Phase 8 | 📋 Planned | Real-time alerting, Slack/Teams integration |
| Phase 9 | 📋 Planned | ML-based risk prediction |
| Phase 10 | 📋 Planned | Cloud-native deployment (ECS/Lambda) |

---

## ⚠️ Disclaimer

Anubis is built for defensive security purposes. All data is sourced from publicly available threat intelligence feeds. Use responsibly.

---

## 📜 License

MIT License — see LICENSE for details.

---

*Anubis — because knowing what's out there is the first step to defending against it.*
