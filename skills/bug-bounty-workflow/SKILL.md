---
name: bug-bounty-workflow
description: Career-critical orchestrator for bug-bounty hunting that protects and maximizes income. Forces focus on Critical and High actionable findings only, blocks social-engineering and informational-only work, and sequences the full pipeline of policy checks, impact classification, scientist investigation, PoC verification, and high-quality reporting. Use on every security finding, testing plan, scope question, report, or hunting session.
---

# Bug Bounty Workflow Orchestrator

This skill is the permanent conductor for all bug-bounty work. It exists so every session maximizes the chance of paid, high-impact findings while staying strictly inside program rules. Treat every request as professional work that directly affects the researcher’s income.

## Hard Rules (Never Violate)

1. **Always prefer Critical / High actionable findings.**  
   Deprioritize or abandon Medium, Low, or Self-Contained issues unless they clearly escalate. Time spent on low-value work is money lost.

2. **Never suggest or assist with social-engineering tests.**  
   Phishing, pretexting, support-ticket social engineering, employee targeting, or any human-manipulation techniques are permanently out of scope.

3. **Never pursue or recommend informational-only disclosures.**  
   Pure version disclosure, missing headers, best-practice opinions, or findings with no realistic security impact waste reviewer time and damage reputation. Kill them early.

## Core Pipeline (Follow in Order)

### Phase 0 — Immediate Filters (Always First)

On any potential finding or testing idea:

1. Load **hackerone-vuln-policy**.
2. Apply the Vulnerability Definition and Core Ineligible Findings lists.
3. Load **bug-classification**.
4. Classify as Actionable/Exploitable vs Self-Contained.
5. Decision gate:
   - Out-of-scope or Ineligible → stop, explain why, do not invest further time.
   - Self-Contained or informational → stop or deprioritize heavily.
   - Actionable + realistic impact (especially Critical/High) → proceed.

### Phase 1 — Investigation

When a lead exists but the vulnerability cannot yet be triggered:

- Load **scientist**.
- Scientist will itself load **serpapi** for historical exploit and report research.
- Exhaust source analysis and payload testing until the issue is either confirmed or proven secure.

### Phase 2 — Verification & Documentation

When a working trigger is obtained:

- Load **poc**.
- Produce only clean, successful, reproducible evidence.
- Discard failed attempts after verification.
- Capture full request/response, minimal working payload, and exact conditions.

### Phase 3 — Report Writing

When ready to submit:

- Structure every report exactly like the gold-standard example in `references/hackerone-report-example.md`.
- Required sections (in order):
  1. **Summary** — One tight paragraph stating the vulnerability and its severity.
  2. **Verified Code Path** — Exact files, functions, and lines that prove the bug (when source is available).
  3. **Steps To Reproduce** — Numbered, complete, runnable by a third party.
  4. **Verified Evidence** — Raw logs, PoC output, cryptographic verification, environment details.
  5. **Supporting Material/References** — Attachments (PoC code, screenshots, etc.).
  6. **Impact** — Concrete attacker capabilities, direct consequences, realistic exploitation scenario, and prerequisites.
- Load **no-redaction** for the entire report and any accompanying PoC code or scripts. No silent omissions, no untracked placeholders.
- Keep language precise, technical, and free of hype. Reviewers reward clarity and completeness.

### Phase 4 — Tooling & Automation

When the user asks to add a feature, script, scanner, or capability:

- Load **the-bigger-picture**.
- Deliver a complete, tested implementation, not an isolated fragment.

## Skill Loading Map

| Situation | Load These Skills |
|-----------|-------------------|
| Any potential finding or scope question | hackerone-vuln-policy + bug-classification |
| Cannot trigger a suspected bug | scientist (+ serpapi) |
| Have a working trigger | poc |
| Writing or editing a report / PoC / script | no-redaction |
| Adding a tool, feature, or automation | the-bigger-picture |
| Historical research, CVE, or public report lookup | serpapi |

Always load this orchestrator skill first on security-related requests so the above decisions are made consciously.

## Quality & Survival Principles

- Time is the scarce resource. Filter aggressively at Phase 0.
- A single well-documented Critical/High report is worth more than ten informational tickets.
- Stay inside good-faith boundaries at all times (see hackerone-vuln-policy).
- Report within 72 hours of confirming a real issue.
- Never cause damage, access unnecessary data, or target customer assets.
- When in doubt about eligibility or impact, ask the user for clarification before deep work.

## Report Template (Canonical Structure)

```markdown
## Summary
[One tight paragraph: what is broken, why it matters, severity]

## Verified Code Path
[Numbered list of exact files/functions/lines that prove the issue]

## Steps To Reproduce
[Complete environment setup + numbered reproduction steps]

## Verified Evidence
[Environment details, raw logs, PoC output, cryptographic or behavioral proof]

## Supporting Material/References
[List of attached PoC files, screenshots, etc.]

## Impact
[Direct consequences, exploitation scenario, attack prerequisites]
```

See `references/hackerone-report-example.md` for a complete real-world example of this structure used successfully.

## Quick Decision Checklist

Before investing serious time, answer:

- [ ] Does it meet the Vulnerability Definition?
- [ ] Is it free of every Core Ineligible Finding category?
- [ ] Is the attack realistic and impactful?
- [ ] Is it Actionable/Exploitable (affects other users or shared infrastructure)?
- [ ] Is severity realistically Critical or High?
- [ ] Can it be demonstrated without social engineering, DoS, or customer data access?

If any answer is “no”, stop or deprioritize.
