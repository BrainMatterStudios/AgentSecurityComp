# Cutoff-3 Live Results — 2026-09-08

**Purpose.** This artifact preserves the compact facts used for the paper's
third evidence cutoff. Like the cutoff-2 artifact, it separates authenticated
platform observations from repository records, from off-platform instrument
measurements, and from author testimony. It does not preserve credentials, API
tokens, private competition data, or unrelated transcript content.

**Retrieval boundary.** The competition rows, leaderboard rows, submission rows,
and the published-notebook row below were returned by authenticated Kaggle
CLI/API queries on 2026-09-08 between 18:21:51Z and 18:25:29Z. The
AgentSecurityComp competition has been closed since 2026-09-01, so its values
are final; the ARC-AGI-3 competition was open, so its values are a dated
mid-competition state and are mutable. Repository facts are cited to the
`ArcAGI3` working branch `winning/duck-patched` at commit `41213de`
(2026-09-08T18:06:51Z) and to `AgentSecurityComp` at commit `1f75a16`.

---

## 1. AgentSecurityComp (closed)

### 1.1 Standing, unchanged from cutoff-2

| Item | Observed value (2026-09-08T18:25:28Z) |
| --- | --- |
| Competition end | 2026-09-01 23:59 UTC |
| User rank returned by the competition query | 171 |
| Entrants returned by the same query | 4,186 |

The cutoff-2 authenticated standing is unchanged. The separately reported Silver
notification of 173 of 4,251 remains **retrospective author testimony**. A
repository-wide search on 2026-09-08 returned only the project's own textual
records of the report (the manuscript, the working note, and the cutoff-2
artifact) — no screenshot, email, or archived notification. That search covered
the repository only; it did not re-run the private-history hash manifest, whose
2026-09-04 state stands. Do not upgrade the medal label.

### 1.2 The full revealed private distribution (new at this cutoff)

Cutoff-2 cited a small hand-picked set of revealed private rows. At cutoff-3 the
complete retained submission list was retrieved. Of **50** submission rows, one
is `ERROR` with no scores (ref `55727914`) and **49** carry both a public and a
private score.

| Item | Observed value |
| --- | --- |
| Rows with a private score | 49 |
| Rows scoring exactly 0.000 private | 38 |
| Rows scoring above 0.000 private | 11 |
| Highest public score among the 0.000-private rows | 92.670 (ref `55766377`, selected Slot A) |
| Rows with public > 50 and private > 0.000 | 0 |
| Highest private score in the population | 16.805 (ref `55904213`, public 16.525) |
| Lowest positive private score | 2.290 (ref `55701675`, public 2.320) |

All eleven positive-private rows come from the confused-deputy `email.send`
line. Nine are the `HEDGE B` / Slot B confused-deputy family (private
15.845–16.805); one is a timing probe of the same family (ref `55701675`,
private 2.290); one is a deliberate diversity arm pairing that line with
untrusted-to-action coverage, "NOVELTY CD+UTA diversity arm (private predicate
coverage)" (ref `55931330`, public 10.520, private 10.745).

**Claim-use limit.** This is the full *retained submission population* for this
account, not a sample of the competition. It establishes a complete
population-level dissociation between the public and private axes **for the
submissions this entrant actually flew**. It does not expose the private
guardrail, prove that every `http.post` submission anywhere must score zero,
isolate which component of a confused-deputy submission earned its private
score, or reconstruct the platform's rank calculation.

### 1.3 Working Note, now an authenticated public artifact

| Item | Observed value (2026-09-08T18:25:29Z) |
| --- | --- |
| Notebook ref | `ahmedmobasher86/working-note-guardrail-predicate-asymmetry` |
| Title | Working Note: Guardrail-Predicate Asymmetry |
| Last run time | 2026-09-02 06:40:02 UTC |
| Total votes | 0 |

At cutoff-2 the Working Note submission was recorded from the repository. It is
now directly observable as a published Kaggle notebook, which upgrades the fact
of publication from repository record to authenticated platform observation. The
**award outcome remains unknown**: the optional Working Note deadline was
2026-09-08 23:59 UTC, and no result had been announced at the time of this query.

---

## 2. ARC-AGI-3 (open)

### 2.1 Standing and field

| Item | Observed value (2026-09-08T18:25:28Z) |
| --- | --- |
| Competition deadline | 2026-11-02 23:59 UTC |
| User rank returned by the competition query | 26 |
| Teams returned by the same query | 2,892 |
| Best public submission | ref `56080757`, public 4.31, submitted 2026-09-07 |
| Private result | Not revealed at this cutoff |

Public leaderboard, top five, same query window:

| Team | Submission date | Score |
| --- | --- | --- |
| Tufa Labs | 2026-09-08 05:57:50 | 11.04 |
| Third Intelligence | 2026-09-07 02:43:50 | 8.21 |
| Daniel Franzen | 2026-09-07 21:16:21 | 7.63 |
| mostik.ai | 2026-09-06 16:33:00 | 7.51 |
| NVARC3 | 2026-09-07 19:34:18 | 5.96 |

At cutoff-2 the same account read 374 of 2,779 at a best public score of 1.94.
Both the rank and the entrant count are mutable while the competition is open;
neither is a stable identifier of any later state.

### 2.2 The adoption step

| Ref | Date | Public | Row |
| --- | --- | --- | --- |
| `55970756` | 2026-09-03 | 1.94 | best in-house arm at cutoff-2 (model-swap redraw) |
| `56042273` | 2026-09-05 | 3.25 | byte-copy of the public notebook `keithtyser/duck-qwen3-8-flash-next-nvfp4-mtp` V14 |

The adopted notebook is public and was independently observable at
2026-09-08T18:25Z under author `ktyser` with 149 votes. The submission
description for ref `56042273` records the adoption explicitly ("PUBLIC-PROFILE
ADOPTION … byte-copy of keithtyser/duck-qwen3-8-flash-next-nvfp4-mtp V14") and
carries a pre-registered reading rule written before the row scored.

**Claim-use limit.** This establishes that the largest single public-score
increase in the case followed the adoption of an external public artifact. It
does not establish a matched causal estimate of the adoption's effect against a
same-slot control, and the single-draw variance below limits how tightly the
3.25 itself can be read.

### 2.3 Byte-identical draw variance

Two families of byte-identical resubmissions were flown, each identified by a
Kaggle script-version id recorded in the submission description.

| Family | Script version | Draws |
| --- | --- | --- |
| Base `arc3-keith-copy` v4 | svid `347562879`, hash `90efdebb` | `56042273` 3.25; `56058136` 2.58; `56073627` **ERROR** (recorded in the project log as a platform system error, slot refunded) |
| Candidate `arc3-keith-yield900` v1 | svid `347926973` | `56080757` 4.31; `56088705` 2.45 |

The candidate differs from the base by exactly one import-time constant
(`LOCAL_ANALYZER_YIELD_SECONDS` 60 → 900), attested in the commit. The repository
records the flown family as mean 3.15, sd 0.85 across the four completed draws.

**Claim-use limit.** This directly establishes that a single public draw in this
competition cannot adjudicate a one-knob change, because unchanged code spans
2.58–3.25 and one draw errored outright. It does not estimate the draw
distribution precisely (n = 4 completed) and it does not show that the
competition metric is uninformative in aggregate.

### 2.4 Off-platform replication instrument

Repository record, `ArcAGI3@41213de`,
`docs/research-2026-09-08/R-loss-ledger-3.md` and
`offkaggle/REGIME_WAVE_STATUS.md`. Runs execute the same docker image on a
Modal-hosted RTX PRO 6000, which the project record identifies as the evaluation
GPU class, over 25 development games per wave.

| Comparison | Result |
| --- | --- |
| `yield900` vs base, 3 runs × 25 games each side (two Modal rig runs plus one Kaggle commit run per side; the pooled totals therefore mix two execution platforms) | 118 levels / 75 runs on both sides; 1.573 vs 1.573 levels per game; paired per-game difference 0.00 ± 0.11 se; 8 games better, 8 worse, 9 same |
| `yield900` live-cap score | 8.42 vs 9.06 per game (−0.63 ± 1.64) — slightly negative |
| What the knob did change | calls per turn 1.02 → 2.05; actions per game 143 → 115; GAME_OVERs 1.31 → 0.87 per run; analysis-only call share 45% → 49% |
| `keith_probe` (harness-enforced probe discipline), pre-registered | ENGAGED strongly: 2.64 refusals per game, acted after first refusal 87.5%, wall actions/baseline median 1.00 (was 0.72), turn-budget yields 0 (was 27–30) |
| `keith_probe` primary read | 41 levels vs pooled six-draw base 39.33 (sd 2.34) = +0.71 sd → **DEAD** under the locked pre-registration (engaged-but-flat) |

The `keith_probe` wave also surfaced an instrument defect: the runner's
`game_overs_from_events` pre-filter matched `'"game_over": true'` with a space
while the harness writes compact JSON, so the safety line read 0 instead of 32.
The defect was found, corrected, regression-tested, and recorded as a correction
line appended to the wave summary rather than a silent edit.

**Claim-use limit.** These are **off-platform local measurements**, not live
competition results. A local null does not by itself refute a live effect, and
the live pre-registered three-draw read on `yield900` was **incomplete** at this
cutoff: two draws had landed (4.31, 2.45; mean 3.38 against an adopt threshold of
4.0) and draw three was armed to fire 2026-09-09 02:00Z. Do not report the live
arm as closed.

---

## 3. Claim-use rules

1. AgentSecurityComp's authenticated standing is unchanged at 171 of 4,186;
   Silver and 173/4,251 remain author testimony with no retained artifact.
2. Cite the AgentSecurity private distribution as complete **for this entrant's
   retained submissions** — 38 of 49 exactly zero, 11 positive, all eleven
   confused-deputy `email.send` — and keep the guardrail mechanism open.
3. Cite Working Note publication as an authenticated platform observation and
   its award outcome as unknown.
4. Timestamp every ARC value. Rank 26 of 2,892 is a mutable mid-competition
   state, and the best public score behind it (4.31) is one draw of a family
   whose byte-identical draws span 2.45–4.31.
5. Attribute the ARC step to adoption of a named public artifact, not to an
   agent-originated mechanism.
6. Keep off-platform rig results labelled as local measurements, and record the
   live `yield900` three-draw read as incomplete at this cutoff.
