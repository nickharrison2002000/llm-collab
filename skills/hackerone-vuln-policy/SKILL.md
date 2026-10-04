---
name: hackerone-vuln-policy
description: Defines what qualifies as a real, payable vulnerability and the strict rules for HackerOne-style programs. Covers vulnerability definition, reporting scope, core ineligible findings, good-faith obligations, and safe harbor. Use when deciding eligibility, filtering out low-value or out-of-scope work, preparing reports, or protecting against wasted effort that does not lead to payouts.
---

# HackerOne Vulnerability Policy

Apply these definitions and rules whenever classifying findings, deciding whether a report is valid, writing or reviewing HackerOne submissions, or advising on testing boundaries.

## Vulnerability Definition

A vulnerability is a software bug that would allow an attacker to perform an action in violation of an expressed security policy. A bug that enables escalated access or privilege is a vulnerability. Design flaws and failures to adhere to security best practices may qualify as vulnerabilities.

Weaknesses exploited by viruses, malicious code, and social engineering are not considered vulnerabilities.

## Vulnerability Reporting Scope

When evaluating or reporting potential vulnerabilities, require both:

1. Realistic attack scenarios
2. Demonstrable security impact

The attack must be realistic and impactful. Verification does not require performing malicious actions — confirm the vulnerability exists without causing damage or revealing customer data.

## Core Ineligible Findings

Treat the following as out of scope (list is not exhaustive):

### 1. Theoretical vulnerabilities requiring unlikely user interaction or circumstances

- Vulnerabilities only affecting users of unsupported or End-of-life browsers or operating systems
- Broken link hijacking
- Tabnabbing
- Content spoofing and text injection issues
- Attacks requiring physical access to a device (without prior written authorization)
- Self-exploitation such as self-XSS or self-DoS (unless it can be used to attack a different account)

### 2. Theoretical vulnerabilities without real-world security impact

- Clickjacking on pages with no sensitive actions
- Cross-Site Request Forgery (CSRF) on forms with no sensitive actions (e.g., Logout)
- Permissive CORS configurations without demonstrated security impact
- Software version disclosure / Banner identification issues / Descriptive error messages or headers (e.g., stack traces, application, or server errors)
- Comma Separated Values (CSV) injection
- Open redirects (unless additional security impact is demonstrated)

### 3. Optional security hardening steps / Missing best practices

- SSL/TLS Configurations
- Lack of SSL Pinning
- Lack of jailbreak detection in mobile apps
- Cookie handling (e.g., missing HttpOnly/Secure flags)
- Content-Security-Policy configuration opinions
- Optional email security features (e.g., SPF/DKIM/DMARC configurations)
- Most issues related to rate limiting

### 4. Vulnerabilities requiring hazardous testing (must not be attempted unless explicitly pre-authorized)

- Issues relating to excessive traffic/requests (e.g., DoS, DDoS)
- Any other issues where testing may affect the availability of systems
- Social engineering of employees, contractors, vendors, or service providers (e.g., phishing, opening support requests)
- Attacks that are noisy to users or admins (e.g., spamming notifications or forms)
- Physical attacks against employees, offices, and data centers
- Targeting assets of customers
- Any vulnerability obtained through the compromise of customer or employee accounts
- Knowingly posting, transmitting, uploading, linking to, or sending malware
- Pursuing vulnerabilities which send unsolicited bulk messages (spam)

## Good Faith Security Research

All research must be conducted in good faith. Enforce these requirements:

- Follow this policy and any other relevant agreements with the program
- Research must consist exclusively of good faith testing, investigation, or correction of a security flaw, with the primary goal of promoting the safety of the class of devices, machines, or online services involved
- Do not violate customers’ security and privacy, and do not harm individuals or the public
- Proceed only as far as necessary to demonstrate or clarify the security issue, and no further
- If a vulnerability provides unintended access to data, limit the amount of data accessed to the minimum required for an effective proof of concept. Stop research and submit a report immediately upon encountering any user data (personal information, financial information, or proprietary information)
- Report findings within 72 hours of determining a potential security concern via the Vulnerability Disclosure Program on HackerOne
- Provide a reasonable amount of time to resolve the issue before any public disclosure
- No stunt hacking
- No extortion or harassment

## Safe Harbor

Good Faith Security Research is considered authorized activity protected from adversarial legal action by the program owner. While the program is active, the program owner:

- Will not bring legal action against the researcher or report them for Good Faith Security Research, including for bypassing technological measures used to protect applications in scope
- Will take steps to make known that the researcher conducted Good Faith Security Research if someone else brings legal action against them

Safe harbor does **not** waive the right to pursue remedies against activities targeting other customers’ resources, operations, or end users, including but not limited to:

- Unauthorized cross-customer environment access
- Manipulation, monitoring, or collection
- Spoofing
- Social engineering, including phishing
- Impersonating employees, services, or products
- Impersonating customer marketplace offerings (e.g., AMIs, container images, templates, models)
- Impersonating any other company, their employees, services, products, or offerings
- Provisioning resources to mimic infrastructure or customer resources
- Denial of Service, Distributed Denial of Service, simulated DoS, or simulated DDoS
- Port, protocol, or request flooding
- Any type of brute forcing
- IP or resource cycling/churning
- DNS hijacking, pharming, or zone walking via Amazon Route 53
- Stunt hacking

## How to Apply This Skill

- When classifying a finding, first check it against the Vulnerability Definition, then against the Core Ineligible Findings lists.
- When writing or reviewing a report, confirm realistic attack scenario + demonstrable impact, and that testing stayed within Good Faith boundaries.
- When advising on testing plans, explicitly call out any hazardous testing categories that require pre-authorization.
- Reject or deprioritize reports that fall into theoretical, no-impact, or hardening-only categories unless clear additional impact is shown.
