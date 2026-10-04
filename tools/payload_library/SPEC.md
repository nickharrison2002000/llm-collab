# payload_library — Payload Corpus Tools

Binding: userLibrary connector over the uploaded reports corpus.
- Library: `doclib://019e4b6e-2185-77d5-a348-d58685596d7b`
- Document: `doclib://019e4b6e-2185-77d5-a348-d58685596d7b/8baad8cc-148b-4c7b-8a66-115c106dd31e` (reports.md, ~1.1 MB)
- Content: real, previously-disclosed vulnerability reports covering XSS, SQL
  injection (union and time-based), SSRF, CSRF, IDOR, SSTI (Jinja2), CRLF,
  CORS misconfiguration, DoS, authentication bypass, and open redirect, each
  with working payloads, requests, and reproduction steps.

## Usage Patterns

1. Craft by weakness type (semantic):
   `search(query="time-based blind SQL injection sleep payload", top_k=5)`
2. Craft by technology:
   `search(query="GraphQL introspection depth query abuse", top_k=5)`
3. Locate a known payload string (exact):
   `grep(pattern="XOR(if(now()=sysdate()", top_k=10)`
4. Read the full report context around a match:
   `read(uri="<chunk uri or its ?start=/?end= expansion links>")`

## Rules

- Payloads pulled from the corpus are field-proven; mutate them for the target
  but retain the working structure (parameter placement, encoding, casing).
- Always read surrounding context before adapting a payload; reproduction
  steps often carry required headers, auth state, or encoding.
- Cite the source chunk URI in any candidate finding derived from the corpus.