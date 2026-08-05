import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_submitter():
    path = ROOT / "dev" / "_submit_l18_at_reset.py"
    spec = importlib.util.spec_from_file_location("submit_l18", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Completed:
    def __init__(self, stdout="", stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


def test_l18_submitter_does_not_write_marker_when_refs_missing(tmp_path, monkeypatch):
    submit = load_submitter()
    versions = {slug: i + 1 for i, slug in enumerate(submit.ORDER)}
    marker = tmp_path / "submitted.marker"
    monkeypatch.setattr(submit, "MARKER", str(marker))
    monkeypatch.setattr(submit.time, "sleep", lambda _seconds: None)

    def fake_run(_cmd, **_kwargs):
        return Completed(stdout="no new submissions yet\n")

    refs = submit.submit_all(versions, run=fake_run, before_refs=set())

    assert refs == {}
    assert not marker.exists()


def test_l18_submitter_writes_marker_only_after_five_confirmed_refs(tmp_path, monkeypatch):
    submit = load_submitter()
    versions = {slug: i + 1 for i, slug in enumerate(submit.ORDER)}
    marker = tmp_path / "submitted.marker"
    monkeypatch.setattr(submit, "MARKER", str(marker))
    monkeypatch.setattr(submit.time, "sleep", lambda _seconds: None)
    calls = {"submit": 0, "list": 0}

    def fake_run(cmd, **_kwargs):
        if "submit" in cmd:
            calls["submit"] += 1
            return Completed(stdout="submitted\n")
        calls["list"] += 1
        rows = [
            "ref,fileName,date,description,status,publicScore,privateScore",
        ]
        for i, slug in enumerate(submit.ORDER, start=1):
            rows.append(
                f"900{i},submission.csv,2026-08-06 00:00:0{i},"
                f"{submit.MSG[slug]},SubmissionStatus.PENDING,,"
            )
        return Completed(stdout="\n".join(rows))

    refs = submit.submit_all(versions, run=fake_run, before_refs=set())

    assert set(refs) == set(submit.ORDER)
    assert marker.exists()
    assert calls["submit"] == 5
    assert calls["list"] >= 5
