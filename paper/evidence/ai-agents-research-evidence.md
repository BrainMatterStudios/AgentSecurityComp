# AI Agents in Research Evidence Ledger

This ledger is the provenance foundation for a living, comparative N-of-1 case
study. AgentSecurityComp is the primary case and ARC-AGI-3 is the comparative
case. OpenCode/DeepSeek is supplementary evidence, not a balanced provider
comparison. Session counts describe records, not research quality, autonomy, or
causal contribution.

## Evidence cutoff and repository revisions

The evidence cutoff for this inventory is 2026-08-16T10:29:29+03:00. Later
revisions must state a new cutoff and preserve earlier unresolved or negative
outcomes rather than silently replacing them.

| Repository | Role | Revision at cutoff | Commit date | Subject |
| --- | --- | --- | --- | --- |
| AgentSecurityComp | Primary case | `2ed68e80705906dcbdf4f707edf8c37089ce0906` | 2026-08-16T10:29:29+03:00 | `chore: ignore local worktrees` |
| ArcAGI3 | Comparative case, read-only | `ebe5b3eca70260910144ae54e057c3d06ea0e14d` | 2026-08-15T18:41:01+03:00 | `feat(duck-38): one-shot armed runner for 2026-08-16 00:01Z slot - SLOT SWAP from duck-p3` |

These hashes bound the repository evidence. They do not establish that every
historical transcript refers to the same revision. Episode-level claims must
also identify the commit, artifact, or live record available at that episode's
time.

Evidence classes used in this ledger are: source fact, local measurement, live
observation, triangulated finding, inference, retrospective testimony, and open
hypothesis. The class must remain visible in working tables even when the final
paper expresses it in prose.

## Privacy and quotation rules

- Claude, Codex, and OpenCode histories are private source material. Publish
  derived tables and short, necessary excerpts, not raw transcripts or database
  exports.
- Exclude credentials, authentication material, secrets, unrelated personal
  material, and operational details that are not needed to support a claim.
- Do not inspect or export the OpenCode credential table. Only the session table
  was used for this inventory.
- Treat external histories and the ArcAGI3 repository as read-only. This audit
  must not modify either source.
- Quote only material relevant to hypothesis formation, confidence, correction,
  intervention, or research governance. Keep it short and preserve enough
  surrounding context to avoid misleading attribution.
- Every admitted quote must retain a private trace to provider, case, session
  identifier, timestamp, speaker, and source location. Public text may use a
  pseudonymous source label where the raw identifier adds no evidentiary value.
- Redaction must not change the proposition or speaker intent. Paraphrase rather
  than quote when safe redaction would make the excerpt ambiguous.
- AI-authored claims, citations, summaries, and interpretations require an
  independent source check before manuscript use. Ahmed Mobasher remains the
  accountable sole author.

## Session provenance and deduplication

### Counting rules

1. A provider's top-level conversation is the default unit for session counts.
2. A subagent or specialist record is linked to its top-level parent and is not
   counted again as an independent conversation.
3. Workflow journals, scratchpad copies, and tool-result derivatives are
   provenance aids, not conversations.
4. A continued Codex session is counted once by its rollout file and session
   identifier even when the file contains repeated metadata records.
5. A content search hit is admitted to a case only when session metadata places
   its working directory in that case repository or a repository-specific
   worktree. Matches from other working directories remain incidental unless a
   source-level review establishes direct case work.
6. Imported, forked, parent, child, or overlapping histories are not summed.
   Parent-child metadata, timestamps, working directories, and matching content
   are used to select one conservative unit.
7. The current paper-design and provenance-audit lineage is excluded from the
   historical case-activity count to prevent the act of studying the corpus from
   inflating it.
8. Token counts are usage descriptors only. They are not measures of thought,
   scientific value, originality, or provider performance.

### Claude inventory

The Claude project stores were enumerated recursively. A top-level UUID-named
file was classified as a primary session. Files below `subagents` were
classified as child work; files named `journal.jsonl` below workflow directories
were classified as workflow journals. No JSONL path in either store matched the
scratchpad-copy or tool-result-derivative naming rules. Unique `sessionId`
values equaled top-level file counts, and no duplicate top-level file hashes
were found.

| Case store | All JSONL files | Primary sessions counted | Direct subagents | Workflow subagents | Workflow journals | Scratchpad copies | Tool-result derivatives |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AgentSecurityComp | 327 | 11 | 52 | 249 | 15 | 0 | 0 |
| ARC-AGI-3 | 942 | 116 | 185 | 627 | 14 | 0 | 0 |
| Total | 1,269 | 127 | 237 | 876 | 29 | 0 | 0 |

The primary Claude record windows are 2026-06-13T09:28:39.036Z through
2026-08-15T14:51:09.743Z for AgentSecurityComp and
2026-06-28T16:54:33.186Z through 2026-08-15T21:28:03.657Z for ARC-AGI-3.
Subagent and journal counts map the scale of the evidence store but must never
be added to the 127-conversation total.

### Codex inventory

The required content search found 68 rollout files at audit time. First metadata
records classify them as follows:

| Classification | Root rollouts | Child rollouts | Count treatment |
| --- | ---: | ---: | --- |
| AgentSecurityComp working directory | 11 | 20 | Case candidates |
| ARC-AGI-3 working directory | 5 | 23 | Case candidates |
| Other working directory with a text match | 5 | 4 | Excluded as incidental |

One AgentSecurityComp root and nine of its children belong to the current
paper-design and provenance-audit lineage. After excluding that lineage, the
historical Codex case corpus contains 15 root sessions and 34 linked child
sessions: 10 roots and 11 children for AgentSecurityComp, and 5 roots and 23
children for ARC-AGI-3. Only the 15 roots enter provider-level conversation
counts.

The direct case records identify native Codex originators and execution sources
in session metadata. Records with other working directories include software
factory, CortexControl, and a generated Codex conversation directory. They may
contain imported, continued, or cross-project references, but no direct case
attribution was established in this inventory, so all nine are excluded.
Legacy history mode is treated as storage metadata, not as evidence of a new
conversation. Parent identifiers and repeated metadata prevent continuation and
subagent inflation.

### OpenCode/DeepSeek inventory

Only non-sensitive columns from the OpenCode session table were inspected. The
15 matching rows separate cleanly by `parent_id`:

| Case | Parent sessions | Specialist sessions | Treatment |
| --- | ---: | ---: | --- |
| AgentSecurityComp | 2 | 0 | Supplementary parent records |
| ARC-AGI-3 | 3 | 10 | Supplementary parents with linked specialists |
| Total | 5 | 10 | Five conversations; ten child records |

The records span 2026-08-06 20:48:41 UTC through 2026-08-10 19:31:37 UTC.
Parent sessions report 4,962,336 input tokens and 512,822 output tokens;
specialists report 2,807,802 input tokens and 307,245 output tokens. These
database totals may include repeated context and must not be combined with
parent totals as a measure of independent work. The sessions used OpenCode
models labelled `big-pickle` and `deepseek-v4-flash-free`. Unequal timing,
models, tasks, and budgets rule out a balanced provider comparison.

### Deduplicated source map

| Source | Independent conversation unit retained | Derivative records retained for traceability | Primary use |
| --- | ---: | ---: | --- |
| Claude Code | 127 top-level sessions | 1,142 subagent and workflow-journal files | Primary transcript evidence across both cases |
| Codex | 15 historical case roots | 34 linked historical children | Supplementary challenge, reset, and implementation evidence |
| OpenCode/DeepSeek | 5 parents | 10 linked specialists | Limited supplementary evidence |
| Git repositories | 2 pinned revisions | Commit history and artifacts | Chronology, implementation, and revision checks |
| Author interview | 1 approved testimony set | Individual statements below | Baseline, oversight, cost, value, and trust judgments |

These rows are not additive across providers. Cross-provider imports, shared
prompts, and work on the same episode require episode-level deduplication before
any quantitative analysis.

## Author baseline and interview testimony

All statements in this section are **retrospective testimony** supplied by the
author. They are not direct measurements unless later corroborated by an
independent record.

- 16+ consulting years in decisioning, omnichannel AI, architecture, and early Java.
- Rusty independent coding; Python mainly with AI assistance.
- Goal: test agent-led research with little domain guidance.
- Role: approve, challenge, and encourage depth/breadth rather than supply hypotheses.
- Oversight: 2-5 hours/day.
- Direct spend: about USD 100 OpenRouter, USD 30 Modal, plus Colab Pro and Claude/Codex subscriptions.
- Value: enabled meaningful participation and accelerated contextual learning.
- Current outcome: neither winning objective achieved.
- Trust issue: confident claims often weakened after challenge; stale records propagated errors.
- No clear unexpected agent-originated discovery came to mind.

The author's broader baseline is an experienced technologist entering unfamiliar
research domains, not a novice-versus-expert comparison. Any counterfactual claim
about time saved or performance without AI must remain explicitly retrospective
and unmeasured.

## AgentSecurityComp chronology

| Boundary or evidence stream | Dated record | Evidentiary use |
| --- | --- | --- |
| Earliest primary Claude timestamp in the case store | 2026-06-13T09:28:39.036Z | Transcript chronology lower bound in the inventoried store |
| Earliest retained Codex root | 2026-06-16T21:32:33.640Z | Native supplementary-agent chronology |
| OpenCode parent records | 2026-08-07 15:44:40 UTC and 2026-08-09 10:50:46 UTC | Supplementary DeepSeek/OpenCode episodes |
| Latest primary Claude timestamp in the case store | 2026-08-15T14:51:09.743Z | Transcript chronology upper bound at inventory |
| Repository boundary | `2ed68e80705906dcbdf4f707edf8c37089ce0906`, 2026-08-16T10:29:29+03:00 | Code and artifact cutoff |

The current competition outcome is retrospective testimony: the winning
objective has not been achieved. Exact submission statuses, scores, and
leaderboard trajectories require live-record verification before manuscript
use.

## ARC-AGI-3 chronology

| Boundary or evidence stream | Dated record | Evidentiary use |
| --- | --- | --- |
| Earliest retained Codex root | 2026-06-16T19:13:15.496Z | Native supplementary-agent chronology |
| Earliest primary Claude timestamp in the case store | 2026-06-28T16:54:33.186Z | Transcript chronology lower bound in the inventoried store |
| OpenCode records | 2026-08-06 20:48:41 UTC through 2026-08-10 19:31:37 UTC | Supplementary parent and specialist episodes |
| Latest primary Claude timestamp in the case store | 2026-08-15T21:28:03.657Z | Transcript chronology upper bound at inventory |
| Repository boundary | `ebe5b3eca70260910144ae54e057c3d06ea0e14d`, 2026-08-15T18:41:01+03:00 | Code and artifact cutoff |

The current competition outcome is retrospective testimony: the winning
objective has not been achieved. The repository and external histories remain
read-only evidence sources.

## Coded research episodes

No episode is admitted in this provenance-only pass. Admission requires one row
containing the question or hypothesis, apparent origin, evidence cited before
implementation, proposed experiment, human review, local result, live result,
claim status, self-correction timing, and durable lesson. Each row must link its
parent session and any child or cross-provider records so one research episode
is not mistaken for several independent discoveries.

Allowed origin codes are human, agent, external source, and mixed. Allowed claim
statuses are confirmed, weakened, refuted, and unresolved. Negative and
superseded episodes remain in the ledger.

## Quote ledger

No transcript quotation is selected in this provenance-only pass. A quote may
be admitted only after a source-level context check and privacy review. Its
private trace must record case, provider, parent session, child session when
applicable, timestamp, speaker, exact source location, topic, surrounding
context, redaction note, evidence class, and manuscript use. Quotes may not be
used as substitutes for code, live evaluation, or literature evidence.

## Descriptive measures and derivations

| Measure | Derivation at this cutoff | Interpretation limit |
| --- | --- | --- |
| Claude primary conversations | 11 AgentSecurityComp + 116 ARC-AGI-3 = 127 | Store coverage, not independent hypotheses or achievements |
| Claude derivative records | 237 direct subagents + 876 workflow subagents + 29 journals = 1,142 | Traceability only; excluded from conversation count |
| Historical Codex roots | 10 AgentSecurityComp + 5 ARC-AGI-3 = 15 | Current paper-audit lineage and incidental matches excluded |
| Historical Codex children | 11 AgentSecurityComp + 23 ARC-AGI-3 = 34 | Linked to parents; not independent conversations |
| OpenCode parents | 2 AgentSecurityComp + 3 ARC-AGI-3 = 5 | Supplementary evidence only |
| OpenCode specialists | 0 AgentSecurityComp + 10 ARC-AGI-3 = 10 | Linked to parents; not independent conversations |
| OpenCode recorded usage | 7,770,138 input tokens and 820,067 output tokens | Descriptive database totals; no quality inference |
| Human oversight | 2-5 hours/day | Retrospective testimony, approximate |
| Direct spend | About USD 100 OpenRouter and USD 30 Modal, plus Colab Pro and Claude/Codex subscriptions | Retrospective testimony, approximate and not a complete cost accounting |

Project duration, active days, commit counts, experiment counts, submission
trajectories, interventions, retractions, and hypothesis outcomes are omitted
until reproducible derivations and source-level deduplication exist. No
productivity multiplier is inferable without a human-only control.

## Literature claim matrix

No scholarly claim is admitted in this provenance inventory. Literature entries
must record the exact claim supported, source type, publication status, stable
identifier, opened source location, supporting passage or result, limitations,
and manuscript destination. Every source must be opened and checked; title or
abstract matching alone is insufficient. Peer-reviewed and primary sources take
priority, while preprints and official releases remain clearly labelled.

## Living outcomes register

| Case | Status at cutoff | Evidence class | Update rule |
| --- | --- | --- | --- |
| AgentSecurityComp | Ongoing; winning objective not achieved | Retrospective testimony | Verify against live submissions and final competition records before revision |
| ARC-AGI-3 | Ongoing; winning objective not achieved | Retrospective testimony | Verify against official scoring and final competition records before revision |

Completed, pending, superseded, failed, and unresolved experiments must remain
distinguishable. Final rankings, costs, and retrospective judgments enter only
after the competitions conclude and the supporting records are checked.

## Known evidence gaps

- Live Kaggle submission histories, exact statuses, scores, and leaderboard
  records were not queried in this provenance task.
- Claude classification is based on filesystem position, naming, unique
  `sessionId` values, and top-level hashes. Episode-level content overlap still
  requires source review.
- The nine Codex matches from other working directories were conservatively
  excluded; their exact imported, continued, or incidental provenance was not
  adjudicated message by message.
- The current paper-audit Codex lineage is excluded from case-activity counts,
  but later research work needs the same lineage test.
- OpenCode database usage totals may include repeated context, retries, and
  parent-specialist overlap. They cannot support quality or productivity claims.
- The testimony on oversight, costs, value, trust, and unachieved objectives is
  not yet independently corroborated.
- No balanced provider assignment, common task set, controlled model versions,
  equal budget, or human-only control exists.
- No quote, coded episode, or literature claim has yet passed the source-level
  admission checks defined above.
- Both competition outcomes remain open, and neither winning objective has been
  achieved at the cutoff.
