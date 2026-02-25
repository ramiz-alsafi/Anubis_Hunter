# 🐺 Anubis — Threat Intelligence Hunter

**Automated threat intelligence aggregation platform collecting, enriching, and reporting from 40+ security feeds in real time. Now with persistent PostgreSQL backend and full host defense via Wazuh.**

By **Ramiz Alsafi** | Deployed on **AWS EC2**

---

## What is Anubis?

Anubis is a self-hosted threat intelligence platform that runs on a schedule and automatically:

- Pulls from **40+ threat intelligence sources** (NVD, CISA KEV, Exploit-DB, MalwareBazaar, URLHaus, AlienVault OTX, Shodan, AbuseIPDB, and more)
- Enriches every threat with **EPSS scores**, **AttackerKB scores**, **MITRE ATT&CK mappings**, and **MSF module coverage**
- Deduplicates and cross-correlates threats across all sources
- Risk-scores every threat using CVSS, EPSS, KEV status, exploit availability, and attacker activity
- Persists all threat data to **PostgreSQL** with full historical tracking and upsert logic
- Generates a formatted **Excel database** with color-coded severity and dashboard charts
- Generates an **interactive HTML dashboard** (~2MB rich report)
- Sends a full **threat report email** with both files attached via Postfix + Gmail relay
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
| Other | MITRE ATT&CK (local CWE mapping), CERT/NCSC, CISA Ransomware, Ubuntu Security |

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
  ├── EPSS Scoring (FIRST.org)
  ├── AttackerKB Scoring
  ├── MITRE ATT&CK Mapping (CWE + Keyword)
  ├── MSF Module Coverage (Rapid7)
  ├── IP Geo/ASN Enrichment (ip-api.com)
  └── NVD CVE Detail Enrichment
       ↓
  Risk Scoring (CVSS + EPSS + KEV + Exploit + Attacker Activity)
       ↓
  ┌─────────────────────────────────────┐
  │           Output Layer              │
  ├── PostgreSQL DB (persistent/upsert) │  ← Phase 5 ✅
  ├── Excel Database (formatted)        │
  ├── Interactive HTML Dashboard        │
  └── Email Report (with attachments)   │
  └─────────────────────────────────────┘
       ↓
  ┌─────────────────────────────────────┐
  │         Host Defense Layer          │
  │                                     │
  │  Wazuh Agent (EC2)                  │  ← Phase 6 🔄 In Progress
  ├── Log Collection (auth, syslog,     │
  │   kernel, dpkg, apt, mail,          │
  │   cloud-init, postgresql, chrony,   │
  │   SSM, journald, dmesg)             │
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
```

---

## 🛡️ Host Defense (Phase 6 — In Progress)

The EC2 instance running Anubis is monitored by a **Wazuh agent** deployed in full defense mode. This is not just a SIEM demo — it's actively protecting the platform that generates the threat intel.

**What's live right now:**

- Full log collection across auth, syslog, kernel, dpkg, apt, mail, cloud-init, postgresql, chrony, SSM, journald, and dmesg
- File integrity monitoring on `/etc`, `/bin`, `/sbin`, SSH keys, and `/home/ubuntu/Anubis` in **realtime mode**
- Custom detection rules tuned for brute force, reverse shell attempts, malware staging, off-hours SSH, privilege escalation, and new user creation
- **Active response** enabled — firewall-drop fires automatically on confirmed brute force
- **VirusTotal integration** — file hashes from FIM alerts are checked against VT automatically
- **Email alerting** — Wazuh alert emails delivered in real time for Level 6+ events

Check the `screenshots/` directory for sanitized real alert examples captured live from the platform.

---

## 🗄️ Database Schema (Phase 5)

PostgreSQL backend with:

- `threats` table — 40+ columns including Phase 6 dashboard metadata
- `runs` table — every Anubis execution logged with stats
- 13 indexes — optimized for priority, severity, EPSS, KEV, full-text search, and JSONB
- 4 views — `critical_threats`, `kev_threats`, `trending_threats`, `threat_stats`
- Upsert logic — existing threats updated with latest scores, `run_count` and `severity_changed` tracked
- Phase 6 ready — `first_seen_at`, `last_seen_at`, `is_trending`, `dashboard_tags` already in schema

**2,199 threats synced on first run.**

---

## 🚀 Getting Started

**Requirements**

- Python 3.10+
- PostgreSQL 14+
- Postfix (for email delivery via Gmail relay)
- Linux (Ubuntu 22.04+ recommended)
- AWS EC2 t3.micro or equivalent (1GB RAM minimum)

---

## 🗺️ Roadmap

| Phase | Status | Description |
|---|---|---|
| Phase 1–4 | ✅ Complete | Core feeds, enrichment, Excel/HTML output, email alerts |
| Phase 5 | ✅ Complete | PostgreSQL backend — persistent storage, upsert, run tracking |
| Phase 6 | 🔄 In Progress | Wazuh SIEM integration — host defense, FIM, custom rules, active response |
| Phase 7 | 📋 Planned | Web dashboard (FastAPI + React) |
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
