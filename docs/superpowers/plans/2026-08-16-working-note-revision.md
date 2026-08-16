# Competition Working Note Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the stale competition Working Note with a source-pinned, submission-backed, award-aligned Markdown manuscript that separates facts, measurements, inferences, and open hypotheses.

**Architecture:** Build a compact Markdown claim ledger first from SDK 3.1.2, official Kaggle pages, live submissions, and Git artifacts. Rewrite the manuscript from that ledger, then run mechanical and evidence-level verification before calling it ready for review.

**Tech Stack:** Markdown, Git, `rg`, `jq`, Kaggle CLI 2.2.4, competition SDK 3.1.2, official Kaggle pages

**Spec:** `docs/superpowers/specs/2026-08-16-paper-revision-and-agent-research-design.md`

## Global Constraints

- Modify the Working Note and Markdown evidence files only; do not change attack code, kernels, experiment configurations, or ARC-AGI-3 files.
- Use a dated evidence cutoff and preserve unresolved experiments as open.
- Keep SDK facts, local measurements, live observations, inferences, testimony, and hypotheses distinct.
- Do not infer private-guardrail behavior from its exposed module name.
- Do not claim that a frontier mechanism was reproduced without matched live evidence.
- Distinguish `ERROR`-status historical scores from `COMPLETE` results.
- Use Ahmed Mobasher as sole author and disclose AI assistance without AI authorship.
- Exclude secrets, credentials, private-guardrail code, and unrelated transcript content.
- Do not submit, publish, push, deploy, or alter shared competition state.

## File Structure

- Create `paper/evidence/working-note-claim-ledger.md`: dated source, experiment, submission, and claim-status record.
- Modify `paper/working_note.md`: competition-facing manuscript centered on guardrail-predicate asymmetry and local-to-live transfer.

---

### Task 1: Freeze the Current Competition Evidence

**Files:**
- Create: `paper/evidence/working-note-claim-ledger.md`

**Interfaces:**
- Consumes: Kaggle submission API, current Git history, SDK 3.1.2 source, approved spec.
- Produces: a dated ledger with canonical submission rows and source anchors.

- [ ] **Step 1: Record repository and SDK identity**

Run:

```bash
git rev-parse HEAD
git branch --show-current
sed -n '1,80p' comp/aicomp_sdk-3.1.2.dist-info/METADATA
shasum -a 256 comp/aicomp_sdk/scoring.py \
  comp/aicomp_sdk/core/predicates.py \
  comp/aicomp_sdk/guardrails/optimal.py \
  comp/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py
```

Expected: repository revision, branch, SDK version, and four source hashes.

- [ ] **Step 2: Query the live submission rows**

Run:

```bash
kaggle competitions submissions \
  -c ai-agent-security-multi-step-tool-attacks \
  --format json --page-size 1000 \
  | jq -r '.[] | select((.description // "") | test("L(9|13|22|23|24|25|26|27|28|29|31)")) | [.ref,.date,.status,.publicScore,.description] | @tsv'
```

Expected: historical high-water rows, L22-L29, L31 fast-emit, and current L31 chainpack statuses.

- [ ] **Step 3: Create the ledger structure**

Create this structure, replacing the example revision text with the real hash:

```markdown
# Working Note Claim Ledger

**Evidence cutoff:** 2026-08-16 with exact retrieval time.

**Repository revision:** the 40-character hash recorded above.

**SDK:** `aicomp-sdk 3.1.2`

## Evidence labels
- Source fact
- Local measurement
- Live observation
- Triangulated finding
- Inference
- Open hypothesis

## Official competition facts
| Claim | Evidence label | Source | Verified wording |
|---|---|---|---|

## Mechanical claims
| Claim | Evidence label | Source path and lines | Verified wording |
|---|---|---|---|

## Live experiments
| Ref | Date | Status | Score | Configuration | Matched control | Interpretation |
|---|---|---:|---:|---|---|---|

## Claim disposition
| Draft claim | Status | Replacement claim | Evidence |
|---|---|---|---|
```

- [ ] **Step 4: Record official facts**

Record the 2026-09-01 competition deadline, 2026-09-08 Working Note deadline, two USD 2,500 awards, and all five judging criteria. Include direct official Evaluation, Timeline, Prizes, and Rules URLs.

- [ ] **Step 5: Populate the canonical experiment rows**

Include exact live records for refs:

```text
55040336; 55336143-55336379; 55362610-55362843;
55391763-55392055; 55418160-55418184; 55444083-55444101;
55469249-55469280; 55493289-55493315; 55500552;
55525506-55525536; 55530790; 55538814-55538875.
```

Update completed L31 rows and retain only genuinely unresolved rows as open.

- [ ] **Step 6: Verify the ledger**

Run:

```bash
rg -n '\b(TBD|TODO|FIXME|XXX)\b|<[^>]+>' paper/evidence/working-note-claim-ledger.md
git diff --check -- paper/evidence/working-note-claim-ledger.md
```

Expected: no placeholder matches and no diff errors.

- [ ] **Step 7: Commit the ledger**

```bash
git add paper/evidence/working-note-claim-ledger.md
git commit -q \
  -m "docs: freeze working note evidence ledger" \
  -m "- pin SDK and repository evidence
- record live submission outcomes and statuses
- classify facts, observations, and hypotheses

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 2: Rewrite the Abstract, Introduction, and Method

**Files:**
- Modify: `paper/working_note.md:1-145`
- Consult: `paper/evidence/working-note-claim-ledger.md`

**Interfaces:**
- Consumes: Task 1 ledger.
- Produces: bounded thesis, contributions, evidence labels, and limitations contract.

- [ ] **Step 1: Replace the title and status block**

Use:

```markdown
# Guardrail-Predicate Asymmetry and the Limits of Local-to-Leaderboard Transfer in Multi-Step Agent Red-Teaming
```

State SDK version, evidence cutoff, sole author, AI disclosure location, and open experiment status.

- [ ] **Step 2: Rewrite the abstract to 250-350 words**

Include problem, source-plus-local-plus-live method, guardrail-predicate result, failed-transfer result, evidence-gating contribution, limitations, and defensive value. Exclude universal hardware ceilings, reproduced-frontier claims, and hidden-guardrail behavior.

- [ ] **Step 3: Rewrite contributions**

Limit them to source-derived asymmetry, a live-tested transfer catalogue, evidence-gated methodology, and defensive/benchmark recommendations.

- [ ] **Step 4: Rewrite methodology around evidence tiers**

Define source fact, local measurement, live observation, triangulated finding, inference, and open hypothesis. Present two-gate validation as the desired protocol rather than a claim that every past result satisfied it.

- [ ] **Step 5: Add a threats preview**

Name hidden hardware, evaluator changes, score variance, contaminated controls, unknown aggregation, competitor-artifact uncertainty, and unavailable private implementation.

- [ ] **Step 6: Check overclaims and formatting**

Run:

```bash
rg -n 'hardware-set ceiling|field frontier uses|private guardrail is a stateful|All methods are validated|in-flight' paper/working_note.md
git diff --check -- paper/working_note.md
```

Expected: no unqualified overclaim matches and no diff errors.

- [ ] **Step 7: Commit the front-matter rewrite**

```bash
git add paper/working_note.md
git commit -q \
  -m "docs: reframe competition working note" \
  -m "- bound the thesis to supported evidence
- define evidence tiers and validity threats
- align contributions with award criteria

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 3: Correct Scoring and Guardrail-Predicate Analysis

**Files:**
- Modify: `paper/working_note.md` scoring, runtime, predicates, and asymmetry sections
- Consult: `comp/aicomp_sdk/scoring.py`
- Consult: `comp/aicomp_sdk/core/predicates.py`
- Consult: `comp/aicomp_sdk/guardrails/optimal.py`
- Consult: `comp/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py`

**Interfaces:**
- Consumes: source hashes and evidence terminology.
- Produces: mechanically accurate analysis with repository-relative citations.

- [ ] **Step 1: Re-derive scoring from source**

Verify severity weights, raw score, novelty term, normalization, predicate-less dropping, and score-cell construction. Cite full paths such as `comp/aicomp_sdk/scoring.py:14`.

- [ ] **Step 2: Correct the budget description**

State that the gateway applies 9,000 seconds to generation and a separate 9,000-second deadline to each configured guardrail replay for each model. Note official prose inconsistencies without inventing a resolution.

- [ ] **Step 3: Verify all four predicates**

For each predicate verify tool, inspected field, success condition, severity, intent gate, and lookback window.

- [ ] **Step 4: Rewrite the asymmetry taxonomy**

Preserve source-demonstrable URL/data mismatch, destructive-write scope, taint-window relationship, and confused-deputy intent relationship. Describe scoreability only under the inspected public SDK.

- [ ] **Step 5: Remove unsupported private behavior**

Replace the existing private section with the limitation that only an entry-point/module identifier is exposed, not implementation behavior.

- [ ] **Step 6: Verify citations and formatting**

Open each cited range with `nl -ba`, then run:

```bash
rg -n 'scoring\.py:|predicates\.py:|optimal\.py:|jed_attack_gateway\.py:' paper/working_note.md
git diff --check -- paper/working_note.md
```

Expected: citations use repository-qualified paths or a defined shorthand; no diff errors.

- [ ] **Step 7: Commit corrected mechanics**

```bash
git add paper/working_note.md
git commit -q \
  -m "docs: correct benchmark mechanics analysis" \
  -m "- pin scoring and predicates to SDK 3.1.2
- clarify generation and replay budgets
- bound hidden-guardrail discussion

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 4: Replace the Throughput Catalogue and Results

**Files:**
- Modify: `paper/working_note.md` empirical sections
- Modify: `paper/evidence/working-note-claim-ledger.md` if live status changes

**Interfaces:**
- Consumes: canonical submission rows and evidence tiers.
- Produces: reproducible results through the execution-time cutoff.

- [ ] **Step 1: Build one canonical results table**

Use:

```markdown
| Ladder | Ref(s) | Status | Test and control | Score(s) | Evidence-supported interpretation |
```

Include L9, L22-L29, GPU diagnostics, and L31.

- [ ] **Step 2: Correct baseline language**

Report 89.640 as an `ERROR`-status historical high-water and 88.730 as the strongest recent `COMPLETE` same-batch control in the analyzed run family.

- [ ] **Step 3: Correct Gemma and dual-forge claims**

Report L25 34.000 versus 27.000 and L26 35.000 versus 34.605. Conclude that an initial matched positive did not become scalable replicated headroom. Report 81.985 and 82.660 dual-forge results below strong controls.

- [ ] **Step 4: Add later negatives**

Report L26 reproductions 77.670/83.115; L27 variants 50.295-57.620 versus 88.730; L28 best 85.410 versus 83.325 but below stronger controls; GPU routes 0.000-50.175; L29 85.675; L31 fast-emit 25.145; and current chainpack outcomes.

- [ ] **Step 5: Narrow saturation language**

State that no monotonic improvement appeared across tested L23 candidate counts and all runs completed; this is consistent with, but does not prove, a throughput or behavior ceiling.

- [ ] **Step 6: Synthesize negative-result mechanisms**

Group local/live divergence, matched-control erosion, hardware assumptions, model-format interference, routing invalidity, and failed public-artifact reproduction.

- [ ] **Step 7: Verify every score**

Run:

```bash
for score in 89.640 88.730 34.000 27.000 35.000 34.605 81.985 82.660 77.670 83.115 50.295 57.620 85.410 83.325 50.175 85.675 25.145; do
  rg -n "$score" paper/evidence/working-note-claim-ledger.md paper/working_note.md
done
```

Expected: every value appears with consistent status and context.

- [ ] **Step 8: Commit updated results**

```bash
git add paper/working_note.md paper/evidence/working-note-claim-ledger.md
git commit -q \
  -m "docs: update working note results through L31" \
  -m "- replace stale pending claims with outcomes
- report matched controls and negative results
- narrow saturation and frontier interpretations

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 5: Finish Recommendations, Limitations, References, and Disclosure

**Files:**
- Modify: `paper/working_note.md` final sections and appendices

**Interfaces:**
- Consumes: corrected mechanics and results.
- Produces: award-aligned synthesis, responsible communication, disclosure, and references.

- [ ] **Step 1: Rewrite defensive recommendations**

Tie each recommendation to a source-demonstrable public asymmetry. Remove recommendations that depend on hidden private behavior.

- [ ] **Step 2: Add threats to validity**

Cover evaluator/SDK changes, hidden runtime, score variance, scarce slots, imperfect controls, unknown aggregation, competitor versions, local model provenance, and absent private source/scores.

- [ ] **Step 3: Add reproducibility and data availability**

Reference repository revision, SDK hashes, ledger, builders, submission refs, and local logs. State which private artifacts are omitted.

- [ ] **Step 4: Add AI and authorship disclosure**

Name Ahmed Mobasher as sole accountable author. Disclose Claude Code and Codex assistance with code, analysis, and drafting.

- [ ] **Step 5: Add verified scholarly references**

Use opened primary or official sources relevant to agent-security evaluation, tool-use risk, reproducibility, and AI-assisted authorship. Keep code citations separate.

- [ ] **Step 6: Run final manuscript checks**

Run:

```bash
rg -n '\b(TBD|TODO|FIXME|XXX)\b' paper/working_note.md
rg -n 'definitive|proves|always|never|the frontier uses|structural cap|crown' paper/working_note.md
git diff --check -- paper/working_note.md paper/evidence/working-note-claim-ledger.md
wc -w paper/working_note.md
```

Expected: no placeholders, justified absolutes only, no diff errors, and recorded word count.

- [ ] **Step 7: Commit the review draft**

```bash
git add paper/working_note.md paper/evidence/working-note-claim-ledger.md
git commit -q \
  -m "docs: complete evidence-led working note revision" \
  -m "- add recommendations and validity limits
- document reproducibility and AI assistance
- prepare Working Note for author review

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 6: Independent Final Verification

**Files:**
- Review: `paper/working_note.md`
- Review: `paper/evidence/working-note-claim-ledger.md`
- Review: `docs/superpowers/specs/2026-08-16-paper-revision-and-agent-research-design.md`

**Interfaces:**
- Consumes: complete review draft.
- Produces: verified Markdown ready for Ahmed's review, not publication.

- [ ] **Step 1: Re-query pending submissions**

Repeat Task 1's Kaggle query and update changed rows, retrieval timestamp, and evidence cutoff.

- [ ] **Step 2: Audit at least 15 source citations**

Sample scoring, all predicates, guardrail, budgets, replay validation, and model settings. Confirm the prose claims no more than the code.

- [ ] **Step 3: Audit every score claim**

Compare manuscript numbers to the ledger and live Kaggle output. Preserve statuses.

- [ ] **Step 4: Audit award alignment**

Confirm visible treatment of clarity/reproducibility, methodology, security insight, community usefulness, and responsible communication.

- [ ] **Step 5: Run final mechanical checks**

Run:

```bash
rg -n '\b(TBD|TODO|FIXME|XXX)\b' paper/working_note.md paper/evidence/working-note-claim-ledger.md
git diff --check 04af340..HEAD -- paper/working_note.md paper/evidence/working-note-claim-ledger.md
git status --short --branch
```

Expected: no placeholders or diff errors; only known unrelated untracked files remain.

- [ ] **Step 6: Prepare the review handoff**

Report evidence cutoff, open rows, word count, commits, verification commands, and intentionally unresolved claims. Stop before Kaggle publication or submission.
