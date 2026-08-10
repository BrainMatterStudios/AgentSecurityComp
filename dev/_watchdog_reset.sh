#!/bin/bash
# Self-healing relauncher for the at-reset submitters.
# Usage: bash dev/_watchdog_reset.sh <submitter_script> <marker_file> <log_file>
# Relaunches the submitter on any exit until the completion marker exists.
# The submitter is idempotent: it re-reads versions and skips slugs whose
# description already appears in the current submissions list.
set -u
cd "$(dirname "$0")/.." || exit 1
SCRIPT="${1:?script}"
MARKER="${2:?marker}"
WLOG="${3:?log}"

while [ ! -f "$MARKER" ]; do
  stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "$stamp [watchdog] launching $SCRIPT" >> "$WLOG"
  python3 "$SCRIPT" >> "$WLOG" 2>&1
  rc=$?
  if [ -f "$MARKER" ]; then
    stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "$stamp [watchdog] marker present; exiting" >> "$WLOG"
    break
  fi
  stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "$stamp [watchdog] $SCRIPT exited rc=$rc; relaunch in 15s" >> "$WLOG"
  sleep 15
done
