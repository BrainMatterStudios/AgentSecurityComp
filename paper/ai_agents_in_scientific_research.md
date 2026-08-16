# Access Without Autonomy: An Instrumented Case Study of AI Agents in Computational Research

## Abstract

Large-language-model agents can search literature, inspect repositories, write
and run code, and maintain long computational workflows, but those capabilities
do not establish scientific autonomy, originality, or reliability. This living,
comparative single-participant (N-of-1) case study examines one experienced
technologist's use of AI
coding agents while entering two unfamiliar competition-based research domains:
AgentSecurityComp as the primary case and ARC-AGI-3 as a comparative case. The
review combines metadata-deduplicated private agent histories, pinned repository
revisions, experiment and result artifacts, independently retrieved
AgentSecurity submission rows, and bounded retrospective testimony. The unit of
analysis is a research episode rather than a provider turn. Thirty-one episodes
were coded for proposition origin, prior evidence, confidence, human
intervention, local and external outcomes, final claim status, and lesson.

The agents provided substantial execution: they inspected software contracts,
implemented public and agent-proposed mechanisms, built harnesses and controls,
repaired parsers and model-serving paths, and preserved negative results. The
record was weaker for dependable hypothesis selection, causal identification,
calibrated interpretation, and independent originality. Four bounded claims
were confirmed, ten partially supported, seven refuted, five were invalid
experiments, one was superseded, and four remained open; these heterogeneous
labels are not an agent accuracy rate. Recurrent failures included broken or
overlapping controls, unproved deployment identity, stale memory, wrong-source
research, and promotion of local gains beyond their evidentiary boundary.
Human review—estimated retrospectively at 2–5 hours per day—was therefore part
of the research system rather than an occasional safeguard.

The resulting governance protocol requires direct-source verification,
falsifiable hypothesis cards, mechanically matched controls, separate local and
external gates, untrusted-memory review, human approval for scarce evaluations,
and append-only outcome records. The cases support a bounded conclusion: agents
lowered the perceived barrier to participating in computational research and
executed useful research work, but did not demonstrate dependable scientific
autonomy. No human-only control exists; provider use, budgets, models, and case
conditions were unequal and changing; external evaluators were partly hidden;
and both winning objectives remained unachieved according to testimony at the
cutoff.

## 1. From Enterprise Architecture to Computational Research

I came to these projects with more than 16 years of consulting experience in
real-time decisioning and omnichannel AI, including Naive Bayes and gradient-
boosting systems; enterprise and solution architecture across cloud and
on-premises environments; more recent agentic-AI work; and early-career Java
development.
That background gave me transferable skills in systems design, integration,
and structured problem solving. It did not make me an expert in agent security,
ARC-AGI-3, scientific research practice, or Kaggle competition mechanics. My
independent coding practice was rusty, and my Python experience had been mainly
AI-assisted rather than the construction of greenfield research systems on my
own. This is therefore neither a novice-versus-expert comparison nor a claim
that general technical experience is equivalent to competition-domain
expertise. It is the account of an experienced technologist entering two
unfamiliar computational-research domains with both relevant strengths and
material gaps.

The original experiment was deliberately ambitious. I wanted to see how far an
agent-led process could go when I supplied little domain guidance rather than
feeding the system hypotheses. In the first case, I instructed the agent to
“continue to work in loops and iterations until you solve the challenge.” That
authorized persistent investigation, not unreviewed changes to shared systems
or independent submission decisions. My intended role was to approve, challenge,
ask for breadth and depth, and decide whether an experiment was ready to move
from local work to a scarce live evaluation.

In practice, this was not hands-off autonomy. I estimate retrospectively that I
spent 2-5 hours per day reviewing claims, asking for stronger tests, redirecting
work, and deciding what could proceed. That estimate is testimony, not a
time-tracking result. I also judge that the agents enabled me to participate
meaningfully and learn context in domains I would otherwise have found difficult
to enter. That is a report of perceived access and value, not a measured claim
about time saved or productivity gained. No human-only control exists, and
neither project had achieved its winning objective at the cutoff.

These distinctions motivate the title of this paper. Access means being able to
turn questions into executable research work: reading an unfamiliar codebase,
implementing a candidate mechanism, running checks, preserving results, and
revising the next test. Autonomy would require something stronger: dependable
selection of worthwhile questions, valid experiment design, calibrated
interpretation, original contribution, and correction without relying on a
human to notice the error. The cases ask whether contemporary agents provided
the first set of capabilities, the second, or an unstable mixture of both.

## 2. What Counts as an AI Research Agent?

The word *agent* covers systems with very different scopes. A conversational
assistant answers a bounded prompt. A tool-using LLM agent can pursue a
multi-step objective by reading files, searching a corpus, editing and running
code, inspecting results, and revising a plan. A closed-loop scientific system
goes further by connecting hypothesis selection to physical or computational
experimentation, observation, and the choice of a next experiment. I use *AI
research agent* operationally for the middle category in this study: an
LLM-based system given enough tools and persistence to execute substantial parts
of a computational research workflow. I do not use the label as evidence that
the system is an autonomous scientist.

### 2.1 Bounded robot scientists and autonomous laboratories

Closed-loop automation in science predates current LLM agents. In a
peer-reviewed 2004 *Nature* article, King and colleagues described a robot
scientist that generated, selected, and tested gene-function hypotheses within
a yeast metabolic model [1]. Its loop was experimentally real but tightly
bounded by deletion mutants, growth assays, and a hand-built logical model. A
peer-reviewed 2020 *Nature* study reported a mobile robotic chemist that
executed 688 experiments over eight days in a predefined ten-variable search
[2]. Human researchers still conceived the study and fixed its hypotheses,
objective, apparatus, and search space. A peer-reviewed 2023 *Nature* article
described an autonomous materials laboratory that combined literature-trained
models, computation, robotics, and active learning, realizing 36 of 57 selected
targets over 17 days [3]. Humans selected the target class and allowable
precursors, while inconclusive measurements and manual follow-up exposed
boundaries outside the active-learning policy.

These systems demonstrate substantial autonomy *inside an engineered
experimental envelope*. They do not establish general scientific autonomy.
Their constraints are also different from those of a coding agent operating in
a repository: the laboratory systems tightly couple specified objectives,
instruments, and feedback, whereas an LLM agent may move fluidly among
literature, code, conjecture, and prose while lacking a reliable mechanism for
deciding whether the resulting chain is scientifically valid.

### 2.2 LLM agents across the research workflow

The current literature spans ideation, synthesis, coding, reproduction, review,
and paper generation, but its publication status and task boundaries matter. A
peer-reviewed perspective by Park and colleagues offered GPT-4 materials-science
hypotheses while also reporting a high error rate and the need for expert
evaluation [4]. This was a demonstration, not a controlled validation of
successful discovery. A peer-reviewed ICLR 2025 paper introduced
ScienceAgentBench, which converts 102 tasks from 44 papers into verifiable
scientific-programming problems; its reported baselines solved only a minority
even with repeated attempts and optional expert knowledge [5]. These are
self-contained workflow tasks, not open-ended research programs. A
peer-reviewed 2026 *Nature* article on Co-Scientist reported biomedical
hypotheses with preliminary in-vitro validation, but experts remained in the
loop and the evidence was concentrated in biomedicine [6].

Several broader claims come from preprints rather than peer-reviewed articles.
The Data-to-paper preprint linked annotated data, code, results, and prose and
could produce simple manuscripts in an autopilot mode, yet its authors reported
limited novelty, material errors, and increasing need for human co-piloting as
complexity rose [7]. The AI Scientist preprint demonstrated an end-to-end
pipeline for ideation, small machine-learning experiments, writing, and
simulated review from supplied seed code and templates; the same paper reported
implementation failures, weak experimental rigor, misleading conclusions, and
occasional hallucinated results [8]. Paper production is consequently not the
same thing as dependable discovery.

Benchmark and human-study evidence reinforces that separation. DiscoveryBench,
a preprint on data-driven discovery, reported a steep performance loss as
workflow and domain complexity increased; its best evaluated system reached 25%
on the authors' metric, within a benchmark that excluded several difficult
workflow classes [9]. CORE-Bench, a preprint on computational reproducibility,
reported that the best evaluated agent reached 21% accuracy on its hardest task
level, even though reproduction from an existing repository and data is
narrower than new research [10]. The official PaperBench release, accompanied
by a preprint, reported that the best tested agent completed an average of 21%
of rubric-weighted requirements across 20 machine-learning replication tasks.
In its direct comparison on a three-paper subset, the compared agent did not
exceed the recruited ML-PhD baseline [11]. A separate preprint found
that expert reviewers rated
LLM-generated NLP ideas as more novel on average but slightly less feasible
than human ideas; the ideas were not executed, their novelty judgments were
subjective, and the system's self-ranking was unreliable [12]. Another preprint
reported strong performance for a literature agent on defined retrieval and
synthesis tasks while noting context-dependent contradiction labels and
overconfidence [13]. A multi-agent review preprint found gains over tested
single-agent baselines. Its automated alignment produced the highest recall but
lower precision and Jaccard than the human-review alignment baseline, while its
separate nine-participant user study still found more good and specific comments;
the two metrics answer different questions and both require accountable judgment
[14].

Even apparently routine research mechanics require verification. A
peer-reviewed *Scientific Reports* study of 84 generated literature reviews
found fabricated citations and errors in real citations from the April 2023
ChatGPT snapshots it tested [15]. Those rates should not be generalized to
current systems, but the methodological lesson remains bounded and important:
a citation-shaped string is not provenance.

Taken together, this literature supports a capability map rather than a single
autonomy score. Agents can perform useful pieces of research and sometimes
connect many pieces into a long workflow. Performance can still degrade with
task complexity, hidden evaluation, invalid experimental controls, unreliable
self-assessment, and weak source provenance. This paper therefore evaluates the
agents as research executors whose outputs must earn trust episode by episode.
It does not infer autonomy from fluency, tool use, conversation volume, token
usage, or a completed manuscript.

## 3. Research Questions and Method

### 3.1 Research questions

The study asks five questions:

1. How much can AI agents lower the entry barrier for an experienced
   technologist entering unfamiliar computational-research domains?
2. Which research tasks do the agents perform effectively?
3. How much scientific direction and originality emerges without
   domain-specific human guidance?
4. Where do agents fail, particularly through confident error, incomplete due
   diligence, stale memory, external imitation, and local-to-live transfer?
5. Which human governance practices improve reliability and research value?

### 3.2 Comparative N-of-1 design and case boundaries

This is a longitudinal, comparative N-of-1 study of one human researcher using
several AI coding agents. AgentSecurityComp is the primary case and ARC-AGI-3
is the comparative case. The comparison is analytical rather than controlled:
the cases expose recurring research activities and failure modes in different
technical settings, but they were not randomly selected or run under matched
conditions. OpenCode/DeepSeek supplies limited supplementary evidence and is not
a balanced third case or provider-comparison arm.

The reviewed corpus combines Claude Code, Codex, and OpenCode/DeepSeek session
records associated with the two repositories; Git history and pinned repository
artifacts; experiment scripts, logs, and result records; and an approved set of
author interview responses. The literature background uses only primary papers,
official publication records, and official editorial-policy pages already
checked in the evidence ledger. Repository and transcript evidence establishes
project events. General literature and policy contextualize those events but do
not prove what happened in either project. The portable
[companion evidence ledger](evidence/ai-agents-research-evidence.md) is the
source-ID register for every coded episode and admitted quotation. Raw private
histories remain controlled source material and are not required to resolve the
public repository, commit, live-row, and symbolic transcript locators recorded
there.

According to retrospective author testimony, Claude Code was the primary
research system, while Codex and OpenCode/DeepSeek were introduced mainly as
perspective resets when the primary line of work appeared stuck, repetitive, or
prematurely settled. Tasks, dates, models, budgets, and exposure differed.
Session or token totals therefore describe use, not independent intellectual
contribution, research quality, or provider superiority. (Testimony: author
baseline and interview)

### 3.3 Research episode and coding scheme

The unit of analysis is a bounded research episode, not an individual message,
agent turn, subagent, commit, or submission. An episode follows one proposition
far enough to connect, where the record allows: the question or hypothesis; its
apparent human, agent, external, or mixed origin; evidence cited before the
test; the proposed implementation or experiment; human review; local outcome;
live or external outcome; final claim status; timing of correction; and the
durable methodological lesson. Cross-provider continuation of the same inquiry
remains one episode.

The reviewed ledger contains 31 such episodes: 14 in AgentSecurityComp, 12 in
ARC-AGI-3, and five supplementary OpenCode investigations. Origins are coded
conservatively as `human`, `agent`, `external`, or `mixed`. A provider's proposal
is not coded as autonomous discovery when human or external input materially
shaped the same episode. Final status is `confirmed`, `partially supported`,
`refuted`, `invalid experiment`, `superseded`, or `open`, and applies only to the
bounded proposition in that row. Local and live outcomes remain separate so
that a valid implementation is not mistaken for an externally transferred
effect.

Qualitative codes cover hypothesis origin, external-method dependence,
implementation and infrastructure value, novel recombination, experimental
validity, confidence and calibration, correction, stale-memory propagation,
human challenge and approval, provider switching, local-to-live transfer,
operational failure, domain learning, and achieved or unachieved goals. Coding
is interpretive and was not independently blinded or replicated. Counts are
descriptive of this reviewed corpus, not estimates of population frequency.

### 3.4 Provenance and deduplication boundaries

The default session-counting unit is a provider's top-level conversation.
Subagents, specialists, workflow journals, scratchpad copies, bridge records,
and tool-result derivatives are linked to their parent or retained only for
traceability; they are not counted again as independent conversations. Imported,
forked, parent-child, and overlapping histories are not summed. Provider
metadata, working directory, timestamps, canonical identifiers, and content
overlap determine the most conservative retained lineage. A content match is
assigned to a case only when metadata places the work in that repository or a
repository-specific worktree. The current paper-design and provenance-audit
Codex lineage is excluded from historical case-activity counts.

These rules prevent conversation volume from masquerading as research output,
but they do not prove intellectual independence. Paraphrased overlap and short
copied fragments can escape exact-content checks, while mutable agent stores can
produce different inventories at a later extraction. Episode-level
deduplication therefore takes precedence over provider-level totals whenever
several agents, imported histories, or repeated prompts concern the same
research question.

### 3.5 Evidence classes, quotation, and claim control

Substantive claims are internally classified as source fact, local measurement,
live observation, triangulated finding, inference, retrospective testimony, or
open hypothesis. The prose does not attach a tag to every sentence, but it
preserves the distinctions. An executable local result cannot by itself
establish live efficacy. A transcript claim cannot replace code or evaluator
evidence. Author estimates about oversight, value, trust, cost, and
counterfactual effort remain testimony unless independently corroborated.

Private agent histories are source material, not a publication appendix. Only
short excerpts relevant to hypothesis formation, confidence, correction,
intervention, or governance may be quoted. Each admitted quotation must have an
`authorized` status in the private trace and retain provider, case, session,
timestamp, speaker, exact location, context, and redaction information. Secrets,
credentials, unrelated personal material, and misleadingly truncated passages
are excluded. The quote identifiers are thematic rather than chronological:
Q04, dated 2026-06-30, precedes Q02, dated 2026-07-01, so Q04 must not be
presented as a retraction of Q02. They concern different ceiling claims.

AI-generated claims, summaries, citations, and interpretations require an
independent source check before manuscript use. Current ICMJE editorial
recommendations and Springer Nature publisher guidance both treat AI tools as
ineligible for authorship and retain human accountability, but those are
general, mutable policies rather than evidence about this project's actual
authorship or tool use [16,17]. Ahmed Mobasher's status as sole author and the
specific roles of Claude Code, Codex, and OpenCode/DeepSeek are project facts
declared below. The target publication's live rules will control at submission.

### 3.6 Limitations and living evidence policy

The design cannot support a causal productivity estimate. It has no human-only
control, no randomized task allocation, no common provider task set, no equal
budget, and no stable model-version comparison. Agent platforms, model versions,
research infrastructure, and competition conditions changed during the study.
Providers were used at different times for different purposes. The cases were
selected because I conducted them, and the episode ledger is a reviewed sample
of those projects rather than an independent census of AI-assisted science.

Competition scores are operational outcomes, not direct measures of scientific
originality, understanding, or research quality. They may also be noisy because
of hidden evaluators, run variance, lifecycle constraints, platform changes,
and imperfect local replicas. Local improvements, submission scores, commits,
active days, token counts, and conversation counts must not be converted into a
productivity multiplier. The unequal cases and uses also preclude a defensible
claim that one provider was better than another.

My baseline, daily oversight estimate, perceived value, trust judgments, and
the statement that neither winning objective had been achieved are retrospective
testimony. They are useful for understanding the case but are not direct
measurements. The same limitation applies to counterfactual judgments about how
long the work might have taken without AI. The sole-author perspective also
creates selection and interpretation bias, and the coding has no independent
inter-rater reliability measure.

This is a living manuscript. The repository evidence cutoff for this inventory
is 2026-08-16T10:29:29+03:00; mutable Claude, Codex, and OpenCode stores were
extracted at 2026-08-16T08:06:05Z under the filters recorded in the private
ledger. The pinned revisions bound repository claims but do not imply that every
historical transcript refers to the same revision. Completed, pending,
superseded, failed, and unresolved experiments remain distinct in later
revisions. New competition results will receive a new dated cutoff and will not
silently overwrite negative or unresolved outcomes. Final rankings, costs, and
retrospective conclusions will be added only after the competitions conclude
and the supporting records are checked.

## 4. Case I: AI Agent Security

**Outcome-evidence note.** The independently retrieved AgentSecurity
live-results artifact is frozen at 2026-08-16T10:56:15Z. Selected rows were
separately rechecked at 2026-08-16T11:10:21Z and again at
2026-08-16T11:26:07Z; a further status-only recheck was made at
2026-08-16T11:59:48Z and another at 2026-08-16T12:44:16Z. None replaces the frozen table. The 11:26 recheck also
resolved the early `ERROR` rows discussed below; the 11:59 recheck found L31 ref
55538848 `COMPLETE` at 73.605 while three chain-pack refs remained pending; the
12:44 recheck found all four complete at 79.985, 79.365, 73.605, and 54.375. All live
observations are later than both the AI-case repository cutoff of
2026-08-16T10:29:29+03:00 (07:29:29Z) and the mutable-history snapshot at
2026-08-16T08:06:05Z. (AgentSecurity live-results ledger:
`paper/evidence/working-note-claim-ledger.md`; AI evidence cutoff table)

### 4.1 Entering the executable problem

The AgentSecurityComp case began on 2026-06-13 with an intentionally broad
instruction to keep iterating toward the competition objective. The agent first
worked against a mock scaffold, then inspected the actual software development
kit (SDK) and ported the attack to its real `AttackCandidate` interface. It also
increased the number of candidate attacks after reading the scorer as additive:
more valid candidates could add more scored findings. The real path ran and
became the basis of later submissions, while candidate volume established a
baseline rather than solving the challenge. These were useful acts of repository
inspection and implementation, not evidence that the system had independently
chosen a scientifically important direction; the human retained verification
and submission approval. (Episode AS-S01; Episode AS-S02; Quote Q01)

The executable contract changed the research problem again on 2026-06-27.
Fabricated secret-like strings had stopped scoring because SDK 3.1.2 required a
literal `SECRET_MARKER` or a value actually read from the protected file. The
agent incorporated the documented marker, validated marker-bearing exfiltration
locally, and restored scoring on the corrected path. The episode shows why
infrastructure work can be research-enabling: a plausible attack was worthless
until it obeyed the evaluator's protocol. The repair depended on external SDK
semantics and zero-score evidence, however, so its apparent agent execution
should not be recast as original discovery. (Episode AS-S03)

Two early statements illustrate both correction and unstable confidence. On
2026-06-30 the agent wrote the correction “my ‘boundary ~570’ was wrong” after
exact-model behavior contradicted an earlier threshold; later that day the
human withheld a decision and asked it to “test the approach locally as much as
possible to verify it thoroughly”. On 2026-07-01 the agent made a different,
new ceiling claim: “Both models are stuck at gpt-oss's ~465 boundary → ~44
ceiling.” The June 30 correction therefore precedes and does not retract the
July 1 claim. Later experiments weakened the certainty of that second claim as
well. (Quote Q04; Quote Q03; Quote Q02; Episode AS-S10)

### 4.2 Practical value through adaptive sizing

The clearest value vignette arrived on 2026-07-25, but it was not an autonomous
invention. Higher-scoring public solutions were reported to size their output
from the time observed in the live environment. The agent reproduced that
mechanism in bounded form: it measured how long accepted candidates took,
estimated how many could be replayed within the evaluator's time budget, and
stopped before the entire submission risked timing out. Local replay-safety
checks passed. A separate Task 8 API recheck found that all five L6 rows had
status `ERROR`: the adaptive arm showed a visible score of 80.145 against a
64.800 control, but an `ERROR` row does not establish a completed live effect.
The contribution was faithful translation of a public method into this
repository and a locally verified implementation; its external efficacy remains
unestablished. It was valuable engineering and experimental execution, not
evidence of independent originality. (Episode AS-S04; Source AS-S04)

Subsequent throughput work showed why a local mechanism and a live benefit must
remain separate claims. On 2026-07-26, stopping decoding after the tool call
closed reduced a local timing from 1.23 seconds to 1.03 seconds. The two matched
L7 rows showed a visible difference of 1.440 points, but both had status
`ERROR`, so they do not establish a completed live effect. On 2026-07-27,
packing several messages into one model call again looked favorable in a local
timing model. No live description matched the planned L8 ladder; the later L9
packing rows were all `ERROR`. Their visible scores were lower than the listed
single-post row, but those rows cannot complete the external adjudication.
Local measurements established that the code ran and changed measured
overhead; whether either mechanism improved a completed competition run remained
open. (Episode AS-S05; Episode AS-S06)

### 4.3 Failure through non-identifying experiments

An August sequence exposed a more serious problem than ordinary negative
results: some tests could not identify the proposed cause. On 2026-08-04 the
agent initially explained Gemma's poor result as model weakness, but the
comparison used an under-powered message frame. The same weak frame made GPT
score zero; only a faithful commitment-forge frame later separated the models.
Because the control was broken, the original comparison was an invalid
experiment, not evidence that the model hypothesis was refuted or confirmed.
(Episode AS-S07)

The router vignette on 2026-08-08 made the same lesson visible at ladder scale.
The agent built deterministic board routing and workload splitting, and both
the router and its self-measurement worked locally. Live arms scored
42.665-47.865 against a 44.320 baseline, with no stable gain. More importantly,
the arms overlapped in what they changed, so their different scores could not
cleanly identify routing as the cause. A multi-arm experiment is not controlled
merely because it has several named variants; its arms must isolate different
mechanisms. The final status is therefore `invalid experiment`, not a successful
breakthrough or a clean negative result. (Episode AS-S08; Source AS-S08;
AgentSecurity live-results ledger, rows 55362610, 55362686, 55362749, 55362800,
and 55362843)

### 4.4 Public dependence, human gates, and the late ladders

On 2026-08-09 the agent reproduced the public dimong4/nctuan commitment-forge
method, which causes a reasoning model to commit to several tool posts within
one candidate. The project record says four posts per candidate fired as designed,
and the live result was 47.850 versus 43.600 for the single-post control.
Mixed-origin recombination then paired that externally derived mechanism with
dual-board routing and a Gemma variant: dual arms reached 81.985 and 82.660, while
the N=600 Gemma isolate was 34.000 versus 27.000 for Gemma single. The N=900
follow-up narrowed to 35.000 versus 34.605 (refs 55444087 and 55444093), and the
N=1200 forge was 35.375 (ref 55444097), so the initial isolate gain was not durable
or scalable in these observations. The episode partially supported bounded
component behavior but did not reach its stated reproduction target or explain
the remaining ceiling. Public method dependence, agent execution, and human
selection therefore all
remain visible in the attribution. (Episode AS-S09; Episode AS-S10;
AgentSecurity live-results ledger, rows 55391763, 55392055, 55418165, 55418171,
55418180, and 55418184)

Governance became increasingly explicit as confident explanations accumulated.
The human approved bounded ladders, demanded controls, and on 2026-08-09 asked a
fresh system to “do not trust the memnory or recorded info, validate everything”.
That memory-blind audit rechecked code and evidence but produced no completed
live adjudication by the cutoff. Its value was epistemic discipline, not a new
competition result: recorded conclusions became claims to revalidate rather
than premises to inherit. The fresh provider was a reset and diversity
mechanism under human direction, not independent corroboration of the primary
agent. (Episode OC-S02; Quote Q05)

The final dated ladders remained mixed or negative. On 2026-08-12, two proposed
throughput knobs collapsed to one effective axis before L27, the project label
for that controlled submission ladder. Its *probe-hop* arms enabled a one-hop
calibration probe before sizing the candidate set. The human insisted on both
tests and a control, and the live variants scored 50.295-57.620 against an
88.730 control. On 2026-08-13 the GPU path was made functional, but its best arm
scored 50.175 against an 83.115 historical CPU reproduction threshold. That
refuted the narrow threshold proposition, not a causal CPU-versus-GPU effect,
because no same-batch hardware control existed. L29 executed on 2026-08-15 and
scored 85.675, below the historical 88.730 L27 threshold. That likewise refuted
the stated threshold target without causally rejecting routing. At the frozen
cutoff, L31—the later named submission ladder—had
four pending *chain-pack* arms, which placed several multi-hop messages inside
one candidate. Only the companion *fast-emit* arm, a separately calibrated path
that generated fixed eight-hop candidates directly in memory, had run; it
scored 25.145. A later 11:59:48Z status-only recheck found one chain-pack arm,
ref 55538848, complete at 73.605 and three still pending; it had no matched
control. By 12:44:16Z, all four were complete at 79.985, 79.365, 73.605, and
54.375. They all remained below the historical 88.730 L27 threshold, but these
unmatched comparisons do not identify a causal chainpack effect. AgentSecurityComp's
winning objective remained unachieved as retrospective testimony. (Episode
AS-S11; Episode AS-S12; Episode AS-S13; Episode AS-S14; Testimony: living
outcomes register; AgentSecurity live-results ledger, rows 55444101, 55469249,
55469255, 55469264, 55469273, 55469280, 55525533, 55530790, 55538814,
55538829, 55538848, 55538855, and 55538875)

### 4.5 Case evidence summary

Table 1 separates what the agent executed from what the human governed and what
the work inherited from external systems. Its outcomes are bounded episode
claims rather than a provider scorecard. (Episodes AS-S01-AS-S14; Episodes
OC-S01-OC-S02)

| Phase | Agent contribution | Human contribution | External dependence | Outcome | Lesson |
| --- | --- | --- | --- | --- | --- |
| Entry and protocol repair, 2026-06-13 to 2026-06-27 | Inspected the SDK, ported the real candidate path, scaled output, and repaired marker handling. | Required real-path checks and retained submission approval. | SDK interfaces and 3.1.2 marker semantics defined validity. | Real-path execution and marker scoring confirmed; volume only partially supported. (Episodes AS-S01-AS-S03) | Verify the executable contract before optimizing it. |
| Adaptive sizing, 2026-07-25 | Implemented replay-safe sizing and local checks. | Approved a bounded ladder. | Mechanism was attributed to higher-scoring public solutions. | Local mechanics passed; all five identified L6 rows were `ERROR`, so the visible score difference does not establish a completed live effect. (Episode AS-S04; Source AS-S04) | Reproduction can be useful without completed external efficacy or originality. |
| Latency and packing, 2026-07-26 to 2026-07-27 | Measured early close and packed-call throughput. | Required controlled live ladders. | Hidden evaluator timing and replay behavior governed transfer. | Local mechanics ran, but every identified L7 and L9 row was `ERROR`; early-close and packing efficacy therefore remained unadjudicated. No live description matched L8. (Episodes AS-S05-AS-S06; Sources AS-S05-AS-S06) | A visible score on an `ERROR` row is not a completed effect estimate. |
| Model and router diagnosis, 2026-08-04 to 2026-08-08 | Built comparisons, routing, splitting, and instrumentation. | Required faithful framing and controlled arms. | Model framing and hidden evaluator behavior confounded attribution. | Both experiments invalid because their controls or arms were non-identifying. (Episodes AS-S07-AS-S08) | Working code is not automatically a valid experiment. |
| Forge reproduction and recombination, 2026-08-09 | Reproduced commitment forge and combined it with board/model variants. | Approved direct controls and live comparisons. | Public dimong4/nctuan method supplied the central mechanism. | Bounded forge and dual-board components were partially supported; the N=600 Gemma isolate gain narrowed at N=900 and did not reach the stated reproduction target. (Episodes AS-S09-AS-S10) | Preserve public provenance when evaluating recombination. |
| Late ladders, 2026-08-12 to 2026-08-16 | Implemented probe-hop, GPU, split, chain-pack, and fast-emit arms. | Insisted on controls and kept unrun arms pending. | Live platform constraints determined efficacy. | L27 refuted its same-batch proposition; GPU and L29 missed historical thresholds without causal controls; L31 was pending at cutoff and all four chainpack arms later completed below the historical L27 threshold, without matched controls; objective unachieved. (Episodes AS-S11-AS-S14; Testimony: living outcomes register; AgentSecurity live-results ledger, rows 55469249, 55469255, 55469264, 55469273, 55469280, 55525533, 55530790, 55538814, 55538829, 55538848, 55538855, and 55538875) | Distinguish functional, failed, pending, and achieved states. |

## 5. Case II: ARC-AGI-3

**Outcome-evidence note.** ARC-AGI-3 scores and evaluation outcomes below were
not independently re-queried from the external platform for this paper. They
are reported only as repository project-ledger, protocol, design, transcript,
or result-artifact records identified in the episode source register; those
records establish what the project recorded, not a fresh live verification.
(Sources ARC-S01-ARC-S12; AI evidence ledger, known evidence gaps)

### 5.1 Exploration, search, and evaluator boundaries

ARC-AGI-3 supplied a different research setting: an agent had to act in
interactive games whose state, goals, and evaluator lifecycle were only partly
visible. The process allowed broad agent-led exploration, but apparent
agent-originated hypotheses still passed through human challenge, local harness
tests, and scarce external evaluations. On 2026-06-29 the agent proposed a double
reset between plays. An eval-faithful validation that day reported
2.6–152-fold on 15 of 25 games after repairing the no-op; a later July 1 handoff
recorded a 7–109-fold local range. Because the artifacts use different ranges
and contexts, neither is treated as the single definitive local estimate. In
competition mode the second
play returned HTTP 400, making the test
invalid for the claimed deployment setting. Exploration produced an executable
idea; it did not supply the missing evaluator permission on which the idea
depended. This outcome is a project design-record result. (Episode ARC-S03;
Source ARC-S03)

On 2026-07-01 the agent recognized that scoring retained the best run and built
a search-and-replay approach: search for a solved path, then replay that action
sequence cleanly. The project design record says it solved all 25 development
games, a substantial local harness result, but the scoring trick did not survive
external conditions. The proper conclusion is split: the solver mechanism was
locally valid, while its
external-transfer claim was not. Calling the development sweep an autonomous
solution would erase both the hidden evaluator boundary and the human demand
for development and external checks. These outcomes are project design-record
claims, not independently re-queried scores. (Episode ARC-S02; Source ARC-S02)

### 5.2 Serving identity and development-to-hidden reversal

The sharpest validity failure occurred on 2026-07-11. A fine-tuned low-rank
adaptation (LoRA) adapter appeared to beat its base model with a local
result of 1.26, and the agent was
highly confident before the human requested proof of the deployed model's
identity. The audit statement was: “Conclusion: the LoRA never served. The
generation ran on base”. The apparent treatment and control were therefore the same model, so the
comparison was an `invalid experiment`, not a failed fine-tune. This is a
general computational-research point: model serving is part of the experiment,
not plumbing outside it. The 1.26 value and serving diagnosis are repository and
transcript records. (Episode ARC-S05; Quote Q06; Source ARC-S05)

A different failure on 2026-07-12 was valid enough to be informative. The
project submission ledger records that reducing prompt tokens raised the
development mean from 0.89 to 1.96, while its hidden-evaluation entry was 0.73.
Unlike the LoRA episode, the intervention actually ran; it simply did not
generalize in the recorded hidden result. The development-to-hidden reversal
distinguishes a refuted transfer claim from an invalid comparison and shows why
large local deltas cannot substitute for the
project's recorded held-out outcome. This is a project-ledger result, not an
independently queried live fact. (Episode ARC-S08; Source ARC-S08)

An executable-world-model (EWM) policy, which tested proposed actions against an
internal executable model before acting, adds a third status. Independent code
review on 2026-07-14
found and repaired defects, after which later campaigns displaced the policy
without a durable isolated gain. The implementation improved, but the efficacy
claim became `superseded`, not confirmed or cleanly refuted. Preserving that
status prevents later work from converting a repaired research artifact into a
result it never produced. (Episode ARC-S04)

### 5.3 Harness and perception as research infrastructure

The case's clearest infrastructure value came from measuring and improving the
observation-and-evaluation harness. The project protocol artifact records that,
on 2026-08-01, four same-versus-same replicate pairs showed root-mean-square
(RMS) variation of 0.707 game levels per pair—a scale summary of the paired
evaluation noise. Two preregistered gates were under-powered, so no
external-effect claim was made and the protocol was amended. Measuring noise
before interpreting small differences turned an unreliable score comparison
into an explicit instrument limitation. The governance rule became: every
submission is an experiment, with an identified question, control, and decision
gate rather than an isolated leaderboard try.
(Episode ARC-S06; Source ARC-S06)

Perception work made the mechanism concrete. On 2026-08-03 the agent corrected
slow-tick heads-up-display bars by virtually rotating and masking them; retained
replay and regression cases passed, but no isolated leaderboard increase was
claimed. On 2026-08-09, the goal-inference input changed from a flat object list
to a role-typed, HUD-masked scene so the reasoner could distinguish the
controllable object, target, and context while suppressing volatile status
elements. The retained comparison changed from 0/9 for the flat input to 6/6
for the combined representation. Because both role typing and HUD masking
changed, the artifact does not isolate which component caused the local
difference; neither had a separable external attribution.

These are confirmed or partially supported improvements to seeing and testing,
not proof of an end-to-end competition advance. (Episode ARC-S07; Episode
ARC-S01; Source ARC-S01; Source ARC-S07)

### 5.4 Hypothesis closure and public-signal noise

Later work shows how hypotheses were closed rather than allowed to survive on
plausibility. A structural plan channel with braking and phase gates executed on
2026-08-09, but project-ledger results remained in the established score band. On
2026-08-10, best-of-N candidate selection worked in the harness, yet its required
reset was swallowed in competition mode and the second play failed. A repaired
duck-memory namespace strategy also stayed within its registered 0.69-1.30
comparison interval (described below as *in-band*);
the project submission ledger records 0.83. Better structure, local selection,
and repaired state were each real implementation work; none established the
proposed score breakthrough. These are project-ledger and design-record results.
(Episode ARC-S10; Episode ARC-S09; Episode OC-S05; Source ARC-S10; Source
OC-S05)

External signals were not automatically trustworthy. On 2026-08-09 an
OpenCode/DeepSeek campaign synthesized nine linked specialist searches into a
research document, but a later audit found that the assumed corpus came from the
wrong model. Parallel breadth could not repair invalid provenance, so the
episode was classified `invalid experiment`. Earlier, a proposed duck-sparse
35B arm looked favorable until a serving audit showed that its path had never
executed; the human killed it before reset, producing neither a slot nor an
external negative result. These episodes show human challenge closing
attractive but unsupported hypotheses before they consumed further evaluation.
(Episode OC-S04; Episode OC-S03)

The correction was converted into an evidence gate rather than left as a memory
of failure. A later adapter comparison began with the rule “Serving identity
proven first.” Deterministic controls established which model was actually
running before outcome interpretation. Together with memory-blind
reassessment—treating stored conclusions as untrusted until rechecked—this
made provenance and deployment identity preconditions for a claim, not cleanup
after a surprising score. Such gates are governance contributions produced by
human challenge and agent execution; they do not turn the agent into the final
arbiter of validity. (Quote Q07; Episode ARC-S05; Episode OC-S04)

### 5.5 Late alternatives and provider switching

On 2026-08-15, Stage 2b—a later engineered candidate intended to replace the
project's *duck baseline*, its nickname for the reactive reference policy—was
tested across all 25 development games (the project's *full-25* verdict). Its
mean was 0.2463 versus 1.6333 for duck, although
it won six individual games. The stated replacement claim was refuted and no
replacement was shipped; only a narrow portfolio possibility remained. This
verdict depends on an audit-time mutable artifact outside the cutoff Git
revision. Its hash, modification time, and extraction time are recorded, but
the exact bytes are not reproducible from the frozen repository, so that
provenance limitation travels with the result. (Episode ARC-S11; Source ARC-S11)

The same day, the project design record reports that Qwen 3.8—an external model
candidate screened in the project—had a stored local row mean of 2.5291 versus
1.4872 for Qwen 3.6 in a one-wave, side-by-side (A/B) directional screen. The
human required an armed but gated live runner. No scored external result existed
in the project records by the cutoff, so Qwen 3.8 remained `open`; its local
advantage was not promoted into a live, ranking, or objective-achievement claim.
This is a repository design-record claim, not an independently queried external
result. External model selection, agent screening, and human approval were all
material to the episode, making its origin mixed rather than autonomously
agent-generated. (Episode ARC-S12; Source ARC-S12)

In retrospective testimony, the author reported that Claude Code was the
primary research system while Codex and OpenCode/DeepSeek were introduced mainly
when the active line appeared stuck, repetitive, or prematurely settled. The
OpenCode episodes illustrate how a fresh system could expose an inherited
assumption or force a memory-blind restatement; they do not independently
establish the broader switching pattern. Switching could not provide independent
corroboration when providers saw overlapping repositories, prompts, public
methods, or prior conclusions. Because task mix, timing, models, budgets, and
exposure were unequal, it is analyzed only as a diversity and reset mechanism,
never as a provider ranking. The author's retrospective assessment likewise
attributes most contributions to work built on other people's methods and
identifies no clear unexpected agent-originated discovery. (Testimony: author
baseline and interview; Episode OC-S01; Episode OC-S02; Episode OC-S04;
Testimony Q09)

At the cutoff, ARC-AGI-3's winning objective remained unachieved as retrospective
testimony. That conclusion does not erase locally supported search, perception,
parser, noise-calibration, or serving-control work, nor does it convert open
Qwen 3.8 transfer or the Stage 2b portfolio possibility into achievements. It
sets the outer boundary of the case. The author assessed that the agents enabled
meaningful participation and contextual learning; this is retrospective
testimony, not a measured productivity or capability effect. Dependable
hypothesis choice, valid evaluation, and claim closure still required
substantial human governance. (Episodes ARC-S01-ARC-S12; Testimony: living
outcomes register; Testimony Q08)

### 5.6 Case evidence summary

Table 2 retains the distinctions among executable mechanisms, valid negative
results, invalid experiments, superseded work, and open transfer claims. It
summarizes research roles, not provider performance. (Episodes ARC-S01-ARC-S12;
Episodes OC-S03-OC-S05)

| Phase | Agent contribution | Human contribution | External dependence | Outcome | Lesson |
| --- | --- | --- | --- | --- | --- |
| Evaluator exploration, 2026-06-29 to 2026-07-01 | Built reset probes and search/replay. | Required competition-mode and external checks. | Hidden lifecycle and scoring semantics controlled transfer. | Project design records classify the reset experiment invalid and report that search solved development but not external conditions. (Episodes ARC-S02-ARC-S03; Source ARC-S02; Source ARC-S03) | A local solver may depend on an unavailable evaluator action. |
| Serving and hidden evaluation, 2026-07-11 to 2026-07-14 | Fine-tuned, reduced prompts, and repaired a reviewed policy. | Demanded serving identity and held-out evaluation. | Base-model serving, held-out tasks, and review shaped the evidence. | Repository, transcript, and project-ledger records classify the LoRA comparison invalid, prompt transfer refuted, and EWM superseded. (Episodes ARC-S04-ARC-S05; Episode ARC-S08; Source ARC-S04; Source ARC-S05; Source ARC-S08) | Distinguish non-running treatments, non-generalizing treatments, and displaced work. |
| Measurement and perception, 2026-08-01 to 2026-08-09 | Measured A/A noise, fixed parsing, and changed goal-inference input to a role-typed, HUD-masked representation. | Required registered gates, replay, and regression checks. | Stochastic evaluation and retained cases bounded interpretation. | Protocol and verdict artifacts confirm the noise-floor and parser claims and partially support the combined representation without isolating typing from masking or an external effect. (Episodes ARC-S01; ARC-S06-ARC-S07; Source ARC-S01; Source ARC-S06; Source ARC-S07) | Instrument quality and representation can be research contributions. |
| Structural and memory strategies, 2026-08-09 to 2026-08-10 | Added planning gates, best-of-N selection, and a repaired namespace. | Required project-ledger comparison and challenged reset assumptions. | Competition lifecycle and prior cross-provider proposal constrained deployment. | Project-ledger and design records partially support structural controls, refute best-of-N, and keep the memory result in-band. (Episodes ARC-S09-ARC-S10; Episode OC-S05; Source ARC-S09; Source ARC-S10; Source OC-S05) | Better internal process does not imply external efficacy. |
| External research and serving audits, 2026-08-06 to 2026-08-10 | Conducted multi-agent searches and plumbing review; articulated and executed the serving-identity gate. | Commissioned challenges, demanded proof, and killed an unserved arm. | The gate emerged from mixed human challenge and agent articulation/execution; wrong-model corpus and an unexecuted serving path invalidated attractive proposals. | Corpus experiment invalid; sparse arm killed without an external result. (Episodes OC-S03-OC-S04; Episode ARC-S05; Quote Q07) | Breadth cannot substitute for source and serving provenance. |
| Late alternatives, 2026-08-15 | Tested Stage 2b and screened Qwen 3.8. | Required full-25 and gated-external verdicts. | Stage 2b uses a mutable outside-Git audit artifact; Qwen was an external model candidate. | Artifacts refute replacement and leave Qwen 3.8 open without an external score; the objective remained unachieved as testimony. (Episodes ARC-S11-ARC-S12; Source ARC-S11; Source ARC-S12; Testimony: living outcomes register) | Carry provenance limits and open transfer status into the conclusion. |

## 6. Cross-Case Findings

### 6.1 Six capabilities, not one autonomy scale

The cases separate six claims that are easy to collapse in ordinary accounts of
agentic research. *Access* is the ability to enter an unfamiliar technical
domain and begin meaningful work. *Execution* is the ability to turn a proposed
mechanism into code, instrumentation, and experiments. *Insight* is an
evidence-supported explanation that distinguishes a mechanism from plausible
alternatives. *Originality* concerns the provenance of the question or method.
*Reliability* is the ability to produce valid, calibrated results across
episodes. *Autonomy* would require the dependable integration of all five other
capabilities, including self-correction and appropriate stopping without a
human having to detect the critical mistake. The two cases provide direct
evidence of access and substantial execution, bounded instances of insight,
and weaker evidence for dependable originality, reliability, or autonomy.
(Episodes AS-S01-AS-S14; Episodes ARC-S01-ARC-S12; Episodes OC-S01-OC-S05;
Testimony Q08-Q09)

The origin codes reinforce this separation but must not be misread. Of the 31
reviewed episodes, 13 propositions were coded `agent`, 15 `mixed`, three
`external`, and zero `human`. Zero human-origin rows is a coding result about
the apparent source of the bounded proposition, not evidence that no human
intellectual contribution occurred. The 15 mixed rows and the intervention
column record human framing, challenge, approval, demand for controls, and
claim closure. Likewise, an agent-origin proposition is not automatically an
original discovery: it may recombine inherited methods, target an already
visible failure, or remain refuted, invalid, superseded, or open. (AI evidence
ledger, descriptive measures and derivations, including the 31 exact episode
IDs)

### 6.2 Access without mastery; execution without dependable originality

The strongest cross-case result is access without demonstrated mastery. The
agents navigated unfamiliar SDKs, evaluator protocols, model-serving paths,
interactive-game harnesses, and experimental artifacts well enough to make both
projects executable. This supports the author's retrospective judgment that
the tools enabled meaningful participation and contextual learning. It does not
show that the author or agents thereby acquired domain mastery, and without a
human-only control it supplies no measured productivity effect. (Episodes
AS-S01-AS-S03; Episodes ARC-S02, ARC-S05-ARC-S07; Testimony Q08; Testimony:
author baseline and interview)

Execution was also more dependable than scientific interpretation. Agents
ported interfaces, repaired parsers, built routers, made a GPU path functional,
audited adapter-serving identity, generated controlled runners, and preserved
result artifacts. Some
of those artifacts were useful even when their motivating efficacy claim failed.
A working router did not identify a routing effect; a working GPU path did not
establish a CPU bottleneck; repaired policy code did not establish durable
superiority. Artifact production is therefore evidence of execution, while
scientific insight additionally requires an identifying comparison and a result
that survives the relevant evaluation boundary. (Episodes AS-S01, AS-S08,
AS-S12; Episodes ARC-S04-ARC-S05, ARC-S07)

The adaptive-sizing and commitment-forge episodes show how valuable
recombination should be attributed. Both central mechanisms came from public or
external sources; the agents translated them into the local repository, tested
them, and in the forge case combined the reproduced mechanism with board and
model variants. Transparent reuse and recombination are not plagiarism when
their provenance is preserved. They are also not independent discovery. The
scientific contribution claimed here is bounded implementation, adaptation,
and component testing, not invention of the public mechanism or attainment of
the stated reproduction target. (Episodes AS-S04, AS-S09-AS-S10;
Testimony Q09)

### 6.3 Review, confidence, and evidence authority

Human oversight was part of the research system rather than an occasional
safety backstop. The author estimates 2-5 hours per day of review, challenge,
redirection, and approval. In the episodes, human intervention exposed broken
controls, demanded serving proof, required hidden or competition-mode tests,
kept unresolved arms pending, and stopped an unserved proposal before it used a
live slot. Learning occurred through this review loop: agent proposals made
assumptions concrete, and adverse review or evaluation converted those
assumptions into reusable gates. This is substantial supervised execution, not
hands-off autonomy. (Episodes AS-S07-AS-S08, AS-S11, AS-S14; Episodes ARC-S05,
ARC-S08-ARC-S09; Episode OC-S03; Testimony: author baseline and interview)

Confidence did not reliably track validity. On June 30, Q04 corrected an earlier
approximately 570 boundary after exact-model evidence contradicted it. Q02, on
July 1, asserted a different approximately 465 boundary and 44-point ceiling
that later work weakened. Q04 therefore precedes and does not retract Q02; the
sequence instead shows that one successful correction did not prevent a new
confident ceiling claim. Other high-confidence lines rested on an unserved
adapter, a broken model frame, unavailable reset behavior, or a wrong-model
corpus. (Quotes Q04 and Q02; Episodes AS-S07; ARC-S03, ARC-S05, ARC-S09;
Episode OC-S04)

Finally, recorded memory and provider changes did not create evidence. A stored
conclusion could propagate a stale assumption or a repaired no-op, so the
memory-blind audit treated memory as a set of claims to revalidate. Introducing
a different provider could broaden candidate explanations or reset a settled
line, but shared repositories, prompts, public methods, and prior conclusions
prevented that switch from constituting independent corroboration. Unequal
tasks, timing, models, and budgets also prevent provider ranking. For efficacy,
the relevant external result remained the authority: directly retrieved live
rows support the cited AgentSecurity scores, while ARC outcomes retain their
narrower project-ledger or artifact qualification because they were not freshly
queried from the external platform. (Episodes OC-S01-OC-S05; Quote Q05;
AgentSecurity live-results ledger; Sources ARC-S01-ARC-S12; AI evidence ledger,
known evidence gaps)

## 7. Where Agents Add Value

The cases support a practical role for agents as research executors. Their value
was distributed across the observed workflow rather than concentrated in
autonomous discovery. (Episodes AS-S01-AS-S14; Episodes ARC-S01-ARC-S12)

- **Navigation and onboarding.** Repository search, SDK inspection, and
  evaluator reading converted unfamiliar systems into executable maps. This
  underlies the author's perceived access and contextual-learning benefit, but
  remains retrospective testimony rather than a measured comparison with
  unaided work. (Episodes AS-S01-AS-S03; Episodes ARC-S02-ARC-S03; Testimony
  Q08)
- **Implementation and operations.** Agents translated proposed mechanisms into
  attack candidates, search/replay systems, model-serving probes, parsers,
  routers, replay-safe sizing, and gated runners. A functional artifact retained
  operational value even when the claimed score mechanism was refuted or never
  externally adjudicated. (Episodes AS-S04, AS-S08, AS-S12, AS-S14; Episodes
  ARC-S02, ARC-S05, ARC-S07, ARC-S12)
- **Instrumentation.** Timing probes, router self-measurement, serving-identity
  checks, retained replay cases, and A/A noise measurement made hidden
  assumptions observable. ARC's 0.707-level RMS estimate and the later rule
  “Serving identity proven first” are stronger contributions to research
  validity than an unqualified leaderboard narrative would have been. (Episodes
  AS-S05, AS-S08; Episodes ARC-S05-ARC-S07; Quote Q07)
- **Experiment generation.** Agents produced alternative mechanisms and
  executable arms, while the human requested bounded ladders, controls, and
  full-game verdicts. The episode ledger records both successful component tests
  and informative closures; generating testable propositions did not make their
  selection or interpretation trustworthy by default. (Episodes AS-S05-AS-S14;
  Episodes ARC-S08-ARC-S12)
- **Literature and method discovery.** Agent search surfaced public strategies,
  model candidates, and specialist syntheses that could guide reproduction or
  challenge. This capability depended on source identity: the public forge was
  useful when attributed and tested, whereas the nine-specialist document was
  invalidated by a wrong-model corpus. (Episodes AS-S04, AS-S09; Episode
  OC-S04; Episode ARC-S12)

These contributions matter even when they do not yield a new scientific
finding. A parser regression suite, a deterministic serving probe, a preserved
negative ladder, or a reproducible runner can improve the next inquiry. The
appropriate claim is that agents produced research infrastructure and
a reviewed record of implemented experiments. Calling every artifact an insight
would erase the causal and provenance work that turns execution into knowledge.
(Episodes ARC-S04-ARC-S07; Episodes AS-S08, AS-S11-AS-S14)

## 8. Where Agents Struggle

The status distribution describes a mixed record rather than a single success
rate: four of 31 bounded claims were confirmed, ten partially supported, seven
refuted, five invalid experiments, one superseded, and four open. Those labels
apply to different propositions and evidence types, so they cannot be collapsed
into a provider accuracy score. They do show why an executable result, an
external effect, a valid experiment, and a durable scientific conclusion must
be adjudicated separately. (AI evidence ledger, descriptive measures and
derivations, with all 31 IDs assigned exactly once)

Hypothesis selection and novelty remained weak points. The ledger contains 14
agent-origin propositions, but several pursued throughput, routing, serving, or
reset explanations that were later refuted or invalidated. The author could not
identify a clear unexpected agent-originated discovery and assessed the
contributions as largely building on other people's work. That testimony does
not prove agents cannot originate discoveries; it limits what these two cases
can claim. Agent generation supplied candidates, while worthwhile selection and
independent originality remained unresolved. (Episodes AS-S07-AS-S08,
AS-S12-AS-S14; Episodes ARC-S03, ARC-S08-ARC-S09; Testimony Q09)

Calibration and due diligence failed at consequential boundaries. High local
confidence preceded discovery that the treatment never served, a comparison
frame was under-powered, a reset was unavailable in competition mode, or a
research corpus concerned the wrong model. These were not cosmetic mistakes:
they changed the classification of the experiment. The agents could articulate
a post hoc correction, but the human challenge or external failure supplied the
trigger. (Episodes AS-S07; ARC-S03, ARC-S05, ARC-S09; Episode OC-S04; Quotes
Q04, Q06-Q07)

Causal inference suffered when arms did not isolate a mechanism. The router
ladder changed overlapping factors, the early Gemma comparison used a broken
control, and the LoRA treatment and base control resolved to the same served
model. Conversely, prompt reduction was a valid intervention whose development
gain reversed on the recorded hidden evaluation. The distinction matters: the
first three episodes could not answer their proposed causal question, while the
last refuted a transfer claim. More runs do not repair a non-identifying design.
(Episodes AS-S07-AS-S08; Episodes ARC-S05, ARC-S08)

Agents also struggled to respect the boundary between local and live evidence.
Early close and packing reached only `ERROR` rows, so neither established a
completed live effect; search/replay solved the development set but not the
external setting; prompt reduction reversed; and Qwen 3.8 remained open despite
a strong local A/B because no scored external result existed by the cutoff.
Local tests established functionality or a within-harness effect. They could
not establish deployment availability, held-out generalization, or competition
efficacy. (Episodes AS-S05-AS-S06; Episodes ARC-S02, ARC-S08-ARC-S09,
ARC-S12)

Stopping and memory discipline did not emerge reliably from the agent alone.
Attractive lines could continue after in-band or adverse results, while stored
summaries could carry earlier assumptions into a new run. Human intervention
bounded ladders, required controls, preserved pending status, killed an
unserved arm, and commissioned memory-blind reassessment. Provider switching
helped reopen the question space, but could also continue the same episode or
produce a broader synthesis over invalid premises. (Episodes AS-S11-AS-S14;
Episodes OC-S02-OC-S05; Episode ARC-S11)

## 9. Governing AI-Assisted Research

The resulting governance framework is a research protocol, not generic advice
to keep a human in the loop. Each control below answers a coded failure and
specifies an operational action that a researcher or IT professional can audit.
(Episodes AS-S01-AS-S14; Episodes ARC-S01-ARC-S12; Episodes OC-S01-OC-S05)

| Control | Operational rule | Coded reason |
| --- | --- | --- |
| Direct-source verification | Resolve each decisive interface, dataset, citation, public method, and result to the primary source. Pin the version, source locator, and access date; verify the quoted or extracted claim before it enters a hypothesis. | SDK semantics repaired a non-scoring attack, while a nine-specialist synthesis over the wrong-model corpus remained invalid despite its breadth. Citation fabrication in the reviewed literature supplies an external reason for the same gate. (Episode AS-S03; Episode OC-S04; [15]) |
| Falsifiable hypothesis card | Before implementation, record one mechanism, predicted observable change, alternative explanation, disconfirming result, evidence boundary, and decision rule. Name the proposition narrowly enough that one outcome can close it. | The router arms overlapped, L27's nominal knobs collapsed to one effective axis, and the GPU and L29 arms missed pre-stated historical thresholds without matched causal controls; those records required narrower propositions and explicit disconfirming rules. (Episodes AS-S08, AS-S11-AS-S13) |
| Matched controls | Hold commit, prompt/frame, served model, evaluator mode, budget, and measurement window constant; vary one proposed cause. Prove treatment identity and confirm that nominal arms are mechanically distinct before launch. | The weak Gemma frame, overlapping router arms, collapsed L27 axes, and unserved LoRA made their original comparisons non-identifying. (Episodes AS-S07-AS-S08, AS-S11; Episode ARC-S05) |
| Local-to-live gates | Use local unit, replay, regression, and smoke tests to establish functionality. Promote efficacy only through a preregistered held-out or live gate, with external execution separately recorded. Never copy a local status into the live field. | Packing, search/replay, prompt reduction, best-of-N, and Qwen 3.8 each showed why local success does not determine external transfer. (Episode AS-S06; Episodes ARC-S02, ARC-S08-ARC-S09, ARC-S12) |
| Memory as untrusted input | Store prior claims with source, cutoff, status, executed path, and unresolved alternatives. At session start, inject them as assertions to check, not facts to obey; stale or source-free summaries cannot authorize an experiment. | A namespace no-op and inherited assumptions survived across continuations, while the memory-blind prompt explicitly required revalidation. (Episode OC-S02; Episode OC-S05; Quote Q05) |
| Memory-blind review | For high-impact or stalled claims, commission a fresh review from primary code, data, and evaluator records before revealing the inherited conclusion. Compare the review's premises with the original; do not call it an outcome until the relevant external test runs. | The AgentSecurity audit improved epistemic discipline but produced no completed live adjudication, demonstrating both the value and the limit of a fresh review. (Episode OC-S02) |
| Provider diversity | Use a second provider to generate counter-hypotheses, inspect plumbing, or challenge a settled interpretation. Record shared context and prior exposure. Treat switching as diversity and reset, not corroboration; corroboration requires independently acquired evidence rather than provider agreement. Never infer provider ranking from unequal assignments. | Provider changes exposed assumptions and broadened search, but the providers shared repositories, methods, or conclusions and were used under unequal conditions. (Episodes OC-S01-OC-S05; Testimony: author baseline and interview) |
| Human approval | Require named human approval before scarce live evaluation, external submission, cost escalation, or any write to shared or production systems. The approver checks the hypothesis card, control identity, evidence class, and rollback or stop rule. | Human gates requested faithful comparisons, hidden tests, full-25 verdicts, and controlled ladders, and prevented an unserved arm from consuming a slot. (Episodes AS-S04, AS-S07-AS-S08, AS-S11; Episodes ARC-S08, ARC-S11-ARC-S12; Episode OC-S03) |
| Preserved negatives and states | Append results to an immutable ledger with separate fields for local and live outcomes and the statuses `confirmed`, `partially supported`, `refuted`, `invalid experiment`, `superseded`, and `open`. Preserve failed controls, killed arms, pending arms, and provenance limits rather than rewriting the project around the latest result. | L27, GPU, L29, Stage 2b, the killed sparse arm, and L31's cutoff-pending/later-partial-completion states have different evidentiary meanings that would disappear in a success-only narrative. (Episodes AS-S11-AS-S14; Episode ARC-S11; Episode OC-S03) |
| Pre-outcome confidence | Record confidence and its evidentiary basis before revealing the result. Afterward, score calibration separately from implementation quality and retain both corrections and later distinct claims. | Q04 corrected the earlier 570-boundary claim before Q02 introduced a different 465-boundary claim; Q04 therefore cannot be a retraction of Q02. Other high-confidence propositions failed serving or evaluation checks. (Quotes Q04 and Q02; Episodes ARC-S03, ARC-S05, ARC-S08-ARC-S09) |
| Stopping and escalation | Stop an arm when its treatment cannot be proven, its control is broken, its required evaluator action is unavailable, or a registered gate is under-powered. Escalate to human redesign when repeated results stay in-band, arms overlap, provenance is unresolved, or a live claim would exceed the evidence. | ARC's noise study amended two under-powered gates; the sparse arm was killed before reset; overlapping routing and adverse late ladders required redesign rather than confident continuation. (Episode ARC-S06; Episode OC-S03; Episodes AS-S08, AS-S11-AS-S14) |

The framework also clarifies ownership. Agents can fill hypothesis cards, build
controls, maintain ledgers, and conduct first-pass audits. The accountable human
decides whether the design identifies the claim, whether an external gate is
justified, and what conclusion the evidence supports. For IT teams, the same
separation can be enforced in tooling: immutable experiment manifests,
content-addressed artifacts, deployment-identity probes, permissioned live
runners, and approval logs make epistemic gates inspectable rather than
dependent on conversational memory. (Episodes ARC-S05-ARC-S06, ARC-S12;
Episodes AS-S11-AS-S14; Quote Q07)

## 10. Implications

**Researchers.** The case-specific lesson is to evaluate an agent by research
role and evidence class, not by a single label. In these episodes, access did
not imply mastery, execution did not imply insight, and useful recombination did
not imply independent originality. Reporting each dimension separately makes a
confirmed parser repair credible without turning it into a ranking claim, and
preserves the value of a reproduced public mechanism without relabelling it as
invention. (Episode ARC-S07; Episodes AS-S04, AS-S09-AS-S10) This separation
aligns with broader evidence: bounded laboratory systems close loops inside
human-engineered envelopes [1-3], while scientific-programming and replication
benchmarks do not establish open-ended research autonomy [5,11].

**IT professionals.** The case-specific operational unit is the
claim-to-evidence path. Repository permissions and model access address
operational risk, but scientific reliability additionally requires versioned
inputs, deployment-identity probes, matched controls, separate local and
external results, append-only outcomes, and permissioned live runners. Memory
systems should retain source, cutoff, contradiction, and unresolved status
rather than compress the project into one preferred narrative. A second model
can challenge assumptions, but shared repositories and prior conclusions must
remain visible so diversity is not mistaken for independence. (Episodes
ARC-S05-ARC-S06; Episodes OC-S01-OC-S05; Episodes AS-S07-AS-S08)

**Research leaders.** The cases do not support a staffing multiplier, provider
ranking, or substitution claim. They support budgeting agents together with
human review, scarce external evaluations, evidence curation, and the authority
to stop invalid work. Leaders should evaluate portfolios by the number and
importance of validly closed claims, not conversation volume, tokens, commits,
or manuscript output. This recommendation is case-derived, while the broader
literature points in the same direction: Data-to-paper reports increasing need
for human co-piloting as complexity rises [7], and the AI Scientist reports
implementation and interpretation failures despite end-to-end production [8].

**Tool builders.** Systems can make the governance protocol executable. Useful
features include content-addressed inputs, immutable experiment manifests,
treatment-identity checks, preregistered decision rules, confidence captured
before outcomes, local/external status fields that cannot overwrite each other,
and approval gates for cost or live execution. Retrieval and synthesis should
expose primary-source locators and uncertainty rather than only fluent answers.
That design implication joins case-specific failures—an unserved adapter and a
wrong-model corpus—with broader findings on context-sensitive literature-agent
judgments and citation errors [13,15]. (Episode ARC-S05; Episode OC-S04)

No general performance rate follows from two competitions, one researcher, and
31 interpretively coded episodes. The bounded implication is operational: the
agents generated executable work in unfamiliar domains, and the author
retrospectively perceived that they enabled participation and contextual
learning. Without a human-only control, the cases cannot measure how much work
became feasible or how quickly it was completed. In these cases, the defensible
role was a governed research executor: materially useful, but dependent on
human accountability for provenance, validity, external transfer, and stopping.
(AI evidence ledger, descriptive measures and derivations; Testimony Q08-Q09)

## 11. Limitations and Living Outcomes

### 11.1 Limitations

This is a comparative N-of-1 study of one researcher and two projects, not a
representative sample of researchers, domains, or agent systems. The projects
were selected because the author conducted them, and the 31 episodes were
chosen and interpretively coded by that same authorial research process. No
second coder was blinded to the cases, no inter-rater reliability estimate
exists, and quotations were selected for explanatory value under the stated
privacy rules. Selection bias and single-author interpretation can therefore
affect episode boundaries, origins, statuses, and the salience of failures or
successes.

There was no human-only control, randomized assignment, common task set, or
matched budget. Providers were used unequally and for different purposes, and
their models, interfaces, context policies, and surrounding infrastructure
changed during the observation window. Conversation histories also overlap:
continuations, imports, shared repositories, provider switches, and parent-child
work can preserve the same premise across nominally different sessions. The
deduplication procedure reduces double counting but cannot establish
independent intellectual contribution or detect every paraphrased dependency.
These constraints preclude provider comparisons, causal productivity estimates,
and claims that a different model or allocation would have produced the same
results.

Competition metrics are imperfect proxies for scientific quality, originality,
understanding, or real-world value. Hidden evaluators, run variance, scarce
submission slots, mutable platform conditions, and incomplete local replicas
limit causal attribution and local-to-external transfer. Both projects also
depended on external SDKs, public methods, model candidates, platform rules,
and partly hidden evaluation behavior. That dependence can enable valuable
reproduction while weakening originality claims and making later replication
sensitive to unavailable versions or services.

Several important statements are retrospective testimony rather than direct
measurement: the author's baseline, 2–5-hour daily oversight estimate, perceived
access and learning value, reported costs, trust judgments, and the unachieved
winning objectives. Costs were not allocated by case or reconciled to receipts,
and subscription amounts were not recorded in the reviewed ledger. The ARC
Stage 2b full-25 verdict has an additional provenance limitation: it was read at
audit time from a mutable file outside the frozen Git revision. Its hash,
modification time, and extraction time are recorded, but the exact bytes cannot
be reconstructed from the cutoff repository alone.

Finally, the outcomes were ongoing. Four AgentSecurity L31 chain-pack rows were
pending at the frozen cutoff; a later status-only recheck found one complete at
73.605 and three still pending, and a second recheck found all four complete at
79.985, 79.365, 73.605, and 54.375. No ARC external state was freshly queried, and
Qwen 3.8 external
transfer remained open. Final competition results, rankings, costs, and
retrospective conclusions could change the outer case narrative, but cannot
retroactively convert an invalid experiment into a valid one or erase a
negative, superseded, or unresolved episode.

### 11.2 Living-outcomes register

The register below records what was known, what was not independently known,
and what a later revision is allowed to add. A statement of “not established”
is a completed evidence status, not a blank field.

| Register item | AgentSecurityComp | ARC-AGI-3 | Authority and update constraint |
| --- | --- | --- | --- |
| Evidence cutoff | Repository `2ed68e8` at 2026-08-16T10:29:29+03:00; mutable histories extracted 2026-08-16T08:06:05Z; frozen live-results artifact retrieved 2026-08-16T10:56:15Z; selected rows separately rechecked 2026-08-16T11:10:21Z, 2026-08-16T11:26:07Z, 2026-08-16T11:59:48Z, and 2026-08-16T12:44:16Z. | Repository `ebe5b3e` at 2026-08-15T18:41:01+03:00; mutable histories extracted 2026-08-16T08:06:05Z; Stage 2b artifact extracted 2026-08-16T08:45:51Z. | Each stream keeps its own cutoff; a later observation appends a new dated state rather than replacing this one. |
| Winning objective | Ongoing and unachieved at cutoff. | Ongoing and unachieved at cutoff. | Retrospective author testimony; verify against final official records. |
| Most recent recorded experiment state | The completed L27 control was 88.730; L29 was 85.675; L31 fast-emit was `COMPLETE` at 25.145. At the frozen cutoff all four L31 chain-pack rows were `PENDING`; at 12:44:16Z refs 55538814, 55538829, 55538848, and 55538855 were all `COMPLETE` at 79.985, 79.365, 73.605, and 54.375. These are identified live submission rows, not a current rank, matched-effect estimate, or final best-system claim. | No current external score or rank was independently queried. Project records report Stage 2b at 0.2463 versus the duck baseline at 1.6333 over 25 development games, and Qwen 3.8 locally at 2.5291 versus 1.4872; neither is asserted as a current external outcome. | AgentSecurity values are selected live observations through the status-only recheck at 2026-08-16T12:44:16Z; the separate frozen artifact remains dated 2026-08-16T10:56:15Z. ARC values are bounded repository or mutable-artifact records and retain those provenance labels. |
| Recorded deadlines | Final submission: 2026-09-01 at 23:59 UTC; optional Working Note: 2026-09-08 at 23:59 UTC. | No official ARC deadline was admitted to the reviewed AI evidence ledger, so this manuscript asserts none. | AgentSecurity dates come from the reviewed official timeline. An ARC deadline requires a primary official source in a later evidence revision. |
| Cost state | No independently corroborated case allocation. | No independently corroborated case allocation. | Cross-case retrospective testimony reports about USD 100 OpenRouter and USD 30 Modal, plus Colab Pro and Claude/Codex subscriptions whose amounts were not recorded. No independently confirmed total existed at cutoff. |
| Human oversight | Not separated by case. | Not separated by case. | Cross-case retrospective estimate: 2–5 hours per day; not a time-tracking result. |
| Reserved post-competition fields | Official final submission status and score, final rank, winning-objective verdict, Working Note outcome, receipt-reconciled cost if available, cumulative oversight if measured, and dated interpretation change. | Official final evaluation status and score, final rank, winning-objective verdict, final Qwen 3.8 transfer result if executed, receipt-reconciled cost if available, cumulative oversight if measured, and dated interpretation change. | Populate only from newly cited official records, preserved project artifacts, or explicitly labelled testimony; retain the cutoff states above in revision history. |

The final update procedure is specified in Appendix A. Until that procedure is
performed, pending means pending, unqueried means unqueried, and the ongoing
objectives remain retrospective testimony rather than verified final outcomes.

## Acknowledgements and AI-Use Disclosure

Ahmed Mobasher is the sole author and is accountable for the manuscript's
claims, citations, originality, integrity, and final wording. Claude Code was
the primary agent used to execute research work across the two cases. Codex and
OpenCode/DeepSeek were used as supplementary perspective resets and challenge
mechanisms; their unequal use does not support a provider ranking. In the
current manuscript collaboration, Codex assisted with evidence-ledger review,
source reconciliation, drafting, editing, and mechanical checks. AI-generated
material was treated as provisional and checked against the reviewed evidence
ledger. These are project-specific facts about tool use and authorship. The
ICMJE and Springer Nature statements cited in Methods are general, mutable
policy guidance [16,17], not evidence that these project facts occurred. None
of Claude Code, Codex, OpenCode, or DeepSeek is an author, and responsibility
for every included claim remains with Ahmed Mobasher.

## References

1. King, R. D., Whelan, K. E., Jones, F. M., et al. “Functional genomic
   hypothesis generation and experimentation by a robot scientist.”
   *Nature* 427, 247-252 (2004). Peer-reviewed article.
   [doi:10.1038/nature02236](https://doi.org/10.1038/nature02236).
2. Burger, B., Maffettone, P. M., Gusev, V. V., et al. “A mobile robotic
   chemist.” *Nature* 583, 237-241 (2020). Peer-reviewed article.
   [doi:10.1038/s41586-020-2442-2](https://doi.org/10.1038/s41586-020-2442-2).
3. Szymanski, N. J., Rendy, B., Fei, Y., et al. “An autonomous laboratory for
   the accelerated synthesis of inorganic materials.” *Nature* 624, 86-91
   (2023). Peer-reviewed article.
   [doi:10.1038/s41586-023-06734-w](https://doi.org/10.1038/s41586-023-06734-w).
4. Park, Y. J., Kaplan, D., Ren, Z., et al. “Can ChatGPT be used to generate
   scientific hypotheses?” *Journal of Materiomics* 10(3), 578-584 (online
   2023; issue 2024). Peer-reviewed perspective.
   [doi:10.1016/j.jmat.2023.08.007](https://doi.org/10.1016/j.jmat.2023.08.007).
5. Chen, Z., Chen, S., Ning, Y., et al. “ScienceAgentBench: Toward Rigorous
   Assessment of Language Agents for Data-Driven Scientific Discovery.” ICLR
   2025. Peer-reviewed conference paper.
   [OpenReview 6z4YKr0GK6](https://openreview.net/forum?id=6z4YKr0GK6).
6. Gottweis, J., Weng, W.-H., Daryin, A., et al. “Accelerating scientific
   discovery with Co-Scientist.” *Nature* 655, 487-496 (2026). Peer-reviewed
   article. [doi:10.1038/s41586-026-10644-y](https://doi.org/10.1038/s41586-026-10644-y).
7. Ifargan, T., Hafner, L., Kern, M., Alcalay, O., and Kishony, R. “Autonomous
   LLM-driven research from data to human-verifiable research papers.” arXiv
   2404.17605v1 (2024). Preprint.
   [arXiv:2404.17605](https://arxiv.org/abs/2404.17605).
8. Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J., and Ha, D. “The AI
   Scientist: Towards Fully Automated Open-Ended Scientific Discovery.” arXiv
   2408.06292v3 (2024). Preprint.
   [arXiv:2408.06292](https://arxiv.org/abs/2408.06292).
9. Majumder, B. P., Surana, H., Agarwal, D., et al. “DiscoveryBench: Towards
   Data-Driven Discovery with Large Language Models.” arXiv 2407.01725v1
   (2024). Preprint.
   [arXiv:2407.01725](https://arxiv.org/abs/2407.01725).
10. Siegel, Z. S., Kapoor, S., Nadgir, N., Stroebl, B., and Narayanan, A.
   “CORE-Bench: Fostering the Credibility of Published Research Through a
   Computational Reproducibility Agent Benchmark.” arXiv 2409.11363v2
   (2024; revised 2026). Preprint.
   [arXiv:2409.11363](https://arxiv.org/abs/2409.11363).
11. Starace, G., Jaffe, O., Sherburn, D., et al. “PaperBench: Evaluating AI's
    Ability to Replicate AI Research.” Official benchmark release and
    accompanying preprint, arXiv 2504.01848 (2025).
    [Official release](https://openai.com/index/paperbench/) and
    [primary paper](https://arxiv.org/abs/2504.01848).
12. Si, C., Yang, D., and Hashimoto, T. “Can LLMs Generate Novel Research Ideas?
    A Large-Scale Human Study with 100+ NLP Researchers.” arXiv 2409.04109v1
    (2024). Preprint. [arXiv:2409.04109](https://arxiv.org/abs/2409.04109).
13. Skarlinski, M. D., Cox, S., Laurent, J. M., et al. “Language agents achieve
    superhuman synthesis of scientific knowledge.” arXiv 2409.13740v2 (2024).
    Preprint. [arXiv:2409.13740](https://arxiv.org/abs/2409.13740).
14. D'Arcy, M., Hope, T., Birnbaum, L., and Downey, D. “MARG: Multi-Agent
    Review Generation for Scientific Papers.” arXiv 2401.04259v1 (2024).
    Preprint. [arXiv:2401.04259](https://arxiv.org/abs/2401.04259).
15. Walters, W. H., and Wilder, E. I. “Fabrication and errors in the
    bibliographic citations generated by ChatGPT.” *Scientific Reports* 13,
    14045 (2023). Peer-reviewed article.
    [doi:10.1038/s41598-023-41032-5](https://doi.org/10.1038/s41598-023-41032-5).
16. International Committee of Medical Journal Editors. “Use of AI by Authors.”
    Current editorial recommendation checked 2026-08-16.
    [ICMJE guidance](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html).
17. Springer Nature. “AI guidance for researchers and communities.” Current
    publisher policy checked 2026-08-16.
    [Springer Nature guidance](https://group.springernature.com/gp/group/ai/ai-guidance-for-our-researchers-and-communities).

## Appendix A: Evidence and Coding Method

### A.1 Source freeze and deduplication

Each manuscript revision begins with separate cutoffs for repositories, mutable
agent stores, live APIs, and audit-time artifacts. Repository claims name a
pinned revision. Mutable histories name the extraction time and filter, and are
not described as byte-reproducible. A later extraction is a new observation.

The default session unit is a provider's top-level conversation. Parent-child
metadata, legacy and bridge identifiers, working directory, timestamps, and
content overlap connect continuations, imported histories, subagents, and
specialists to one canonical lineage. Workflow journals, scratchpads, and tool
results remain trace material rather than additional conversations. Records
are assigned to a case only when repository or worktree metadata supports the
assignment. The current paper-production lineage is excluded from historical
case counts. Finally, cross-provider work on the same proposition is merged at
the episode level; session totals are never added to estimate ideas or output.

To reproduce the inventory, an auditor applies those rules in order, records
every included canonical root and linked derivative, checks that all 31 episode
IDs occur exactly once, and reconciles origin and status totals to the row-level
IDs in the evidence ledger. Exact private transcript contents are not required
for the published count; an authorized auditor can resolve the private locators
without releasing the histories.

### A.2 Episode construction and coding

An episode begins with a bounded proposition and ends when the reviewed record
supports a final status or a dated open state. The coding row records case,
date, proposition, origin (`human`, `agent`, `external`, or `mixed`), prior
evidence, pre-outcome confidence, human intervention, local outcome, external
outcome, final status, lesson, and source locator. The six final statuses are
`confirmed`, `partially supported`, `refuted`, `invalid experiment`,
`superseded`, and `open`. Status belongs to the proposition, not to the provider
or artifact. A functioning implementation can coexist with a refuted efficacy
claim; a broken control produces `invalid experiment`, not a negative result.

Origin is coded conservatively. Agent generation is `agent` only when no
material human or external contribution shaped that proposition; public-method
reproduction remains `external`, and substantial combinations are `mixed`.
Human challenge, approval, or closure is recorded independently of origin.
Because one author performed the interpretive coding, a later recode must keep
the old row, state the changed field and reason, and recalculate descriptive
totals rather than silently changing history.

### A.3 Evidence authority and claim promotion

The method uses three authority tiers without treating them as interchangeable.
Tier 1 is a direct record: a primary publication or policy page, pinned code or
artifact, exact local measurement, or identified external submission row. Tier
2 is a triangulated finding supported by at least two appropriately independent
Tier-1 records. Tier 3 contains inference, retrospective testimony, and open
hypotheses. Within Tier 1, local measurements and live observations answer
different questions; neither automatically outranks the other. A claim may be
promoted only to the scope established by its source, control, and evaluator.
Exact scores retain submission status, comparator, retrieval time, and whether
the record was independently queried or merely present in a project ledger.

### A.4 Quotations and privacy

Only excerpts about hypothesis formation, confidence, correction, intervention,
or governance are eligible. Each must be short, authorized, and privately
traceable to case, provider, parent or child session, timestamp, speaker, exact
location, surrounding context, redaction, and intended manuscript use. Secrets,
credentials, unrelated personal material, third-party personal information,
and context-altering truncation are excluded. If safe redaction changes meaning,
the text is paraphrased or omitted. Public appendices disclose quote IDs and
method, not raw histories. Quote IDs are thematic: Q04 on 2026-06-30 corrects an
earlier approximately 570 boundary and predates Q02 on 2026-07-01, so it is not
a retraction of Q02's distinct approximately 465 claim.

### A.5 Cost and oversight accounting

Costs are recorded by date, vendor, currency, amount, case allocation, source,
and whether they are direct usage, subscription, compute, or other expense.
Only receipt- or billing-supported amounts may enter an independently confirmed
total. Shared subscriptions remain cross-case unless a documented allocation
rule exists; missing subscription prices are reported as unpriced, not zero.
The current USD 100 OpenRouter and USD 30 Modal figures, additional subscriptions,
and 2–5 hours per day of oversight remain retrospective testimony. Human time is
reported separately from cash cost and is not monetized without a declared rate
and contemporaneous time record.

### A.6 Post-competition update procedure

1. Freeze the prior manuscript and ledger state; add a new UTC cutoff for every
   repository, mutable store, official results page, and API query.
2. Retrieve official final submissions, statuses, scores, rankings, and relevant
   deadlines. Preserve identifiers and raw statuses. For ARC, do not promote a
   project-ledger value until the external record has actually been queried.
3. Append every newly completed, failed, cancelled, or still-pending arm. Never
   infer an unrun arm's result from a companion submission.
4. Reconcile the reserved fields in Section 11: final objective verdict, score,
   rank, Working Note outcome where applicable, Qwen 3.8 transfer if executed,
   receipt-supported costs, measured oversight if available, and interpretation
   changes. “Not measured” remains a permissible final value.
5. Recode an episode only when new evidence changes its bounded proposition;
   retain the previous code, reason, and date. Recalculate all descriptive
   totals and citation-reference checks.
6. Recheck the target venue's current authorship and AI-disclosure rules, issue
   a dated change note, and obtain sole-author approval before submission.
