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

🔢 Performance Snapshot (v6.4.9)
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


🗺️ Project Evolution
Phase 1–6: ✅ Core Intelligence, Database Persistence, and Host Defense.
Phase 6.4: ✅ Dashboard v2 — Risk Calculator, GRC Compliance, and Interactive MITRE mapping.
Phase 7: 🔄 Web Evolution — Transitioning to a live Web Portal (FastAPI/React).
Phase 8: 📋 The Sandbox — Isolated environment for safe exploit testing.
Phase 9: 📋 Instant Alerts — Real-time Slack and Teams notification system.

Anubis — because knowing what's out there is the first step to defending against it.
