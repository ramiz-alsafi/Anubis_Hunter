# 🐺 Anubis — Threat Intelligence Hunter

> Automated threat intelligence aggregation platform collecting, enriching, and reporting from 40+ security feeds in real-time. Now with persistent PostgreSQL backend.

**By Ramiz Alsafi** | Deployed on AWS EC2

---

## 🔍 What is Anubis?

Anubis is a self-hosted threat intelligence platform that runs on a schedule and automatically:

- Pulls from **40+ threat intelligence sources** (NVD, CISA KEV, Exploit-DB, MalwareBazaar, URLHaus, AlienVault OTX, Shodan, AbuseIPDB, and more)
- **Enriches** every threat with EPSS scores, AttackerKB scores, MITRE ATT&CK mappings, and MSF module coverage
- **Deduplicates** and cross-correlates threats across sources
- **Risk-scores** every threat using CVSS, EPSS, KEV status, exploit availability, and attacker activity
- **Persists** all threat data to PostgreSQL with full historical tracking and upsert logic
- Generates a **formatted Excel database** with color-coded severity and dashboard charts
- Generates an **interactive HTML dashboard** (~2MB rich report)
- Sends a **full threat report email** with both files attached via Postfix + Gmail

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
```

---

## 🗄️ Database Schema (Phase 5)

PostgreSQL backend with:

- **`threats`** table — 40+ columns including Phase 6 dashboard metadata
- **`runs`** table — every Anubis execution logged with stats
- **13 indexes** — optimized for priority, severity, EPSS, KEV, full-text search, JSONB
- **4 views** — `critical_threats`, `kev_threats`, `trending_threats`, `threat_stats`
- **Upsert logic** — existing threats updated with latest scores, `run_count` and `severity_changed` tracked
- **Phase 6 ready** — `first_seen_at`, `last_seen_at`, `is_trending`, `dashboard_tags` already in place

---

## 🚀 Getting Started

### Requirements

- Python 3.10+
- PostgreSQL 14+
- Postfix (for email delivery via Gmail relay)
- Linux (Ubuntu 22.04+ recommended)
- AWS EC2 t3.micro or equivalent (1GB RAM minimum)

### Installation

```bash
git clone https://github.com/yourusername/anubis.git
cd anubis
pip install -r requirements.txt
```

### Database Setup

```bash
# Run once to create DB, user, schema, indexes and views
bash setup_db.sh
```

### API Keys

| Key | Source | Free? |
|---|---|---|
| `ABUSEIPDB_API_KEY` | AbuseIPDB | ✅ Free tier |
| `ALIENVAULT_API_KEY` | AlienVault OTX | ✅ Free |
| `VULNCHECK_API_KEY` | VulnCheck KEV | ✅ Free tier |
| `ATTACKERKB_API_KEY` | AttackerKB | ✅ Free |
| `URLSCAN_API_KEY` | URLScan.io | ✅ Free |
| `LEAKIX_API_KEY` | LeakIX | ✅ Free |
| `VULNERS_API_KEY` | Vulners | Paid |
| `SHODAN_API_KEY` | Shodan | Paid |

### Running

```bash
cd ~/anubis
python3 Anubis_hunter_v6_3.py
```

---

## 📁 Repository Structure

```
anubis/
├── Anubis_hunter_v6_3.py     # Main script
├── anubis_db.py               # PostgreSQL integration module (Phase 5)
├── anubis_schema.sql          # Database schema, indexes, views
├── setup_db.sh                # One-shot DB setup script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Excludes output files and secrets
├── README.md                  # This file
└── CHANGELOG.md               # Version history
```

---

## 🗺️ Roadmap

| Phase | Status | Description |
|---|---|---|
| Phase 1–4 | ✅ Complete | Core feeds, enrichment, Excel/HTML output, email alerts |
| Phase 5 | ✅ Complete | PostgreSQL backend — persistent storage, upsert, run tracking |
| Phase 6 | 📋 Planned | Web dashboard (FastAPI + React) |
| Phase 7 | 📋 Planned | Real-time alerting, Slack/Teams integration |
| Phase 8 | 📋 Planned | ML-based risk prediction |
| Phase 9 | 📋 Planned | Cloud-native deployment (ECS/Lambda) |

---

## ⚠️ Disclaimer

Anubis is built for **defensive security purposes**. All data is sourced from publicly available threat intelligence feeds. Use responsibly.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Anubis — because knowing what's out there is the first step to defending against it.*
