# 🐺 Anubis  
### The Ultimate Threat Intelligence Hunter

<p align="center">
  <img src="https://github.com/user-attachments/assets/f2171717-ff15-404a-93dc-a6d811ec88b2" width="1000">
</p>

---

A high-performance automated threat intelligence platform that aggregates, analyzes, and reports on global security risks in real time. Designed to provide instant visibility into the evolving threat landscape.  

**By Ramiz Alsafi**  
Deployed on AWS EC2  
Version 6.5.1  live at https://anubispro.duckdns.org/ platform soon at https://riskwatchpro.duckdns.org/ 👀

---

## 👁️ What is Anubis?

Anubis operates 24/7 to scan the digital horizon, identifying vulnerabilities and active attacks before they impact infrastructure.

- **Unified Intelligence** — Combines 60 security feeds into a single source of truth  
- **Deep Enrichment** — Pulls exploit data, MITRE ATT&CK mappings, and severity scoring  
- **Intelligent Risk Scoring** — Weighs exploit availability, attacker activity, and contextual risk  
- **Actionable Reporting** — Generates Excel databases and interactive dashboards  
- **Built-in Resilience** — Integrated Wazuh-based host defense monitoring  

---

## 📡 Intelligence Network (60+ Sources)

Anubis monitors multiple threat categories:

- **Global Vulnerabilities** — NVD, CISA KEV, vendor advisories (Cisco, Palo Alto, Fortinet)  
- **Exploit & Malware Intelligence** — MalwareBazaar, Exploit-DB, Zero Day Initiative  
- **Dark Web & Reputation** — IP reputation, phishing URLs, leaked credentials (AlienVault, Shodan)  
- **Industry Reporting** — SANS, BleepingComputer, TheHackerNews  

---

## 📊 Interactive Command Center

The dashboard is a fully self-contained HTML portal designed for operational and strategic visibility.

- **Strategic Overview** — Risk levels, remediation priorities, threat trends  
- **Risk Calculator** — Budget-driven annual risk exposure and ROI estimation  
- **MITRE ATT&CK Matrix** — Live technique mapping  
- **Compliance & GRC** — ISO 27001, NIST, SOC 2, PCI DSS gap scoring  
- **Incident Response Playbooks** — Generated response guidance per threat  

---

## 🛡️ Self-Defending Architecture

Hosted on a hardened AWS EC2 instance with integrated defense monitoring.

- Real-time system log monitoring  
- File integrity monitoring  
- Automated IP blocking  
- Full audit trail tracking  

---

## 🔢 Performance Snapshot (v6.5.1)

| Metric | Status |
|--------|--------|
| Active Intelligence Sources | 37 (6,933+ records) |
| Enriched CVE Records | 1,168 Scored |
| Threat Mappings | 691 MITRE Techniques |
| Active Exploits Tracked | 1,529 (CISA KEV) |
| System Failures | 0 (Stable) |

---

## 📡 Data Sources (60 Concurrent)

| Category | Sources |
|----------|---------|
| CVE / Vulnerability | NVD, CISA KEV, VulnCheck KEV, RedHat, GitHub Advisories, CIRCL, OSV.dev, Vulners |
| Exploit Intelligence | Exploit-DB, ZDI, Metasploit (Rapid7), PacketStorm, Vulners |
| Malware / IOC | MalwareBazaar, ThreatFox, URLHaus, Hybrid Analysis, Abuse.ch SSLBL |
| IP Reputation | AbuseIPDB, Shodan InternetDB, Feodo Tracker, Talos, Emerging Threats, Blocklist.de, FireHOL L1+L2, IPsum, Tor Exit Nodes |
| Phishing | OpenPhish, URLScan.io |
| Threat Intel Platforms | AlienVault OTX, LeakIX, AttackerKB |
| Firewall / Vendor Advisories | Fortinet, Palo Alto, Cisco, CheckPoint, WatchGuard, Juniper, F5, Citrix, SonicWall, Sophos, Zyxel, Aruba, Barracuda, pfSense |
| News & Reports | SANS ISC, BleepingComputer, TheHackerNews, SecurityAffairs, DarkReading, SecurityWeek, InfoSecurity, HackRead |
| Microsoft | MSRC (REST API), Windows CVEs, Patch Tuesday |
| MITRE | ATT&CK Enterprise STIX bundle (691 techniques), CWE mapping |
| Other | CERT/NCSC, CISA Ransomware, Ubuntu Security, AI Incident Database, Huntr AI/ML CVEs |

---

## ⚙️ Architecture

```text
Threat Feeds (60 concurrent)
       ↓
ThreadPoolExecutor — parallel fetch with timeout handling
       ↓
Normalization & Deduplication
       ↓
Enrichment Layer
├── EPSS Scoring (FIRST.org)
├── AttackerKB Scoring
├── MITRE ATT&CK Mapping
├── ZDI Cross-correlation
├── MSF Module Coverage (Rapid7 — 3,000+ CVEs)
├── IP Geo/ASN Enrichment
└── NVD CVE Detail Enrichment
       ↓
Risk Scoring (CVSS + EPSS + KEV + Exploit + Activity)
       ↓
┌───────────────────────────────────────────────┐
│                  Output Layer                 │
├── PostgreSQL Database (persistent, indexed)   │
├── Excel Database (PowerBI-ready)              │
├── Interactive HTML Dashboard                  │
└── Email Report (Excel + HTML attached)        │
└───────────────────────────────────────────────┘
       ↓
┌───────────────────────────────────────────────┐
│              Host Defense Layer               │
│  Wazuh Agent (EC2)                            │
├── Log Collection                              │
├── File Integrity Monitoring                   │
├── Rootcheck & Syscollector                    │
├── Custom Detection Rules                      │
└── Active Response                             │
└───────────────────────────────────────────────┘
       ↓
Wazuh Manager
```

---

## 🗃️ Enrichment & Feed Cache Layer (v6.5.1)

All enrichment and correlation layers are now fully cached to eliminating redundant API calls on repeat runs and providing resilience against network failures.

| Feed / Enrichment | Cache File | TTL |
|---|---|---|
| NVD Vendor Advisories (all 14 vendors) | 24h |
| Vulners / CIRCL / NVD fallback  | 12h |
| FireHOL L1 + L2 blocklists  | 12h |
| Shodan InternetDB enrichment | 6h |
| LeakIX vulnerable hosts | 6h |
| LeakIX exposed services (per service) |6h |
| AbuseIPDB blacklist | 6h |
| EPSS scores (FIRST.org) | 6h |
| Feodo Tracker C2 IPs |2h |
| Talos / Community IP blacklist | 6h |
| Blocklist.de | 6h |
| Tor exit nodes  | 6h |
| Emerging Threats IPs  | 6h |
| MSF module coverage (Rapid7) | 24h |
| AttackerKB CVE enrichment | PostgreSQL DB skip | Permanent |

**Stale-cache fallback** — if any API is unreachable or rate-limited, the last successful result is served automatically. No silent data loss on network blips or API outages.

---
