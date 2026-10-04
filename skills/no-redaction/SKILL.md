---
name: no-redaction
description: Prevents silent redaction and untracked placeholders that destroy PoCs, reports, scripts, and configs. Critical for multi-turn and multi-file bug-bounty work so nothing valuable is lost and submission-ready artifacts stay complete. Use on every report, PoC, script, or code reconstruction to protect time and payout quality.
---

# No-Redaction / No-Placeholder

Prevent two specific LLM failure modes that quietly corrupt work:

- **Silent redaction** — omitting or eliding parts of the real content "for brevity" (`# ... rest of code ...`, `// unchanged`, `[truncated]`, `...`, etc.) without the user asking.
- **Silent placeholders** — substituting generic stand-ins (`YOUR_API_KEY`, `example.com`, `TODO`, `foo`, `path/to/file`, `some_value`) instead of real values or tracked, named variables.

Both are forms of the same anti-pattern: the LLM abstracted something the user needed verbatim, and didn't tell them. This skill exists to make that impossible.

## Core Principle

Never silently drop, elide, or abstract content. If something must be substituted or omitted, it must be (a) explicitly named, (b) tracked in one place, and (c) trivially restorable.

Two rules fall out of that:

1. **Rule 1 — No silent redaction.** Emit verbatim, or explicitly flag the omission and why.
2. **Rule 2 — No untracked placeholders.** Every placeholder becomes a named variable recorded in a single, maintained config/registry file.

## When to Load

- Any multi-turn code or script authoring/editing
- Any work spanning multiple files
- Any config, env, secret, or path handling
- Any reconstruction or reassembly task
- Any time you're tempted to write `...`, `# rest`, `unchanged`, or `TODO`
- Any time you're about to write `your_value_here` or `example.com`
- Reviewing an LLM's output for completeness before acting on it

## Rule 1: No Silent Redaction

### What counts as redaction

Anything that replaces real content with a stand-in for brevity, including:

- `# ... rest of the code ...` / `// ...` / `/* ... */`
- `# unchanged` / `# same as before` / `# omitted for brevity`
- `[truncated]` / `[snip]` / `...`
- "and so on" / "etc." when the actual content matters
- Summarizing a block instead of emitting it
- Quietly dropping a section because it "seems unchanged"
- Collapsing repeated structures into prose ("repeat for each X")

### Rules

- Default to verbatim. If the user is working on a file, emit the whole thing (or the whole changed region plus unambiguous boundaries).
- If you must omit, say so explicitly, out loud, in the output — not in a preamble. The omission marker must be visible in the artifact itself, e.g.:
  ```
  # [OMITTED: lines 40–120 unchanged — see previous message]
  # [OMITTED: 3 helper functions identical to v2]
  ```
- Never omit across turns without re-emitting. If a later turn depends on earlier content, re-emit it. Do not assume the user still has it.
- When editing, show the change with enough surrounding context to anchor it — but not at the cost of dropping lines the user needs.
- When summarizing is genuinely wanted, ask first. "Do you want the full file or a diff?" is a 2-second question that saves an hour of reconstruction.
- If you catch yourself about to redact, stop and emit instead. The cost of a longer message is always lower than the cost of a corrupted artifact.

### Why this matters

Redactions are invisible until you try to run the code, diff two versions, or hand it to someone else. By then, reconstructing is manual archaeology. Emitting verbatim costs tokens; redacting costs hours.

## Rule 2: No Untracked Placeholders

### What counts as a placeholder

Anything that stands in for a real value but isn't a real, named, tracked variable, including:

- `YOUR_API_KEY`, `your_token_here`, `<insert value>`
- `example.com`, `foo`, `bar`, `baz`, `some_value`, `path/to/file`
- `TODO`, `FIXME`, `XXX` (when used as a stand-in rather than a real task marker)
- Hardcoded stand-ins scattered across files
- The same logical value written differently in different places

### Rules

- Every placeholder becomes a named variable. No bare stand-ins in the artifact.
- Every named variable is declared in a single config/registry file — one file, one source of truth, built up incrementally as work proceeds. Examples:
  - `config.py` / `settings.py` / `.env` / `config.yaml` / `constants.ts` / `config.json` — whatever fits the project
  - A `PLACEHOLDERS.md` or `REGISTRY.md` if the project has no natural config layer yet
- The registry is append-only during a session. When a new placeholder appears, add it to the registry first, then reference it.
- Names are descriptive, not generic. `S3_BUCKET_NAME` beats `BUCKET`; `PROD_DB_HOST` beats `DB_HOST_1`.
- Every variable has: name, purpose (one line), example/expected format, and where it's used. Keep the registry scannable.
- Never invent a second name for the same value. If a value already exists in the registry, reuse it.
- When the real value becomes known, it replaces the variable in exactly one place — the registry — not scattered across files.
- Flag any placeholder you cannot resolve. Say so explicitly and add it to the registry with `UNRESOLVED` status so it can't silently ship.

### Registry format (example)

See `references/registry-format.md` for the canonical example.

## Enforcement Protocol (both rules)

Before emitting any artifact, run this checklist:

- □ Did I use `...`, `etc.`, `unchanged`, `rest of`, or any elision? If yes, either emit the real content or add an explicit, visible `[OMITTED: …]` marker with a reason.
- □ Did I write a bare stand-in (`YOUR_*`, `example.com`, `foo`, `TODO`) instead of a named variable? If yes, add it to the registry and reference the variable.
- □ Does every variable I referenced exist in the registry? If not, add it.
- □ Is the registry consistent with the artifact? No orphan variables, no missing entries.
- □ If this is turn N of a multi-turn session, have I re-emitted anything the user will need but doesn't have? If not, re-emit.

If any box is unchecked, fix it before sending.

## Handling the Two Together

When you'd otherwise write something like:

```python
# ... rest of config ...
API_KEY = "YOUR_API_KEY"
DB = "postgres://user:pass@example.com/db"
```

…the skill says: emit the real content, and route the substitutions through the registry:

```python
# config.py
from config_loader import cfg

API_KEY = cfg.API_KEY            # see config.yaml
DB_URL  = cfg.DB_URL             # see config.yaml
# (all other config keys emitted verbatim below)
LOG_LEVEL = "INFO"
RETRY_MAX = 3
TIMEOUT_S = 30
```

And in `config.yaml`:

```yaml
API_KEY:
  purpose: Backend API key
  status: UNRESOLVED   # user must supply
  used_in: ["config.py"]

DB_URL:
  purpose: Postgres connection string
  example: "postgres://user:pass@host:5432/db"
  used_in: ["config.py"]
```

Now nothing is lost, and everything variable lives in one place.

## Deliverables

When this skill is active, every artifact you produce must be accompanied by (or reference) the current registry. If the registry doesn't exist yet, create it on first use.

## Important Notes

- This is a default-on behavior, not a one-time fix. Apply it every turn.
- A longer message is always cheaper than a corrupted artifact.
- If the user explicitly asks for brevity or a summary, honor it — but say what you're omitting, and keep the registry authoritative. The rule is "no silent omission," not "no summaries ever."
- Secrets and PII are the one exception. If real values are sensitive, these need to be placed in a proper location like `.env` with a properly setup `.gitignore` file — do not silently inline or silently drop them.
- If you're reviewing an LLM's output, treat any `...`, `TODO`, or bare stand-in as a red flag to surface, not something to quietly pass along.
- The registry grows with the work. Add to it as you go; never let it lag behind the artifacts.
