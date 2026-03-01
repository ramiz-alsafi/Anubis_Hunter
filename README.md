# 🐺 Anubis — Threat Intelligence Hunter

**Automated threat intelligence aggregation platform collecting, enriching, and reporting from 60 concurrent security feeds. Persistent PostgreSQL backend. Host defense via Wazuh. Interactive dashboard with Risk Calculator and GRC compliance mapping.**

By **Ramiz Alsafi** | Deployed on **AWS EC2** | v6.4.9

---

## What is Anubis?

Anubis is a self-hosted threat intelligence platform that runs on a schedule and automatically:

- Pulls from **60 concurrent threat intelligence sources** (NVD, CISA KEV, Exploit-DB, MalwareBazaar, URLHaus, AlienVault OTX, Shodan, AbuseIPDB, ZDI, and more)
- Enriches every threat with **EPSS scores**, **AttackerKB scores**, **MITRE ATT&CK mappings**, and **MSF module coverage**
- Deduplicates and cross-correlates threats across all sources
- Risk-scores every threat using CVSS, EPSS, KEV status, exploit availability, and attacker activity
- Persists all threat data to **PostgreSQL** with full historical tracking and upsert logic
- Generates a formatted **Excel database** with color-coded severity and dashboard charts
- Generates an **interactive HTML dashboard** (~4MB rich report, no external dependencies)
- Sends a full **threat report email** with both files attached
- Defends itself: the EC2 instance running Anubis is protected by a **Wazuh agent** with custom detection rules, FIM, and active response

---

## 📡 Data Sources (60 Concurrent)

| Category | Sources |
|---|---|
| CVE / Vulnerability | NVD, CISA KEV, VulnCheck KEV, RedHat, GitHub Advisories, CIRCL, OSV.dev, Vulners |
| Exploit Intelligence | Exploit-DB, ZDI (Zero Day Initiative), Metasploit (Rapid7), PacketStorm, Vulners |
| Malware / IOC | MalwareBazaar, ThreatFox, URLHaus, Hybrid Analysis, Abuse.ch SSLBL |
| IP Reputation | AbuseIPDB, Shodan InternetDB, Feodo Tracker, Talos, Emerging Threats, Blocklist.de, FireHOL L1+L2, IPsum, Tor Exit Nodes |
| Phishing | OpenPhish, URLScan.io |
| Threat Intel Platforms | AlienVault OTX, LeakIX, AttackerKB |
| Firewall / Vendor Advisories | Fortinet, Palo Alto, Cisco, CheckPoint, WatchGuard, Juniper, F5, Citrix, SonicWall, Sophos, Zyxel, Aruba, Barracuda, pfSense |
| News & Reports | SANS ISC, BleepingComputer, TheHackerNews, SecurityAffairs, DarkReading, SecurityWeek, InfoSecurity, HackRead |
| Microsoft | MSRC (official REST API), Windows CVEs, Patch Tuesday |
| MITRE | ATT&CK Enterprise STIX bundle (691 techniques/sub-techniques), CWE mapping |
| Other | CERT/NCSC, CISA Ransomware, Ubuntu Security, AI Incident Database, Huntr AI/ML CVEs |

---

## ⚙️ Architecture

```
Threat Feeds (60 concurrent)
       ↓
  ThreadPoolExecutor — parallel fetch with timeout handling
       ↓
  Normalization & Deduplication
       ↓
  Enrichment Layer
  ├── EPSS Scoring (FIRST.org) — batch with retry
  ├── AttackerKB Scoring (per-CVE)
  ├── MITRE ATT&CK Mapping (CWE + keyword correlation)
  ├── ZDI Cross-correlation (CVE ID + product keyword)
  ├── MSF Module Coverage (Rapid7 — 3,000+ CVEs)
  ├── IP Geo/ASN Enrichment (ip-api.com + AbuseIPDB)
  └── NVD CVE Detail Enrichment (full 2,400+ CVE coverage)
       ↓
  Risk Scoring (CVSS + EPSS + KEV + Exploit + Attacker Activity)
       ↓
  ┌───────────────────────────────────────────────┐
  │                 Output Layer                  │
  ├── PostgreSQL DB (persistent, upsert, indexed) │
  ├── Excel Database (formatted, PowerBI-ready)   │
  ├── Interactive HTML Dashboard (self-contained) │
  └── Email Report (Excel + HTML attached)        │
  └───────────────────────────────────────────────┘
       ↓
  ┌───────────────────────────────────────────────┐
  │             Host Defense Layer                │
  │  Wazuh Agent (EC2)                            │
  ├── Log Collection (auth, syslog, kernel,       │
  │   dpkg, apt, mail, cloud-init, postgresql,    │
  │   chrony, SSM, journald, dmesg)               │
  ├── File Integrity Monitoring                   │
  ├── Rootcheck & Syscollector                    │
  ├── Custom Detection Rules                      |       │
  └── Active Response                             │
  └───────────────────  ──────────────────────────┘
       ↓
  Wazuh Manager
```

---

## 📊 Interactive Dashboard

The generated HTML dashboard is fully self-contained (no backend, no external libraries) and includes:

**Overview Tab**
- Risk level distribution, top threat types, remediation priority breakdown
- EPSS score distribution with coverage badge
- Exploit status breakdown, confidence scoring, patch availability
- Threats over time — Daily / Weekly / Monthly toggle (builds across runs)
- Risk heatmap — Type × Severity
- **MITRE ATT&CK Tactic Coverage** — live-computed from all 691 mapped techniques
- Live TTP simulation — click any kill chain phase to expand Sigma rules, red/blue team guidance
- Full filterable threat table (50+ columns, paginated, exportable to CSV)

**Detection Rules Tab** — Wazuh/Sigma, Suricata IPS, and hardening checklists generated per-threat

**Incident Response Tab** — Structured IR playbooks mapped to MITRE tactics

**Risk Calculator Tab** — Input your budget, incident frequency, patch velocity, detection coverage, and MTTR. Returns annual risk exposure, projected savings, and priority recommendations — all computed from your live threat dataset.

**GRC & Compliance Tab** — ISO/IEC 27001:2022 Annex A and NIST SP 800-53 Rev 5 controls scored and color-coded based on actual threat composition. Open compliance gaps surfaced automatically.

**Sandbox & Emulation Tab** *(Coming Soon)* — Isolated emulation environment for testing exploits and CVEs from the dataset against your own stack without touching production.

---

## 🛡️ Host Defense

The EC2 instance running Anubis is monitored by a **Wazuh agent** deployed in full defense mode.

**Live right now:**
- Full log collection across 13 sources (auth, syslog, kernel, dpkg, apt, mail, cloud-init, postgresql, chrony, SSM, journald, dmesg)
- File integrity monitoring in **realtime mode**
- Custom detection rules for brute force, reverse shell attempts, malware staging, off-hours SSH, privilege escalation, and new user creation
- **Active response** — firewall-drop fires automatically on confirmed brute force
- **VirusTotal integration** — file hashes from FIM alerts checked against VT automatically
- **Email alerting** — Wazuh alert emails for Level 6+ events in real time


## 🔢 Sample Output (v6.4.9 run)

```
✅ Active sources:          37  (6,933 total records)
🔬 NVD CVE enrichment:    966 CVEs fetched
⚔️  MITRE ATT&CK:          691 techniques loaded
🎯 ZDI advisories:          27 cross-correlated
🔮 EPSS coverage:        1168/1191 CVEs scored
🛡️  Firewall advisories:    29 across 14 vendors
🔥 CISA KEV:            1,529 actively exploited CVEs
📰 Security news:           28 items (11 sources)
💀 Hard failures:            0
```

---


## 🗺️ Roadmap

| Phase | Status | Description |
|---|---|---|
| Phase 1–4 | ✅ Complete | Core feeds, enrichment, Excel/HTML output, email alerts |
| Phase 5 | ✅ Complete | PostgreSQL backend — persistent storage, upsert, run tracking |
| Phase 6 | ✅ Complete | Wazuh SIEM integration — host defense, FIM, custom rules, active response |
| Phase 6.4 | ✅ Complete | Dashboard v2 — Risk Calculator, GRC/Compliance, MITRE ATT&CK live chart, interactive timeline |
| Phase 7 | 🔄 In Progress | Web frontend (FastAPI + React) — replace static HTML with live backend (django)|
| Phase 8 | 📋 Planned | Sandbox & Emulation — isolated CVE/exploit testing against vendor-specific environments |
| Phase 9 | 📋 Planned | Real-time alerting — Slack/Teams integration, webhook support |
| Phase 10 | 📋 Planned | ML-based risk prediction |
| Phase 11 | 📋 Planned | Cloud-native deployment (ECS/Lambda) |

---

## ⚠️ Disclaimer

Anubis is built for defensive security purposes. All data is sourced from publicly available threat intelligence feeds. Use responsibly.

---

## 📜 License

MIT License — see LICENSE for details.

---

*Anubis — because knowing what's out there is the first step to defending against it.*
