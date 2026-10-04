# research — Web Research Tools (SerpAPI-style)

Bindings: web_search connector.

- `research.web_search` → `tools.web_search.web_search` (limit max 20)
- `research.open_url` → `tools.web_search.open_url` (only for results with
  can_open = true)
- `research.news_search` → `tools.web_search.news_search` (always pair with a
  web_search call; use explicit start_date/end_date, never "latest"/"today")

## Standard Security Research Queries

CVEs:        "[Product]" CVE site:cve.mitre.org OR site:nvd.nist.gov
GitHub PoCs: site:github.com "[Technology]" "exploit" OR "PoC" OR "payload"
HackerOne:   site:hackerone.com "[Technology]" "vulnerability"
Advisories:  site:thehackernews.com OR site:bleepingcomputer.com "[Topic]"
Docs:        site:docs.[vendor].com "[Feature]" "security"
text
Copy

## Rules

- Formulate 3-5 query variations per research goal; start broad, then narrow.
- Deduplicate by URL; verify credibility and recency before trusting a result.
- Rate limits: if a response reports a hit limit, do not retry the tool.
- Cite every fact drawn from a result with its reference key.

