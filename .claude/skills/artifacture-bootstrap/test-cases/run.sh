#!/usr/bin/env bash
# Regression über alle Fixtures. Aufruf: bash test-cases/run.sh
# Erwartung: "expect-ok" derivt fehlerfrei, "bad-*" scheitert mit Exit != 0.
set -uo pipefail

BUNDLE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$(mktemp -d)"
trap 'rm -rf "$OUT"' EXIT
fail=0

run() { python3 "$BUNDLE/scripts/derive.py" "$@"; }

echo "== Katalog-Validierung"
run --validate || { echo "   FAIL: Katalog ungueltig"; exit 1; }

echo
echo "== Fixtures, die derivieren muessen"
for f in "$BUNDLE"/test-cases/*.json; do
  name="$(basename "$f" .json)"
  case "$name" in bad-*) continue ;; esac
  if out=$(run --answers "$f" --out "$OUT/$name" 2>&1); then
    printf '   ok    %-14s %s\n' "$name" "$(echo "$out" | head -1 | sed 's/ ->.*//')"
  else
    printf '   FAIL  %-14s %s\n' "$name" "$(echo "$out" | head -1)"; fail=1
  fi
done

echo
echo "== Fixtures, die abgewiesen werden muessen"
for f in "$BUNDLE"/test-cases/bad-*.json; do
  name="$(basename "$f" .json)"
  if out=$(run --answers "$f" --out "$OUT/$name" 2>&1); then
    printf '   FAIL  %-14s haette scheitern muessen\n' "$name"; fail=1
  else
    printf '   ok    %-14s %s\n' "$name" "$(echo "$out" | head -1 | cut -c1-70)"
  fi
done

echo
if [ "$fail" -eq 0 ]; then echo "Alle Checks gruen."; else echo "FEHLER: siehe oben."; fi
exit "$fail"
