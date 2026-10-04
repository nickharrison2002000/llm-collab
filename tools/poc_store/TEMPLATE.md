# POC-{ID}

Vulnerability Type: {RCE/SQLi/XSS/SSRF/CSRF/IDOR/SSTI/CRLF/...}
Severity: {Critical/High/Medium/Low}
Date Discovered: {YYYY-MM-DD}
Date Verified: {YYYY-MM-DD}
Status: confirmed

---

## ENDPOINT
URL: {FULL_URL}
Method: {HTTP_METHOD}
Type: {REST/GraphQL/WebSocket}
Authentication: {Auth/Unauth, Role, Session state}
Technology Stack: {Framework, Language, Server, Database}

---

## REQUEST
Headers:
{HEADER}: {VALUE}

Body:
{RAW_BODY}

Parameters:
{PARAM}={VALUE}

Cookies:
{COOKIE}={VALUE}

Timing: {TIMESTAMP}

---

## PAYLOAD
Raw: {EXACT_PAYLOAD_BEFORE_ENCODING}
Encoded: {PAYLOAD_AS_SENT}
Type: {PAYLOAD_TYPE}
Structure: {HOW_IT_WAS_CONSTRUCTED, corpus chunk position if adapted from payload_library}
Obfuscation: {ENCODING_APPLIED}

---

## RESPONSE
Status: {HTTP_STATUS}
Headers:
{HEADER}: {VALUE}

Body:
{RAW_RESPONSE_BODY}

Timing: {RESPONSE_TIME}
Behavior: {OBSERVED_BEHAVIOR proving the vulnerability}

---

## VULNERABILITY DETAILS
Root Cause: {DESCRIPTION with file/line reference where known}
Impact: {WHAT_AN_ATTACKER_CAN_DO}
Affected Versions: {VERSIONS}
Suggested Fix: {REMEDIATION}

---

## REPRODUCTION STEPS
1. {STEP_1}
2. {STEP_2}

Repeatability: Executed {N} times with consistent results on {DATE}.

---

## DISCOVERY PATH
Original Discovery Method: {SKILL/TOOL}
Key Steps:
1. {STEP}
2. {STEP}

Chain References: {POC IDs this chains with, or "none"}