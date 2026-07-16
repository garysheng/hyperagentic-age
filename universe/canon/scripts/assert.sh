#!/usr/bin/env bash
# Load-bearing PRE-RENDER GATE for this universe, via the Agentic Story engine.
#
# A renderer/gen-script MUST call this BEFORE generating a unit. If a required
# character sheet is missing or a spread's setting is not locked, this exits
# non-zero and the render is refused. That refusal is the feature.
#
# Usage:
#   assert.sh validate
#   assert.sh spread --characters hero,guide [--location the-hall]
#   assert.sh story  the-first-step
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNIVERSE="$(cd "$HERE/../.." && pwd)"                 # <universe> (this file is at <universe>/canon/scripts/)
ENGINE="${AGENTICSTORY_ENGINE:-/Users/garysheng/Documents/github-repos/agenticstory/engine}"     # override with $AGENTICSTORY_ENGINE if the engine moves
[ -d "$ENGINE" ] || { echo "agenticstory engine not found at $ENGINE — set AGENTICSTORY_ENGINE" >&2; exit 3; }

[ $# -ge 1 ] || { echo "usage: assert.sh validate|spread|story ..." >&2; exit 2; }
mode="$1"; shift
cd "$ENGINE"
case "$mode" in
  validate) exec python3 -m agenticstory.cli validate     "$UNIVERSE" ;;
  spread)   exec python3 -m agenticstory.cli assert-spread "$UNIVERSE" "$@" ;;
  story)    exec python3 -m agenticstory.cli assert-story  "$UNIVERSE" "$@" ;;
  *) echo "usage: assert.sh validate|spread|story ..." >&2; exit 2 ;;
esac
