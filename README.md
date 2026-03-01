<img width="1252" height="768" alt="Gemini_Generated_Image_5v5rnd5v5rnd5v5r" src="https://github.com/user-attachments/assets/f2171717-ff15-404a-93dc-a6d811ec88b2" />


🐺 Anubis — The Ultimate Threat Intelligence Hunter
A high-performance automated threat intelligence platform that aggregates, analyzes, and reports on global security risks in real-time. Designed to provide instant visibility into the evolving threat landscape.
By Ramiz Alsafi | Deployed on AWS EC2 | v6.5.0

👁️ What is Anubis?
Anubis is your personal "Eye in the Sky" for cybersecurity. It operates 24/7 to scan the digital horizon, identifying vulnerabilities and active attacks before they hit your infrastructure.
Unified Intelligence: Combines 60 world-class security feeds into one single source of truth.
Deep Enrichment: Automatically pulls exploit data, attacker behavior (MITRE ATT&CK), and severity scores for every threat.
Intelligent Risk Scoring: Not all threats are equal. Anubis calculates risk based on exploit availability, attacker activity, and your specific industry.
Actionable Reporting: Generates professional-grade Excel databases and interactive web dashboards for stakeholders.
Built-in Resilience: The platform doesn't just hunt; it defends itself using a Wazuh-integrated host defense system.

📡 The Intelligence Network (60+ Sources)
Anubis monitors the most critical categories of the web to ensure no threat goes unnoticed:
Global Vulnerabilities: NVD, CISA KEV, and major vendor advisories (Cisco, Palo Alto, Fortinet).
Exploit & Malware Watch: Live tracking of MalwareBazaar, Exploit-DB, and Zero-Day Initiatives.
Dark Web & Reputation: Monitoring IP reputations, Phishing URLs, and leaked credentials via AlienVault and Shodan.
Industry News: Real-time updates from SANS, BleepingComputer, and TheHackerNews.

📊 Interactive Command Center
The Anubis Dashboard is a self-contained, interactive portal designed for rapid decision-making:
Strategic Overview: Visual breakdowns of risk levels, remediation priorities, and threat trends over time.
The Risk Calculator: A financial tool where you can input your budget and environment details to see your Annual Risk Exposure and Security ROI.
MITRE ATT&CK Matrix: A live-computed map showing exactly which attacker techniques are currently trending.
Compliance & GRC: Instant scoring against ISO 27001, NIST, SOC 2, and PCI DSS. It identifies your compliance gaps based on live threat data.
Incident Response Playbooks: Dynamically generated "How-To" guides for responding to the specific threats found in each report.

🛡️ Self-Defending Architecture
Anubis is hosted on a hardened AWS EC2 instance. It utilizes an integrated Defense Layer to monitor its own health and security:
Real-time Monitoring: Constant surveillance of system logs and file integrity.
Active Response: Automatically blocks suspicious IPs or unauthorized access attempts.
Audit Trails: Full tracking of all system changes and administrative actions.

🔢 Performance Snapshot (v6.5.0)
Metric
Status
Active Intelligence Sources
37 (6,933+ records)
Enriched CVE Records
1,168 Scored
Threat Mappings
691 MITRE Techniques
Active Exploits Tracked
1,529 (CISA KEV)
System Failures
0 (Stable)

📡 Data Sources (60 Concurrent)
Category	Sources
CVE / Vulnerability	NVD, CISA KEV, VulnCheck KEV, RedHat, GitHub Advisories, CIRCL, OSV.dev, Vulners
Exploit Intelligence	Exploit-DB, ZDI (Zero Day Initiative), Metasploit (Rapid7), PacketStorm, Vulners
Malware / IOC	MalwareBazaar, ThreatFox, URLHaus, Hybrid Analysis, Abuse.ch SSLBL
IP Reputation	AbuseIPDB, Shodan InternetDB, Feodo Tracker, Talos, Emerging Threats, Blocklist.de, FireHOL L1+L2, IPsum, Tor Exit Nodes
Phishing	OpenPhish, URLScan.io
Threat Intel Platforms	AlienVault OTX, LeakIX, AttackerKB
Firewall / Vendor Advisories	Fortinet, Palo Alto, Cisco, CheckPoint, WatchGuard, Juniper, F5, Citrix, SonicWall, Sophos, Zyxel, Aruba, Barracuda, pfSense
News & Reports	SANS ISC, BleepingComputer, TheHackerNews, SecurityAffairs, DarkReading, SecurityWeek, InfoSecurity, HackRead
Microsoft	MSRC (official REST API), Windows CVEs, Patch Tuesday
MITRE	ATT&CK Enterprise STIX bundle (691 techniques/sub-techniques), CWE mapping
Other	CERT/NCSC, CISA Ransomware, Ubuntu Security, AI Incident Database, Huntr AI/ML CVEs
⚙️ Architecture
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
📊 Interactive Dashboard
The generated HTML dashboard is fully self-contained (no backend, no external libraries) and includes:

Overview Tab

Risk level distribution, top threat types, remediation priority breakdown
EPSS score distribution with coverage badge
Exploit status breakdown, confidence scoring, patch availability
Threats over time — Daily / Weekly / Monthly toggle (builds across runs)
Risk heatmap — Type × Severity
MITRE ATT&CK Tactic Coverage — live-computed from all 691 mapped techniques
Live TTP simulation — click any kill chain phase to expand Sigma rules, red/blue team guidance
Full filterable threat table (50+ columns, paginated, exportable to CSV)
Detection Rules Tab — Wazuh/Sigma, Suricata IPS, and hardening checklists generated per-threat

Incident Response Tab — Structured IR playbooks mapped to MITRE tactics

Risk Calculator Tab — Input your budget, incident frequency, patch velocity, detection coverage, and MTTR. Returns annual risk exposure, projected savings, and priority recommendations — all computed from your live threat dataset.

GRC & Compliance Tab — ISO/IEC 27001:2022 Annex A and NIST SP 800-53 Rev 5 controls scored and color-coded based on actual threat composition. Open compliance gaps surfaced automatically.

Sandbox & Emulation Tab (Coming Soon) — Isolated emulation environment for testing exploits and CVEs from the dataset against your own stack without touching production.

🗺️ Project Evolution
Phase 1–6: ✅ Core Intelligence, Database Persistence, and Host Defense.
Phase 6.4: ✅ Dashboard v2 — Risk Calculator, GRC Compliance, and Interactive MITRE mapping.
Phase 7: 🔄 Web Evolution — Transitioning to a live Web Portal (FastAPI/React).
Phase 8: 📋 The Sandbox — Isolated environment for safe exploit testing.
Phase 9: 📋 Instant Alerts — Real-time Slack and Teams notification system.

Anubis — because knowing what's out there is the first step to defending against it.
