---
name: bug-classification
description: Classifies vulnerabilities by real impact into actionable/exploitable versus self-contained so time is spent only on findings that can produce payouts. Use when deciding whether a bug can affect other users or shared infrastructure and therefore deserves deep investigation or should be deprioritized.
---

# Bug Classification by Impact Scope

Use this skill to classify security vulnerabilities into two distinct impact categories based on their potential reach and exploitability.

## Category 1: Actionable/Exploitable Vulnerabilities

**Definition:** Vulnerabilities that can be exploited by attackers for personal gain, affect multiple customers, or cause financial/commercial loss to the company.

**Key Characteristics:**
- Attacker can leverage the vulnerability against other users, tenants, or the system
- Has potential for widespread impact beyond the initiating user
- May result in data breaches, financial loss, reputational damage, or compliance violations
- Typically requires immediate remediation priority

**Examples:**
- Stored/Reflected XSS (affects all users who view the malicious content)
- SQL Injection (can access/modify shared database resources)
- Remote Code Execution (RCE)
- CSRF (Cross-Site Request Forgery - forces actions on behalf of users)
- DoS attacks against internal infrastructure (affects all users)
- Authentication bypass (allows unauthorized access to any account)
- Privilege escalation (grants elevated access to system resources)
- Server-side request forgery (SSRF) targeting internal services

## Category 2: Self-Contained Vulnerabilities

**Definition:** Vulnerabilities that are isolated to the user's own browser/session and cannot reach or impact other tenants, users, or shared infrastructure.

**Key Characteristics:**
- Only affects the specific user who triggers the vulnerability
- Cannot be weaponized against other users or systems
- Limited blast radius (single user session/browser)
- Typically lower remediation priority, though still important to fix

**Examples:**
- Self-XSS (user must execute malicious script themselves via their own input)
- DoS that only affects the user's own browser (e.g., excessive client-side computation)
- Client-side validation bypass that only affects the user's own data display
- Browser-specific rendering issues that don't expose data
- Local storage manipulation that only affects the current user's session
- Console errors that only impact the current user's debugging experience

## Classification Decision Tree

To determine which category a vulnerability belongs to, answer these questions:

1. **Can an attacker exploit this vulnerability to affect users other than themselves?**
   - Yes → **Actionable/Exploitable**
   - No → Go to question 2

2. **Can this vulnerability impact shared infrastructure, data, or services?**
   - Yes → **Actionable/Exploitable**
   - No → Go to question 3

3. **Does the vulnerability require the user to perform an action that cannot be forced on others?**
   - Yes → **Self-Contained**
   - No → **Actionable/Exploitable**

## Usage Notes

- When in doubt, default to **Actionable/Exploitable** for conservative classification
- Document the reasoning for each classification decision
- Re-evaluate classifications as new information about the vulnerability emerges
- Consider the specific architecture and multi-tenancy model of your system when classifying
