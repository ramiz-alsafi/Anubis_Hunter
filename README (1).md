# 🐍 Anubis -- Automated Threat Intelligence Hunter

**Anubis** is an automated threat intelligence aggregation and
enrichment platform designed to collect, analyze, correlate, and
prioritize cybersecurity threats from multiple global sources in real
time.

It acts as a **mini Threat Intelligence Platform (TIP)** and SOC
assistant, transforming raw security feeds into actionable intelligence
with risk scoring and remediation guidance.

------------------------------------------------------------------------

## 🚀 Features

### 🔍 Multi-Source Threat Intelligence Collection

Anubis gathers data from 40+ security feeds including:

-   NVD (CVE database)
-   CISA KEV exploited vulnerabilities
-   Exploit-DB
-   MalwareBazaar & ThreatFox
-   URLHaus & OpenPhish
-   Shodan, Censys, LeakIX
-   Vendor advisories (Cisco, Fortinet, Palo Alto, Juniper, etc.)
-   Security news feeds (SANS, DarkReading, BleepingComputer, etc.)

------------------------------------------------------------------------

### 🧩 IOC & Threat Enrichment

-   IP reputation and geo-context enrichment (ip-api + AbuseIPDB)
-   URL analysis via URLScan
-   Exploit detection via Metasploit module mapping
-   MITRE ATT&CK technique mapping using CWE + keyword correlation

------------------------------------------------------------------------

### 📊 Risk Scoring & Prioritization Engine

-   CVSS scoring
-   Likelihood × Impact risk matrix
-   EPSS exploitation probability scoring
-   AttackerKB exploitation maturity scoring
-   Automated remediation priority classification (P1--P4)
-   Confidence scoring based on source reliability

------------------------------------------------------------------------

### 📨 Automated Reporting

-   Excel threat intelligence reports
-   Interactive HTML dashboard
-   Automated email alerts with attachments
-   Hourly scheduled execution with run-state tracking

------------------------------------------------------------------------

## 🧠 Architecture Overview

Threat Feeds → Normalization → Enrichment → MITRE Mapping\
                        ↓\
               Risk & Priority Engine\
                        ↓\
               Reports (Excel + HTML + Email)

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   Python 3
-   Requests, Pandas, BeautifulSoup
-   Feedparser, Pytz
-   SMTP email automation
-   Threat intelligence APIs (NVD, AbuseCH, Shodan, Censys, etc.)

------------------------------------------------------------------------

## ⚙️ Installation

### 1️⃣ Clone the repository

``` bash
git clone https://github.com/yourusername/anubis-threat-hunter.git
cd anubis-threat-hunter
```

### 2️⃣ Install dependencies

``` bash
pip install -r requirements.txt
```

### 3️⃣ Configure API Keys (Recommended via Environment Variables)

``` bash
export VULNERS_API_KEY="your_key"
export SHODAN_API_KEY="your_key"
export ABUSEIPDB_API_KEY="your_key"
export CENSYS_API_ID="your_id"
export CENSYS_API_SECRET="your_secret"
```

------------------------------------------------------------------------

## ▶️ Usage

Run manually:

``` bash
python3 Anubis_v6_3.py
```

Schedule hourly execution with cron:

``` bash
0 * * * * python3 /path/to/Anubis_v6_3.py
```

------------------------------------------------------------------------

## 📁 Output

Anubis generates: - threat_intelligence_log.xlsx → Structured threat
data - dashboard.html → Interactive visualization - Email alerts with
attachments

------------------------------------------------------------------------

## 🔐 Security Notes

-   API keys are loaded via environment variables
-   Base64 fallback keys are obfuscated (not plaintext)
-   Recommended to use .env or secret managers in production

------------------------------------------------------------------------

## 🎯 Use Cases

-   SOC threat monitoring
-   Vulnerability management automation
-   Blue team threat hunting
-   Security research & labs
-   Enterprise cyber threat intelligence pipelines

------------------------------------------------------------------------

## 🧪 Roadmap

-   PostgreSQL backend storage
-   Web-based SOC dashboard
-   Real-time alerting via Slack/Discord/Teams
-   Machine learning risk prediction
-   Cloud deployment (AWS / Azure)

------------------------------------------------------------------------

## 👨‍💻 Author

**Ramiz Alsafi**\
Cybersecurity Engineer & Threat Researcher

------------------------------------------------------------------------

## ⚠️ Disclaimer

This project is for **educational and defensive security research
purposes only**.\
Do not use it for unauthorized scanning or offensive activities.
