# SupportPulse 🛠️

**Application Health & Troubleshooting Toolkit**

SupportPulse is a lightweight Python-based support engineering tool that analyzes application logs, checks REST API health, monitors local system resources, classifies common production issues, and tracks incidents.

## Why this project?

Support engineers often spend time manually reviewing logs, checking APIs, and collecting system information. SupportPulse demonstrates how some of these repetitive checks can be automated.

## Features

- Application log analysis
- Error and warning detection
- HTTP 500 detection
- Database timeout detection
- Authentication failure detection
- Rule-based issue classification
- REST API health checks
- CPU, memory and disk monitoring
- SQLite incident tracking
- Automated tests
- GitHub Actions CI

## Technology

- Python
- Streamlit
- Requests
- psutil
- SQLite
- Git / GitHub
- GitHub Actions

## Architecture

```text
Application Logs
       |
       v
   Log Analyzer
       |
       v
Issue Classification
       |
       +------> Incident Database
       |
       v
 Streamlit Dashboard

REST API ------> Health Checker
Local Machine -> System Monitor
```

## Run locally

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

Run the dashboard:

```bash
streamlit run app.py
```

## Example troubleshooting scenarios

### INC-001 — Database Connectivity

The sample database failure log contains database timeouts and HTTP 500 responses. SupportPulse classifies this as a high-priority database connectivity/performance issue and recommends checking database availability, connection pools and SQL errors.

### INC-002 — Application Error

The API failure log contains HTTP 500 responses and a NullPointerException. SupportPulse classifies this as an application error and recommends reviewing the stack trace and recent changes.

### INC-003 — Authentication

Authentication failures are detected and classified separately so that credentials, permissions and security configuration can be investigated.

## Interview discussion

The project demonstrates:

- Log analysis
- Production troubleshooting
- REST API monitoring
- System health monitoring
- SQL/SQLite
- Python automation
- Testing
- GitHub Actions CI
- Incident documentation
