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

The rows below are bounded episodes rather than provider turns. `Prior evidence`
records what was cited before the test; `Local outcome` and `Live outcome` remain
separate. Origin is coded conservatively as `human`, `agent`, `external`, or
`mixed`; status is one of `confirmed`, `partially supported`, `refuted`,
`invalid experiment`, `superseded`, or `open`. A provider's proposal is not
treated as autonomous discovery when the record also contains human or external
input. OpenCode specialist sessions are linked to their parent investigation.

### AgentSecurityComp episodes

| Case | Date | Episode | Origin | Prior evidence | Agent confidence | Human intervention | Local outcome | Live outcome | Final status | Lesson | Source IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASC | 2026-06-13 | Port the attack from a mock scaffold to the real SDK. | mixed | SDK inspection contradicted the scaffold. | High after inspection. | Required real-path verification and submission approval. | Real `AttackCandidate` path ran. | Subsequent submissions used the real SDK. | confirmed | Inspect the executable interface before optimizing it. | AS-S01 |
| ASC | 2026-06-13 | Increase candidate volume because the scorer appeared additive. | agent | Initial SDK/scorer reading. | High. | Continued local and live testing. | Hundreds of compliant candidates were generated. | Scale helped establish a baseline but did not solve the task. | partially supported | A valid scoring direction need not be the decisive lever. | AS-S02 |
| ASC | 2026-06-27 | Add the required `SECRET_MARKER` after fabricated tokens stopped scoring. | external | SDK 3.1.2 semantics and zero-score evidence. | High after correction. | Accepted the compatibility repair. | Marker-bearing exfiltration validated. | Scoring resumed on the corrected path. | confirmed | Protocol semantics can invalidate an otherwise plausible attack. | AS-S03 |
| ASC | 2026-07-25 | Adapt output size to replay-safe observed limits. | external | Mechanism attributed to higher-scoring public solutions. | High. | Approved a bounded ladder. | Replay-safe adaptive sizing passed local checks. | L6 reached 80.145. | confirmed | External ideas require a faithful, bounded reproduction. | AS-S04 |
| ASC | 2026-07-26 | Stop decoding after `close_ok` to reduce per-candidate latency. | agent | Local timing of 1.03 s versus 1.23 s. | Called it a decisive roughly 20% lever. | Submitted a controlled ladder. | Clear local latency reduction. | About +1.44 points, materially smaller than implied. | partially supported | Directional local effects may transfer at a much smaller magnitude. | AS-S05 |
| ASC | 2026-07-27 | Pack more messages per call to amortize overhead. | mixed | Human throughput objective plus local timing model. | High enough to arm L8. | Requested live discrimination. | Local packing looked favorable. | Live ladder failed to improve the leader. | refuted | Throughput models must include hidden evaluator behavior. | AS-S06 |
| ASC | 2026-08-04 | Explain Gemma's failure as model weakness. | agent | An under-powered hop-pack comparison. | Initially high, then retracted. | Required a faithful framing comparison. | GPT also scored zero under the weak frame; the real forge separated models. | No clean live test of the original claim. | invalid experiment | A comparison is invalid when the control is broken. | AS-S07 |
| ASC | 2026-08-08 | Route candidates deterministically by board and split the workload. | agent | An apparent isolation/throughput gap after L22. | High. | Authorized a controlled router ladder. | Router and self-measurement worked locally. | 42.665-47.865 versus 44.320 baseline; no stable gain. | invalid experiment | A multi-arm ladder can still be non-identifying when arms overlap. | AS-S08 |
| ASC | 2026-08-09 | Reproduce the public commitment-forge mechanism. | external | Public dimong4/nctuan strategy. | Moderate to high. | Required faithful implementation and live test. | Four posts per candidate fired as designed. | 47.850 versus 43.600 single-forge control. | partially supported | Faithful reproduction can validate mechanism without matching public performance. | AS-S09 |
| ASC | 2026-08-09 | Use dual-board/Gemma forge to beat the reproduced baseline. | agent | Commitment-forge result and model-specific local behavior. | High. | Approved direct single-versus-dual comparisons. | Both-board logic ran. | Dual arms 81.985 and 82.660; Gemma forge 34 versus Gemma single 27. | partially supported | Component gains can coexist with a still-unexplained ceiling. | AS-S10 |
| ASC | 2026-08-12 | Test both proposed throughput knobs in one L27 ladder. | mixed | Agent hypotheses and human instruction to test both. | Confidence fell when both reduced to one axis. | Insisted on both tests and a control. | Probe-hop variants were executable. | 50.295-57.620 versus 88.730 control. | refuted | Before launch, verify that nominally distinct arms identify distinct mechanisms. | AS-S11 |
| ASC | 2026-08-13 | Move generation to GPU to remove a suspected CPU cap. | agent | Timing observations and a CPU-cap hypothesis. | Described as likely the lever. | Approved a CPU/GPU A/B ladder. | GPU path became functional after zero-score failures. | Best GPU arm 50.175 versus CPU reference 83.115. | partially supported | Infrastructure functionality was established; efficacy was not. | AS-S12 |
| ASC | 2026-08-15 | Split hop-pack work in L29. | agent | Residual throughput hypothesis after L27. | Moderate. | Allowed a bounded live test. | Split runner executed. | 85.675, below the 88.730 L27 control. | refuted | A near-baseline score is not evidence of improvement. | AS-S13 |
| ASC | 2026-08-16 | Chain packed generations in L31. | agent | Packing and forge follow-up hypotheses. | Moderate. | Kept the ladder pending rather than declaring success. | Chainpack arms were prepared; fast-emit arm ran. | Chainpack arms pending; fast emit scored 25.145. | open | Pending arms and failed companion arms must remain distinct. | AS-S14 |

### ARC-AGI-3 episodes

| Case | Date | Episode | Origin | Prior evidence | Agent confidence | Human intervention | Local outcome | Live outcome | Final status | Lesson | Source IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ARC | 2026-08-09 | Type observations by role before goal inference. | mixed | Failure review of flat-frame perception. | High. | Directed retesting on retained cases. | Flat frame 0/9; right frame 6/6. | No isolated live attribution. | partially supported | Representation can be causal locally without a separable live estimate. | ARC-S01 |
| ARC | 2026-07-01 | Search solved paths, then replay them. | agent | Verification that scoring used the best run. | High. | Required dev and live checks. | Search solved all 25 development games. | The scoring trick did not survive live conditions. | partially supported | Separate solver validity from evaluator transfer. | ARC-S02 |
| ARC | 2026-06-29 | Double-reset between plays to improve geodesic efficiency. | agent | Local state-machine analysis. | High. | Challenged the result against competition mode. | Claimed 7-109x efficiency after repairing a no-op. | Second play returned HTTP 400. | invalid experiment | Test lifecycle semantics in the actual evaluation mode. | ARC-S03 |
| ARC | 2026-07-14 | Use an EWM policy after independent code review. | agent | Reviewer findings and local evaluations. | High after review. | Continued comparative testing. | Review defects were repaired. | Later campaigns displaced the policy; no durable isolated gain. | superseded | Review can improve implementation without establishing lasting efficacy. | ARC-S04 |
| ARC | 2026-07-11 | Serve a fine-tuned adapter that appeared to beat base. | mixed | Local 1.26 result and human interest in fine-tuning. | High before serving audit. | Asked for proof of the deployed model identity. | The apparent gain was generated by base, not the adapter. | The LoRA never served. | invalid experiment | Serving identity is part of experimental validity. | ARC-S05 |
| ARC | 2026-08-01 | Measure A/A leaderboard noise before reading small deltas. | mixed | Repeated submission variability and human skepticism. | High. | Required registered gates. | Two gates were under-powered relative to noise. | Submission ledger preserved the noise result. | confirmed | Calibrate the instrument before interpreting changes. | ARC-S06 |
| ARC | 2026-08-03 | Correct slow-tick HUD bar parsing. | agent | Error analysis on m0r0-class bars. | High after targeted tests. | Required replay/regression checks. | Virtual rotation and masks fixed retained cases. | No isolated leaderboard delta claimed. | confirmed | A narrowly verified parser correction can be confirmed without a ranking claim. | ARC-S07 |
| ARC | 2026-07-12 | Reduce prompt tokens to improve performance. | agent | Development mean 1.96 versus 0.89. | High from the local result. | Required hidden evaluation. | Roughly doubled dev performance. | Hidden score was 0.73. | refuted | Large development gains can be distribution-specific. | ARC-S08 |
| ARC | 2026-08-10 | Use best-of-N with reset-based repeated plays. | agent | Probe results and repeated-play theory. | High before boundary test. | Required independent competition-mode verification. | Candidate selection worked in the harness. | Competition mode swallowed the boundary reset; second play failed. | refuted | A strategy depending on unavailable evaluator actions is not deployable. | ARC-S09 |
| ARC | 2026-08-09 | Add a structural plan channel with brake and phase gates. | mixed | Human strategy goals plus prior failure analysis. | Moderate. | Required live ledger comparison. | Structural controls executed. | Results stayed in the existing score band. | partially supported | Better process structure is not automatically a score breakthrough. | ARC-S10 |
| ARC | 2026-08-15 | Replace duck baseline with engineered Stage 2b. | mixed | Portfolio analysis and staged local benchmark. | Moderate. | Required a full-25 verdict. | 0.2463 versus duck 1.6333, with six game wins. | No replacement claim was shipped; narrow edge retained. | partially supported | Preserve a narrow portfolio edge while rejecting the broad paradigm. | ARC-S11 |
| ARC | 2026-08-15 | Promote Qwen 3.8 after a controlled local A/B. | mixed | External model candidate, agent screening, human competition goal. | High locally. | Required an armed but gated live runner. | Mean 2.5291 versus Qwen 3.6 at 1.4872. | No scored live result existed by cutoff. | open | A strong local A/B remains an open transfer claim until live scoring. | ARC-S12 |

### OpenCode primary investigations

| Case | Date | Episode | Origin | Prior evidence | Agent confidence | Human intervention | Local outcome | Live outcome | Final status | Lesson | Source IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASC | 2026-08-07 | Independently review L20/L21 mechanisms and next tests. | mixed | Repository state and submission ledger. | Moderate. | Framed the audit and retained submission authority. | Produced a bounded diagnosis with no child specialists. | Later evidence supported only parts of it. | partially supported | An independent review is evidence synthesis, not an independent project. | OC-S01 |
| ASC | 2026-08-09 | Re-audit the case without trusting memory or recorded conclusions. | mixed | Parent prompt required primary validation. | Deliberately provisional. | Explicitly imposed the memory-blind rule. | Rechecked code and evidence; no child specialists. | No completed live adjudication by cutoff. | open | A strong epistemic instruction improves audit discipline but is not an outcome. | OC-S02 |
| ARC | 2026-08-06 | Audit duck-sparse behavior. | mixed | Repository artifacts and a parent-led question. | Moderate. | Set scope and reviewed the linked child. | Parent plus one specialist produced a diagnosis. | Later competition behavior did not validate the implied path. | invalid experiment | Parent and specialist outputs are one investigation, not two discoveries. | OC-S03 |
| ARC | 2026-08-09 | Run a nine-specialist research campaign over an assumed corpus. | mixed | Parent synthesis plus nine linked specialist searches. | High in the synthesis. | Commissioned and challenged the campaign. | Produced a research document. | Later audit found wrong-model corpus provenance. | invalid experiment | Parallel breadth cannot repair invalid source provenance. | OC-S04 |
| ARC | 2026-08-10 | Repair and test the duck-memory namespace strategy. | mixed | Prior OpenCode proposal plus Ahmed's critique of earlier mistakes. | Moderate. | Demanded explicit correction and verification. | Later Claude work repaired a namespace no-op. | Duck-memory result stayed in-band. | partially supported | Cross-provider continuation must retain one episode identity and modest claims. | OC-S05 |

### Episode source register

Each source ID below resolves either to an inventoried transcript locator, an
OpenCode parent/child identifier, a repository object in the pinned case
history, or an explicitly identified read-only working-tree artifact. Short Git
hashes are unambiguous in the named repository and are ancestors of the stated
cutoff.

| Source ID | Resolvable locator |
| --- | --- |
| AS-S01 | AgentSecurityComp commit `3e30121`; `claude:AgentSecurityComp/d02227a2-1ed0-471c-abb2-994217974264.jsonl#L164`, message `17b5c3bc` |
| AS-S02 | AgentSecurityComp commit `3e30121`; `claude:AgentSecurityComp/d02227a2-1ed0-471c-abb2-994217974264.jsonl#L264,#L369`, messages `a216cca8` and `eb60b846` |
| AS-S03 | AgentSecurityComp commit `1ac76a0` |
| AS-S04 | AgentSecurityComp commit `e85a7ba`; `paper/evidence/working-note-claim-ledger.md`, row L6 score 80.145 |
| AS-S05 | AgentSecurityComp commit `242a855`; `claude:AgentSecurityComp/25c84940-5ede-4850-a639-5579fdef6ebe.jsonl#L255-L258,#L491`, continuation linked to canonical `f1ef3669-1d5f-4caf-ab9b-c4eedf643569` |
| AS-S06 | AgentSecurityComp commit `77862ef`; `claude:AgentSecurityComp/25c84940-5ede-4850-a639-5579fdef6ebe.jsonl#L566`, continuation linked to canonical `f1ef3669-1d5f-4caf-ab9b-c4eedf643569`; `paper/evidence/working-note-claim-ledger.md`, row L8 |
| AS-S07 | AgentSecurityComp commit `a322c7b`; `claude:AgentSecurityComp/9f138e71-bfaa-49fa-93aa-e6cf5f592493.jsonl#L1084`, continuation linked to canonical `a809e3ce-6bd5-4997-914a-1100fe705967` |
| AS-S08 | AgentSecurityComp commit `2298119`; `claude:AgentSecurityComp/0385f350-248c-431f-a9f2-1604c96b5ce2.jsonl#L761-L772`; `paper/evidence/working-note-claim-ledger.md`, rows L22-L23 |
| AS-S09 | AgentSecurityComp commit `f2eeee4`; `paper/evidence/working-note-claim-ledger.md`, row L24 submissions `55391763`, `55392055` |
| AS-S10 | AgentSecurityComp commit `6fbe6e5`; `paper/evidence/working-note-claim-ledger.md`, row L25 submissions `55418160`, `55418165`, `55418171`, `55418180`, `55418184` |
| AS-S11 | AgentSecurityComp commit `0504391`; `claude:AgentSecurityComp/9d0f25c3-7d3c-4eaf-a219-001b44ea5ec4.jsonl#L1291-L1313`, continuation linked to canonical `0385f350-248c-431f-a9f2-1604c96b5ce2`; `paper/evidence/working-note-claim-ledger.md`, row L27 |
| AS-S12 | AgentSecurityComp commit `52d7f0f`; `claude:AgentSecurityComp/9d0f25c3-7d3c-4eaf-a219-001b44ea5ec4.jsonl#L1488-L1573`; `paper/evidence/working-note-claim-ledger.md`, GPU submissions `55500552`, `55525506`, `55525507`, `55525533`, `55525536` |
| AS-S13 | AgentSecurityComp commit `6018877`; `paper/evidence/working-note-claim-ledger.md`, row L29 submission `55530790` |
| AS-S14 | AgentSecurityComp commit `b02d457`; `paper/evidence/working-note-claim-ledger.md`, row L31 submissions `55538814`, `55538829`, `55538848`, `55538855`, `55538875` |
| ARC-S01 | ArcAGI3 commit `19fd560`; cutoff `ebe5b3e:scripts/research_2026_07_01/goal_inference/exp_b_reasoner/retest_roletyped/VERDICT.md#L1-L23` |
| ARC-S02 | ArcAGI3 commits `8b5ab48`, `4270936`, `a077012`; cutoff `docs/DESIGN-2026-08-14-engineered-agent.md#L28-L35` |
| ARC-S03 | ArcAGI3 commits `df9b96b`, `25e7a78`; cutoff `docs/DESIGN-2026-08-14-engineered-agent.md#L30-L33` |
| ARC-S04 | ArcAGI3 commit `10a94c6`; `claude:ARC-AGI-3/38ec9bae-690c-4713-aa14-c3245497ca9e.jsonl#L29`, continuation linked to canonical `573f46bd-f297-4c15-8028-9676d148ba1b` |
| ARC-S05 | ArcAGI3 commit `7bc3cfc`; `claude:ARC-AGI-3/573f46bd-f297-4c15-8028-9676d148ba1b.jsonl#L6491,#L6766-L6819`, messages `069646ee`, `cd994208` |
| ARC-S06 | ArcAGI3 commits `8d8b671`, `59baf3c`; cutoff `docs/submission-ledger.json` |
| ARC-S07 | ArcAGI3 commits `bab2aea`, `f0ec605`; cutoff `docs/test-artifacts-2026-08-02/AB-ROUND3-ANALYSIS-2026-08-03.md#L28` |
| ARC-S08 | ArcAGI3 cutoff `docs/submission-ledger.json`, submission `54603982`; `docs/DESIGN-2026-08-14-engineered-agent.md#L168-L173` |
| ARC-S09 | ArcAGI3 commit `b5ad790`; cutoff `docs/DESIGN-2026-08-14-engineered-agent.md#L30-L33` |
| ARC-S10 | ArcAGI3 commits `4bb431d`, `cfeb92a`; cutoff `docs/submission-ledger.json` structural entries |
| ARC-S11 | ArcAGI3 commit `da37afd`; read-only working-tree artifact `/Users/ahmed/Documents/ArcAGI3/scratchpad/engineered_stage2/stage2b_verdict.md#L100-L125` (not a Git object at cutoff) |
| ARC-S12 | ArcAGI3 commits `4f3d330`, `ebe5b3e`; cutoff `docs/RESEARCH-2026-08-15-field-sweep-and-qwen38.md` and `scratchpad/qwen38/wave1_shipped_result.json` |
| OC-S01 | OpenCode parent `ses_0231a2013ffeeQefgINsuGs4Is`; parts `prt_fdceb7e16001ewOtfo1IejX335`, `prt_fdd5782a4001yvBGaK16aVW6Ul`, `prt_fdd99103a001Kl13c0eW6b4uA7`; no child sessions |
| OC-S02 | OpenCode parent `ses_019da7b0effeSVV74ieACHE15I`; message `msg_fe6258538001IR3J7Nyc6r9Ul5`; parts `prt_fe6258539001I0glvysE6QnNH1`, `prt_fe6735d130015A4EbSnvC3Zp01`, `prt_fe800cd8e001YHesMMKyNQMCLE`; no child sessions |
| OC-S03 | OpenCode parent `ses_0272a2568ffeSoBW8bBagLOznD`; child `ses_02728fff5ffeWMGhU1bTBxcIW7` |
| OC-S04 | OpenCode parent `ses_019d88ca1ffe3iOYWxPRUUcfAA`; parent part `prt_fe74f3faf001pnW7paA43QMreY`; children `ses_019ca316cffegBxl0NpwvitlLO`, `ses_019c9dd5bffeuX588N88Xn5WSF`, `ses_019c9b9e2ffexGiL2Ode8mpfKV`, `ses_01990f651ffeMalEJ9WV0K773P`, `ses_017f9fdb1ffeBuyqRX0He6wj71`, `ses_017f9dc39ffeIbLmAP4q7R6DLU`, `ses_017f9b1a7ffeeTpM2a9aZHaH0w`, `ses_017f98cb8ffeu7uREep8fiwApw`, `ses_017f96940ffeOZMamaLyLZjIEo` |
| OC-S05 | OpenCode parent `ses_012d743fcffeBoq8D4McmfGQTH`; parts `prt_fed28bc42002PXmQG8QKoFfAbb`, `prt_fed3e0b84001O1GyQL97xzc4a6`, `prt_fed457d11001LPejrLwsq84k3s`; no child sessions |

## Quote ledger

These nine excerpts passed the source-context and privacy checks required by the
approved design. They are intentionally short. No credential, secret, unrelated
personal detail, or third-party personal information is present. `None` in the
redaction column means that the excerpt needed no alteration. Quotations provide
process or retrospective evidence only; they do not replace code or live results.

| Quote ID | Case and topic | Short excerpt | Date | Speaker | Provider | Parent/child session | Exact locator | Surrounding context | Redaction | Evidence class | Authorization and manuscript use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q01 | ASC original goal | “continue to work in loops and iterations until you solve the challenge” | 2026-06-13 | Ahmed | Claude Code | parent `d02227a2-1ed0-471c-abb2-994217974264`; no child | `claude:AgentSecurityComp/d02227a2-1ed0-471c-abb2-994217974264.jsonl#L8`, message `27c64ae4-8719-4127-ac37-7d59fbea14a4`, 09:30:27Z | The opening goal asked for iterative competition work; it did not authorize unreviewed shared-state changes. | None | Human instruction | authorized; scope and persistence framing |
| Q02 | ASC confident claim | “Both models are stuck at gpt-oss's ~465 boundary → ~44 ceiling.” | 2026-07-01 | Claude Code assistant | Claude Code | parent `d02227a2-1ed0-471c-abb2-994217974264`; no child | `claude:AgentSecurityComp/d02227a2-1ed0-471c-abb2-994217974264.jsonl#L5294`, message `a574e226-e272-4d2e-98a2-b1f9e517fdb9`, 06:53:23Z | Presented as definitively established before later experiments weakened the ceiling claim. | None | Agent process claim, not measured fact | authorized; overconfidence example |
| Q03 | ASC human challenge | “test the approach locally as much as possible to verify it thoroughly” | 2026-06-30 | Ahmed | Claude Code | parent `d02227a2-1ed0-471c-abb2-994217974264`; no child | `claude:AgentSecurityComp/d02227a2-1ed0-471c-abb2-994217974264.jsonl#L5055`, message `040e05e3-bc81-4bea-ba43-8939e30a66a6`, 11:37:50Z | Ahmed withheld a decision pending deeper local verification. | None | Human governance instruction | authorized; oversight example |
| Q04 | ASC retraction | “my ‘boundary ~570’ was wrong” | 2026-06-30 | Claude Code assistant | Claude Code | parent `d02227a2-1ed0-471c-abb2-994217974264`; no child | `claude:AgentSecurityComp/d02227a2-1ed0-471c-abb2-994217974264.jsonl#L4988`, message `16af8f5a-e874-4197-901c-dab74be702fe`, 05:39:16Z | The assistant corrected a prior threshold after exact-model behavior contradicted it. | None | Agent self-correction | authorized; retraction example |
| Q05 | ASC memory-blind audit | “do not trust the memnory or recorded info, validate everything” | 2026-08-09 | Ahmed | OpenCode/DeepSeek | parent `ses_019da7b0effeSVV74ieACHE15I`; no child | message `msg_fe6258538001IR3J7Nyc6r9Ul5`, part `prt_fe6258539001I0glvysE6QnNH1`, 10:50:46Z | The parent prompt required primary revalidation and skepticism; original spelling retained. | None | Human governance instruction | authorized; audit-method example |
| Q06 | ARC invalid experiment | “The LoRA never served. The generation ran on base” | 2026-07-11 | Claude Code assistant | Claude Code | parent `573f46bd-f297-4c15-8028-9676d148ba1b`; no child | `claude:ARC-AGI-3/573f46bd-f297-4c15-8028-9676d148ba1b.jsonl#L6784`, message `cd994208-74ea-4adc-a259-36aed85360be`, 19:37:00Z | A serving audit invalidated the earlier fine-tune comparison. | None | Agent self-correction corroborated by repository evidence | authorized; invalid-experiment example |
| Q07 | ARC evidence gate | “Serving identity proven first.” | 2026-08-10 | Claude Code assistant | Claude Code | parent `32add479-d332-44f0-ae03-8ed849c86377`; no child | `claude:ARC-AGI-3/32add479-d332-44f0-ae03-8ed849c86377.jsonl#L1673`, message `753f259a-c79e-48e1-a438-5412cb982430`, 18:38:57Z | A later adapter A/B used deterministic controls before interpreting outcomes. | None | Agent process statement corroborated by test artifacts | authorized; evidence-gate example |
| Q08 | Cross-case value assessment | “They enabled me a non domain expert to actually participate and contribute” | 2026-08-16 | Ahmed | Codex author interview | interview root `01a0091e-6c06-72e0-ba1c-e5499447d566`; no child | `codex:2026/08/16/rollout-2026-08-16T08-49-43-01a0091e-6c06-72e0-ba1c-e5499447d566.jsonl#L569`, retained message `msg_01a00956-c14a-7bd0-96d8-dad7d140e42a` | Ahmed described perceived participation value while also reporting that neither winning objective had been achieved. | None | Retrospective testimony | authorized; value assessment only, not productivity measurement |
| Q09 | Cross-case originality assessment | “the contributions are mostly built on top of other people’s work” | 2026-08-16 | Ahmed | Codex author interview | interview root `01a0091e-6c06-72e0-ba1c-e5499447d566`; no child | `codex:2026/08/16/rollout-2026-08-16T08-49-43-01a0091e-6c06-72e0-ba1c-e5499447d566.jsonl#L569`, retained message `msg_01a00956-c14a-7bd0-96d8-dad7d140e42a` | The same answer qualified originality and did not identify an unexpected autonomous discovery. | None | Retrospective testimony | authorized; originality limitation only |

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
| Coded episodes | 14 AgentSecurityComp + 12 ARC-AGI-3 + 5 OpenCode primary investigations = 31 | Episode boundaries, not provider turns or independent discoveries |
| Episode origins | `human`: 0; `agent`: 14; `external`: 3; `mixed`: 14 | Origin is apparent provenance under the conservative coding rule, not a measure of autonomy |
| Episode final statuses | `confirmed`: 5; `partially supported`: 11; `refuted`: 5; `invalid experiment`: 6; `superseded`: 1; `open`: 3 | Status applies only to the bounded claim in its row |
| Human oversight | 2-5 hours/day | Retrospective testimony, approximate |
| Direct spend | About USD 100 OpenRouter and USD 30 Modal, plus Colab Pro and Claude/Codex subscriptions | Retrospective testimony, approximate and not a complete cost accounting |

The origin count uses exact row IDs: `human` none; `agent` AS-S02, AS-S05,
AS-S07, AS-S08, AS-S10, AS-S12, AS-S13, AS-S14, ARC-S02, ARC-S03, ARC-S04,
ARC-S07, ARC-S08, ARC-S09; `external` AS-S03, AS-S04, AS-S09; `mixed` AS-S01,
AS-S06, AS-S11, ARC-S01, ARC-S05, ARC-S06, ARC-S10, ARC-S11, ARC-S12, OC-S01,
OC-S02, OC-S03, OC-S04, OC-S05.

The status count uses exact row IDs: `confirmed` AS-S01, AS-S03, AS-S04,
ARC-S06, ARC-S07; `partially supported` AS-S02, AS-S05, AS-S09, AS-S10,
AS-S12, ARC-S01, ARC-S02, ARC-S10, ARC-S11, OC-S01, OC-S05; `refuted` AS-S06,
AS-S11, AS-S13, ARC-S08, ARC-S09; `invalid experiment` AS-S07, AS-S08,
ARC-S03, ARC-S05, OC-S03, OC-S04; `superseded` ARC-S04; `open` AS-S14,
ARC-S12, OC-S02. These lists contain all 31 source IDs exactly once in each
derivation.

Project duration, active days, commit counts, submission trajectories, and
productivity multipliers remain omitted. No productivity multiplier is
inferable without a human-only control.

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
- The coded episodes and selected quotes have passed the stated source-level
  checks, but the literature claim matrix remains empty and retrospective
  testimony remains uncorroborated unless a row says otherwise.
- Both competition outcomes remain open, and neither winning objective has been
  achieved at the cutoff.
