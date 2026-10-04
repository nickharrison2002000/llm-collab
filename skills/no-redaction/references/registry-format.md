# Registry Format

Single source of truth for all substitutions. Use whatever file fits the project (`config.yaml`, `config.py`, `.env`, `PLACEHOLDERS.md`, `REGISTRY.md`, etc.).

## Canonical YAML example

```yaml
# config.yaml — single source of truth for all substitutions

API_BASE_URL:
  purpose: Base URL for the backend API
  example: "https://api.example.com/v1"
  used_in: ["client.py", "tests/test_client.py"]

API_KEY:
  purpose: Auth token for API_BASE_URL
  example: "sk-..."
  status: UNRESOLVED   # user must supply
  used_in: ["client.py"]

DB_HOST:
  purpose: Postgres host
  example: "localhost"
  used_in: ["db.py", "migrations/env.py"]
```

## Required fields per entry

- `purpose` — one-line description of what the value is for
- `used_in` — list of files or modules that reference it
- `example` or `status: UNRESOLVED` — either show the expected format or mark it as needing a real value

## Rules

- Append-only during a session. Add new entries; do not silently rename or delete.
- Descriptive names only (`S3_BUCKET_NAME`, not `BUCKET`).
- Never invent a second name for the same logical value.
- When the real value becomes known, update it in exactly one place (the registry).
