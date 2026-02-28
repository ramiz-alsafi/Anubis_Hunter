# 🐺 Anubis v6.4.8 — Threat Intelligence Hunter

**Built and deployed by Ramiz Alsafi 👑**
🌐 Live at [anubispro.duckdns.org](https://anubispro.duckdns.org) | Hosted on AWS EC2

---

## What is Anubis?

Anubis is a self-hosted threat intelligence platform that runs fully automated on a schedule. It aggregates data from 50+ security feeds, enriches and cross-correlates everything it finds, and delivers a live interactive dashboard, a formatted database, and an email report — no manual steps involved.

The EC2 instance running Anubis is hardened and actively monitored. The platform defends itself just as much as it monitors the threat landscape.

---

## What it does

- Pulls from **50+ threat intelligence sources** across CVEs, exploits, malware, IP reputation, phishing, vendor advisories, and threat news
- Enriches every finding with **EPSS scores, CVSS data, MITRE ATT&CK mappings, KEV status, and exploit availability**
- Cross-correlates threats across all sources and risk-scores everything automatically
- Persists all data to a **PostgreSQL backend** with full historical tracking across runs
- Generates an **interactive HTML dashboard** served live at [anubispro.duckdns.org](https://anubispro.duckdns.org)
- Delivers a formatted **Excel database** and **email report** on every run
- The host is protected by a **Wazuh SIEM deployment** with active response and VirusTotal integration

---

## Sources

50+ feeds spanning:

- CVE & vulnerability databases
- Exploit intelligence
- Malware & IOC feeds
- IP reputation & blocklists
- Phishing feeds
- Threat intel platforms
- Vendor security advisories
- Security news aggregation
- Microsoft patch intelligence
- MITRE ATT&CK & ICS/OT feeds

---

## Stack

- **Python** — core engine
- **PostgreSQL** — persistent backend, 3,100+ threats tracked across runs
- **Nginx + Let's Encrypt** — HTTPS dashboard, live at [anubispro.duckdns.org](https://anubispro.duckdns.org)
- **Wazuh** — host defense, SIEM, active response
- **AWS EC2** — deployment
- **Postfix** — automated email delivery

---

## Public Dashboard

The dashboard updates automatically on every run and is live at **[anubispro.duckdns.org](https://anubispro.duckdns.org)**.

HTTPS only, TLS 1.2/1.3, hardened Nginx config, UFW firewall with locked-down inbound rules.

---

## Roadmap

| Phase | Status | Description |
|---|---|---|
| Phase 1–4 | ✅ Done | Core feeds, enrichment, Excel/HTML output, email alerts |
| Phase 5 | ✅ Done | PostgreSQL backend |
| Phase 6 | ✅ Done | Wazuh SIEM + host defense + public deployment |
| Phase 7 | 📋 Planned | Web dashboard — FastAPI + React |
| Phase 8 | 📋 Planned | Real-time alerting — Slack/Teams |
| Phase 9 | 📋 Planned | ML-based risk prediction |
| Phase 10 | 📋 Planned | Cloud-native deployment |

---

## Disclaimer

Built for defensive security purposes. All data is sourced from publicly available threat intelligence feeds. Use responsibly.

---

## License

MIT — see LICENSE for details.

---

*Anubis — because knowing what's out there is the first step to defending against it.*
