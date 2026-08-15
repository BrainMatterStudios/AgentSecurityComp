"""Durable L31 submitter.

Runs from a self-contained arm directory. It resumes safely:
- pushes any L31 kernels that do not yet have recorded versions,
- waits for pushed kernels to finish,
- waits until the recorded UTC quota-reset target,
- submits each exact kernel version once, recording markers.
"""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
from pathlib import Path


COMPETITION = "ai-agent-security-multi-step-tool-attacks"
DEFAULT_MARGIN_MINUTES = 7
MANIFEST_PATH = Path("l31_manifest.json")
LOG_DIR = Path("logs")

DEFAULT_MANIFEST = {
    "target_reset_utc": None,
    "submissions": [
        {
            "label": "chainpack-2x8",
            "directory": "submission_kernel_l31_chainpack_2x8",
            "slug": "ahmedmobasher86/jed-public-pt-safe",
            "version": None,
            "message": "L31 chainpack 2x8: GPT-routed two K8 messages per candidate",
        },
        {
            "label": "chainpack-3x8",
            "directory": "submission_kernel_l31_chainpack_3x8",
            "slug": "ahmedmobasher86/jed-public-pt-probe",
            "version": None,
            "message": "L31 chainpack 3x8: stretch GPT chainpack",
        },
        {
            "label": "chainpack-4x8",
            "directory": "submission_kernel_l31_chainpack_4x8",
            "slug": "ahmedmobasher86/jed-public-k1nx-1000",
            "version": None,
            "message": "L31 chainpack 4x8: crown shot",
        },
        {
            "label": "chainpack-4x4",
            "directory": "submission_kernel_l31_chainpack_4x4",
            "slug": "ahmedmobasher86/jed-public-k1nx-1200",
            "version": None,
            "message": "L31 chainpack 4x4: lower-hop both-board transfer probe",
        },
        {
            "label": "fastemit-k8",
            "directory": "submission_kernel_l31_fastemit_k8",
            "slug": "ahmedmobasher86/jed-public-k1nx-800",
            "version": None,
            "message": "L31 fast-emit K8: calibrated high-ceiling backup",
        },
    ],
}


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


def next_reset_time(now: dt.datetime, margin_minutes: int = DEFAULT_MARGIN_MINUTES) -> dt.datetime:
    tomorrow = now.date() + dt.timedelta(days=1)
    reset = dt.datetime.combine(tomorrow, dt.time(0, 0), tzinfo=dt.UTC)
    return reset + dt.timedelta(minutes=margin_minutes)


def log(message: str) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    stamp = utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{stamp}] {message}"
    print(line, flush=True)
    with (LOG_DIR / "submit_l31.log").open("a") as f:
        f.write(line + "\n")


def run_command(command: list[str], cwd: Path | None = None) -> tuple[int, str]:
    proc = subprocess.run(
        command,
        cwd=str(cwd) if cwd is not None else None,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return proc.returncode, proc.stdout


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text())
    return json.loads(json.dumps(DEFAULT_MANIFEST))


def save_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True))


def quota_exhausted(output: str) -> bool:
    needles = (
        "daily Submission allowance",
        "Submission not allowed",
        "You have already submitted",
        "exceeded",
    )
    return any(needle.lower() in output.lower() for needle in needles)


def parse_pushed_version(output: str) -> str | None:
    match = re.search(r"Kernel version\s+(\d+)\s+successfully pushed", output)
    return match.group(1) if match else None


def gpu_slots_full(output: str) -> bool:
    return "Maximum batch GPU session count" in output


def push_missing_versions(manifest: dict, retry_interval_seconds: int, dry_run: bool) -> None:
    for item in manifest["submissions"]:
        if item.get("version"):
            continue
        local_dir = Path("kernels") / item["directory"]
        if not local_dir.exists():
            raise FileNotFoundError(f"missing kernel directory: {local_dir}")
        while not item.get("version"):
            if dry_run:
                log(f"dry-run: would push {item['label']} from {local_dir}")
                item["version"] = "0"
                save_manifest(manifest)
                break
            code, output = run_command(["kaggle", "kernels", "push", "-p", str(local_dir)])
            log(f"{item['label']}: kernel push exit={code}")
            if output.strip():
                print(output, flush=True)
            version = parse_pushed_version(output)
            if code == 0 and version:
                item["version"] = version
                save_manifest(manifest)
                break
            if gpu_slots_full(output):
                log(f"{item['label']}: GPU batch slots full; retrying")
                time.sleep(retry_interval_seconds)
                continue
            raise RuntimeError(f"kernel push failed for {item['label']}: {output[:500]}")


def kernel_status(slug: str) -> str:
    code, output = run_command(["kaggle", "kernels", "status", slug])
    if code != 0:
        raise RuntimeError(f"kernel status failed for {slug}: {output[:500]}")
    match = re.search(r'KernelWorkerStatus\.([A-Z_]+)', output)
    return match.group(1) if match else output.strip()


def wait_for_kernel_completion(manifest: dict, retry_interval_seconds: int, dry_run: bool) -> None:
    if dry_run:
        for item in manifest["submissions"]:
            log(f"dry-run: would wait for {item['slug']} version {item['version']}")
        return
    pending = {item["slug"] for item in manifest["submissions"]}
    while pending:
        finished = set()
        for slug in sorted(pending):
            status = kernel_status(slug)
            log(f"{slug}: status={status}")
            if status == "COMPLETE":
                finished.add(slug)
            elif status in {"ERROR", "CANCELLED", "FAILED"}:
                raise RuntimeError(f"{slug} ended with status {status}")
        pending -= finished
        if pending:
            time.sleep(retry_interval_seconds)


def wait_until_target(manifest: dict, dry_run: bool) -> None:
    raw = manifest.get("target_reset_utc")
    if raw:
        target = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    else:
        target = next_reset_time(utc_now())
        manifest["target_reset_utc"] = target.isoformat().replace("+00:00", "Z")
        save_manifest(manifest)
    wait_s = max(0.0, (target - utc_now()).total_seconds())
    log(f"target reset submit time {target.strftime('%Y-%m-%dT%H:%M:%SZ')} wait={wait_s:.0f}s")
    if not dry_run and wait_s > 0:
        time.sleep(wait_s)


def submitted_marker(label: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", label)
    return LOG_DIR / f"{safe}.submitted"


def submit_remaining(
    manifest: dict,
    retry_minutes: int,
    retry_interval_seconds: int,
    dry_run: bool,
) -> int:
    deadline = utc_now() + dt.timedelta(minutes=retry_minutes)
    remaining = [item for item in manifest["submissions"] if not submitted_marker(item["label"]).exists()]
    while remaining and utc_now() <= deadline:
        item = remaining[0]
        version = str(item["version"])
        command = [
            "kaggle",
            "competitions",
            "submit",
            COMPETITION,
            "-f",
            "submission.csv",
            "-k",
            item["slug"],
            "-v",
            version,
            "-m",
            item["message"],
        ]
        if dry_run:
            log(f"dry-run: would submit {item['label']} {item['slug']} v{version}")
            remaining.pop(0)
            continue
        code, output = run_command(command)
        log(f"{item['label']}: submit exit={code}")
        if output.strip():
            print(output, flush=True)
        if code == 0:
            submitted_marker(item["label"]).write_text(output)
            remaining.pop(0)
            time.sleep(15)
            continue
        if quota_exhausted(output):
            log(f"{item['label']}: quota unavailable; retrying")
            time.sleep(retry_interval_seconds)
            continue
        return code or 1
    if remaining:
        log(f"timed out with {len(remaining)} submissions remaining")
        return 1
    log("all L31 submissions completed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--retry-minutes", type=int, default=180)
    parser.add_argument("--retry-interval-seconds", type=int, default=300)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    Path("submission.csv").write_text("Id,Score\ngpt_oss_public,0.0\n")
    manifest = load_manifest()
    push_missing_versions(manifest, args.retry_interval_seconds, args.dry_run)
    wait_for_kernel_completion(manifest, args.retry_interval_seconds, args.dry_run)
    wait_until_target(manifest, args.dry_run)
    return submit_remaining(
        manifest,
        retry_minutes=args.retry_minutes,
        retry_interval_seconds=args.retry_interval_seconds,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
