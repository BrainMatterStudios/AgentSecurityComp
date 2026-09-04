# Cutoff-2 Live Results — 2026-09-04

**Purpose.** This artifact preserves the compact facts used for the paper's
second evidence cutoff. It separates authenticated platform observations from
author testimony and from inferences. It does not preserve credentials, API
tokens, private competition data, or unrelated transcript content.

**Retrieval boundary.** The competition and submission values below were
returned by authenticated Kaggle CLI/API queries on 2026-09-04. The retained
ARC competition query was recorded at 16:56:36Z and the AgentSecurity
competition query at 16:57:02Z. The retained query records are in
`claude:AgentSecurityComp/a8b27783-6519-42d5-bcd6-6440c6d602ab.jsonl`
(ARC competition row at JSONL record 254; AgentSecurity competition and
submission rows at records 259 and the immediately preceding query records).
The source file's SHA-256 digest is recorded in
`source-availability-manifest.md`.

## 1. AgentSecurityComp

### Authenticated observations

| Item | Observed value |
| --- | --- |
| Competition end | 2026-09-01 23:59 UTC |
| User rank returned by the competition query | 171 |
| Entrants returned by the same query | 4,186 |
| Best public submission | ref `55766377`, public 92.670 |
| Best private score among the queried submissions | ref `55904213`, public 16.525, private 16.805 |
| High-public EXFIL row 1 | ref `55927148`, public 89.680, private 0.000 |
| High-public EXFIL row 2 | ref `55902731`, public 91.600, private 0.000 |
| Selected Slot A | ref `55766377`, public 92.670, private 0.000 |
| Selected Slot B | ref `55805571`, public 16.555, private 16.735 |
| Other clean confused-deputy draws | ref `55906645`, public 16.380, private 16.580; ref `55928754`, public 15.795, private 15.845 |

These rows establish only the observed submission-level pattern. They do not
expose the private guardrail, prove why a row received its score, establish
that every `http.post` submission must score zero, or isolate which component
of the confused-deputy submissions produced the positive private scores.

### Public-frontier observation

An authenticated public-leaderboard query directly returned a leading score of
147.530 on 2026-08-29, with the same value observed again on 2026-08-30. The
retained command output is in
`codex:2026/08/29/rollout-2026-08-29T21-40-52-01a04f0a-0694-7301-b343-f082024a492c.jsonl`
(records 253 and 554–555). This supports the bounded statement that the public
frontier had reached **at least 147.530 by 2026-08-29**. It does not establish
the exact frontier at the 2026-09-01 deadline.

Relative to the best banked public score, the directly observed frontier was
at least `147.530 / 92.670 = 1.5920`, or about 1.59 times as high.

### Medal and final-standing testimony

The author recorded a platform medal notification of **Silver, 173 of 4,251**
on 2026-09-02. The first retained repository record is commit
`4c4f437bb0d8db314f536c05585ca596683531c1`. No screenshot, email, or archived
notification was found in the 2026-09-04 evidence audit. The medal and
173/4,251 values are therefore **retrospective author testimony**, not an
independently auditable platform observation. The authenticated 171/4,186
query above is the primary retained standing evidence.

## 2. ARC-AGI-3

### Authenticated observations at the manuscript cutoff

| Item | Observed value |
| --- | --- |
| Competition deadline | 2026-11-02 23:59 UTC |
| User rank returned by the cutoff query | 374 |
| Entrants returned by the same query | 2,779 |
| Best public submission | ref `55970756`, public 1.94, submitted 2026-09-03 |
| Private result | Not revealed at this cutoff |

These are a dated mid-competition state, not final outcomes. Rank and entrant
count are mutable and must not be treated as stable identifiers of the later
competition state.

### Same-day mutability check

A separate authenticated read-only query at 2026-09-04T20:12:04Z returned ARC
rank 379 of 2,787 entrants. It also returned the unchanged closed
AgentSecurity rank of 171 of 4,186. The later ARC observation is preserved to
demonstrate live-state movement; it does not overwrite the defined 16:56:36Z
cutoff used in the manuscript.

## 3. Claim-use rules

1. Cite 171/4,186 as the retained authenticated AgentSecurity standing.
2. Attribute Silver and 173/4,251 to author testimony and state that the
   notification artifact was not retained.
3. Describe 147.530 as a directly observed 2026-08-29/30 frontier lower bound,
   not as the exact deadline frontier.
4. Treat the private submission pattern as confirmed at the row level while
   leaving its causal guardrail mechanism open.
5. Keep the ARC values timestamped because the competition was ongoing and its
   rank changed within the same day.
