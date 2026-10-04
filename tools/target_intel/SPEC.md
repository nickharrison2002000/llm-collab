# target_intel — Per-Target Intelligence Tools

The agent is target-agnostic. Intelligence for whichever target is in scope is
supplied at runtime by the operator, who drops exported files into
tools/data/target/:

- GraphQL/REST schemas (introspection dumps, openapi.yaml, swagger.json)
- API documentation
- Exported site pages (HTML-to-text, markdown)
- Configuration or deployment exports relevant to scope

target_intel.search performs keyword-scored search over every file in that
directory. If the directory is empty or absent, the tool returns an
instructive error telling the agent to request target files from the operator
or to use research.web_search against the live target documentation.

## Discovery Workflow

1. Map the mutation/input surface (GraphQL) or route/parameter surface (REST)
   with targeted queries.
2. Enumerate object relationships and ownership models.
3. Map site functionality: forms, file uploads, account flows, admin pages.
4. Generate hypotheses as concrete statements, e.g. "the updateEmail mutation
   accepts a customer ID without ownership validation".

## Rules

- Never assume an endpoint or field exists; it must appear in a tool result.
- Record which files and areas have been reviewed; expand iteratively.
- If no target files are present, say so and ask the operator for exports
  rather than inventing a surface.