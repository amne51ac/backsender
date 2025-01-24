.. backsender documentation master file, created by
   sphinx-quickstart on Thu Oct 14 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to backsender's documentation!
======================================

Overview
--------

**Backsender** is a Python-based tool designed for the ethical testing of email systems’ resilience against spoofing and backscatter attacks. It allows users to simulate scenarios wherein emails with spoofed sender addresses and non-existent recipient addresses are generated. The tool helps assess the robustness of email filtering systems and security mechanisms.

Visit our website: `backsender.com <https://backsender.com>`_ for more information.

Understanding the Attack
------------------------

**Backscatter Attack**

A backscatter attack exploits how email servers handle undeliverable messages. By spoofing legitimate users' email addresses:

1. An attacker sends emails to non-existent addresses.
2. The receiving server returns Non-Delivery Reports (NDRs) or bounce-back messages to the spoofed sender.
3. This can flood the legitimate user's inbox, potentially causing denial of service (DoS).

**Risks and Impact**

- **Denial of Service**: Overwhelming inboxes makes legitimate communication difficult.
- **Reputation Damage**: Being associated with bounce-back messages can harm domain reputation.
- **Security Noise**: Spike in bounce traffic can create unnecessary alerts.

How Backsender Works
--------------------

Backsender operates in two modes:

1. **Simulate**: A local SMTP server is run to capture outgoing emails.
2. **Send**: Emails are sent using specified SMTP server details, testing against real email systems.

**Key Features**

- Multiple spoofed senders
- Random generation of non-existent email addresses for specified domains
- Configurable volume of emails per domain

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
