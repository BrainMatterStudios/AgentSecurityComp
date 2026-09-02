#!/usr/bin/env python3
"""Build a Kaggle NOTEBOOK (kernel) carrying the full Working Note as markdown cells.

Discussion posts cap at 30,000 chars but the note is ~105k, so the full note lives in a notebook
(no length cap; the conventional Working Note format for this competition). Splits working_note.md
into one markdown cell per top-level (## ) section for readability. Pushed PRIVATE; the author
reviews in-browser and makes it public.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
md = (ROOT / "paper" / "working_note.md").read_text()

# Split into markdown cells at top-level "## " section boundaries; everything before the
# first "## " (title + front-matter + abstract heading) is the first cell.
lines = md.splitlines(keepends=True)
cells_src, cur = [], []
for ln in lines:
    if ln.startswith("## ") and cur:
        cells_src.append("".join(cur))
        cur = [ln]
    else:
        cur.append(ln)
if cur:
    cells_src.append("".join(cur))


def mdcell(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


nb = {
    "cells": [mdcell(s) for s in cells_src],
    "metadata": {"kernelspec": {"language": "python", "name": "python3", "display_name": "Python 3"},
                 "language_info": {"name": "python"}},
    "nbformat": 4, "nbformat_minor": 5,
}

d = ROOT / "submission_kernel_working_note"
d.mkdir(exist_ok=True)
(d / "working-note.ipynb").write_text(json.dumps(nb))
(d / "kernel-metadata.json").write_text(json.dumps({
    "id": "ahmedmobasher86/jed-working-note",
    "title": "Working Note: Guardrail-Predicate Asymmetry",
    "code_file": "working-note.ipynb",
    "language": "python", "kernel_type": "notebook",
    "is_private": True,            # author makes it public after review
    "enable_gpu": False, "enable_internet": False,
    "competition_sources": ["ai-agent-security-multi-step-tool-attacks"],
    "dataset_sources": [], "kernel_sources": []}, indent=2))
print(f"built {d} with {len(cells_src)} markdown cells ({len(md)} chars total)")
