---
name: poc
description: Verifies and documents clean, reproducible proofs of concept for high-value vulnerabilities. Confirms the bug is real, keeps only successful payloads and full request/response evidence, and discards failed attempts so reports are submission-ready and maximize chance of acceptance and payout.
---

# POC: Vulnerability Proof of Concept Verification & Documentation

Load this skill after a potential vulnerability has been identified and you need to:
- Verify the vulnerability is real and exploitable
- Validate the steps that led to its discovery
- Document only the successful exploitation (discard all failed attempts)

This skill ensures that every confirmed vulnerability has a reproducible, well-documented proof of concept with complete technical details.

## Core Principle

Only successful, verified exploitation data is stored. Failed attempts, non-working payloads, and dead-end paths are captured for verification, then discarded. This keeps documentation clean, actionable, and focused solely on what works.

## Workflow

### Phase 1: Vulnerability Verification

1. **Reproduce the Discovery**
   - Re-execute the exact steps that initially identified the vulnerability
   - Use the same environment, configuration, and context
   - Confirm the vulnerability triggers consistently

2. **Isolate the Trigger**
   - Identify the minimal working payload that exploits the vulnerability
   - Strip away any unnecessary components
   - Confirm it works in isolation

3. **Test Consistency**
   - Execute the PoC multiple times to ensure reliability
   - Test across different sessions/contexts if applicable
   - Document any conditions required for successful exploitation

### Phase 2: Step Validation

4. **Trace the Discovery Path**
   - Review how the vulnerability was originally found (from scientist skill or other)
   - Reconstruct the exact sequence of actions
   - Identify which specific test, payload, or mutation triggered the vulnerability

5. **Verify Each Critical Step**
   - For each step in the discovery process:
     - Confirm it was necessary to reach the vulnerability
     - Document the purpose of each step
     - Remove redundant or unnecessary steps

### Phase 3: Complete Documentation (Successful Attempts Only)

6. **Document the Endpoint**
   - Full URL: Complete endpoint path including protocol, domain, path, and query parameters
   - HTTP Method: GET, POST, PUT, DELETE, PATCH, etc.
   - Endpoint Type: REST API, GraphQL, WebSocket, RPC, etc.
   - Authentication Context: Authenticated/Unauthenticated, user role, session state
   - Technology Stack: Framework, language, server, database (if known)

7. **Document the Full Request**
   - Headers: All request headers (including Content-Type, Authorization, custom headers)
   - Body: Complete request body (raw, not parsed/interpreted)
   - Parameters: All parameters with their exact values (query string, path params, form data)
   - Cookies: Any session or authentication cookies
   - Timing: Timestamp of the request

8. **Document the Full Response**
   - Status Code: HTTP status code received
   - Headers: All response headers
   - Body: Complete response body (raw)
   - Timing: Response time, timestamp
   - Behavior: Observed behavior (error messages, data exposure, code execution, etc.)

9. **Document the Payload**
   - Raw Payload: Exact payload that triggered the vulnerability (before any encoding)
   - Encoded Payload: Payload as it appears in the request (after encoding)
   - Payload Type: SQL injection, XSS, command injection, etc.
   - Payload Structure: How the payload was constructed
   - Obfuscation: Any encoding, escaping, or obfuscation applied

10. **Document the Vulnerability**
    - Type: RCE, SQLi, XSS, IDOR, SSRF, etc.
    - Severity: Critical, High, Medium, Low (based on impact)
    - Impact: What an attacker can achieve (data access, code execution, DoS, etc.)
    - Root Cause: Underlying issue (missing validation, improper sanitization, etc.)
    - Affected Versions: Software versions known to be vulnerable
    - Fixed Versions: If known, versions where the issue is patched

### Phase 4: Data Handling

11. **Capture All Attempts**
    - During verification, capture all test attempts (successful and failed)
    - Log each with: timestamp, payload/request, response, outcome

12. **Verify Each Attempt**
    - For each captured attempt, verify if it successfully triggered the vulnerability
    - Classify as: SUCCESS or FAIL

13. **Process Based on Outcome**
    - For SUCCESSFUL attempts:
      - STORE the complete documentation (from Phase 3)
      - Tag with metadata (vulnerability type, severity, date, etc.)
      - Archive in the POC repository
      - Generate a unique POC ID for reference
    - For FAILED attempts:
      - VERIFY they truly failed (not a false negative)
      - EXTRACT any useful diagnostic information (why it failed)
      - DELETE the attempt data (do not store)
      - Document only the failure reason in a summary (not the full payload)

## Documentation Standards

### What MUST Be Stored (Successful Only)

```
POC ID: [UNIQUE_ID]
Vulnerability Type: [RCE/SQLi/XSS/etc.]
Severity: [Critical/High/Medium/Low]
Date Discovered: [YYYY-MM-DD]
Date Verified: [YYYY-MM-DD]
---
### ENDPOINT
URL: [FULL_URL]
Method: [HTTP_METHOD]
Type: [REST/GraphQL/WebSocket/etc.]
Authentication: [Auth/Unauth, Role: ...]
---
### REQUEST
Headers:
[HEADER_NAME]: [HEADER_VALUE]
...
Body:
[RAW_BODY]
Parameters:
[PARAM_NAME]=[PARAM_VALUE]
...
Cookies:
[COOKIE_NAME]=[COOKIE_VALUE]
...
---
### PAYLOAD
Raw: [EXACT_PAYLOAD]
Encoded: [ENCODED_PAYLOAD]
Type: [PAYLOAD_TYPE]
Obfuscation: [ENCODING_APPLIED]
---
### RESPONSE
Status: [HTTP_STATUS]
Headers:
[HEADER_NAME]: [HEADER_VALUE]
...
Body:
[RAW_RESPONSE_BODY]
Behavior: [OBSERVED_BEHAVIOR]
---
### VULNERABILITY DETAILS
Root Cause: [DESCRIPTION]
Impact: [WHAT_ATTACKER_CAN_DO]
Affected Versions: [VERSIONS]
Fixed Versions: [FIXED_VERSIONS]
---
### DISCOVERY PATH
Original Discovery Method: [SCIENTIST/SKILL_NAME]
Key Steps:
1. [STEP_1]
2. [STEP_2]
...
```

### What MUST NOT Be Stored
- Non-working payloads
- Failed request/response pairs
- Partial or incomplete attempts
- Redundant or duplicate successful attempts (store only the cleanest version)
- Sensitive data not related to the PoC (credentials, tokens, etc. — redact these)

## Verification Checklist

Before finalizing a POC, confirm:
- Vulnerability triggers consistently with the documented payload
- The minimal working payload is identified and documented
- All required conditions are documented (auth state, headers, context)
- Full request and response are captured (nothing truncated)
- No sensitive data is included in the documentation
- No failed attempts are stored
- POC is reproducible by someone else following the documentation
- Unique POC ID is assigned
- All metadata fields are populated

## Integration with Other Skills

### From Scientist Skill
When the scientist skill completes Phase 5 with a Vulnerability Confirmed conclusion:
- Load poc skill
- Provide: discovery path, endpoint details, successful payload
- Execute: verification and documentation workflow
- Return: verified POC with complete documentation

### From Bug-Classification Skill
When bug-classification identifies an Actionable/Exploitable vulnerability:
- Load poc skill to verify and document
- Provide: vulnerability classification and context
- Execute: POC verification workflow
- Return: verified and documented POC

### From Deep-Research Skill
When deep-research uncovers a potential vulnerability in source materials:
- Load poc skill to verify the finding
- Provide: research context and potential vulnerability details
- Execute: POC verification workflow
- Return: verified POC or confirmation that vulnerability cannot be reproduced

## Deliverables

When this skill completes, it produces:

1. **Verified POC Documentation (stored)**
   - Complete technical details of the successful exploitation
   - Unique POC identifier
   - All metadata and context

2. **Verification Report**
   - Confirmation that the vulnerability is real
   - Summary of verification steps taken
   - Any limitations or constraints on reproducibility

3. **Discovery Path Validation**
   - Confirmation that the original discovery steps are valid
   - Any corrections or clarifications to the discovery process

4. **Failed Attempts Summary (not stored, but reported)**
   - Count of failed attempts
   - Common reasons for failure (for diagnostic purposes only)
   - Lessons learned (without storing the actual failed payloads)

## Storage Format

POCs should be stored in a structured format for easy retrieval and analysis:
- File-based: One file per POC (e.g., POC-[ID].md or POC-[ID].json)
- Database: Structured entries in a vulnerability tracking system
- Version Control: Committed to a secure repository (for authorized access)

## Security Considerations

- Access Control: POCs contain sensitive information — restrict access appropriately
- Redaction: Remove or redact any credentials, tokens, or sensitive data from POCs
- Encryption: Consider encrypting POC storage at rest
- Audit Trail: Maintain logs of who accesses POCs and when
- Retention Policy: Define how long POCs are retained and when they can be deleted

## Quick Reference

**When to Load POC Skill:**
- After discovering a potential vulnerability that needs verification
- When you need to create a reproducible proof of concept
- When you need to document a verified vulnerability for reporting
- When another skill (scientist, bug-classification, etc.) identifies a confirmed vulnerability

**When NOT to Load POC Skill:**
- During initial discovery (use scientist skill instead)
- For classifying vulnerabilities (use bug-classification skill instead)
- For general research (use deep-research or serpapi skills instead)
- When you only have a hypothesis without any successful exploitation

Remember: This skill is about verification and documentation of confirmed vulnerabilities only. If you cannot reproduce the vulnerability, return to the discovery skill.
