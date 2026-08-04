"""Submit the prepared Kaggle kernels after the UTC daily quota resets."""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
import time
from pathlib import Path


COMPETITION = "ai-agent-security-multi-step-tool-attacks"
SUBMISSIONS = (
    (
        "adaptive",
        "ahmedmobasher86/jed-public-k1-adaptive",
        "2",
        "hardened adaptive governor v2",
    ),
    (
        "private-chain",
        "ahmedmobasher86/jed-public-private-chain-400",
        "2",
        "hardened private-chain hedge v2",
    ),
)


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


def next_reset_time(now: dt.datetime, margin_minutes: int) -> dt.datetime:
    tomorrow = now.date() + dt.timedelta(days=1)
    reset = dt.datetime.combine(tomorrow, dt.time(0, 0), tzinfo=dt.UTC)
    return reset + dt.timedelta(minutes=margin_minutes)


def log(message: str) -> None:
    stamp = utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{stamp}] {message}", flush=True)


def run_command(command: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return proc.returncode, proc.stdout


def quota_exhausted(output: str) -> bool:
    return "daily Submission allowance" in output or "Submission not allowed" in output


def submit_one(label: str, kernel: str, version: str, message: str) -> bool:
    command = [
        "kaggle",
        "competitions",
        "submit",
        COMPETITION,
        "-f",
        "submission.csv",
        "-k",
        kernel,
        "-v",
        version,
        "-m",
        message,
    ]
    code, output = run_command(command)
    log(f"{label}: exit={code}")
    if output.strip():
        print(output, flush=True)
    return code == 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--margin-minutes", type=int, default=7)
    parser.add_argument("--retry-minutes", type=int, default=90)
    parser.add_argument("--retry-interval-seconds", type=int, default=300)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    target = next_reset_time(utc_now(), args.margin_minutes)
    wait_s = max(0.0, (target - utc_now()).total_seconds())
    log(f"waiting until {target.strftime('%Y-%m-%dT%H:%M:%SZ')} ({wait_s:.0f}s)")
    if args.dry_run:
        for label, kernel, version, message in SUBMISSIONS:
            log(f"dry-run: would submit {label} {kernel} v{version}: {message}")
        return 0

    time.sleep(wait_s)
    deadline = utc_now() + dt.timedelta(minutes=args.retry_minutes)
    remaining = list(SUBMISSIONS)
    while remaining and utc_now() <= deadline:
        label, kernel, version, message = remaining[0]
        code, output = run_command(
            [
                "kaggle",
                "competitions",
                "submit",
                COMPETITION,
                "-f",
                "submission.csv",
                "-k",
                kernel,
                "-v",
                version,
                "-m",
                message,
            ]
        )
        log(f"{label}: exit={code}")
        if output.strip():
            print(output, flush=True)
        if code == 0:
            remaining.pop(0)
            time.sleep(15)
            continue
        if quota_exhausted(output):
            log(f"{label}: quota still exhausted; retrying")
            time.sleep(args.retry_interval_seconds)
            continue
        return code

    if remaining:
        log("timed out before all submissions completed")
        return 1
    log("all submissions completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
