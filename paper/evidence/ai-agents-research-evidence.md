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
- The author has authorized short quotations from the local agent transcripts
  for this paper. Admission still requires an `authorized` status in the private
  quote trace; withheld or revoked material must not appear in the manuscript.
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

| Case store | All JSONL files | Substantive top-level chunks | Top-level tool derivatives | Direct subagents | Workflow subagents | Workflow journals | Canonical conversation groups |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AgentSecurityComp | 327 | 10 | 1 | 52 | 249 | 15 | 5 |
| ARC-AGI-3 | 942 | 13 | 103 | 185 | 627 | 14 | 5 |
| Total | 1,269 | 23 | 104 | 237 | 876 | 29 | 10 |

The 103 ARC-AGI-3 top-level derivatives comprise 99 `sdk-cli` records and four
bridge or initialization stubs. The AgentSecurityComp derivative is a bridge
stub. No scratchpad-copy path was found. All 104 derivatives are excluded from
conversation counts.

The canonical mapping below lists every substantive chunk and any linked
top-level stub. The complete map also assigns all 1,142 child and journal files
to their top-level parent and canonical group.

| Case | Canonical conversation ID | Linked top-level record IDs |
| --- | --- | --- |
| AgentSecurityComp | `d02227a2-1ed0-471c-abb2-994217974264` | `d02227a2-1ed0-471c-abb2-994217974264`, `d368bb45-0b14-4073-9740-774ade58e769`, bridge stub `ce940de4-1381-4ae1-a0bf-1d6a0005f13f` |
| AgentSecurityComp | `f1ef3669-1d5f-4caf-ab9b-c4eedf643569` | `f1ef3669-1d5f-4caf-ab9b-c4eedf643569`, `25c84940-5ede-4850-a639-5579fdef6ebe` |
| AgentSecurityComp | `a809e3ce-6bd5-4997-914a-1100fe705967` | `a809e3ce-6bd5-4997-914a-1100fe705967`, `84f715ee-9b96-4ee0-9950-48acf7a82447`, `9f138e71-bfaa-49fa-93aa-e6cf5f592493` |
| AgentSecurityComp | `42258c4d-4471-458b-a3c0-757cf6791024` | `42258c4d-4471-458b-a3c0-757cf6791024` |
| AgentSecurityComp | `0385f350-248c-431f-a9f2-1604c96b5ce2` | `0385f350-248c-431f-a9f2-1604c96b5ce2`, `9d0f25c3-7d3c-4eaf-a219-001b44ea5ec4` |
| ARC-AGI-3 | `573f46bd-f297-4c15-8028-9676d148ba1b` | `573f46bd-f297-4c15-8028-9676d148ba1b`, `c9ecf8fc-b749-4067-9622-38b0060db14f`, `5174edda-9963-4cdd-9306-18d2695d0fd0`, `38ec9bae-690c-4713-aa14-c3245497ca9e`, `0ba5f0b9-392e-404c-824f-ade3803cc524`, `0e3cf55e-6aa2-408c-bf63-8dfa02fe7d9a`, bridge stubs `28a15468-c114-4b85-9aac-74810ea52076` and `92fbe257-daaf-4f72-a7c7-de4a2c44ea2e` |
| ARC-AGI-3 | `626c7722-330b-4125-b1de-439d21bef0a0` | `626c7722-330b-4125-b1de-439d21bef0a0`, `066c8134-787a-41a1-8dcb-dd4815d4a1d1`, `d093e020-dbb1-4965-958c-471bfea0138e` |
| ARC-AGI-3 | `32add479-d332-44f0-ae03-8ed849c86377` | `32add479-d332-44f0-ae03-8ed849c86377`, `ff31ed86-9a67-4b4a-9261-458a5f2e9819` |
| ARC-AGI-3 | `2c317a12-f48d-4a3f-8ddc-8b48615ad490` | `2c317a12-f48d-4a3f-8ddc-8b48615ad490`, initialization stub `852362d3-8371-4164-a10a-be12b9571208` |
| ARC-AGI-3 | `de216582-726c-415f-9dd5-71c05fb4d2c3` | `de216582-726c-415f-9dd5-71c05fb4d2c3` |

ARC-AGI-3 record `0f234577-1d7a-4a1a-841e-1398fbf6b99c` is an unlinked
bridge/initialization stub and is excluded. A privacy-preserving overlap audit
of the 23 substantive chunks found zero shared message-UUID pairs, zero repeated
prompt-and-timestamp pairs, zero identical three-prompt prefixes, and zero
identical contiguous three-prompt runs. Prompt text was normalized and hashed in
memory; neither text nor hashes are written to the map. These checks address
regenerated identifiers and copied prefixes without publishing transcript
content.

The substantive Claude record windows are 2026-06-13T09:28:39.036Z through
2026-08-15T14:51:09.743Z for AgentSecurityComp and
2026-06-28T16:54:33.186Z through 2026-08-15T21:28:03.657Z for ARC-AGI-3.
The reported quantity is 10 metadata- and overlap-deduplicated canonical
conversation groups, not 127 top-level files.

### Codex inventory

The refreshed content search found 69 rollout files at fix-round audit time.
First metadata records classify them as follows:

| Classification | Root rollouts | Child rollouts | Count treatment |
| --- | ---: | ---: | --- |
| AgentSecurityComp working directory | 11 | 21 | Case candidates |
| ARC-AGI-3 working directory | 5 | 23 | Case candidates |
| Other working directory with a text match | 5 | 4 | Excluded as incidental |

One AgentSecurityComp root and ten of its children belong to the current
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
conversation. Every one of the 69 rows, including all inclusions and exclusions,
is mapped in the companion source map. Its `canonical_conversation_id` applies
the explicit `session_id` / ultimate-parent / own-ID rule above; the 15 retained
roots have 15 distinct canonical identifiers.

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

### Reproducible source map

The auditable row-level map is
`paper/evidence/ai-agents-research-source-map.tsv`; its derivation utility is
`paper/evidence/build_ai_agents_source_map.py`. The map contains 1,356 data rows
and these columns: provider, case, record ID, record class, privacy-preserving
source locator, canonical parent ID, canonical conversation ID, disposition,
and reason. It includes all 1,269 Claude JSONL files, all 69 Codex search hits,
all 15 matching OpenCode sessions, both repository revisions, and the approved
testimony source.

Source locators resolve against these private read-only bases:

- `claude:AgentSecurityComp/` resolves under
  `/Users/ahmed/.claude/projects/-Users-ahmed-Documents-AgentSecurityComp/`;
- `claude:ARC-AGI-3/` resolves under
  `/Users/ahmed/.claude/projects/-Users-ahmed-Documents-ArcAGI3/`;
- `codex:` resolves under `/Users/ahmed/.codex/sessions/`;
- `opencode:session/` resolves to the `session.id` row in
  `/Users/ahmed/.local/share/opencode/opencode.db`; and
- `git:`, `brief:` locators resolve to the pinned repositories and approved
  task brief already identified in this ledger.

Rebuild the map with `python3 paper/evidence/build_ai_agents_source_map.py`.
The utility reads only Claude/Codex metadata plus normalized prompt hashes and
non-sensitive OpenCode session columns. It never writes transcript content or
prompt hashes to the manifest.

### Deduplicated source summary

| Source | Independent conversation unit retained | Derivative records retained for traceability | Primary use |
| --- | ---: | ---: | --- |
| Claude Code | 10 canonical conversation groups | 13 continuation chunks and 1,246 trace-only records | Primary transcript evidence across both cases |
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
be admitted only after a source-level context check, privacy review, and an
`authorized` status under the author's project-level permission for short local
transcript quotations. Its private trace must record case, provider, parent
session, child session when applicable, timestamp, speaker, exact source
location, topic, surrounding context, redaction note, evidence class,
authorization status, and manuscript use. Withheld or revoked authorization
blocks admission. Quotes may not be used as substitutes for code, live
evaluation, or literature evidence.

## Descriptive measures and derivations

| Measure | Derivation at this cutoff | Interpretation limit |
| --- | --- | --- |
| Claude canonical conversation groups | 5 AgentSecurityComp + 5 ARC-AGI-3 = 10 | Metadata- and overlap-deduplicated groups, not hypotheses or achievements |
| Claude raw record map | 23 substantive chunks + 104 top-level tool derivatives + 1,113 subagents + 29 journals = 1,269 | Every record has a source locator and disposition in the TSV map |
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
- Claude classification and canonical groups are reproducible from entrypoint,
  prompt-source, legacy-session, bridge, and path metadata. The hashed overlap
  audit detects exact copied prompt runs of three or more, but paraphrased or
  shorter overlap remains possible; the value 10 therefore describes canonical
  conversation groups under this stated rule, not independent intellectual work.
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
