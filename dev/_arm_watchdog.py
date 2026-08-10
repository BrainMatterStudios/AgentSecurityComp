#!/usr/bin/env python3
"""Detach a watchdog for a reset submitter into its own session so it survives
parent-shell teardown (the L20 submitter was reaped when its spawning session
ended). Prints the detached caffeinate pid.

Usage: python3 dev/_arm_watchdog.py <watchdog_sh> <submitter_py> <marker> <logfile>
"""
import os
import subprocess
import sys

sub_script, script, marker, wlog = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
cmd = ["caffeinate", "-i", "-s", "bash", sub_script, script, marker, wlog]
p = subprocess.Popen(
    cmd,
    start_new_session=True,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
print(f"detached watchdog session pid={p.pid}")
