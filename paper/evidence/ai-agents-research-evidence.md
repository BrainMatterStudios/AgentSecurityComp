# AI Agents in Research Evidence Ledger

This ledger is the provenance foundation for a living, comparative N-of-1 case
study. AgentSecurityComp is the primary case and ARC-AGI-3 is the comparative
case. OpenCode/DeepSeek is supplementary evidence, not a balanced provider
comparison. Session counts describe records, not research quality, autonomy, or
causal contribution.

## Evidence cutoff and repository revisions

The repository evidence cutoff for this inventory is
2026-08-16T10:29:29+03:00. The mutable agent stores were extracted separately
at the exact snapshot times below. Later revisions must state new cutoffs and
preserve earlier unresolved or negative outcomes rather than silently replacing
them.

| Repository | Role | Revision at cutoff | Commit date | Subject |
| --- | --- | --- | --- | --- |
| AgentSecurityComp | Primary case | `2ed68e80705906dcbdf4f707edf8c37089ce0906` | 2026-08-16T10:29:29+03:00 | `chore: ignore local worktrees` |
| ArcAGI3 | Comparative case, read-only | `ebe5b3eca70260910144ae54e057c3d06ea0e14d` | 2026-08-15T18:41:01+03:00 | `feat(duck-38): one-shot armed runner for 2026-08-16 00:01Z slot - SLOT SWAP from duck-p3` |

| Mutable source snapshot | Private source locator | Extraction time | Snapshot cutoff or filter |
| --- | --- | --- | --- |
| Claude AgentSecurityComp store | `claude:AgentSecurityComp/` under `/Users/ahmed/.claude/projects/-Users-ahmed-Documents-AgentSecurityComp/` | 2026-08-16T08:06:05Z | Substantive record window through 2026-08-15T14:51:09.743Z |
| Claude ARC-AGI-3 store | `claude:ARC-AGI-3/` under `/Users/ahmed/.claude/projects/-Users-ahmed-Documents-ArcAGI3/` | 2026-08-16T08:06:05Z | Substantive record window through 2026-08-15T21:28:03.657Z |
| Codex rollout store | `codex:` under `/Users/ahmed/.codex/sessions/` | 2026-08-16T08:06:05Z | Files matching `AgentSecurityComp|/Users/ahmed/Documents/ArcAGI3` at extraction time |
| OpenCode session store | `opencode:session/` in `/Users/ahmed/.local/share/opencode/opencode.db` | 2026-08-16T08:06:05Z | Matching session rows created through 2026-08-10 19:31:37 UTC |

These are frozen inventory observations, not immutable content-addressed
artifacts. Claude, Codex, and OpenCode stores can change after extraction, so a
later live query may produce different counts or classifications and must be
reported as a new snapshot rather than a byte-reproducible rebuild.

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
- The approved paper design at
  `docs/superpowers/specs/2026-08-16-paper-revision-and-agent-research-design.md:82-93`
  records Ahmed's authorization for short quotations from the local agent
  transcripts. That authority is limited to excerpts relevant to hypothesis
  formation, confidence, correction, intervention, or research governance;
  excerpts must be short, contextualized, privacy-preserving, and stripped of
  secrets, credentials, and unrelated personal information. Admission still
  requires an `authorized` status in the private quote trace; withheld or
  revoked material must not appear in the manuscript.
- Every admitted quote must retain a private trace to provider, case, session
  identifier, timestamp, speaker, source location, and authorization status.
  Public text may use a pseudonymous source label where the raw identifier adds
  no evidentiary value.
- Redaction must not change the proposition or speaker intent. Paraphrase rather
  than quote when safe redaction would make the excerpt ambiguous.
- AI-authored claims, citations, summaries, and interpretations require an
  independent source check before manuscript use. Ahmed Mobasher remains the
  accountable sole author. Both the Methods and Acknowledgements must disclose
  assistance from Claude Code, Codex, and OpenCode/DeepSeek; none is an author.

## Session provenance and deduplication

### Counting rules

1. A provider's top-level conversation is the default unit for session counts.
2. A subagent or specialist record is linked to its top-level parent and is not
   counted again as an independent conversation.
3. Workflow journals, scratchpad copies, and tool-result derivatives are
   provenance aids, not conversations.
4. A Codex rollout's canonical conversation identifier is the first
   `session_meta.payload.session_id` when present, otherwise the ultimate
   `parent_thread_id`, otherwise its own `id`. Multiple files with the same
   canonical identifier form one lineage. Only a native historical root may be
   counted; children and repeated metadata records remain trace-only.
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
8. Claude top-level files are joined when their legacy `session_id`, bridge
   identifier, or file identifier overlaps. Within each connected component,
   the earliest substantive CLI record is the canonical conversation; later
   substantive records are continuations and all SDK or bridge-only records are
   derivatives.
9. Token counts are usage descriptors only. They are not measures of thought,
   scientific value, originality, or provider performance.

### Claude inventory

The Claude project stores were enumerated recursively. Files below `subagents`
are child work; `journal.jsonl` files below workflow directories are workflow
journals. Top-level files require metadata classification: a native `cli` record
with at least one typed or queued prompt is a substantive primary-session chunk;
an `sdk-cli` record or a bridge/initialization record without an explicit prompt
is a tool-result derivative. This corrects the earlier, invalid assumption that
every top-level UUID file was an independent conversation.

| Case store | Substantive top-level chunks | Included canonical groups | Excluded continuations |
| --- | ---: | ---: | ---: |
| AgentSecurityComp | 10 | 5 | 5 |
| ARC-AGI-3 | 13 | 5 | 8 |
| Total | 23 | 10 | 13 |

SDK-created records, bridge/initialization stubs without explicit prompts,
subagents, workflow journals, scratchpad copies, and tool-result derivatives
are trace-only provenance and are not counted as conversations. This Markdown
inventory does not claim an exhaustive row-level manifest of those mutable raw
records.

The 13 excluded substantive continuations resolve to the canonical groups below
through legacy-session or bridge identifiers:

| Case | Excluded continuation IDs | Canonical conversation ID |
| --- | --- | --- |
| AgentSecurityComp | `d368bb45-0b14-4073-9740-774ade58e769` | `d02227a2-1ed0-471c-abb2-994217974264` |
| AgentSecurityComp | `25c84940-5ede-4850-a639-5579fdef6ebe` | `f1ef3669-1d5f-4caf-ab9b-c4eedf643569` |
| AgentSecurityComp | `84f715ee-9b96-4ee0-9950-48acf7a82447`, `9f138e71-bfaa-49fa-93aa-e6cf5f592493` | `a809e3ce-6bd5-4997-914a-1100fe705967` |
| AgentSecurityComp | `9d0f25c3-7d3c-4eaf-a219-001b44ea5ec4` | `0385f350-248c-431f-a9f2-1604c96b5ce2` |
| ARC-AGI-3 | `c9ecf8fc-b749-4067-9622-38b0060db14f`, `5174edda-9963-4cdd-9306-18d2695d0fd0`, `38ec9bae-690c-4713-aa14-c3245497ca9e`, `0ba5f0b9-392e-404c-824f-ade3803cc524`, `0e3cf55e-6aa2-408c-bf63-8dfa02fe7d9a` | `573f46bd-f297-4c15-8028-9676d148ba1b` |
| ARC-AGI-3 | `066c8134-787a-41a1-8dcb-dd4815d4a1d1`, `d093e020-dbb1-4965-958c-471bfea0138e` | `626c7722-330b-4125-b1de-439d21bef0a0` |
| ARC-AGI-3 | `ff31ed86-9a67-4b4a-9261-458a5f2e9819` | `32add479-d332-44f0-ae03-8ed849c86377` |

A privacy-preserving overlap audit of the 23 substantive chunks found zero
shared message-UUID pairs, zero repeated prompt-and-timestamp pairs, zero
identical three-prompt prefixes, and zero identical contiguous three-prompt
runs. Prompt text was normalized and hashed in memory; neither text nor hashes
were retained. These checks address regenerated identifiers and copied prefixes
without publishing transcript content.

The substantive Claude record windows are 2026-06-13T09:28:39.036Z through
2026-08-15T14:51:09.743Z for AgentSecurityComp and
2026-06-28T16:54:33.186Z through 2026-08-15T21:28:03.657Z for ARC-AGI-3.
The reported quantity is 10 metadata- and overlap-deduplicated canonical
conversation groups, not 127 top-level files.

### Codex inventory

The frozen 2026-08-16T08:06:05Z content search found 70 rollout files. First
metadata records classify them as follows:

| Classification | Root rollouts | Child rollouts | Count treatment |
| --- | ---: | ---: | --- |
| AgentSecurityComp working directory | 11 | 22 | Case candidates |
| ARC-AGI-3 working directory | 5 | 23 | Case candidates |
| Other working directory with a text match | 5 | 4 | Excluded as incidental |

One AgentSecurityComp root and eleven of its children belong to the current
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
conversation. The compact canonical map below applies the explicit `session_id`
/ ultimate-parent / own-ID rule; the 15 retained roots have 15 distinct
canonical identifiers. The 34 historical children are trace-only, the 12
current paper-audit records are excluded, and the nine incidental working-
directory matches are excluded.

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

### Canonical evidence-source map

This compact, privacy-safe map lists only the included canonical conversation
or parent-session groups observed in the frozen mutable-store snapshot. Locators
resolve against the private read-only bases in the snapshot table above.

| Provider | Case | Canonical ID | Source locator | Disposition |
| --- | --- | --- | --- | --- |
| Claude Code | ARC-AGI-3 | `2c317a12-f48d-4a3f-8ddc-8b48615ad490` | `claude:ARC-AGI-3/2c317a12-f48d-4a3f-8ddc-8b48615ad490.jsonl` | included-canonical |
| Claude Code | ARC-AGI-3 | `32add479-d332-44f0-ae03-8ed849c86377` | `claude:ARC-AGI-3/32add479-d332-44f0-ae03-8ed849c86377.jsonl` | included-canonical |
| Claude Code | ARC-AGI-3 | `573f46bd-f297-4c15-8028-9676d148ba1b` | `claude:ARC-AGI-3/573f46bd-f297-4c15-8028-9676d148ba1b.jsonl` | included-canonical |
| Claude Code | ARC-AGI-3 | `626c7722-330b-4125-b1de-439d21bef0a0` | `claude:ARC-AGI-3/626c7722-330b-4125-b1de-439d21bef0a0.jsonl` | included-canonical |
| Claude Code | ARC-AGI-3 | `de216582-726c-415f-9dd5-71c05fb4d2c3` | `claude:ARC-AGI-3/de216582-726c-415f-9dd5-71c05fb4d2c3.jsonl` | included-canonical |
| Claude Code | AgentSecurityComp | `0385f350-248c-431f-a9f2-1604c96b5ce2` | `claude:AgentSecurityComp/0385f350-248c-431f-a9f2-1604c96b5ce2.jsonl` | included-canonical |
| Claude Code | AgentSecurityComp | `42258c4d-4471-458b-a3c0-757cf6791024` | `claude:AgentSecurityComp/42258c4d-4471-458b-a3c0-757cf6791024.jsonl` | included-canonical |
| Claude Code | AgentSecurityComp | `a809e3ce-6bd5-4997-914a-1100fe705967` | `claude:AgentSecurityComp/a809e3ce-6bd5-4997-914a-1100fe705967.jsonl` | included-canonical |
| Claude Code | AgentSecurityComp | `d02227a2-1ed0-471c-abb2-994217974264` | `claude:AgentSecurityComp/d02227a2-1ed0-471c-abb2-994217974264.jsonl` | included-canonical |
| Claude Code | AgentSecurityComp | `f1ef3669-1d5f-4caf-ab9b-c4eedf643569` | `claude:AgentSecurityComp/f1ef3669-1d5f-4caf-ab9b-c4eedf643569.jsonl` | included-canonical |
| Codex | ARC-AGI-3 | `019ed1da-2605-7a63-b99e-69db1f12161b` | `codex:2026/06/16/rollout-2026-06-16T21-13-15-019ed1da-2605-7a63-b99e-69db1f12161b.jsonl` | included-canonical |
| Codex | ARC-AGI-3 | `019ed98f-89e6-7530-bcf1-c453709e4434` | `codex:2026/06/18/rollout-2026-06-18T09-08-43-019ed98f-89e6-7530-bcf1-c453709e4434.jsonl` | included-canonical |
| Codex | ARC-AGI-3 | `019ed98f-8a24-7bb2-8aa4-1f14fd24088b` | `codex:2026/06/18/rollout-2026-06-18T09-08-43-019ed98f-8a24-7bb2-8aa4-1f14fd24088b.jsonl` | included-canonical |
| Codex | ARC-AGI-3 | `019fce51-2e83-73b1-92d9-2a24d75c102a` | `codex:2026/08/04/rollout-2026-08-04T22-47-34-019fce51-2e83-73b1-92d9-2a24d75c102a.jsonl` | included-canonical |
| Codex | ARC-AGI-3 | `01a005ec-999c-7573-9626-e89e51ad4f6b` | `codex:2026/08/15/rollout-2026-08-15T17-56-27-01a005ec-999c-7573-9626-e89e51ad4f6b.jsonl` | included-canonical |
| Codex | AgentSecurityComp | `019ed259-af2a-7020-9160-0b55c823dac1` | `codex:2026/06/16/rollout-2026-06-16T23-32-33-019ed259-af2a-7020-9160-0b55c823dac1.jsonl` | included-canonical |
| Codex | AgentSecurityComp | `019ed25a-827c-7202-81f7-f635cc301017` | `codex:2026/06/16/rollout-2026-06-16T23-33-27-019ed25a-827c-7202-81f7-f635cc301017.jsonl` | included-canonical |
| Codex | AgentSecurityComp | `019ed98f-8976-7c43-a9c1-5ca274e2de36` | `codex:2026/06/18/rollout-2026-06-18T09-08-43-019ed98f-8976-7c43-a9c1-5ca274e2de36.jsonl` | included-canonical |
| Codex | AgentSecurityComp | `019fad04-b6b5-7370-b5ac-bfbf870e1c16` | `codex:2026/07/29/rollout-2026-07-29T11-36-35-019fad04-b6b5-7370-b5ac-bfbf870e1c16.jsonl` | included-canonical |
| Codex | AgentSecurityComp | `019fad19-326f-7503-90a8-0df3753259d3` | `codex:2026/07/29/rollout-2026-07-29T11-58-57-019fad19-326f-7503-90a8-0df3753259d3.jsonl` | included-canonical |
| Codex | AgentSecurityComp | `019fad7d-427a-7d00-9818-33698703ce2c` | `codex:2026/07/29/rollout-2026-07-29T13-48-15-019fad7d-427a-7d00-9818-33698703ce2c.jsonl` | included-canonical |
| Codex | AgentSecurityComp | `019fad85-1933-7f80-804a-e3395635559b` | `codex:2026/07/29/rollout-2026-07-29T13-56-48-019fad85-1933-7f80-804a-e3395635559b.jsonl` | included-canonical |
| Codex | AgentSecurityComp | `019fce03-3854-79b1-a5ed-c0cd803a0575` | `codex:2026/08/04/rollout-2026-08-04T21-22-25-019fce03-3854-79b1-a5ed-c0cd803a0575.jsonl` | included-canonical |
| Codex | AgentSecurityComp | `019fce29-2147-70b1-a1f1-054e020cd692` | `codex:2026/08/04/rollout-2026-08-04T22-03-49-019fce29-2147-70b1-a1f1-054e020cd692.jsonl` | included-canonical |
| Codex | AgentSecurityComp | `01a005ed-b434-76a0-95e0-5fe82f4dc768` | `codex:2026/08/15/rollout-2026-08-15T17-57-39-01a005ed-b434-76a0-95e0-5fe82f4dc768.jsonl` | included-canonical |
| OpenCode/DeepSeek | ARC-AGI-3 | `ses_012d743fcffeBoq8D4McmfGQTH` | `opencode:session/ses_012d743fcffeBoq8D4McmfGQTH` | included-canonical |
| OpenCode/DeepSeek | ARC-AGI-3 | `ses_019d88ca1ffe3iOYWxPRUUcfAA` | `opencode:session/ses_019d88ca1ffe3iOYWxPRUUcfAA` | included-canonical |
| OpenCode/DeepSeek | ARC-AGI-3 | `ses_0272a2568ffeSoBW8bBagLOznD` | `opencode:session/ses_0272a2568ffeSoBW8bBagLOznD` | included-canonical |
| OpenCode/DeepSeek | AgentSecurityComp | `ses_019da7b0effeSVV74ieACHE15I` | `opencode:session/ses_019da7b0effeSVV74ieACHE15I` | included-canonical |
| OpenCode/DeepSeek | AgentSecurityComp | `ses_0231a2013ffeeQefgINsuGs4Is` | `opencode:session/ses_0231a2013ffeeQefgINsuGs4Is` | included-canonical |

| Exclusion or deduplication disposition | Snapshot treatment |
| --- | --- |
| Claude substantive continuations | 13 excluded and mapped to the 10 Claude canonical groups above |
| Claude SDK/bridge records, subagents, journals, scratchpads, and tool-result derivatives | Trace-only; excluded from conversation counts |
| Codex historical children | 34 trace-only children linked through the canonical-ID rule |
| Codex current paper-audit lineage | 12 records excluded, including root `01a0091e-6c06-72e0-ba1c-e5499447d566` |
| Codex incidental working-directory matches | 9 records excluded from both cases |
| OpenCode specialists | 10 trace-only sessions linked by `session.parent_id` |

### Deduplicated source summary

| Source | Independent conversation unit retained | Derivative records retained for traceability | Primary use |
| --- | ---: | ---: | --- |
| Claude Code | 10 canonical conversation groups | 13 mapped substantive continuations; other derivatives remain trace-only without an exhaustive row manifest | Primary transcript evidence across both cases |
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

No transcript quotation is selected in this provenance-only pass. Under the
approved design authority cited in the privacy rules, a quote may be admitted
only if it satisfies every stated relevance, brevity, context, privacy, and
secret-removal constraint, passes a source-level context check and privacy
review, and has an `authorized` status. Its private trace must record case,
provider, parent session, child session when applicable, timestamp, speaker,
exact source location, topic, surrounding context, redaction note, evidence
class, authorization status, and manuscript use. Withheld or revoked
authorization blocks admission. Quotes may not be used as substitutes for
code, live evaluation, or literature evidence.

## Descriptive measures and derivations

| Measure | Derivation at this cutoff | Interpretation limit |
| --- | --- | --- |
| Claude canonical conversation groups | 5 AgentSecurityComp + 5 ARC-AGI-3 = 10 | Metadata- and overlap-deduplicated groups, not hypotheses or achievements |
| Claude excluded continuations | 13 of 23 substantive chunks | Linked to the 10 canonical groups by legacy or bridge identifiers |
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
- Claude classification and canonical groups were derived at the stated store
  snapshot from entrypoint, prompt-source, legacy-session, bridge, and path
  metadata. The hashed overlap audit detects exact copied prompt runs of three
  or more, but paraphrased or shorter overlap remains possible; the value 10
  therefore describes canonical conversation groups under this stated rule,
  not independent intellectual work or a promise that a later mutable-store
  extraction will match.
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
  admission and authorization checks defined above.
- Both competition outcomes remain open, and neither winning objective has been
  achieved at the cutoff.
