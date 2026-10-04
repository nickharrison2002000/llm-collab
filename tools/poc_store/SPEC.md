# poc_store — Verified PoC Storage Contract

Bindings: filesystem under `tools/pocs/`.

- `poc_store.save` → `poc_store/save_poc.sh save <file.md>` (validates then stores)
- `poc_store.discard` → `poc_store/save_poc.sh discard "<reason>"` (one-line log only)
- `poc_store.list` → `poc_store/save_poc.sh list`

## Contract

1. Only successful, verified attempts are stored, one file per POC:
   `pocs/POC-{ID}-{TYPE}.md`, ID format `YYYYMMDD-NN`.
2. Validation is mandatory: a PoC missing any required section
   (ENDPOINT, REQUEST, PAYLOAD, RESPONSE, VULNERABILITY DETAILS, DISCOVERY PATH)
   is rejected and must not be stored.
3. Failed attempts are discarded; only a single failure line per attempt is
   appended to `pocs/_failures.log` with timestamp and reason. No payloads, no
   responses, no partial data.
4. Credentials and tokens in stored PoCs are redacted.
5. Stored POCs feed chaining analysis: before generating a chain hypothesis,
   run `poc_store.list` and reference existing POC IDs.

## Mandatory Template

See `TEMPLATE.md`. The save script enforces its section headers.