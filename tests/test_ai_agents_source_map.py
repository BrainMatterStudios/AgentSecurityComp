import importlib.util
import json
from pathlib import Path


SCRIPT = (
    Path(__file__).parents[1]
    / "paper"
    / "evidence"
    / "build_ai_agents_source_map.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("source_map", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def test_claude_continuations_share_one_canonical_conversation(tmp_path):
    module = load_module()
    first = tmp_path / "first.jsonl"
    second = tmp_path / "second.jsonl"
    write_jsonl(
        first,
        [
            {
                "type": "user",
                "sessionId": "first",
                "session_id": "legacy",
                "entrypoint": "cli",
                "promptSource": "typed",
                "timestamp": "2026-01-01T00:00:00Z",
                "uuid": "u1",
                "message": {"content": "first prompt"},
            }
        ],
    )
    write_jsonl(
        second,
        [
            {
                "type": "user",
                "sessionId": "second",
                "session_id": "legacy",
                "entrypoint": "cli",
                "promptSource": "typed",
                "timestamp": "2026-01-02T00:00:00Z",
                "uuid": "u2",
                "message": {"content": "second prompt"},
            }
        ],
    )

    records = [
        module.read_claude_root(first, "Case"),
        module.read_claude_root(second, "Case"),
    ]
    module.assign_claude_canonicals(records)

    assert {record["canonical_conversation_id"] for record in records} == {"first"}
    assert [record["disposition"] for record in records] == [
        "included-canonical",
        "excluded-continuation",
    ]


def test_claude_sdk_and_empty_bridge_records_are_not_conversations(tmp_path):
    module = load_module()
    sdk = tmp_path / "sdk.jsonl"
    bridge = tmp_path / "bridge.jsonl"
    write_jsonl(
        sdk,
        [
            {
                "type": "user",
                "sessionId": "sdk",
                "entrypoint": "sdk-cli",
                "promptSource": "sdk",
                "message": {"content": "tool prompt"},
            }
        ],
    )
    write_jsonl(
        bridge,
        [{"type": "bridge-session", "sessionId": "bridge"}],
    )

    records = [
        module.read_claude_root(sdk, "Case"),
        module.read_claude_root(bridge, "Case"),
    ]
    module.assign_claude_canonicals(records)

    assert [record["record_class"] for record in records] == [
        "tool-result-derivative",
        "tool-result-derivative",
    ]
    assert all(record["disposition"] == "trace-only" for record in records)


def test_overlap_audit_reports_copied_prompt_prefix_without_text(tmp_path):
    module = load_module()
    first = tmp_path / "first.jsonl"
    second = tmp_path / "second.jsonl"
    common = ["sensitive first", "sensitive second", "sensitive third"]
    write_jsonl(
        first,
        [
            {
                "type": "user",
                "sessionId": "first",
                "entrypoint": "cli",
                "promptSource": "typed",
                "timestamp": f"2026-01-0{index}T00:00:00Z",
                "uuid": f"a{index}",
                "message": {"content": text},
            }
            for index, text in enumerate(common, 1)
        ],
    )
    write_jsonl(
        second,
        [
            {
                "type": "user",
                "sessionId": "second",
                "entrypoint": "cli",
                "promptSource": "typed",
                "timestamp": f"2026-02-0{index}T00:00:00Z",
                "uuid": f"b{index}",
                "message": {"content": text},
            }
            for index, text in enumerate(common, 1)
        ],
    )
    records = [
        module.read_claude_root(first, "Case"),
        module.read_claude_root(second, "Case"),
    ]

    audit = module.audit_claude_overlap(records)

    assert audit["copied_prefix_pairs"] == 1
    assert "sensitive" not in json.dumps(audit)


def test_codex_canonical_uses_ultimate_parent_when_session_id_is_absent():
    module = load_module()
    records = [
        {"id": "root", "parent_id": "", "session_id": ""},
        {"id": "child", "parent_id": "root", "session_id": ""},
        {"id": "grandchild", "parent_id": "child", "session_id": ""},
    ]

    module.assign_codex_canonicals(records)

    assert [record["canonical"] for record in records] == ["root", "root", "root"]
