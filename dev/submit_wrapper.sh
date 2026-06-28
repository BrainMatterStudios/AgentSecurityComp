#!/bin/bash
# launchd-invoked wrapper: fire the one-shot accelerator A/B submitter at the UTC
# reset. Sets the framework python on PATH (launchd's minimal env otherwise grabs
# Xcode python with no kaggle). Retries on transient startup errors (codex hit a
# one-off EINTR in sitecustomize). The submitter itself is idempotent via its marker.
export PATH="/Library/Frameworks/Python.framework/Versions/3.14/bin:/usr/local/bin:/usr/bin:/bin"
export PYTHONSTARTUP=""
cd /Users/ahmed/Documents/AgentSecurityComp || exit 1
mkdir -p logs
LOG=logs/launchd_submit.log
echo "==== launchd fired at $(date -u '+%Y-%m-%dT%H:%M:%SZ') ====" >> "$LOG"
for attempt in 1 2 3 4 5; do
  /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 dev/oneshot_submit_v312.py >> "$LOG" 2>&1
  rc=$?
  echo "attempt $attempt exit=$rc" >> "$LOG"
  if [ $rc -eq 0 ] && [ -f logs/v312_oneshot_DONE ]; then
    echo "submit complete; unloading launchd job" >> "$LOG"
    launchctl unload "$HOME/Library/LaunchAgents/com.ahmed.jed.submit.plist" 2>>"$LOG"
    exit 0
  fi
  sleep 30
done
echo "all attempts exhausted" >> "$LOG"
