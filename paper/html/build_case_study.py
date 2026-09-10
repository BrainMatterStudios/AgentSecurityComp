"""Render the plain-language case study in the BrainMatterStudios brand.

Reuses the brand kit, embedded fonts and wordmark from render.py so the
case study cannot drift from the research papers it accompanies. The page
furniture differs on purpose: a case study wants a masthead, a reading
estimate and pull-quotes, not a document record and numbered sections.
"""
from __future__ import annotations

import re
from html import escape
from pathlib import Path

from markdown_it import MarkdownIt

import render as brand

SOURCE = brand.ROOT / "paper" / "case-study.md"
OUTPUT = brand.OUTPUT_DIR / "case-study.html"

# Numbers that carry the argument. Rendered as pull-outs beside the prose.
PULLOUTS = {
    "The scoreboard that didn't count": ("38 of 49", "submissions scored exactly zero on the board that decided the prizes"),
    "The competition where I did better by copying": ("+1.31", "from one copied notebook, against +0.44 for the best idea of my own"),
    "The ruler that wouldn't hold still": ("2.45–4.31", "the range returned by submitting identical code"),
}

EXTRA_CSS = r"""
.masthead { border-bottom:1px solid var(--hair); padding:2.4rem 0 1.6rem; margin-bottom:3.2rem; }
/* base CSS gives .logo-lockup its own rule and spacing; the masthead supplies both here */
.masthead .logo-lockup { display:flex; flex-direction:column; gap:.55rem;
  border-bottom:0; padding-bottom:0; margin-bottom:0; }
.masthead .wordmark { font-size:1.6rem; }
.kicker { font-family:var(--mono); font-size:.66rem; letter-spacing:.19em; text-transform:uppercase;
  color:var(--ember-text); display:flex; flex-wrap:wrap; gap:.7rem; margin:0 0 1.5rem; }
.kicker .sep { color:var(--hair-2); }
h1.title { font-family:var(--serif); font-weight:400; font-size:clamp(2.4rem,6.4vw,3.9rem);
  line-height:1.04; letter-spacing:-.033em; margin:0 0 1.5rem; max-width:22ch; text-wrap:balance; }
h1.title .stop { color:var(--ember); }
.standfirst { font-size:clamp(1.12rem,2.5vw,1.34rem); line-height:1.45; color:var(--ink-2);
  letter-spacing:-.014em; max-width:34rem; margin:0 0 2.2rem; text-wrap:balance; }
.byline { display:flex; flex-wrap:wrap; gap:.6rem 1.4rem; font-family:var(--mono); font-size:.68rem;
  letter-spacing:.1em; text-transform:uppercase; color:var(--muted);
  border-top:1px solid var(--hair); padding-top:1.1rem; margin-bottom:3.6rem; }
.byline b { color:var(--ink-2); font-weight:500; }
article { max-width:var(--measure); margin:0 auto; }
article h2 { font-family:var(--serif); font-weight:400; font-size:clamp(1.5rem,3.6vw,1.95rem);
  line-height:1.18; letter-spacing:-.024em; margin:3.6rem 0 1.1rem; text-wrap:balance; }
article h2::after { content:"."; color:var(--ember); }
article p { margin:0 0 1.15rem; }
article strong { font-weight:600; color:var(--ink); }
article hr { border:0; height:1px; background:var(--hair); margin:3.2rem 0; }
article em { font-style:italic; }
blockquote { margin:2rem 0; padding-left:1.15rem; border-left:2px solid var(--ember); color:var(--ink-2); }
.pullout { margin:2.4rem 0; padding:1.5rem 1.6rem; background:var(--ember-wash);
  border-left:2px solid var(--ember); }
.pullout .fig { font-family:var(--serif); font-size:clamp(2.1rem,5.5vw,2.9rem); line-height:1;
  letter-spacing:-.03em; color:var(--ember-text); display:block; margin-bottom:.5rem; }
.pullout .cap { font-size:.93rem; line-height:1.45; color:var(--ink-2); }
.coda { margin:4rem 0 0; padding:1.3rem 1.5rem; background:var(--paper-2);
  border-left:2px solid var(--hair-2); font-size:.9rem; line-height:1.55; color:var(--muted); }
.coda em { font-style:normal; color:var(--ink-2); }
.signoff { max-width:var(--measure); margin:4.4rem auto 0; padding-top:1.4rem;
  border-top:1px solid var(--hair); display:flex; flex-wrap:wrap; gap:.6rem 1.2rem;
  align-items:baseline; justify-content:space-between; }
.signoff .wordmark-mono { font-size:.74rem; }
.signoff .meta { font-family:var(--mono); font-size:.64rem; letter-spacing:.11em;
  text-transform:uppercase; color:var(--muted); }
.signoff a { color:var(--ember-text); text-decoration:none; border-bottom:1px solid var(--hair-2); }
@media (max-width:640px){ body{ font-size:16px; } .byline{ margin-bottom:2.6rem; } }
@media print { body{ background:#fff; } .pullout{ background:none; } }
"""


def typeset(text: str) -> str:
    """Curl apostrophes and quotes in strings that bypass the markdown renderer."""
    text = re.sub(r"(?<=\w)'(?=\w)", "\u2019", text)
    text = re.sub(r'"([^"]+)"', "\u201c\\1\u201d", text)
    return text


def build() -> str:
    text = SOURCE.read_text(encoding="utf-8")
    lines = text.split("\n")

    title = typeset(lines[0].lstrip("# ").strip())
    rest = "\n".join(lines[1:]).lstrip("\n")

    # The standfirst is the leading bolded paragraph; the coda is the trailing italic note.
    stand = re.match(r"\*\*(.+?)\*\*\s*\n\s*\n", rest, re.S)
    standfirst = typeset(stand.group(1).replace("\n", " ").strip()) if stand else ""
    body_md = rest[stand.end():] if stand else rest

    coda = ""
    coda_m = re.search(r"\n---\s*\n\s*\*(.+?)\*\s*$", body_md, re.S)
    if coda_m:
        coda = typeset(coda_m.group(1).replace("\n", " ").strip())
        body_md = body_md[: coda_m.start()]

    # The papers use a plain commonmark renderer. Prose set in Fraunces needs real
    # apostrophes and dashes, so the case study enables the typographer.
    md = MarkdownIt("commonmark", {"html": False, "linkify": False, "typographer": True})
    md.enable(["table", "smartquotes", "replacements"])
    body = md.render(body_md)

    for heading, (figure, caption) in PULLOUTS.items():
        # Keys are trusted literals. Match the typeset form, since the renderer
        # curls apostrophes in headings too.
        anchor = f"<h2>{typeset(heading)}</h2>"
        assert anchor in body, f"pull-out heading not found: {heading}"
        block = (
            f'<div class="pullout"><span class="fig">{escape(figure)}</span>'
            f'<span class="cap">{escape(caption)}</span></div>'
        )
        body = body.replace(anchor, anchor + block, 1)

    words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", text))
    minutes = max(1, round(words / 230))

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — BrainMatter Studios</title>
<meta name="description" content="{escape(standfirst)}">
<meta name="author" content="Ahmed Mobasher">
<style>{brand.embedded_font_css()}{brand.CSS}{EXTRA_CSS}</style>
</head><body>
<div class="wrap">
  <header class="masthead"><div class="logo-lockup">{brand.wordmark()}
    <span class="descriptor"><span>Studios</span><span class="sep">·</span>
    <span>The Hague × Cairo</span><span class="sep">·</span>
    <span class="tag">Bespoke AI. Built to think.</span></span></div></header>

  <article>
    <p class="kicker"><span>Case study</span><span class="sep">·</span>
      <span>AI agents in research</span><span class="sep">·</span>
      <span>BMS-CS-26-01</span></p>
    <h1 class="title">{escape(title)}<span class="stop">.</span></h1>
    <p class="standfirst">{escape(standfirst)}</p>
    <p class="byline"><span><b>Ahmed Mobasher</b></span><span>September 2026</span>
      <span>{minutes} min read</span><span>{words:,} words</span></p>
    {body}
    <p class="coda"><em>{escape(coda)}</em></p>
  </article>

  <div class="signoff">
    <span class="wordmark-mono">BRAIN<span class="mid">MATTER</span>STUDIOS</span>
    <span class="meta">BMS-CS-26-01 · <a href="https://brainmatterstudios.com">brainmatterstudios.com</a></span>
  </div>
</div>
</body></html>"""


if __name__ == "__main__":
    html = build()
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"rendered {OUTPUT.relative_to(brand.ROOT)} ({len(html):,} bytes)")
