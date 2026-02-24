# 🐺 Anubis — Threat Intelligence Hunter

> Automated threat intelligence aggregation platform collecting, enriching, and reporting from 40+ security feeds in real-time.

**By Ramiz Alsafi**

---

## 🔍 What is Anubis?

Anubis is a self-hosted threat intelligence platform that runs on a schedule and automatically:

- Pulls from **40+ threat intelligence sources** (NVD, CISA KEV, Exploit-DB, MalwareBazaar, URLHaus, AlienVault OTX, Shodan, AbuseIPDB, and more)
- **Enriches** every threat with EPSS scores, AttackerKB scores, MITRE ATT&CK mappings, and MSF module coverage
- **Deduplicates** and cross-correlates threats across sources
- **Risk-scores** every threat using CVSS, EPSS, KEV status, exploit availability, and attacker activity
- Generates a **formatted Excel database** with color-coded severity and dashboard charts
- Generates an **interactive HTML dashboard** (2MB+ rich report)
- Sends a **full threat report email** with both files attached

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
| News & Reports | SANS ISC, BleepingComputer, TheHackerNews, SecurityAffairs, DarkReading, SecurityWeek, InfoSecurity Magazine, HackRead |
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
  Output
  ├── Excel Database (color-coded, dashboard charts, PowerBI export)
  ├── Interactive HTML Dashboard
  └── Email Report (with attachments)
```

---

## 🚀 Getting Started

### Requirements

- Python 3.10+
- Postfix (for email delivery)
- Linux (Ubuntu 22.04+ recommended)

### Installation

```bash
git clone https://github.com/yourusername/anubis.git
cd anubis
pip install -r requirements.txt
```

### API Keys

Anubis works out of the box with free sources. Optional API keys unlock additional sources:

| Key | Source | Free? |
|---|---|---|
| `ABUSEIPDB_API_KEY` | AbuseIPDB | ✅ Free tier |
| `ALIENVAULT_API_KEY` | AlienVault OTX | ✅ Free |
| `VULNCHECK_API_KEY` | VulnCheck KEV | ✅ Free tier |
| `ATTACKERKB_API_KEY` | AttackerKB | ✅ Free |
| `URLSCAN_API_KEY` | URLScan.io | ✅ Free |
| `LEAKIX_API_KEY` | LeakIX | ✅ Free |
| `VULNERS_API_KEY` | Vulners | Paid |
| `VIRUSTOTAL_API_KEY` | VirusTotal | Free tier |
| `SHODAN_API_KEY` | Shodan | Paid |

Keys can be set as environment variables or configured directly in the script.

### Running

```bash
cd ~/anubis
python3 Anubis_hunter_v6_3.py
```

### Email Setup (Postfix + Gmail)

Anubis sends reports via local Postfix relay to Gmail SMTP. See [Email Setup Guide](#) for full configuration.

---

## 📊 Output Example

**Every run produces:**

- `threat_intelligence_log.xlsx` — Full threat database with:
  - Color-coded severity rows (Critical/High/Medium/Low)
  - AutoFilter on all columns
  - Summary dashboard sheet with charts
  - PowerBI-ready export sheet

- `anubis_threat_dashboard.html` — Interactive HTML report (~2MB) with:
  - Threat breakdown by type, severity, source
  - Exploitable CVE highlights
  - IOC tables
  - MITRE ATT&CK technique distribution

- **Email** — Both files attached and delivered to configured recipient

---

## 📁 Repository Structure

```
anubis/
├── Anubis_hunter_v6_3.py     # Main script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Excludes output files and secrets
├── README.md                  # This file
└── docs/
    └── CHANGELOG.md           # Version history
```

---

## 🗺️ Roadmap

| Phase | Status | Description |
|---|---|---|
| Phase 1-4 | ✅ Complete | Core feeds, enrichment, Excel/HTML output, email alerts |
| Phase 5 | 🔄 In Progress | PostgreSQL backend — persistent storage, historical queries |
| Phase 6 | 📋 Planned | Web dashboard (FastAPI + React) |
| Phase 7 | 📋 Planned | Real-time alerting, Slack/Teams integration |
| Phase 8 | 📋 Planned | ML-based risk prediction |
| Phase 9 | 📋 Planned | Cloud-native deployment (ECS/Lambda) |

---

## ⚠️ Disclaimer

Anubis is built for **defensive security purposes** — threat awareness, vulnerability management, and security monitoring. All data is sourced from publicly available threat intelligence feeds. Use responsibly and in accordance with applicable laws and regulations.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Anubis — because knowing what's out there is the first step to defending against it.*
