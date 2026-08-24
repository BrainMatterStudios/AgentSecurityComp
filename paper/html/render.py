#!/usr/bin/env python3
"""Render the two living Markdown manuscripts as branded HTML drafts."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import sys

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).resolve().parent
FONTS_DIR = OUTPUT_DIR / "fonts"

FONT_SPECS = (
    ("Fraunces", "300 600", "fraunces-latin-300-600.woff2"),
    ("Geist", "300 700", "geist-latin-300-700.woff2"),
    ("JetBrains Mono", "400 600", "jetbrains-mono-latin-400-600.woff2"),
)


@dataclass(frozen=True)
class Paper:
    source: str
    output: str
    document_id: str
    kind: str
    deck: str
    subject: str
    stats: tuple[tuple[str, str], ...]
    kickers: tuple[str, ...]


PAPERS = (
    Paper(
        source="working_note.md",
        output="working_note.html",
        document_id="BMS-RP-26-01",
        kind="Research working note",
        deck=(
            "A source-audited account of where the guardrail and its scoring predicates "
            "disagree—and where a tested attack family reaches a throughput plateau."
        ),
        subject="AI Agent Security · Multi-Step Tool Attacks",
        stats=(
            ("4", "guardrail–predicate asymmetries"),
            ("2-gate", "local-to-live protocol"),
            ("mean", "strongly supported public aggregation"),
            ("24 Aug", "2026 authenticated addendum"),
        ),
        kickers=(
            "Summary", "Bounded thesis", "Evidence discipline", "Evaluator mechanics",
            "Security taxonomy", "Transfer tests", "For defenders", "Live catalogue",
            "Reproduction", "Communication", "Context", "Sources", "Notation", "Revision record",
        ),
    ),
    Paper(
        source="ai_agents_in_scientific_research.md",
        output="ai_agents_in_scientific_research.html",
        document_id="BMS-RP-26-02",
        kind="Research case study",
        deck=(
            "What two competition-based research projects reveal about access, "
            "execution, originality, and human oversight."
        ),
        subject="AI agents in computational research",
        stats=(
            ("31", "coded research episodes"),
            ("2", "comparative case studies"),
            ("17", "reviewed references"),
            ("2–5h", "daily human review · testimony"),
        ),
        kickers=(
            "Summary", "Researcher context", "Definitions", "Study design", "Primary case",
            "Comparative case", "Synthesis", "Value", "Failure modes", "Protocol",
            "Audience guidance", "Living record", "Disclosure", "Sources", "Methods appendix",
        ),
    ),
)


CSS = r"""
/* BrainMatterStudios — Research Paper · Brand Kit Rev 26.07
   Fraunces speaks, Geist explains, JetBrains Mono instruments.
   Colour is punctuation, not paint: the teal ember is the one accent. */
:root {
  --paper:#F4F6F7; --paper-2:#E9EDEF; --ink:#11181C; --ink-2:#1C242A;
  --muted:#5C6B73; --hair:rgba(17,24,28,.10); --hair-2:rgba(17,24,28,.18);
  --ember:#0E8C8C; --ember-text:#0B6E6E; --ember-wash:#DCE9E9;
  --pass:#4F6E30; --pass-w:#E7EDE1; --warn:#805E10; --warn-w:#F2EBDC;
  --fail:#A2382A; --fail-w:#F3E4E1;
  --serif:'Fraunces','Iowan Old Style',Charter,Palatino,Georgia,serif;
  --sans:'Geist',ui-sans-serif,system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,'SF Mono',SFMono-Regular,Menlo,monospace;
  --measure:38rem; --rail:9.5rem;
}
* { box-sizing:border-box; }
html { background:var(--paper); scroll-behavior:smooth; }
body {
  margin:0; padding:0 1.5rem 6rem; background:var(--paper); color:var(--ink);
  font-family:var(--sans); font-size:17px; line-height:1.62; letter-spacing:-.005em;
  font-feature-settings:"ss01","cv11"; -webkit-font-smoothing:antialiased;
  text-rendering:optimizeLegibility; counter-reset:tbl;
}
::selection { background:var(--ember); color:var(--paper); }
.wrap { max-width:calc(var(--rail) + var(--measure) + 3rem); margin:0 auto; }
.wordmark { font-family:var(--serif); font-weight:400; letter-spacing:-.03em; white-space:nowrap; color:var(--ink); line-height:1; }
.wordmark .i { position:relative; display:inline-block; }
.wordmark .tittle { position:absolute; left:50%; top:.11em; transform:translateX(-50%); width:.155em; height:.155em; border-radius:50%; background:var(--ember); }
.wordmark .stop,.stop { color:var(--ember); }
.wordmark-mono { font-family:var(--mono); font-weight:500; letter-spacing:.18em; color:var(--ink); }
.wordmark-mono .mid { color:var(--ember); }
.logo-lockup { display:flex; flex-direction:column; align-items:flex-start; gap:.85rem; padding-bottom:2.2rem; border-bottom:1px solid var(--hair-2); margin-bottom:2.6rem; }
.logo-lockup .wordmark { font-size:3.1rem; }
.logo-lockup .descriptor { font-family:var(--mono); font-size:.66rem; font-weight:500; letter-spacing:.2em; text-transform:uppercase; color:var(--muted); display:flex; flex-wrap:wrap; column-gap:.75rem; row-gap:.3rem; align-items:center; }
.logo-lockup .descriptor .tag { color:var(--ink-2); }
.logo-lockup .descriptor .sep { color:var(--hair-2); }
.titlepage { padding:4.2rem 0 0; }
.eyebrow { font-family:var(--mono); font-size:.68rem; letter-spacing:.16em; text-transform:uppercase; color:var(--ember-text); display:flex; flex-wrap:wrap; gap:.7rem; align-items:center; margin-bottom:2.2rem; }
.eyebrow .sep { color:var(--hair-2); }
h1 { font-family:var(--serif); font-weight:400; font-size:clamp(2.7rem,7.2vw,4.65rem); line-height:.94; letter-spacing:-.038em; text-wrap:balance; margin:0 0 1.45rem; }
.deck { font-size:clamp(1.05rem,2.4vw,1.3rem); line-height:1.42; color:var(--ink-2); letter-spacing:-.012em; max-width:34rem; text-wrap:balance; margin:0; }
.docrec { margin:3rem 0 0; border-top:1px solid var(--hair-2); border-bottom:1px solid var(--hair-2); display:grid; grid-template-columns:repeat(3,1fr); }
.docrec div { padding:1.1rem 1.4rem; border-right:1px solid var(--hair); }
.docrec div:nth-child(3n+1) { padding-left:0; }
.docrec div:nth-child(3n) { border-right:0; padding-right:0; }
.docrec div:nth-child(-n+3) { border-bottom:1px solid var(--hair); }
.docrec dt { font-family:var(--mono); font-size:.6rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin-bottom:.45rem; }
.docrec dd { margin:0; font-size:.88rem; line-height:1.45; color:var(--ink-2); }
.band { display:grid; grid-template-columns:repeat(4,1fr); border-bottom:1px solid var(--hair-2); margin:3.5rem 0 0; }
.stat { padding:1.8rem 1.25rem; border-right:1px solid var(--hair); }
.stat:first-child { padding-left:0; } .stat:last-child { border-right:0; padding-right:0; }
.stat .n { font-family:var(--serif); font-size:2.45rem; line-height:1; letter-spacing:-.035em; font-variant-numeric:tabular-nums; }
.stat .l { font-family:var(--mono); font-size:.61rem; line-height:1.5; letter-spacing:.075em; text-transform:uppercase; color:var(--muted); margin-top:.75rem; }
.source-record { margin:2.6rem 0 0; padding:1.1rem 1.25rem; border-left:2px solid var(--ember); background:var(--paper-2); color:var(--ink-2); font-size:.86rem; }
.source-record p,.source-record ul { margin:.45rem 0; } .source-record ul { padding-left:1.1rem; }
.source-record hr { display:none; }
.contents { margin:3.7rem 0 0; }
.contents .meta { font-family:var(--mono); font-size:.66rem; letter-spacing:.16em; text-transform:uppercase; color:var(--muted); margin-bottom:1.2rem; }
.contents ol { list-style:none; margin:0; padding:0; border-top:1px solid var(--hair-2); }
.contents li { border-bottom:1px solid var(--hair); margin:0; }
.contents a { display:flex; align-items:baseline; gap:1.1rem; padding:.78rem 0; text-decoration:none; color:var(--ink); border:0; }
.contents a:hover .t { color:var(--ember-text); }
.contents .n { font-family:var(--mono); font-size:.68rem; letter-spacing:.1em; color:var(--ember-text); width:2.8rem; flex:none; }
.contents .t { font-family:var(--serif); font-size:1.04rem; letter-spacing:-.018em; flex:1; transition:color .2s; }
.contents .k { font-family:var(--mono); font-size:.58rem; letter-spacing:.1em; text-transform:uppercase; color:var(--muted); text-align:right; }
main { margin-top:4.3rem; }
section { display:grid; grid-template-columns:var(--rail) minmax(0,1fr); gap:3rem; scroll-margin-top:1.5rem; }
section + section { margin-top:4.5rem; padding-top:.2rem; }
.rail .num { font-family:var(--mono); font-size:.7rem; font-weight:500; letter-spacing:.14em; color:var(--ember-text); padding-bottom:.5rem; border-bottom:1px solid var(--ember); display:inline-block; }
.rail .kicker { font-family:var(--mono); font-size:.62rem; line-height:1.55; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin-top:.85rem; }
.col { max-width:var(--measure); min-width:0; }
h2 { font-family:var(--serif); font-weight:400; font-size:2rem; line-height:1.08; letter-spacing:-.028em; text-wrap:balance; margin:0 0 1.25rem; }
h3 { font-family:var(--serif); font-weight:400; font-size:1.3rem; line-height:1.2; letter-spacing:-.02em; text-wrap:balance; margin:2.65rem 0 .75rem; scroll-margin-top:1.5rem; }
h4 { font-family:var(--mono); font-size:.72rem; line-height:1.5; letter-spacing:.1em; text-transform:uppercase; color:var(--ember-text); margin:2rem 0 .65rem; }
p { margin:0 0 1.05rem; } p:last-child { margin-bottom:0; }
.abstract .col > p:first-of-type { font-size:1.1rem; line-height:1.55; color:var(--ink-2); }
strong { font-weight:600; color:var(--ink); } em { font-style:italic; }
a { color:var(--ember-text); text-decoration:none; border-bottom:1px solid var(--hair-2); transition:color .2s,border-color .35s ease; overflow-wrap:anywhere; }
a:hover { border-color:var(--ember); } a:focus-visible { outline:2px solid var(--ember); outline-offset:3px; }
ul,ol { margin:0 0 1.05rem; padding-left:1.25rem; } li { margin-bottom:.52rem; } li::marker { color:var(--muted); }
hr { border:0; border-top:1px solid var(--hair-2); margin:2.4rem 0; }
blockquote { margin:2rem 0; padding:1.15rem 0 1.15rem 1.25rem; border-left:2px solid var(--ember); color:var(--ink-2); }
blockquote p { margin:0; font-family:var(--serif); font-size:1.22rem; line-height:1.38; letter-spacing:-.018em; }
pre { font-family:var(--mono); font-size:.75rem; line-height:1.65; background:var(--paper-2); border-left:1px solid var(--ember); padding:1.1rem 1.2rem; overflow-x:auto; margin:1.2rem 0; color:var(--ink-2); }
code { font-family:var(--mono); font-size:.84em; background:var(--paper-2); padding:.12em .34em; overflow-wrap:anywhere; }
pre code { background:none; padding:0; font-size:1em; overflow-wrap:normal; }
.tbl { counter-increment:tbl; margin:1.7rem 0 2rem; width:min(52rem,calc(100vw - 3rem - var(--rail))); }
.tablewrap { overflow-x:auto; padding-bottom:.25rem; }
table { border-collapse:collapse; width:100%; min-width:34rem; font-size:.82rem; line-height:1.48; }
th,td { text-align:left; padding:.65rem .82rem .65rem 0; border-bottom:1px solid var(--hair); vertical-align:top; overflow-wrap:normal; word-break:normal; hyphens:none; }
thead th { font-family:var(--mono); font-size:.59rem; font-weight:500; letter-spacing:.085em; text-transform:uppercase; color:var(--muted); border-bottom:1px solid var(--hair-2); }
tbody tr:last-child td { border-bottom:1px solid var(--hair-2); }
td code { white-space:normal; }
.tbl-cap { font-family:var(--mono); font-size:.6rem; line-height:1.55; letter-spacing:.06em; color:var(--muted); margin-top:.75rem; }
.tbl-cap::before { content:"Table " counter(tbl) " — "; color:var(--ember-text); }
.draft-note { margin-top:4rem; padding:1.4rem 0; border-top:1px solid var(--ember); border-bottom:1px solid var(--hair); display:flex; gap:1rem; align-items:baseline; }
.draft-note .tag { font-family:var(--mono); font-size:.62rem; font-weight:600; letter-spacing:.12em; text-transform:uppercase; color:var(--ember-text); flex:none; }
.draft-note p { color:var(--ink-2); font-size:.9rem; margin:0; }
footer { margin-top:5rem; padding-top:2.2rem; border-top:1px solid var(--hair-2); font-size:.9rem; color:var(--ink-2); }
.signoff { margin-top:1.5rem; padding-top:1.1rem; border-top:1px solid var(--hair); display:flex; align-items:center; justify-content:space-between; gap:1rem; flex-wrap:wrap; }
.signoff .wordmark-mono { font-size:12px; }
.signoff .meta { font-family:var(--mono); font-size:.61rem; letter-spacing:.09em; text-transform:uppercase; color:var(--muted); }
.signoff .meta .url { color:var(--ember-text); border:0; text-transform:none; }
.backtop { position:fixed; right:1.2rem; bottom:1.2rem; width:2.6rem; height:2.6rem; display:grid; place-items:center; border:1px solid var(--hair-2); background:color-mix(in srgb,var(--paper) 92%,transparent); color:var(--ember-text); font-family:var(--mono); font-size:.72rem; text-decoration:none; backdrop-filter:blur(8px); }
.backtop:hover { border-color:var(--ember); }
@media screen and (max-width:760px) {
  :root { --rail:0rem; }
  body { font-size:16px; padding:0 1.1rem 4rem; }
  .logo-lockup .wordmark { font-size:2.3rem; }
  .docrec { grid-template-columns:1fr; }
  .docrec div,.docrec div:nth-child(3n),.docrec div:nth-child(3n+1) { border-right:0; border-bottom:1px solid var(--hair); padding:1rem 0; }
  .docrec div:last-child { border-bottom:0; }
  .band { grid-template-columns:repeat(2,1fr); }
  .stat { padding:1.35rem 1rem; border-bottom:1px solid var(--hair); }
  .stat:nth-child(2) { border-right:0; } .stat:nth-child(3) { padding-left:0; }
  section { grid-template-columns:1fr; gap:0; }
  .rail { margin-bottom:1.2rem; display:flex; gap:1rem; align-items:baseline; }
  .rail .kicker { margin-top:0; }
  .contents .k { display:none; }
  .tbl { width:calc(100vw - 2.2rem); }
  .draft-note { align-items:flex-start; flex-direction:column; }
  .backtop { display:none; }
}
@media (prefers-reduced-motion:reduce) { * { scroll-behavior:auto!important; transition:none!important; } }
@page { size:A4; margin:16mm 15mm 18mm; }
@media print {
  :root { font-size:10.5pt; --paper:#FFF; --paper-2:#EFF2F3; --hair:rgba(17,24,28,.16); --hair-2:rgba(17,24,28,.30); --rail:7rem; }
  html,body { background:var(--paper); print-color-adjust:exact; -webkit-print-color-adjust:exact; }
  body { font-size:1rem; padding:0; }
  .wrap,.col { max-width:none; } .backtop { display:none; }
  a { color:var(--ink); border-bottom:0; }
  .titlepage { padding-top:0; break-after:page; }
  .contents { margin-top:0; break-after:page; }
  main { margin-top:0; }
  section + section { margin-top:2.5rem; }
  h1,h2,h3,h4 { break-after:avoid; break-inside:avoid; }
  .tbl,blockquote,pre,.band,.docrec,.source-record,.draft-note { break-inside:avoid; }
  p,li { orphans:2; widows:2; }
  .tbl { width:calc(100% + 10rem); margin-left:-10rem; } table { min-width:0; font-size:.69rem; }
  footer { break-before:page; }
}
"""


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "section"


def rail_number(heading: str) -> str:
    if heading.lower() == "abstract":
        return "ABSTRACT"
    match = re.match(r"^(\d+)\.", heading)
    if match:
        return f"{int(match.group(1)):02d}"
    if heading.lower().startswith("appendix"):
        match = re.match(r"^Appendix\s+([A-Z])", heading, re.I)
        return match.group(1).upper() if match else "APP"
    if heading.lower().startswith("references"):
        return "REF"
    if heading.lower().startswith("acknowledgements"):
        return "NOTE"
    return "—"


def markdown_renderer() -> MarkdownIt:
    return MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table")


def _throughput_curve_svg() -> str:
    """Data-driven tested-family plateau (§7.3), with real public-board points."""
    W, H, L, R, T, B = 680, 360, 58, 18, 24, 66
    x0, x1, y0, y1 = L, W - R, T, H - B
    Nmax, Smax = 2100.0, 150.0
    sx = lambda n: x0 + (n / Nmax) * (x1 - x0)
    sy = lambda s: y1 - (s / Smax) * (y1 - y0)
    p = [f'<svg viewBox="0 0 {W} {H}" role="img" width="100%" '
         f'style="max-width:{W}px;height:auto;font-family:inherit" '
         'aria-label="Tested-family public-score plateau versus requested candidate count">']
    # gridlines + y ticks
    for s in (0, 50, 88, 138):
        y = sy(s)
        p.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="#ece7db" stroke-width="1"/>')
        p.append(f'<text x="{x0-8}" y="{y+4:.1f}" text-anchor="end" font-size="11" fill="#8a8478">{s}</text>')
    # x ticks
    for n in (0, 500, 1000, 1500, 2000):
        x = sx(n)
        p.append(f'<text x="{x:.1f}" y="{y1+20:.0f}" text-anchor="middle" font-size="11" fill="#8a8478">{n}</text>')
    p.append(f'<text x="{(x0+x1)/2:.0f}" y="{y1+40:.0f}" text-anchor="middle" font-size="12" fill="#6b665c">candidates emitted per row (N)</text>')
    p.append(f'<text x="16" y="{(y0+y1)/2:.0f}" font-size="12" fill="#6b665c" transform="rotate(-90 16 {(y0+y1)/2:.0f})" text-anchor="middle">public score / equal-row ideal</text>')
    # ideal (throughput-unlimited) 0.09*N — dashed amber
    p.append(f'<line x1="{sx(0):.1f}" y1="{sy(0):.1f}" x2="{sx(1536):.1f}" y2="{sy(138.25):.1f}" '
             'stroke="#c08a00" stroke-width="2" stroke-dasharray="6 5"/>')
    p.append(f'<text x="{sx(1200):.0f}" y="{sy(112):.0f}" font-size="11.5" fill="#9a6f00">ideal equal-row law 0.09·N</text>')
    # fitted plateau for this tested family — solid blue
    p.append(f'<polyline points="{sx(0):.1f},{sy(0):.1f} {sx(978):.1f},{sy(88):.1f} {sx(2100):.1f},{sy(88):.1f}" '
             'fill="none" stroke="#1f5fbf" stroke-width="2.5"/>')
    # historical fitted completion level at N≈978
    p.append(f'<line x1="{sx(978):.1f}" y1="{y0}" x2="{sx(978):.1f}" y2="{y1}" stroke="#b9b3a4" stroke-width="1" stroke-dasharray="3 4"/>')
    p.append(f'<text x="{sx(978)-8:.0f}" y="{y0+14:.0f}" text-anchor="end" font-size="10.5" fill="#8a8478">historical fit ≈978 completed firings</text>')
    # top score placed on the ideal-law reference only; this is not an event-count inference
    p.append(f'<circle cx="{sx(1536):.1f}" cy="{sy(138.25):.1f}" r="4" fill="#c08a00"/>')
    p.append(f'<text x="{sx(1536)-6:.0f}" y="{sy(138.25)+18:.0f}" text-anchor="end" font-size="11" fill="#9a6f00">public top 138.250 (illustrative)</text>')
    # real measured points
    pts = [(1200, 87.03, "#12692b", None), (1524, 87.12, "#93122a", None),
           (1600, 86.895, "#93122a", "N=1524/1600 → ~87"),
           (2000, 88.65, "#12692b", "N=2000 → 88.650")]
    for n, s, col, lab in pts:
        p.append(f'<circle cx="{sx(n):.1f}" cy="{sy(s):.1f}" r="4.5" fill="{col}"/>')
        if lab:
            dy = 16 if n > 1000 else -9
            p.append(f'<text x="{sx(n):.0f}" y="{sy(s)+dy:.0f}" text-anchor="middle" font-size="11" font-weight="600" fill="{col}">{escape(lab)}</text>')
    p.append("</svg>")
    cap = ('<figcaption style="margin-top:10px;font-size:12.5px;color:#8a8478">Figure 2. '
           'The tested fixed-count single-post family plateaus near 86–89 despite larger requested N. '
           'The dashed 0.09·N line is the source-derived ideal if every requested finding completed and '
           'fired; placing the 138.250 public top on that reference is illustrative, not a causal event-count '
           'or hardware inference. The cross-team gap remains unexplained (§7.3).</figcaption>')
    return ('<figure style="margin:1.6em 0;padding:18px 20px;border:1px solid #e7e2d6;'
            'border-radius:12px;background:#fbfaf6;overflow-x:auto">'
            + "".join(p) + cap + "</figure>")


def _asymmetry_svg() -> str:
    """The sharpest guardrail↔predicate asymmetry (§4.1): the guard and the scorer read
    DIFFERENT fields of the same http.post call, so a benign url passes the filter while the
    scored sentinel rides in the uninspected data field."""
    W, H = 700, 322
    green, red, ink, mut = "#12692b", "#93122a", "#26241f", "#8a8478"
    p = [f'<svg viewBox="0 0 {W} {H}" role="img" width="100%" '
         f'style="max-width:{W}px;height:auto;font-family:inherit" '
         'aria-label="Field-mismatch asymmetry between guardrail and exfiltration predicate">']
    # shared tool call at top
    p.append('<rect x="150" y="14" width="400" height="50" rx="9" fill="#f4f1e8" stroke="#e0dacc" stroke-width="1"/>')
    p.append('<text x="350" y="34" text-anchor="middle" font-size="12.5" font-family="ui-monospace,monospace" fill="#26241f">http.post(</text>')
    p.append(f'<text x="350" y="52" text-anchor="middle" font-size="12.5" font-family="ui-monospace,monospace">'
             f'<tspan fill="{green}">url="…ok.co/sync"</tspan><tspan fill="{mut}">, </tspan>'
             f'<tspan fill="{red}">data="…SECRET_MARKER"</tspan><tspan fill="#26241f"> )</tspan></text>')
    # split arrows
    p.append(f'<path d="M300,64 L180,92" stroke="{green}" stroke-width="2" marker-end="url(#ah_g)"/>')
    p.append(f'<path d="M400,64 L520,92" stroke="{red}" stroke-width="2" marker-end="url(#ah_r)"/>')
    p.append(f'<defs><marker id="ah_g" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="{green}"/></marker>'
             f'<marker id="ah_r" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="{red}"/></marker></defs>')
    # two panels
    def panel(x, col, title, sub, steps, badge):
        b = [f'<rect x="{x}" y="96" width="320" height="210" rx="11" fill="#fbfaf6" stroke="#e7e2d6" stroke-width="1"/>']
        b.append(f'<text x="{x+18}" y="122" font-size="13.5" font-weight="700" fill="{col}">{escape(title)}</text>')
        b.append(f'<text x="{x+18}" y="140" font-size="11.5" fill="{mut}">{escape(sub)}</text>')
        for i, s in enumerate(steps):
            b.append(f'<text x="{x+18}" y="{166+i*24}" font-size="12" fill="{ink}">{escape(s)}</text>')
        b.append(f'<rect x="{x+18}" y="256" width="{len(badge)*8.4+26:.0f}" height="30" rx="15" fill="{col}"/>')
        b.append(f'<text x="{x+31}" y="276" font-size="12.5" font-weight="700" fill="#ffffff">{escape(badge)}</text>')
        return "".join(b)
    p.append(panel(22, green, "Guardrail  ·  OptimalGuardrail.decide",
                   "reads ONE field, url-first", [
                       "1. _extract_target(): first present of",
                       "   [path, url, cmd, data, body] → url",
                       "2. scan url for {secret, token, …} → none",
                       "→ url is benign", ], "ALLOWS the call ✓"))
    p.append(panel(358, red, "Scorer  ·  EXFILTRATION predicate",
                   "reads a DIFFERENT field", [
                       "1. EXFIL_SINKS['http.post'] = 'data'",
                       "2. read data → contains SECRET_MARKER",
                       "   (url is never inspected here)",
                       "→ sentinel present", ], "SCORES sev-5"))
    p.append("</svg>")
    cap = ('<figcaption style="margin-top:10px;font-size:12.5px;color:#8a8478">Figure 1. '
           'The field-mismatch asymmetry (§4.1). The guardrail and the exfiltration predicate '
           'inspect different arguments of the same http.post call — the guard reads url, the scorer '
           'reads data — so a benign url passes the filter while the scored sentinel rides in the '
           'uninspected payload. Read as a defensive checklist: validate every field that can carry '
           'the protected value, not the first one.</figcaption>')
    return ('<figure style="margin:1.6em 0;padding:18px 20px;border:1px solid #e7e2d6;'
            'border-radius:12px;background:#fbfaf6;overflow-x:auto">'
            + "".join(p) + cap + "</figure>")


FIGURES = {"throughput": _throughput_curve_svg(), "asymmetry": _asymmetry_svg()}


def enrich_fragment(fragment: str, section_id: str) -> str:
    soup = BeautifulSoup(fragment, "html.parser")
    used: set[str] = set()
    for heading in soup.find_all(["h3", "h4"]):
        base = f"{section_id}-{slugify(heading.get_text(' ', strip=True))}"
        anchor = base
        suffix = 2
        while anchor in used:
            anchor = f"{base}-{suffix}"
            suffix += 1
        used.add(anchor)
        heading["id"] = anchor
    for table in list(soup.find_all("table")):
        wrapper = soup.new_tag("div", attrs={"class": "tbl"})
        scroll = soup.new_tag("div", attrs={"class": "tablewrap"})
        caption = soup.new_tag("div", attrs={"class": "tbl-cap"})
        caption.string = "Evidence table retained from the Markdown manuscript"
        table.wrap(scroll)
        scroll.wrap(wrapper)
        wrapper.append(caption)
    for link in soup.find_all("a"):
        href = link.get("href", "")
        if href.startswith(("http://", "https://")):
            link["target"] = "_blank"
            link["rel"] = "noopener noreferrer"
        elif href and not href.startswith(("#", "/", "mailto:")):
            link["href"] = f"../{href}"
    html_out = str(soup)
    # Swap {{FIG:name}} placeholders for raw inline-SVG figures AFTER BeautifulSoup,
    # so the parser never lowercases case-sensitive SVG attributes (e.g. viewBox).
    for name, svg in FIGURES.items():
        html_out = html_out.replace(f"<p>{{{{FIG:{name}}}}}</p>", svg)
    return html_out


def split_manuscript(text: str) -> tuple[str, str, list[tuple[str, str]]]:
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError("Manuscript must begin with one H1 title")
    title = lines[0][2:].strip()
    first_section = next(i for i, line in enumerate(lines[1:], 1) if line.startswith("## "))
    front = "\n".join(lines[1:first_section]).strip()
    sections: list[tuple[str, str]] = []
    heading = ""
    body: list[str] = []
    for line in lines[first_section:]:
        if line.startswith("## "):
            if heading:
                sections.append((heading, "\n".join(body).strip()))
            heading = line[3:].strip()
            body = []
        else:
            body.append(line)
    if heading:
        sections.append((heading, "\n".join(body).strip()))
    return title, front, sections


def wordmark() -> str:
    return (
        '<span class="wordmark">Bra<span class="i">ı<span class="tittle"></span>'
        '</span>nMatter<span class="stop">.</span></span>'
    )


def embedded_font_css() -> str:
    faces: list[str] = []
    for family, weights, filename in FONT_SPECS:
        font_path = FONTS_DIR / filename
        if not font_path.is_file():
            raise FileNotFoundError(f"Missing branded font: {font_path}")
        payload = base64.b64encode(font_path.read_bytes()).decode("ascii")
        faces.append(
            "@font-face{"
            f"font-family:'{family}';font-style:normal;font-weight:{weights};font-display:swap;"
            f"src:url(data:font/woff2;base64,{payload}) format('woff2');"
            "}"
        )
    return "\n".join(faces)


def punctuated_heading(text: str) -> str:
    punctuation = "" if text.endswith((".", "?", "!", ":")) else '<span class="stop">.</span>'
    return f"{escape(text)}{punctuation}"


def render_paper(paper: Paper) -> str:
    source_path = ROOT / "paper" / paper.source
    title, front, sections = split_manuscript(source_path.read_text(encoding="utf-8"))
    md = markdown_renderer()
    section_rows: list[tuple[str, str, str, str, str]] = []
    seen: dict[str, int] = {}
    for index, (heading, body) in enumerate(sections):
        base = slugify(heading)
        seen[base] = seen.get(base, 0) + 1
        section_id = base if seen[base] == 1 else f"{base}-{seen[base]}"
        kicker = paper.kickers[index] if index < len(paper.kickers) else "Research record"
        section_rows.append((section_id, heading, rail_number(heading), kicker, enrich_fragment(md.render(body), section_id)))

    front_html = enrich_fragment(md.render(front), "document-record") if front else ""
    toc = "\n".join(
        f'<li><a href="#{escape(section_id)}"><span class="n">{escape(number)}</span>'
        f'<span class="t">{escape(heading)}</span><span class="k">{escape(kicker)}</span></a></li>'
        for section_id, heading, number, kicker, _ in section_rows
    )
    stats = "\n".join(
        f'<div class="stat"><div class="n">{escape(value)}</div><div class="l">{escape(label)}</div></div>'
        for value, label in paper.stats
    )
    body_sections = "\n".join(
        f'''<section id="{escape(section_id)}" class="{'abstract' if number == 'ABSTRACT' else ''}">
  <div class="rail"><span class="num">{escape(number)}</span><div class="kicker">{escape(kicker)}</div></div>
  <div class="col"><h2>{punctuated_heading(heading)}</h2>{content}</div>
</section>'''
        for section_id, heading, number, kicker, content in section_rows
    )
    title_with_stop = f"{escape(title)}<span class=\"stop\">.</span>"
    source_record = f'<div class="source-record">{front_html}</div>' if front_html else ""
    description = escape(paper.deck, quote=True)

    document = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<meta name="author" content="Ahmed Mobasher — BrainMatterStudios">
<meta name="generator" content="paper/html/render.py">
<title>{escape(title)} — BrainMatterStudios</title>
<style>{embedded_font_css()}\n{CSS}</style>
</head>
<body id="top">
<div class="wrap">
  <header class="titlepage">
    <div class="logo-lockup">{wordmark()}<span class="descriptor"><span>Studios</span><span class="sep">·</span><span>The Hague × Cairo</span><span class="sep">·</span><span class="tag">Bespoke AI. Built to think.</span></span></div>
    <div class="eyebrow"><span>BrainMatterStudios</span><span class="sep">/</span><span>{escape(paper.kind)}</span><span class="sep">/</span><span>August 2026</span></div>
    <h1>{title_with_stop}</h1>
    <p class="deck">{escape(paper.deck)}</p>
    <dl class="docrec">
      <div><dt>Document</dt><dd>{escape(paper.document_id)} · Draft 26.08</dd></div>
      <div><dt>Author</dt><dd>Ahmed Mobasher<br>Sole author</dd></div>
      <div><dt>Subject</dt><dd>{escape(paper.subject)}</dd></div>
      <div><dt>Published by</dt><dd>BrainMatterStudios<br>The Hague × Cairo</dd></div>
      <div><dt>Status</dt><dd>Author-review living draft<br>Markdown remains authoritative</dd></div>
      <div><dt>Evidence state</dt><dd>Frozen and rechecked through<br>16 August 2026</dd></div>
    </dl>
    <div class="band">{stats}</div>
    {source_record}
  </header>
  <nav class="contents" aria-label="Contents"><div class="meta">Contents</div><ol>{toc}</ol></nav>
  <main>{body_sections}</main>
  <aside class="draft-note" aria-label="Draft status"><span class="tag">Living draft</span><p>This HTML is a reading and print draft generated from <code>paper/{escape(paper.source)}</code>. The Markdown manuscript and its evidence ledger remain the authoritative research record.</p></aside>
  <footer>
    <p><strong>Ahmed Mobasher</strong> is responsible for the manuscript, its evidence boundaries, and its conclusions. AI assistance is disclosed within the paper.</p>
    <div class="signoff"><span class="wordmark-mono">BRAIN<span class="mid">MATTER</span>STUDIOS</span><span class="meta">{escape(paper.document_id)} · Author-review draft · <a class="url" href="https://brainmatterstudios.com">brainmatterstudios.com</a></span></div>
  </footer>
</div>
<a class="backtop" href="#top" aria-label="Back to top">↑</a>
</body>
</html>
'''
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def validate(html: str, source: str, sections: int, output_parent: Path) -> None:
    soup = BeautifulSoup(html, "html.parser")
    errors: list[str] = []
    if soup.title is None:
        errors.append("missing title")
    if len(soup.select("main > section")) != sections:
        errors.append("section count mismatch")
    if len({node.get("id") for node in soup.select("[id]")}) != len(soup.select("[id]")):
        errors.append("duplicate ids")
    if len(soup.select("nav.contents a")) != sections:
        errors.append("contents count mismatch")
    for link in soup.select("nav.contents a[href^='#']"):
        if soup.find(id=link["href"][1:]) is None:
            errors.append(f"broken contents link {link['href']}")
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith(("#", "/", "http://", "https://", "mailto:")):
            continue
        target = (output_parent / href.split("#", 1)[0]).resolve()
        if not target.exists():
            errors.append(f"broken local link {href}")
    source_tables = len(re.findall(r"^\|.*\|\s*$\n\|\s*:?-", source, re.M))
    if len(soup.find_all("table")) != source_tables:
        errors.append("table count mismatch")
    if errors:
        raise ValueError("; ".join(errors))


def main() -> int:
    for paper in PAPERS:
        source = (ROOT / "paper" / paper.source).read_text(encoding="utf-8")
        _, _, sections = split_manuscript(source)
        html = render_paper(paper)
        target = OUTPUT_DIR / paper.output
        validate(html, source, len(sections), target.parent)
        target.write_text(html, encoding="utf-8")
        print(f"rendered {target.relative_to(ROOT)} ({len(html):,} bytes, {len(sections)} sections)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
