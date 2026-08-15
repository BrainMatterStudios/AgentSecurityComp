"""Arm L31 submission through macOS launchd.

The launchd job runs from ~/l31_arm rather than the repo under Documents, because
older arms showed launchd can be blocked by macOS privacy controls when reading
Documents directly.
"""

import datetime as dt
import json
import os
import plistlib
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _build_l31 as build_l31


ROOT = Path(__file__).resolve().parents[1]
ARM_DIR = Path.home() / "l31_arm"
KERNEL_DIR = ARM_DIR / "kernels"
LOG_DIR = ARM_DIR / "logs"
LAUNCHD_LABEL = "com.ahmed.agentsecuritycomp.l31-submit"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{LAUNCHD_LABEL}.plist"
DEFAULT_MARGIN_MINUTES = 7

# Versions already pushed before the durable arm encountered Kaggle's two-GPU
# batch-session limit.
KNOWN_VERSIONS = {
    "chainpack-2x8": "34",
    "chainpack-3x8": "36",
}


def next_target_reset(now: dt.datetime | None = None) -> str:
    current = now or dt.datetime.now(dt.UTC)
    tomorrow = current.date() + dt.timedelta(days=1)
    target = dt.datetime.combine(tomorrow, dt.time(0, 0), tzinfo=dt.UTC)
    target += dt.timedelta(minutes=DEFAULT_MARGIN_MINUTES)
    return target.isoformat().replace("+00:00", "Z")


def _label_for_directory(directory: str) -> str:
    if "2x8" in directory:
        return "chainpack-2x8"
    if "3x8" in directory:
        return "chainpack-3x8"
    if "4x8" in directory:
        return "chainpack-4x8"
    if "4x4" in directory:
        return "chainpack-4x4"
    return "fastemit-k8"


def manifest() -> dict:
    submissions = []
    for rung in build_l31.RUNGS:
        label = _label_for_directory(rung.directory)
        submissions.append(
            {
                "label": label,
                "directory": rung.directory,
                "slug": rung.slug,
                "version": KNOWN_VERSIONS.get(label),
                "message": rung.note,
            }
        )
    return {"target_reset_utc": next_target_reset(), "submissions": submissions}


def copy_payload() -> None:
    ARM_DIR.mkdir(exist_ok=True)
    KERNEL_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "dev" / "_submit_l31_after_reset.py", ARM_DIR / "submit_l31.py")
    (ARM_DIR / "l31_manifest.json").write_text(json.dumps(manifest(), indent=2, sort_keys=True))
    (ARM_DIR / "submission.csv").write_text("Id,Score\ngpt_oss_public,0.0\n")
    for rung in build_l31.RUNGS:
        src = ROOT / rung.directory
        dst = KERNEL_DIR / rung.directory
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)


def plist() -> dict:
    return {
        "Label": LAUNCHD_LABEL,
        "ProgramArguments": [
            "/usr/bin/caffeinate",
            "-i",
            "-s",
            sys.executable,
            str(ARM_DIR / "submit_l31.py"),
        ],
        "WorkingDirectory": str(ARM_DIR),
        "RunAtLoad": True,
        "KeepAlive": {"SuccessfulExit": False},
        "EnvironmentVariables": {
            "PATH": (
                "/Library/Frameworks/Python.framework/Versions/3.14/bin:"
                "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
            ),
        },
        "StandardOutPath": str(LOG_DIR / "launchd.out.log"),
        "StandardErrorPath": str(LOG_DIR / "launchd.err.log"),
    }


def install_launchd() -> None:
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PLIST_PATH.open("wb") as f:
        plistlib.dump(plist(), f)
    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", domain, str(PLIST_PATH)], check=False)
    subprocess.run(["launchctl", "bootstrap", domain, str(PLIST_PATH)], check=True)
    subprocess.run(["launchctl", "kickstart", "-k", f"{domain}/{LAUNCHD_LABEL}"], check=False)


def main() -> int:
    copy_payload()
    install_launchd()
    print(f"armed {LAUNCHD_LABEL}")
    print(f"arm dir: {ARM_DIR}")
    print(f"plist: {PLIST_PATH}")
    print(f"target: {json.loads((ARM_DIR / 'l31_manifest.json').read_text())['target_reset_utc']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
