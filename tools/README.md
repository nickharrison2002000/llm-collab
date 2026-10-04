# Bug Bounty Agent — Tool Suite (local runtime)

Single source of truth for the tools exposed to the LLM in ai.py. ai.py loads
this registry, generates the OpenAI-style tool definitions from it, and
dispatches every tool call by the same names.

## Backend Bindings
   Tool | Backend |
 |------|---------|
 | payload_library.search / grep / read | Local corpus tools/data/reports.md |
 | target_intel.search_schema | Local tools/data/crypto-com-introspection.txt |
 | target_intel.search_site | Local exports under tools/data/site/ |
 | repo_intel.get_file / search_code / list_commits | GitHub REST API |
 | research.web_search / news_search | SerpAPI |
 | research.open_url | Python requests, HTML stripped |
 | http_request | Python requests: arbitrary method, full request echo, status, headers, body, timing |
 | poc_store.save / discard / list | tools/poc_store/save_poc.sh (tested) |

## Anti-Hallucination Contract

1. A finding may be labeled "confirmed" only if produced by http_request output
   or direct tool output (repo_intel, target_intel, research).
2. Everything else is a "candidate" finding.
3. poc_store.save refuses records without all mandatory sections and
   confirmed status.
4. poc_store.discard is mandatory for every failed attempt; only the failure
   reason is retained in pocs/_failures.log.
5. Every turn, request, tool call, and result is logged to logs/run-*.jsonl.

## Data Prerequisites

Export from the document library into tools/data/:
- reports.md — the payload corpus (real disclosed reports)
- crypto-com-introspection.txt — the target GraphQL schema
- site/ — any exported target site pages (optional)

## Workflow Binding (system prompt -> tools)

1. Discover: target_intel -> repo_intel -> research
2. Hypothesize: concrete, testable candidate statements
3. Craft: payload_library -> adapt a field-proven payload
4. Verify: http_request, at least twice per finding
5. Report: poc_store.save (confirmed) / poc_store.discard (failures)