# repo_intel — GitHub Repository Intelligence Tools

Bindings: github_app connector (MCP).

- `get_file` → `tools.github_app.get_file_contents`
- `search_code` → `tools.github_app.search_code`
- `list_commits` → `tools.github_app.list_commits`
- `get_commit` → `tools.github_app.get_commit`

## Pull Order (github-repo-intel skill)

1. Repository metadata; get_me for permission context.
2. README.md, .gitignore, dependency manifests (package.json,
   requirements.txt, Cargo.toml), Dockerfile/docker-compose.yml,
   .env.example, openapi.yaml / swagger.json.
3. Entry points (app.js, main.py, server.ts), route handlers, controllers,
   middleware, auth implementation, DB models.
4. Security-critical code: validation/sanitization, JWT/OAuth/session
   handling, crypto, file upload handlers, deserialization, CORS config.

## Code Search Patterns

- Credentials: `password`, `secret`, `api_key`, `token`
- Dangerous functions: `eval(`, `exec(`, `system(`, `spawn`
- SQL: `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- File ops: `fs.readFile`, `fs.writeFile`, `open(`
- Deserialization: `unserialize`, `pickle.loads`, `JSON.parse`
- Template engines: `render`, `template`, `ejs`, `handlebars`

## Rules

- Cite file and line references for every hypothesis.
- Use pagination with batches of 5-10 items; minimal_output when full data
  is not needed.
- Search query strings must contain only criteria, never sort: syntax.