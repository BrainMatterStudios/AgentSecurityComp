# Public Episode Ledger — Redacted Companion

Supplementary material for *Access Without Autonomy: An Instrumented Case Study
of AI Agents in Computational Research* (Ahmed Mobasher, sole author).

**Purpose.** This is the reviewer-auditable, public cut of the coded-episode
corpus behind the paper. It reproduces every coded episode, its origin, status,
and the **public** locators that resolve it (repository commits, submission
references, repository file paths, and published policy or paper records). It
supports independent audit of the paper's descriptive tallies without releasing
the controlled private agent histories.

**Redaction rule.** Private-history locators — Claude/Codex/OpenCode session,
message, and part identifiers (`claude:…`, `codex:…`, `ses_…`, `prt_…`,
`msg_…`) — are withheld and shown as "private trace (authorized-auditor
access)." No secrets, credentials, or third-party personal data appear here. The
full private-locator register remains in the controlled ledger
`ai-agents-research-evidence.md`, resolvable by an authorized auditor. This
redaction limits what a reviewer can independently verify to public artifacts;
that limitation is stated in the paper (§3.4, §11.1).

**Cutoff.** Cutoff-1 is 2026-08-16 (31 episodes). Cutoff-2 (2026-09-04) adds two
AgentSecurityComp episodes, AS-S15 and AS-S16, from authenticated Kaggle live
queries; no earlier episode's code changed. Totals below are the cutoff-2 state.

**Selection boundary.** The 33 rows are a purposive, maximum-variation analytic
sample, not an exhaustive census of project activity. Inclusion required a
bounded adjudicable proposition, traceable evidence, an implementation,
experiment, or explicit evidence adjudication, and enough record to code origin
and status. Routine debugging, purely operational work, duplicate provider
continuations, repeated variants without a new evidentiary issue, and
propositions lacking an adjudicable record were excluded. No denominator of all
possible project episodes was constructed.

**Status vocabulary.** `confirmed`, `partially supported`, `refuted`,
`invalid experiment`, `superseded`, `open`. Status belongs to the bounded
proposition in the row, not to a provider or artifact. **Origin** is coded
conservatively as `human`, `agent`, `external`, or `mixed`. Neither dimension is
an agent accuracy or autonomy score.

---

## 1. AgentSecurityComp episodes (16)

| Episode | Date | Proposition | Origin | Human intervention | Local outcome | Live outcome | Status | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AS-S01 | 2026-06-13 | Port the attack from a mock scaffold to the real SDK. | mixed | Required real-path verification and submission approval. | Real `AttackCandidate` path ran. | Subsequent submissions used the real SDK. | confirmed | Inspect the executable interface before optimizing it. |
| AS-S02 | 2026-06-13 | Increase candidate volume because the scorer appeared additive. | agent | Continued local and live testing. | Hundreds of compliant candidates generated. | Scale set a baseline but did not solve the task. | partially supported | A valid scoring direction need not be the decisive lever. |
| AS-S03 | 2026-06-27 | Add the required `SECRET_MARKER` after fabricated tokens stopped scoring. | external | Accepted the compatibility repair. | Marker-bearing exfiltration validated. | Scoring resumed on the corrected path. | confirmed | Protocol semantics can invalidate an otherwise plausible attack. |
| AS-S04 | 2026-07-25 | Adapt output size to replay-safe observed limits. | external | Approved a bounded ladder. | Replay-safe adaptive sizing passed local checks. | All five identified L6 rows were `ERROR` (adaptive 80.145 vs 64.800 visible control); not a completed effect. | partially supported | A local mechanism stays externally unestablished when every identified live row errors. |
| AS-S05 | 2026-07-26 | Stop decoding after `close_ok` to cut per-candidate latency. | agent | Submitted a controlled ladder. | Local latency 1.03 s vs 1.23 s. | Matched L7 rows differed by 1.440 visible points but both `ERROR`. | partially supported | A visible difference on error rows cannot calibrate external transfer. |
| AS-S06 | 2026-07-27 | Pack more messages per call to amortize overhead. | mixed | Requested live discrimination. | Local packing mechanics ran. | No returned description matched L8; all identified L9 rows `ERROR`. | open | Failed execution status must remain distinct from a refuted treatment effect. |
| AS-S07 | 2026-08-04 | Explain Gemma's failure as model weakness. | agent | Required a faithful framing comparison. | GPT also scored zero under the weak frame; the real forge separated models. | No clean live test of the original claim. | invalid experiment | A comparison is invalid when the control is broken. |
| AS-S08 | 2026-08-08 | Route candidates deterministically by board and split the workload. | agent | Authorized a controlled router ladder. | Router and self-measurement worked locally. | 42.665–47.865 vs 44.320 baseline; no stable gain. | invalid experiment | A multi-arm ladder can still be non-identifying when arms overlap. |
| AS-S09 | 2026-08-09 | Reproduce the public commitment-forge mechanism. | external | Required faithful implementation and live test. | Project record says four posts per candidate fired; raw stdout/hash absent. | 47.850 vs 43.600 single-post control. | partially supported | Faithful reproduction can validate a bounded mechanism without reaching its stated target. |
| AS-S10 | 2026-08-09 | Use dual-board/Gemma forge to beat the reproduced baseline. | mixed | Approved single-vs-dual comparisons. | Both-board logic ran; count claims at project-record provenance. | Dual arms 81.985/82.660; Gemma isolate 34.000 vs 27.000 (N=600) narrowing to 35.000 vs 34.605 (N=900); N=1200 forge 35.375. | partially supported | The initial isolate gain was not durable or scalable; mixed provenance stays visible. |
| AS-S11 | 2026-08-12 | Test both proposed throughput knobs in one L27 ladder. | mixed | Insisted on both tests and a control. | Probe-hop variants executable. | 50.295–57.620 vs 88.730 control. | refuted | Verify that nominally distinct arms identify distinct mechanisms before launch. |
| AS-S12 | 2026-08-13 | Test whether GPU would meet/exceed the 83.115 historical CPU-reproduction threshold. | agent | Approved a GPU ladder; no same-batch hardware control survived. | GPU path became functional. | Best GPU arm 50.175 vs 83.115 threshold. | refuted | The threshold proposition was refuted; the unmatched comparison identifies no causal CPU-vs-GPU effect. |
| AS-S13 | 2026-08-15 | Test whether the L29 split would exceed the 88.730 historical L27 threshold. | agent | Allowed a bounded test without a same-batch routing control. | Split runner executed. | 85.675, below 88.730. | refuted | The threshold proposition was refuted; the unmatched comparison does not causally reject routing. |
| AS-S14 | 2026-08-16 | Test whether L31 chainpack arms would exceed the 88.730 historical L27 threshold. | agent | Preserved cutoff-pending state; later updates kept separate. | Chainpack prepared; fast-emit ran. | Chainpack pending at cutoff; by 12:44:16Z all four `COMPLETE` at 79.985/79.365/73.605/54.375; fast-emit 25.145. | refuted | The historical-threshold proposition was refuted; unmatched comparisons identify no causal chainpack effect. |
| **AS-S15** | 2026-08-22 to 2026-09-01 | Among the revealed tested rows, the two queried high-public EXFIL submissions score 0.000 private while the queried confused-deputy `email.send` rows score positively. | mixed | Directed the private-board pivot and selected the two final submissions. | Confused-deputy hedge scored against mock private guardrails; EXFIL blocked. | Revealed rows: EXFIL 0.000 (refs 55927148, 55902731); selected Slot A 55766377 (private 0.000) and Slot B 55805571 (private 16.735); best queried hedge draw 16.805 (ref 55904213, not selected). | confirmed | The row-level pattern transferred; the private guardrail mechanism, universal family behavior, and causal contribution to rank remain unobserved. |
| **AS-S16** | 2026-08-24 to 2026-09-01 | A final-week attacker lever (forge wording, adaptive sizing, inter-hop suppression, or probe-hop) closes the public-throughput gap to the frontier. | agent | Approved bounded ladders and controls. | Levers executable and measured locally. | No lever beat about 92.670; several lowered the row; a direct query showed the frontier had reached at least 147.530 by 2026-08-29 (about 1.59 times the best banked score). | refuted | Exhausting a family of attacker levers is a valid negative result, not evidence the gap is unclosable. |

## 2. ARC-AGI-3 episodes (12)

| Episode | Date | Proposition | Origin | Human intervention | Local outcome | Live outcome | Status | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ARC-S01 | 2026-08-09 | Replace a flat object list with a role-typed, HUD-masked scene before goal inference. | mixed | Directed retesting on retained cases. | Flat input 0/9; combined representation 6/6. | No isolated live attribution. | partially supported | Typing and masking changed together and cannot receive separate causal credit. |
| ARC-S02 | 2026-07-01 | Search solved paths, then replay them. | agent | Required dev and live checks. | Search solved all 25 development games. | The scoring trick did not survive live conditions. | partially supported | Separate solver validity from evaluator transfer. |
| ARC-S03 | 2026-06-29 | Double-reset between plays to improve geodesic efficiency. | agent | Challenged the result against competition mode. | Eval-faithful artifact 2.6–152× on 15/25 after no-op repair; a later handoff recorded 7–109×. | Second play returned HTTP 400. | invalid experiment | Preserve differing local measurements and test lifecycle semantics in the real evaluation mode. |
| ARC-S04 | 2026-07-14 | Use an EWM policy after independent code review. | agent | Continued comparative testing. | Review defects repaired. | Later campaigns displaced the policy; no durable isolated gain. | superseded | Review can improve implementation without establishing lasting efficacy. |
| ARC-S05 | 2026-07-11 | Serve a fine-tuned adapter that appeared to beat base. | mixed | Asked for proof of the deployed model identity. | The apparent gain came from base, not the adapter. | The adapter never served. | invalid experiment | Serving identity is part of experimental validity. |
| ARC-S06 | 2026-08-01 | Measure A/A evaluation noise before reading small deltas. | mixed | Required registered gates. | RMS per game 0.707 levels; two registered gates under-powered. | No live-effect claim; protocol amendment preserved the result. | confirmed | Calibrate the instrument before interpreting changes. |
| ARC-S07 | 2026-08-03 | Correct slow-tick HUD bar parsing. | agent | Required replay/regression checks. | Virtual rotation and masks fixed retained cases. | No isolated leaderboard delta claimed. | confirmed | A narrowly verified parser correction can be confirmed without a ranking claim. |
| ARC-S08 | 2026-07-12 | Reduce prompt tokens to improve performance. | agent | Required hidden evaluation. | Roughly doubled dev performance (1.96 vs 0.89). | Hidden score 0.73. | refuted | Large development gains can be distribution-specific. |
| ARC-S09 | 2026-08-10 | Use best-of-N with reset-based repeated plays. | agent | Required independent competition-mode verification. | Candidate selection worked in the harness. | Competition mode swallowed the reset; second play failed. | refuted | A strategy depending on unavailable evaluator actions is not deployable. |
| ARC-S10 | 2026-08-09 | Add a structural plan channel with brake and phase gates. | mixed | Required live ledger comparison. | Structural controls executed. | Results stayed in the existing score band. | partially supported | Better process structure is not automatically a score breakthrough. |
| ARC-S11 | 2026-08-15 | Replace duck baseline with engineered Stage 2b. | mixed | Required a full-25 verdict. | 0.2463 vs duck 1.6333, with six game wins. | No replacement shipped; only a narrow portfolio edge remained. | refuted | Preserve a narrow portfolio edge while rejecting the stated replacement claim. |
| ARC-S12 | 2026-08-15 | Promote Qwen 3.8 after a controlled local A/B. | mixed | Required an armed but gated live runner. | Stored row mean 2.5291 vs Qwen 3.6 1.4872 (one-wave directional screen). | No scored live result by cutoff. | open | A strong local A/B remains an open transfer claim until live scoring. |

## 3. OpenCode primary investigations (5)

| Episode | Case | Date | Proposition | Origin | Human intervention | Outcome | Status | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OC-S01 | ASC | 2026-08-07 | Independently review L20/L21 mechanisms and next tests. | mixed | Framed the audit; retained submission authority. | Local smoke supported some mechanics; no new live result. | partially supported | An independent review is evidence synthesis, not an independent project. |
| OC-S02 | ASC | 2026-08-09 | Re-audit the case without trusting memory or recorded conclusions. | mixed | Imposed the memory-blind rule. | Rechecked code/evidence; no completed live adjudication by cutoff. | open | A strong epistemic instruction improves discipline but is not an outcome. |
| OC-S03 | ARC | 2026-08-06 | Audit the proposed duck-sparse 35B arm. | mixed | Commissioned, challenged, then killed the arm. | Serving path had not executed; arm killed before reset. | open | A killed arm is not a negative live result. |
| OC-S04 | ARC | 2026-08-09 | Run a nine-specialist research campaign over an assumed corpus. | mixed | Commissioned and challenged the campaign. | Produced a document; later audit found wrong-model corpus. | invalid experiment | Parallel breadth cannot repair invalid source provenance. |
| OC-S05 | ARC | 2026-08-10 | Repair and test the duck-memory namespace strategy. | mixed | Demanded explicit correction and verification. | Namespace no-op repaired; result stayed in-band. | partially supported | Cross-provider continuation must retain one episode identity and modest claims. |

---

## 4. Public source register (private locators withheld)

Each episode resolves to the public artifacts below. Short Git hashes are
unambiguous ancestors of the stated cutoff in the named repository. Submission
references are Kaggle numeric IDs. Private-history locators are withheld per the
redaction rule.

| Episode | Public locators |
| --- | --- |
| AS-S01 | AgentSecurityComp commit `3e30121`; private trace (authorized-auditor access) |
| AS-S02 | AgentSecurityComp commit `3e30121`; private trace (authorized-auditor access) |
| AS-S03 | AgentSecurityComp commit `1ac76a0`; `1ac76a0:attack.py`, `1ac76a0:dev/validate_312_score.py` |
| AS-S04 | AgentSecurityComp commit `e85a7ba`; `e85a7ba:dev/_replay_safe_smoke.py`; live refs `54986870`, `54986885`, `54986896`, `54986905`, `54986916` (all `ERROR`) |
| AS-S05 | AgentSecurityComp commit `242a855`; live refs `55013491`, `55013500`, `55013507` (all `ERROR`); private trace (authorized-auditor access) |
| AS-S06 | AgentSecurityComp commit `77862ef`; `77862ef:dev/_build_l8.py`; live L9 refs `55040336`, `55040351`, `55040363`, `55040369`, `55040377` (all `ERROR`); private trace (authorized-auditor access) |
| AS-S07 | AgentSecurityComp commit `a322c7b`; private trace (authorized-auditor access) |
| AS-S08 | AgentSecurityComp commit `2298119`; `paper/evidence/working-note-claim-ledger.md` rows L22–L23; private trace (authorized-auditor access) |
| AS-S09 | AgentSecurityComp commit `f2eeee4`; claim ledger row L24, refs `55391763`, `55392055` |
| AS-S10 | AgentSecurityComp commits `6fbe6e5`, `22cebb7`; claim ledger L25 refs `55418160`, `55418165`, `55418171`, `55418180`, `55418184`; L26 refs `55444087`, `55444093`, `55444097` |
| AS-S11 | AgentSecurityComp commit `0504391`; claim ledger row L27; private trace (authorized-auditor access) |
| AS-S12 | AgentSecurityComp commit `52d7f0f`; claim ledger GPU refs `55500552`, `55525506`, `55525507`, `55525533`, `55525536`; private trace (authorized-auditor access) |
| AS-S13 | AgentSecurityComp commit `6018877`; claim ledger row L29, ref `55530790` |
| AS-S14 | AgentSecurityComp commit `b02d457`; claim ledger row L31, refs `55538814`, `55538829`, `55538848`, `55538855`, `55538875` |
| AS-S15 | `paper/working_note.md` §7.4–§7.5; `paper/evidence/cutoff-2-live-results-2026-09-04.md`; authenticated Kaggle rows (2026-09-04): EXFIL private 0.000 refs `55927148`, `55902731`; selected Slot A `55766377` (private 0.000), selected Slot B `55805571` (public 16.555, private 16.735); confused-deputy rows private about 15.8–16.8 refs `55904213` (16.805, best, not selected), `55906645`, `55928754`; private trace (authorized-auditor access) |
| AS-S16 | `paper/working_note.md` §7.5; `paper/evidence/cutoff-2-live-results-2026-09-04.md`; authenticated Kaggle rows (2026-09-04): best public 92.670 ref `55766377`; lever refs `55877747`, `55877752`, `55879084`, `55879086`, `55927142`, `55928757`; authenticated public frontier observation 147.530 on 2026-08-29/30 |
| ARC-S01 | ArcAGI3 commit `19fd560`; `ebe5b3e:scripts/research_2026_07_01/goal_inference/exp_b_reasoner/retest_roletyped/VERDICT.md` |
| ARC-S02 | ArcAGI3 commits `8b5ab48`, `4270936`, `a077012`; `docs/DESIGN-2026-08-14-engineered-agent.md` |
| ARC-S03 | ArcAGI3 commits `df9b96b`, `25e7a78`; `docs/geodesic-fix-validation.html`, `docs/HANDOFF-2026-07-01-research-continuation.md`, `docs/superpowers/specs/2026-08-01-sacrificial-recon-spine-design.md` |
| ARC-S04 | ArcAGI3 commit `10a94c6`; private trace (authorized-auditor access) |
| ARC-S05 | ArcAGI3 commit `7bc3cfc`; private trace (authorized-auditor access) |
| ARC-S06 | ArcAGI3 commit `8d8b671`; `docs/A1-PROTOCOL-2026-08.md`, `8d8b671:scratchpad/rl_gate/aa_noise_floor.py` |
| ARC-S07 | ArcAGI3 commits `bab2aea`, `f0ec605`; `docs/test-artifacts-2026-08-02/AB-ROUND3-ANALYSIS-2026-08-03.md` |
| ARC-S08 | ArcAGI3 `docs/submission-ledger.json`, submission `54603982`; `docs/DESIGN-2026-08-14-engineered-agent.md` |
| ARC-S09 | ArcAGI3 commit `b5ad790`; `docs/DESIGN-2026-08-14-engineered-agent.md` |
| ARC-S10 | ArcAGI3 commits `4bb431d`, `cfeb92a`; `docs/submission-ledger.json`, submissions `55493742`, `55450891`, `55418633` |
| ARC-S11 | ArcAGI3 cutoff-ancestor commit `da37afd`; audit-time mutable artifact `scratchpad/engineered_stage2/stage2b_verdict.md` (SHA-256 `aa341694…64b2fa`, mtime `2026-08-14T23:22:57Z`), outside Git and not cutoff-reproducible |
| ARC-S12 | ArcAGI3 commits `4f3d330`, `ebe5b3e`; `docs/superpowers/specs/2026-08-15-qwen38-emergency-promotion-design.md`, `docs/RESEARCH-2026-08-15-field-sweep-and-qwen38.md`, `scratchpad/qwen38/wave1_shipped_result.json` |
| OC-S01 | OpenCode parent session; no child sessions; private trace (authorized-auditor access) |
| OC-S02 | OpenCode parent session; no child sessions; private trace (authorized-auditor access) |
| OC-S03 | OpenCode parent + one linked child; private trace (authorized-auditor access) |
| OC-S04 | OpenCode parent + nine linked children; corpus refutation at cutoff-ancestor commit `4a17e8f:docs/RESULTS-2026-08-08-overnight-gates.md`; private trace (authorized-auditor access) |
| OC-S05 | OpenCode parent session; later Claude repair at cutoff-ancestor commit `fbd1197`, `ebe5b3e:submission/_duck_mem/harness_mem.py`; `ebe5b3e:docs/submission-ledger.json`, submission `55488796` (0.83); private trace (authorized-auditor access) |

## 5. Quote ledger (locators redacted)

Nine short excerpts were admitted for process or retrospective evidence at
cutoff-1. Exact private trace locations are withheld; date, speaker, provider,
and evidence class are retained. At the 2026-09-04 re-audit, the canonical
Claude originals for Q01-Q04 and Q06 were absent at their recorded paths. Q01's
user text survives in Claude prompt history; Q02-Q04 and Q06 survive only as
prior controlled-ledger extracts plus identified repository corroboration.
Quotations do not replace code or live results.

| Quote | Topic | Excerpt | Date | Speaker | Provider | Evidence class |
| --- | --- | --- | --- | --- | --- | --- |
| Q01 | ASC original goal | "continue to work in loops and iterations until you solve the challenge" | 2026-06-13 | Ahmed | Claude Code | Human instruction |
| Q02 | ASC confident claim | "Both models are stuck at gpt-oss's ~465 boundary → ~44 ceiling." | 2026-07-01 | Claude Code | Agent process claim, not measured fact |
| Q03 | ASC human challenge | "test the approach locally as much as possible to verify it thoroughly" | 2026-06-30 | Ahmed | Claude Code | Human governance instruction |
| Q04 | ASC self-correction | "my 'boundary ~570' was wrong" | 2026-06-30 | Claude Code | Agent self-correction (predates and does not retract Q02) |
| Q05 | ASC memory-blind audit | "do not trust the memnory or recorded info, validate everything" | 2026-08-09 | Ahmed | OpenCode/DeepSeek | Human governance instruction |
| Q06 | ARC invalid experiment | "Conclusion: the LoRA never served. The generation ran on base" | 2026-07-11 | Claude Code | Agent self-correction, corroborated by repository evidence |
| Q07 | ARC evidence gate | "Serving identity proven first." | 2026-08-10 | Claude Code | Agent process statement, corroborated by test artifacts |
| Q08 | Value assessment | "They enabled me a non domain expert to actually participate and contribute" | 2026-08-16 | Ahmed | Codex interview | Retrospective testimony |
| Q09 | Originality assessment | "the contributions are mostly built on top of other people's work" | 2026-08-16 | Ahmed | Codex interview | Retrospective testimony |

## 6. Descriptive measures (cutoff-2, 2026-09-04)

| Measure | Value |
| --- | --- |
| Coded episodes | 33 (16 AgentSecurityComp + 12 ARC-AGI-3 + 5 OpenCode); 31 at cutoff-1 plus AS-S15, AS-S16 |
| Origins | `human` 0; `agent` 14; `external` 3; `mixed` 16 |
| Statuses | `confirmed` 5; `partially supported` 10; `refuted` 8; `invalid experiment` 5; `superseded` 1; `open` 4 |

**Exact origin IDs.** `agent`: AS-S02, AS-S05, AS-S07, AS-S08, AS-S12, AS-S13,
AS-S14, AS-S16, ARC-S02, ARC-S03, ARC-S04, ARC-S07, ARC-S08, ARC-S09.
`external`: AS-S03, AS-S04, AS-S09. `mixed`: AS-S01, AS-S06, AS-S10, AS-S11,
AS-S15, ARC-S01, ARC-S05, ARC-S06, ARC-S10, ARC-S11, ARC-S12, OC-S01, OC-S02,
OC-S03, OC-S04, OC-S05. `human`: none.

**Exact status IDs.** `confirmed`: AS-S01, AS-S03, AS-S15, ARC-S06, ARC-S07.
`partially supported`: AS-S02, AS-S04, AS-S05, AS-S09, AS-S10, ARC-S01, ARC-S02,
ARC-S10, OC-S01, OC-S05. `refuted`: AS-S11, AS-S12, AS-S13, AS-S14, AS-S16,
ARC-S08, ARC-S09, ARC-S11. `invalid experiment`: AS-S07, AS-S08, ARC-S03,
ARC-S05, OC-S04. `superseded`: ARC-S04. `open`: AS-S06, ARC-S12, OC-S02, OC-S03.

Each of the 33 IDs occurs exactly once in each derivation. These are descriptive
counts of the reviewed corpus, not estimates of population frequency, and are
not an agent accuracy or autonomy score.
