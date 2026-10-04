#!/usr/bin/env python3
"""
ai.py | Bug Bounty Agent Orchestrator

Ties together:
  prompts/system-prompt.md    | the agent role (head bug bounty hunter)
  skills/*.md                 | capability instructions (lazily routed)
  tools/registry.json         | single source of truth for tool exposure + dispatch
  tools/poc_store/save_poc.sh | validated PoC persistence (tested)
  .env                        | API_URL, API_MODEL, API_CTX, API_TOKEN, SERPAPI

Loop: assemble system prompt -> send conversation to GitHub Copilot chat
completions (OpenAI-compatible, GPT-4o) -> dispatch any tool_calls via the
registry -> append results -> repeat until a final report or max turns.
Every request/response pair is logged to logs/ for the anti-hallucination audit.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

import requests

ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
LOG_DIR = ROOT / "logs"
DATA_DIR = ROOT / "tools" / "data"
REGISTRY_PATH = ROOT / "tools" / "registry.json"
PROMPT_PATH = ROOT / "prompts" / "system-prompt.md"
SKILLS_DIR = ROOT / "skills"
POC_SCRIPT = ROOT / "tools" / "poc_store" / "save_poc.sh"

MAX_TURNS = 50
MAX_TOOL_RESULT_CHARS = 25000

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

def load_env(path: Path) -> dict:
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

ENV = load_env(ENV_PATH)
API_URL = os.environ.get("API_URL", ENV.get("API_URL", ""))
API_MODEL = os.environ.get("API_MODEL", ENV.get("API_MODEL", "gpt-4o"))
API_CTX = int(os.environ.get("API_CTX", ENV.get("API_CTX", "16384")))
API_TOKEN = os.environ.get("API_TOKEN", ENV.get("API_TOKEN", ""))
SERPAPI_KEY = os.environ.get("SERPAPI", ENV.get("SERPAPI", ""))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", ENV.get("GITHUB_TOKEN", ""))

if not API_URL or not API_TOKEN:
    sys.exit("error: API_URL and API_TOKEN must be set in .env or the environment")

# --------------------------------------------------------------------------
# Prompt assembly: system prompt + lazy skill router
# --------------------------------------------------------------------------

SKILL_TRIGGERS: dict[str, list[str]] = {
    "bug-classification-skill.md": ["classify", "classification", "actionable", "exploitable", "severity"],
    "github-vuln-skill.md": ["github.com", "repository", "repo", "commit", "pull request"],
    "poc-skill.md": ["verify", "poc", "proof of concept", "reproduce", "confirmed"],
    "scientist-skill.md": ["cannot trigger", "not firing", "investigate endpoint", "endpoint analysis"],
    "serpapi-skill.md": ["research", "cve", "search", "advisory", "exploit-db"],
}

def build_system_prompt(user_task: str) -> str:
    base = PROMPT_PATH.read_text(encoding="utf-8")
    task_l = user_task.lower()
    loaded = []
    for fname, triggers in SKILL_TRIGGERS.items():
        path = SKILLS_DIR / fname
        if path.exists() and any(t in task_l for t in triggers):
            loaded.append(f"--- SKILL: {fname} ---\n{path.read_text(encoding='utf-8')}")
    skills_block = "\n\n".join(loaded) if loaded else "(no skill matched this turn)"
    return f"{base}\n\n=== ACTIVE SKILLS (loaded for this task) ===\n{skills_block}"

# --------------------------------------------------------------------------
# Tool exposure: registry.json -> OpenAI function definitions
# --------------------------------------------------------------------------

def load_registry() -> dict:
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)

def registry_to_functions(registry: dict) -> list[dict]:
    functions = []
    for tool in registry["tools"]:
        props, required = {}, []
        for pname, pmeta in tool.get("parameters", {}).items():
            if not isinstance(pmeta, dict):
                continue
            schema = {"type": pmeta.get("type", "string")}
            if "enum" in pmeta:
                schema["enum"] = pmeta["enum"]
            if "description" in pmeta:
                schema["description"] = pmeta["description"]
            props[pname] = schema
            if pmeta.get("required"):
                required.append(pname)
        functions.append({
            "type": "function",
            "function": {
                "name": tool["name"].replace(".", "_"),
                "description": tool["description"],
                "parameters": {
                    "type": "object",
                    "properties": props,
                    "required": required,
                },
            },
        })
    return functions

# --------------------------------------------------------------------------
# Local tool backends
# --------------------------------------------------------------------------

def _clip(text: str, limit: int = MAX_TOOL_RESULT_CHARS) -> str:
    return text if len(text) <= limit else text[:limit] + f"\n... [truncated {len(text) - limit} chars]"

def _data_file(name: str) -> Path:
    p = DATA_DIR / name
    if not p.exists():
        raise FileNotFoundError(
            f"data file not found: {p}. Export it from your library into tools/data/."
        )
    return p

def _keyword_search(text: str, query: str, top_k: int) -> list[dict]:
    """Chunk-based keyword scoring search over a local corpus."""
    chunks = re.split(r"\n(?=#{2,3} |\*\*|=|\-\-\-)", text)
    terms = [t for t in re.split(r"\W+", query.lower()) if len(t) > 3]
    scored = []
    for chunk in chunks:
        chunk_l = chunk.lower()
        score = sum(chunk_l.count(t) for t in terms)
        if score > 0:
            scored.append({"score": score, "chunk": chunk[:2000], "position": text.find(chunk)})
    scored.sort(key=lambda x: -x["score"])
    return scored[:top_k]

def _http_get(url: str, params: dict | None = None, headers: dict | None = None,
              timeout: int = 20) -> requests.Response:
    return requests.get(url, params=params, headers=headers, timeout=timeout)

# --- payload_library ---

def tool_payload_library_search(query: str, top_k: int = 5) -> str:
    text = _data_file("reports.md").read_text(encoding="utf-8", errors="replace")
    hits = _keyword_search(text, query, top_k)
    return _clip(json.dumps({"corpus": "reports.md", "results": hits}, ensure_ascii=False))

def tool_payload_library_grep(pattern: str, top_k: int = 10) -> str:
    text = _data_file("reports.md").read_text(encoding="utf-8", errors="replace")
    hits = []
    for m in re.finditer(re.escape(pattern), text, re.IGNORECASE):
        start = max(0, m.start() - 800)
        hits.append({"position": m.start(), "chunk": text[start:m.end() + 800]})
        if len(hits) >= top_k:
            break
    return _clip(json.dumps({"pattern": pattern, "results": hits}, ensure_ascii=False))

def tool_payload_library_read(uri: str) -> str:
    """uri format: local://reports.md?at=12345 or local://<filename>"""
    m = re.match(r"local://([^?]+)(\?at=(\d+))?", uri)
    if not m:
        raise ValueError(f"unsupported payload_library uri: {uri}")
    name, at = m.group(1), int(m.group(3) or 0)
    text = _data_file(name).read_text(encoding="utf-8", errors="replace")
    return _clip(text[at:at + 4000])

# --- target_intel ---

def tool_target_intel_search(query: str, top_k: int = 5) -> str:
    """Keyword-scored search over per-target files in tools/data/target/."""
    target_dir = DATA_DIR / "target"
    results = []
    files = []
    if target_dir.exists():
        files = (sorted(target_dir.glob("*.txt")) + sorted(target_dir.glob("*.md"))
                 + sorted(target_dir.glob("*.json")) + sorted(target_dir.glob("*.yaml"))
                 + sorted(target_dir.glob("*.yml")))
    if not files:
        return ("no target intelligence files found. Ask the operator to export the "
                "target's schema/API docs/site pages into tools/data/target/, or use "
                "research_web_search against the target's public documentation.")
    for p in files:
        text = p.read_text(encoding="utf-8", errors="replace")
        for hit in _keyword_search(text, query, top_k):
            hit["file"] = p.name
            results.append(hit)
    results.sort(key=lambda x: -x["score"])
    return _clip(json.dumps({"results": results[:top_k]}, ensure_ascii=False))

def tool_target_intel_search_site(query: str, top_k: int = 5) -> str:
    """Searches any local site-intel exports placed in tools/data/site/."""
    site_dir = DATA_DIR / "site"
    results = []
    if site_dir.exists():
        for p in sorted(site_dir.glob("*.txt")) + sorted(site_dir.glob("*.md")):
            text = p.read_text(encoding="utf-8", errors="replace")
            results.extend(_keyword_search(text, f"{query} {p.name}", top_k))
    if not results:
        return ("no local site export found; place exported site documents in "
                "tools/data/site/ or use research_web_search for the live site.")
    results.sort(key=lambda x: -x["score"])
    return _clip(json.dumps({"results": results[:top_k]}, ensure_ascii=False))

# --- repo_intel (GitHub REST API) ---

def _gh_headers() -> dict:
    h = {"Accept": "application/vnd.github+json",
         "User-Agent": "bug-bounty-agent"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h

def tool_repo_intel_get_file(owner: str, repo: str, path: str, branch: str | None = None) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path.lstrip('/')}"
    params = {"ref": branch} if branch else {}
    r = _http_get(url, params=params, headers=_gh_headers())
    r.raise_for_status()
    data = r.json()
    if data.get("type") == "file":
        import base64
        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        return _clip(f"path: {data['path']}\nsha: {data['sha']}\n\n{content}")
    return _clip(json.dumps(data, ensure_ascii=False))  # directory listing

def tool_repo_intel_search_code(query: str) -> str:
    url = "https://api.github.com/search/code"
    r = _http_get(url, params={"q": query, "per_page": 10}, headers=_gh_headers())
    r.raise_for_status()
    items = [{"repo": it["repository"]["full_name"], "path": it["path"],
              "url": it["html_url"]} for it in r.json().get("items", [])]
    return _clip(json.dumps({"query": query, "results": items}, ensure_ascii=False))

def tool_repo_intel_list_commits(owner: str, repo: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    r = _http_get(url, params={"per_page": 10}, headers=_gh_headers())
    r.raise_for_status()
    items = [{"sha": c["sha"][:12], "date": c["commit"]["author"]["date"],
              "message": c["commit"]["message"].splitlines()[0]} for c in r.json()]
    return _clip(json.dumps({"repo": f"{owner}/{repo}", "commits": items}, ensure_ascii=False))

# --- research (SerpAPI + open_url) ---

def tool_research_web_search(query: str, start_date: str | None = None,
                             end_date: str | None = None, limit: int = 10) -> str:
    if not SERPAPI_KEY:
        return "error: SERPAPI key not configured in .env"
    params = {"api_key": SERPAPI_KEY, "engine": "google", "q": query, "num": min(limit, 20)}
    if start_date:
        params["q"] += f" after:{start_date}"
    if end_date:
        params["q"] += f" before:{end_date}"
    r = _http_get("https://serpapi.com/search.json", params=params)
    r.raise_for_status()
    data = r.json()
    results = [{"position": o.get("position"), "title": o.get("title"),
                "link": o.get("link"), "snippet": o.get("snippet"),
                "date": o.get("date")} for o in data.get("organic_results", [])]
    return _clip(json.dumps({"query": query, "results": results}, ensure_ascii=False))

def tool_research_open_url(url: str) -> str:
    r = _http_get(url, headers={"User-Agent": "Mozilla/5.0 (research)"}, timeout=25)
    content_type = r.headers.get("Content-Type", "")
    if "html" in content_type.lower():
        text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", r.text, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
    else:
        text = r.text
    return _clip(f"status: {r.status_code}\ncontent-type: {content_type}\n\n{text}")

def tool_research_news_search(query: str, start_date: str | None = None,
                              end_date: str | None = None) -> str:
    if not SERPAPI_KEY:
        return "error: SERPAPI key not configured in .env"
    params = {"api_key": SERPAPI_KEY, "engine": "google_news", "q": query}
    if start_date:
        params["q"] += f" after:{start_date}"
    if end_date:
        params["q"] += f" before:{end_date}"
    r = _http_get("https://serpapi.com/search.json", params=params)
    r.raise_for_status()
    results = [{"title": n.get("title"), "link": n.get("link"),
                "date": n.get("date"), "source": n.get("source")}
               for n in r.json().get("news_results", [])]
    return _clip(json.dumps({"query": query, "results": results}, ensure_ascii=False))

# --- http.request (full PoC execution) ---

def tool_http_request(url: str, method: str = "GET", headers: dict | None = None,
                      body: str | None = None, timeout_ms: int = 15000) -> str:
    if method.upper() not in {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}:
        return f"error: unsupported method {method}"
    timeout = max(1, timeout_ms / 1000)
    t0 = time.time()
    try:
        resp = requests.request(method.upper(), url, headers=headers or {}, data=body,
                                timeout=timeout, allow_redirects=False)
        elapsed_ms = int((time.time() - t0) * 1000)
        record = {
            "request_echo": {"url": url, "method": method.upper(),
                             "headers": headers or {}, "body": body},
            "status": resp.status_code,
            "headers": dict(resp.headers),
            "body": resp.text[:3000],
            "timing_ms": elapsed_ms,
        }
    except requests.RequestException as e:
        record = {"request_echo": {"url": url, "method": method.upper(), "body": body},
                  "error": str(e)}
    return _clip(json.dumps(record, ensure_ascii=False))

# --- poc_store (tested shell script) ---

def tool_poc_store_save(poc_markdown: str) -> str:
    tmp = ROOT / "logs" / "_pending_poc.md"
    LOG_DIR.mkdir(exist_ok=True)
    tmp.write_text(poc_markdown, encoding="utf-8")
    result = subprocess.run(["bash", str(POC_SCRIPT), "save", str(tmp)],
                            capture_output=True, text=True)
    tmp.unlink(missing_ok=True)
    out = result.stdout.strip() or result.stderr.strip()
    return f"exit={result.returncode} {out}"

def tool_poc_store_discard(reason: str) -> str:
    result = subprocess.run(["bash", str(POC_SCRIPT), "discard", reason],
                            capture_output=True, text=True)
    return f"exit={result.returncode} {result.stdout.strip() or result.stderr.strip()}"

def tool_poc_store_list() -> str:
    result = subprocess.run(["bash", str(POC_SCRIPT), "list"],
                            capture_output=True, text=True)
    return result.stdout or result.stderr

HANDLERS: dict[str, Callable[..., str]] = {
    "payload_library_search": tool_payload_library_search,
    "payload_library_grep": tool_payload_library_grep,
    "payload_library_read": tool_payload_library_read,
    "target_intel_search": tool_target_intel_search,
    "repo_intel_get_file": tool_repo_intel_get_file,
    "repo_intel_search_code": tool_repo_intel_search_code,
    "repo_intel_list_commits": tool_repo_intel_list_commits,
    "research_web_search": tool_research_web_search,
    "research_open_url": tool_research_open_url,
    "research_news_search": tool_research_news_search,
    "http_request": tool_http_request,
    "poc_store_save": tool_poc_store_save,
    "poc_store_discard": tool_poc_store_discard,
    "poc_store_list": tool_poc_store_list,
}

def dispatch_tool(name: str, arguments: dict) -> str:
    handler = HANDLERS.get(name)
    if not handler:
        return f"error: unknown tool {name}"
    try:
        return handler(**arguments)
    except TypeError as e:
        return f"error: bad arguments for {name}: {e}"
    except Exception as e:
        return f"error: {type(e).__name__}: {e}"

# --------------------------------------------------------------------------
# Main agent loop
# --------------------------------------------------------------------------

def log_turn(log_file: Path, entry: dict) -> None:
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def run_agent(user_task: str) -> str:
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"run-{time.strftime('%Y%m%d-%H%M%S')}.jsonl"

    registry = load_registry()
    functions = registry_to_functions(registry)
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }
    if "githubcopilot" in API_URL:
        headers["Editor-Version"] = "ai.py/1.0"
        headers["Editor-Plugin-Version"] = "ai.py/1.0"
        headers["Copilot-Integration-Id"] = "vscode-chat"

    messages = [
        {"role": "system", "content": build_system_prompt(user_task)},
        {"role": "user", "content": user_task},
    ]

    for turn in range(MAX_TURNS):
        payload = {
            "model": API_MODEL,
            "messages": messages,
            "tools": functions,
            "tool_choice": "auto",
            "temperature": 0.2,
        }
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        log_turn(log_file, {"turn": turn, "request": payload, "http_status": resp.status_code})
        if resp.status_code != 200:
            return f"error: API returned {resp.status_code}: {resp.text[:500]}"
        data = resp.json()
        choice = data["choices"][0]
        assistant_msg = choice["message"]
        messages.append(assistant_msg)
        log_turn(log_file, {"turn": turn, "response": assistant_msg})

        tool_calls = assistant_msg.get("tool_calls") or []
        if not tool_calls:
            return assistant_msg.get("content", "(no final content)")

        for tc in tool_calls:
            fn = tc["function"]
            name = fn["name"]
            try:
                arguments = json.loads(fn["arguments"] or "{}")
            except json.JSONDecodeError:
                arguments = {"_raw": fn["arguments"]}
            print(f"[turn {turn}] tool: {name} args: {json.dumps(arguments)[:200]}")
            result = dispatch_tool(name, arguments)
            log_turn(log_file, {"turn": turn, "tool": name, "arguments": arguments,
                                "result": result})
            messages.append({"role": "tool", "tool_call_id": tc["id"],
                             "content": result})

    return "error: maximum turns reached without a final answer"

def main() -> None:
    if len(sys.argv) < 2:
        print('usage: python ai.py "<bug bounty task, e.g. target and scope>"')
        sys.exit(1)
    user_task = " ".join(sys.argv[1:])
    print(f"[ai.py] model={API_MODEL} ctx={API_CTX} registry={REGISTRY_PATH}")
    final = run_agent(user_task)
    print("\n===== FINAL OUTPUT =====\n")
    print(final)

if __name__ == "__main__":
    main()
