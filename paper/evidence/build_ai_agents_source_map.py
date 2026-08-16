#!/usr/bin/env python3
"""Build a privacy-preserving provenance map for the AI-agents case study."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sqlite3
import subprocess
from collections import Counter
from pathlib import Path


CASE_ROOTS = {
    "AgentSecurityComp": "-Users-ahmed-Documents-AgentSecurityComp",
    "ARC-AGI-3": "-Users-ahmed-Documents-ArcAGI3",
}
PAPER_AUDIT_CODEX_ROOT = "01a0091e-6c06-72e0-ba1c-e5499447d566"
FIELDS = [
    "provider",
    "case",
    "record_id",
    "record_class",
    "source_locator",
    "canonical_parent_id",
    "canonical_conversation_id",
    "disposition",
    "reason",
]


def normalized_text_hash(content):
    parts = []
    if isinstance(content, str):
        parts = [content]
    elif isinstance(content, list):
        parts = [
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        ]
    normalized = re.sub(r"\s+", " ", "\n".join(parts)).strip()
    if not normalized:
        return None
    return hashlib.sha256(normalized.encode()).hexdigest()


def read_claude_root(path, case):
    entrypoints = set()
    legacy_ids = set()
    bridge_ids = set()
    message_uuids = set()
    timestamps = []
    explicit_prompt_hashes = []
    explicit_prompt_time_hashes = []
    type_counts = Counter()

    with path.open(errors="replace") as source:
        for line in source:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            type_counts[row.get("type", "unknown")] += 1
            if row.get("entrypoint"):
                entrypoints.add(str(row["entrypoint"]))
            if row.get("session_id"):
                legacy_ids.add(str(row["session_id"]))
            if row.get("bridgeSessionId"):
                bridge_ids.add(str(row["bridgeSessionId"]))
            if row.get("uuid"):
                message_uuids.add(str(row["uuid"]))
            if row.get("timestamp"):
                timestamps.append(str(row["timestamp"]))
            if row.get("type") == "user" and row.get("promptSource") in {
                "typed",
                "queued",
            }:
                digest = normalized_text_hash((row.get("message") or {}).get("content"))
                if digest:
                    explicit_prompt_hashes.append(digest)
                    explicit_prompt_time_hashes.append((row.get("timestamp", ""), digest))

    if entrypoints == {"cli"} and explicit_prompt_hashes:
        record_class = "primary-session"
        reason = "native CLI record with an explicit typed or queued prompt"
    elif entrypoints == {"sdk-cli"}:
        record_class = "tool-result-derivative"
        reason = "SDK-created record; excluded from human conversation counts"
    else:
        record_class = "tool-result-derivative"
        reason = "bridge or initialization stub without an explicit prompt"

    return {
        "case": case,
        "id": path.stem,
        "path": path,
        "entrypoints": entrypoints,
        "legacy_ids": legacy_ids,
        "bridge_ids": bridge_ids,
        "message_uuids": message_uuids,
        "timestamps": timestamps,
        "explicit_prompt_hashes": explicit_prompt_hashes,
        "explicit_prompt_time_hashes": explicit_prompt_time_hashes,
        "type_counts": type_counts,
        "record_class": record_class,
        "reason": reason,
        "canonical_parent_id": "not-recorded",
        "canonical_conversation_id": "not-counted",
        "disposition": "trace-only",
    }


def assign_claude_canonicals(records):
    parent = {record["id"]: record["id"] for record in records}

    def find(item):
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(left, right):
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    identities = {}
    for record in records:
        identities[record["id"]] = (
            {record["id"]} | record["legacy_ids"] | record["bridge_ids"]
        )

    for index, left in enumerate(records):
        for right in records[index + 1 :]:
            if identities[left["id"]] & identities[right["id"]]:
                union(left["id"], right["id"])

    components = {}
    for record in records:
        components.setdefault(find(record["id"]), []).append(record)

    for members in components.values():
        substantive = [
            record for record in members if record["record_class"] == "primary-session"
        ]
        if not substantive:
            continue
        canonical = min(
            substantive,
            key=lambda record: (
                min(record["timestamps"]) if record["timestamps"] else "9999",
                record["id"],
            ),
        )["id"]
        for record in members:
            record["canonical_parent_id"] = canonical
            record["canonical_conversation_id"] = canonical
            if record["record_class"] == "primary-session":
                if record["id"] == canonical:
                    record["disposition"] = "included-canonical"
                    record["reason"] = "earliest substantive record in linked continuation group"
                else:
                    record["disposition"] = "excluded-continuation"
                    record["reason"] = "linked by legacy session or bridge identifier"


def audit_claude_overlap(records):
    substantive = [
        record for record in records if record["record_class"] == "primary-session"
    ]
    copied_prefix_pairs = 0
    copied_prompt_run_pairs = 0
    shared_uuid_pairs = 0
    repeated_prompt_time_pairs = 0

    for index, left in enumerate(substantive):
        for right in substantive[index + 1 :]:
            if left["message_uuids"] & right["message_uuids"]:
                shared_uuid_pairs += 1
            if set(left["explicit_prompt_time_hashes"]) & set(
                right["explicit_prompt_time_hashes"]
            ):
                repeated_prompt_time_pairs += 1

            left_hashes = left["explicit_prompt_hashes"]
            right_hashes = right["explicit_prompt_hashes"]
            common_prefix = 0
            for left_hash, right_hash in zip(left_hashes, right_hashes):
                if left_hash != right_hash:
                    break
                common_prefix += 1
            if common_prefix >= 3:
                copied_prefix_pairs += 1

            left_runs = {
                tuple(left_hashes[offset : offset + 3])
                for offset in range(max(0, len(left_hashes) - 2))
            }
            right_runs = {
                tuple(right_hashes[offset : offset + 3])
                for offset in range(max(0, len(right_hashes) - 2))
            }
            if left_runs & right_runs:
                copied_prompt_run_pairs += 1

    return {
        "substantive_records": len(substantive),
        "shared_uuid_pairs": shared_uuid_pairs,
        "repeated_prompt_time_pairs": repeated_prompt_time_pairs,
        "copied_prefix_pairs": copied_prefix_pairs,
        "copied_prompt_run_pairs": copied_prompt_run_pairs,
    }


def claude_rows(claude_projects):
    rows = []
    all_roots = []
    root_by_case_and_id = {}

    for case, directory in CASE_ROOTS.items():
        base = claude_projects / directory
        roots = [read_claude_root(path, case) for path in sorted(base.glob("*.jsonl"))]
        assign_claude_canonicals(roots)
        all_roots.extend(roots)
        root_by_case_and_id.update({(case, record["id"]): record for record in roots})

        for record in roots:
            rows.append(
                {
                    "provider": "Claude Code",
                    "case": case,
                    "record_id": record["id"],
                    "record_class": record["record_class"],
                    "source_locator": f"claude:{case}/{record['path'].name}",
                    "canonical_parent_id": record["canonical_parent_id"],
                    "canonical_conversation_id": record[
                        "canonical_conversation_id"
                    ],
                    "disposition": record["disposition"],
                    "reason": record["reason"],
                }
            )

        for path in sorted(base.rglob("*.jsonl")):
            relative = path.relative_to(base)
            if len(relative.parts) == 1:
                continue
            root_id = relative.parts[0]
            root = root_by_case_and_id[(case, root_id)]
            relative_text = relative.as_posix()
            if relative.name == "journal.jsonl" and "workflows" in relative.parts:
                record_class = "workflow-journal"
                reason = "workflow journal; traceability only"
            elif "scratchpad" in relative_text.lower():
                record_class = "scratchpad-copy"
                reason = "scratchpad copy; excluded from conversation counts"
            elif "tool-result" in relative_text.lower() or "tool_result" in relative_text.lower():
                record_class = "tool-result-derivative"
                reason = "tool-result derivative; excluded from conversation counts"
            else:
                record_class = "subagent"
                reason = "child record linked to top-level Claude record"
            rows.append(
                {
                    "provider": "Claude Code",
                    "case": case,
                    "record_id": f"{root_id}:{relative.with_suffix('').as_posix()}",
                    "record_class": record_class,
                    "source_locator": f"claude:{case}/{relative_text}",
                    "canonical_parent_id": root_id,
                    "canonical_conversation_id": root[
                        "canonical_conversation_id"
                    ],
                    "disposition": "trace-only",
                    "reason": reason,
                }
            )

    return rows, all_roots, audit_claude_overlap(all_roots)


def first_codex_metadata(path):
    with path.open(errors="replace") as source:
        for line in source:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("type") == "session_meta":
                return row.get("payload") or {}
    return {}


def assign_codex_canonicals(records):
    by_id = {record["id"]: record for record in records}

    def resolve(record):
        if record.get("session_id"):
            return record["session_id"]
        current = record
        visited = set()
        while current.get("parent_id") and current["id"] not in visited:
            visited.add(current["id"])
            parent_id = current["parent_id"]
            parent = by_id.get(parent_id)
            if parent is None:
                return parent_id
            if parent.get("session_id"):
                return parent["session_id"]
            current = parent
        return current["id"]

    for record in records:
        record["canonical"] = resolve(record)


def codex_rows(codex_sessions):
    result = subprocess.run(
        [
            "rg",
            "-l",
            "AgentSecurityComp|/Users/ahmed/Documents/ArcAGI3",
            str(codex_sessions),
            "-g",
            "*.jsonl",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    paths = [Path(line) for line in result.stdout.splitlines() if line]
    records = []
    for path in sorted(paths):
        metadata = first_codex_metadata(path)
        cwd = str(metadata.get("cwd", ""))
        if "AgentSecurityComp" in cwd:
            case = "AgentSecurityComp"
        elif "ArcAGI3" in cwd:
            case = "ARC-AGI-3"
        else:
            case = "incidental-match"
        record_id = str(metadata.get("id", path.stem))
        parent_id = str(metadata.get("parent_thread_id", ""))
        session_id = str(metadata.get("session_id", ""))
        records.append(
            {
                "path": path,
                "case": case,
                "id": record_id,
                "parent_id": parent_id,
                "session_id": session_id,
            }
        )

    assign_codex_canonicals(records)
    for record in records:
        parent_id = record["parent_id"]
        canonical = record["canonical"]
        if record["case"] == "incidental-match":
            disposition = "excluded-incidental"
            reason = "content match but metadata working directory is outside both cases"
        elif canonical == PAPER_AUDIT_CODEX_ROOT:
            disposition = "excluded-paper-audit"
            reason = "current paper-design and provenance-audit lineage"
        elif parent_id:
            disposition = "trace-only"
            reason = "child rollout linked to canonical root"
        else:
            disposition = "included-canonical"
            reason = "native historical root rollout in a case working directory"
        yield {
            "provider": "Codex",
            "case": record["case"],
            "record_id": record["id"],
            "record_class": "subagent" if parent_id else "primary-session",
            "source_locator": f"codex:{record['path'].relative_to(codex_sessions).as_posix()}",
            "canonical_parent_id": parent_id or record["id"],
            "canonical_conversation_id": canonical,
            "disposition": disposition,
            "reason": reason,
        }


def opencode_rows(database):
    connection = sqlite3.connect(database)
    try:
        records = connection.execute(
            """
            select id, parent_id, directory
            from session
            where lower(directory) like '%agentsecuritycomp%'
               or lower(directory) like '%arcagi3%'
            order by time_created
            """
        ).fetchall()
    finally:
        connection.close()

    for record_id, parent_id, directory in records:
        case = "AgentSecurityComp" if "AgentSecurityComp" in directory else "ARC-AGI-3"
        yield {
            "provider": "OpenCode/DeepSeek",
            "case": case,
            "record_id": record_id,
            "record_class": "specialist" if parent_id else "primary-session",
            "source_locator": f"opencode:session/{record_id}",
            "canonical_parent_id": parent_id or record_id,
            "canonical_conversation_id": parent_id or record_id,
            "disposition": "trace-only" if parent_id else "included-canonical",
            "reason": (
                "specialist linked by session.parent_id"
                if parent_id
                else "supplementary parent session"
            ),
        }


def static_rows():
    return [
        {
            "provider": "Git",
            "case": "AgentSecurityComp",
            "record_id": "2ed68e80705906dcbdf4f707edf8c37089ce0906",
            "record_class": "repository-revision",
            "source_locator": "git:AgentSecurityComp@2ed68e80705906dcbdf4f707edf8c37089ce0906",
            "canonical_parent_id": "not-applicable",
            "canonical_conversation_id": "not-applicable",
            "disposition": "included-source",
            "reason": "pinned primary repository boundary",
        },
        {
            "provider": "Git",
            "case": "ARC-AGI-3",
            "record_id": "ebe5b3eca70260910144ae54e057c3d06ea0e14d",
            "record_class": "repository-revision",
            "source_locator": "git:ArcAGI3@ebe5b3eca70260910144ae54e057c3d06ea0e14d",
            "canonical_parent_id": "not-applicable",
            "canonical_conversation_id": "not-applicable",
            "disposition": "included-source",
            "reason": "pinned comparative repository boundary",
        },
        {
            "provider": "Author interview",
            "case": "cross-case",
            "record_id": "approved-testimony-2026-08-16",
            "record_class": "retrospective-testimony",
            "source_locator": "brief:task-1-author-testimony",
            "canonical_parent_id": "not-applicable",
            "canonical_conversation_id": "not-applicable",
            "disposition": "included-source",
            "reason": "approved retrospective testimony set",
        },
    ]


def summarize(rows, claude_roots, overlap):
    provider_counts = Counter(row["provider"] for row in rows)
    class_counts = Counter(
        (row["provider"], row["record_class"]) for row in rows
    )
    disposition_counts = Counter(
        (row["provider"], row["disposition"]) for row in rows
    )
    claude_canonical_by_case = Counter(
        record["case"]
        for record in claude_roots
        if record["disposition"] == "included-canonical"
    )
    codex_canonical_by_case = Counter(
        row["case"]
        for row in rows
        if row["provider"] == "Codex"
        and row["disposition"] == "included-canonical"
    )
    opencode_canonical_by_case = Counter(
        row["case"]
        for row in rows
        if row["provider"] == "OpenCode/DeepSeek"
        and row["disposition"] == "included-canonical"
    )
    return {
        "rows_total": len(rows),
        "provider_rows": dict(sorted(provider_counts.items())),
        "class_rows": {
            f"{provider}|{record_class}": count
            for (provider, record_class), count in sorted(class_counts.items())
        },
        "disposition_rows": {
            f"{provider}|{disposition}": count
            for (provider, disposition), count in sorted(disposition_counts.items())
        },
        "canonical_conversations": {
            "Claude Code": dict(sorted(claude_canonical_by_case.items())),
            "Codex": dict(sorted(codex_canonical_by_case.items())),
            "OpenCode/DeepSeek": dict(sorted(opencode_canonical_by_case.items())),
        },
        "claude_overlap_audit": overlap,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("ai-agents-research-source-map.tsv"),
    )
    parser.add_argument(
        "--claude-projects", type=Path, default=Path.home() / ".claude" / "projects"
    )
    parser.add_argument(
        "--codex-sessions", type=Path, default=Path.home() / ".codex" / "sessions"
    )
    parser.add_argument(
        "--opencode-database",
        type=Path,
        default=Path.home() / ".local" / "share" / "opencode" / "opencode.db",
    )
    arguments = parser.parse_args()

    claude_manifest, claude_roots, overlap = claude_rows(arguments.claude_projects)
    rows = (
        claude_manifest
        + list(codex_rows(arguments.codex_sessions))
        + list(opencode_rows(arguments.opencode_database))
        + static_rows()
    )
    rows.sort(
        key=lambda row: (
            row["provider"],
            row["case"],
            row["source_locator"],
            row["record_id"],
        )
    )

    with arguments.output.open("w", newline="") as destination:
        writer = csv.DictWriter(
            destination,
            fieldnames=FIELDS,
            dialect="excel-tab",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps(summarize(rows, claude_roots, overlap), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
