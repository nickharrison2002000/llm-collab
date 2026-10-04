# http_client — PoC HTTP Execution Contract

## Interface

http.request({
url: string,          // full URL; must be in scope
method: "GET"|"POST"|"PUT"|"PATCH"|"DELETE"|"HEAD"|"OPTIONS",
headers: object,      // all headers incl. Content-Type, Authorization, cookies
body: string|null,    // raw body, exactly as sent (pre-encoding payload also recorded)
timeout_ms: integer   // default 15000
})

Returns: `{ status, headers, body, timing_ms, request_echo }`. The request echo
is mandatory: the POC record requires the complete sent request.

## Backends

1. Default (available now): GET retrieval via `tools.web_search.open_url`.
   Suitable for reflected XSS, open redirect, path traversal reads, and any
   payload delivered purely through a crafted URL.
2. Extension point (arbitrary methods): the runtime that hosts the agent LLM
   must provide an HTTP client transport (for example a serverless function,
   Burp Repeater export, or curl executed by the operator). Bind it by
   replacing `backend.function` in `registry.json`. The interface above is
   transport-agnostic and must not change.

## Rules

- Every request is executed at least twice to demonstrate consistency before
  a finding may be labeled confirmed (timing-sensitive payloads: compare
  measured response times against a control request).
- Record the raw payload AND the encoded payload as sent.
- Never send destructive payloads (DELETE on production data, drop tables).
  Data-creation payloads must be rolled back or clearly flagged.
- Only in-scope targets. If the program scope is unclear, ask before firing.




