# Backsender

[![CI](https://github.com/amne51ac/backsender/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/amne51ac/backsender/actions/workflows/ci.yml)

## Overview

**Backsender** is a Python-based tool designed for the ethical testing of email systems’ resilience against spoofing and backscatter attacks. It allows users to simulate scenarios wherein emails with spoofed sender addresses and non-existent recipient addresses are generated. The tool helps assess the robustness of email filtering systems and security mechanisms.

Visit our website: [backsender.com](https://backsender.com) for more information.

## Understanding the Attack

### Backscatter Attack

A backscatter attack exploits how email servers handle undeliverable messages. By spoofing legitimate users' email addresses:

1. An attacker sends emails to non-existent addresses.
2. The receiving server returns Non-Delivery Reports (NDRs) or bounce-back messages to the spoofed sender.
3. This can flood the legitimate user's inbox, potentially causing denial of service (DoS).

### Risks and Impact

- **Denial of Service**: Overwhelming inboxes makes legitimate communication difficult.
- **Reputation Damage**: Being associated with bounce-back messages can harm domain reputation.
- **Security Noise**: Spike in bounce traffic can create unnecessary alerts.

## How Backsender Works

Backsender operates in two modes:

1. **Simulate**: A local SMTP server is run to capture outgoing emails.
2. **Send**: Emails are sent using specified SMTP server details, testing against real email systems.

### Key Features

- Multiple spoofed senders
- Random generation of non-existent email addresses for specified domains
- Configurable volume of emails per domain

## Planned Improvements

- **Rate Limiting**: Manage the sending rate for load testing.
- **Advanced Headers**: Enhance spoofing with more header options.
- **Enhanced Logging**: Provide detailed logs and reports for analysis.

## Usage Instructions

### Prerequisites

- Python 3.x
- SMTP server access (for send mode)

### Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd backsender
   ```

2. **Install Dependencies** (for use):
   ```bash
   pip install -r requirements.txt
   ```
   **OR Install dev dependencies** (for development):
   ```bash
   pip install -r requirements-dev.txt
   ```

### Running Backsender

#### Simulate SMTP Server

Run a local SMTP server:
```bash
python backsender.py --mode simulate --server-port 1025
```

#### Send Spoofed Emails

To send emails using an actual SMTP server:
```bash
python backsender.py --mode send --smtp-server smtp.example.com --smtp-port 587 --smtp-user your_email@example.com --smtp-password your_password --spoofed-senders spoof1@yourdomain.com spoof2@yourdomain.com --domain-list targetdomain1.com targetdomain2.com --num-emails-per-domain 5
```

### Parameters

- `--mode`: Choose "simulate" to run an SMTP server or "send" to send emails.
- `--smtp-server`: SMTP server address for sending.
- `--smtp-port`: SMTP server port (default: 587).
- `--smtp-user`: SMTP user authentication.
- `--smtp-password`: SMTP password.
- `--spoofed-senders`: List of email addresses for spoofing.
- `--domain-list`: Domains for non-existent email generation.
- `--num-emails-per-domain`: Number of emails per domain.
- `--server-port`: Local SMTP server port (default: 1025).

## Ethical Considerations

Conduct all testing within authorized environments and with explicit permission. Unlawful spoofing and testing are against legal and ethical standards.

## Contribution

Contributions, bug reports, and feature suggestions are welcome. Please open an issue or submit a pull request to contribute.

## License

Backsender is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
