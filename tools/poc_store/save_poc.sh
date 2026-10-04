#!/usr/bin/env bash
# poc_store tool implementation: save / discard / list
set -eu
DIR="$(cd "$(dirname "$0")/.." && pwd)"
POCS="$DIR/pocs"
FAILLOG="$POCS/_failures.log"
mkdir -p "$POCS"

REQUIRED_SECTIONS=("## ENDPOINT" "## REQUEST" "## PAYLOAD" "## RESPONSE" "## VULNERABILITY DETAILS" "## REPRODUCTION STEPS" "## DISCOVERY PATH")

usage() { echo "usage: save_poc.sh save <file.md> | discard \"<reason>\" | list" >&2; exit 1; }
[ $# -ge 1 ] || usage
MODE="$1"

case "$MODE" in
  save)
    [ $# -eq 2 ] || usage
    FILE="$2"
    [ -f "$FILE" ] || { echo "error: file not found: $FILE" >&2; exit 1; }
    for s in "${REQUIRED_SECTIONS[@]}"; do
      grep -qF "$s" "$FILE" || { echo "error: rejected — missing required section '$s'. PoC not stored." >&2; exit 2; }
    done
    grep -qE '^Status: confirmed' "$FILE" || { echo "error: rejected — Status must be 'confirmed'. Use discard for failed attempts." >&2; exit 2; }
    ID="$(grep -m1 -E '^# POC-' "$FILE" | sed 's/^# POC-//' | tr -d '[:space:]')"
    [ -n "$ID" ] || { echo "error: rejected — first line must be '# POC-{ID}'" >&2; exit 2; }
    TYPE="$(grep -m1 -E '^Vulnerability Type:' "$FILE" | cut -d: -f2- | tr -dc '[:alnum:]' || true)"
    DEST="$POCS/POC-${ID}-${TYPE:-UNK}.md"
    if [ -f "$DEST" ]; then
      echo "error: rejected — duplicate POC ID: $ID" >&2; exit 3
    fi
    cp "$FILE" "$DEST"
    echo "stored: $DEST"
    ;;
  discard)
    [ $# -eq 2 ] || usage
    echo "$(date -u +%FT%TZ) FAIL: $2" >> "$FAILLOG"
    echo "discarded (reason logged): $2"
    ;;
  list)
    shopt -s nullglob
    for f in "$POCS"/POC-*.md; do
      TYPE="$(grep -m1 -E '^Vulnerability Type:' "$f" | cut -d: -f2- | sed 's/^ *//' || true)"
      SEV="$(grep -m1 -E '^Severity:' "$f" | cut -d: -f2- | sed 's/^ *//' || true)"
      echo "$(basename "$f") | ${TYPE:-?} | ${SEV:-?}"
    done
    [ -f "$FAILLOG" ] && echo "-- failures logged: $(wc -l < "$FAILLOG")"
    ;;
  *) usage ;;
esac