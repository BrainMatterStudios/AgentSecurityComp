# Access Without Autonomy: An Instrumented Case Study of AI Agents in Computational Research

## Abstract

Large-language-model agents can search literature, inspect repositories, write
and run code, and maintain long workflows, but those capabilities do not
establish scientific autonomy. This comparative single-participant (N-of-1)
case study examines one experienced technologist's use of coding agents in two
unfamiliar competition-based domains: AgentSecurityComp and ARC-AGI-3. Evidence
combines private agent histories, pinned repository revisions, experiment
artifacts, authenticated submission rows, and retrospective testimony.
A purposive, maximum-variation sample of 38 research episodes was coded for
proposition origin, evidence, human intervention, outcomes, status, and lesson.

Agents inspected software contracts, implemented candidate mechanisms, built
harnesses and controls, repaired parsers and model-serving paths, and preserved
negative results. The record was weaker for dependable hypothesis selection,
causal identification, calibrated interpretation, and independent originality.
Eight claims were confirmed, ten partially supported, ten refuted,
five were invalid experiments, one was superseded, and four remained open.
These labels describe the selected episodes, not agent accuracy. Human review,
estimated retrospectively at 2–5 hours per day, was integral to the system.

Neither top-prize objective was won. After AgentSecurityComp closed, an
authenticated query returned rank 171 of 4,186. The author separately reported
a Silver notification of 173 of 4,251, but no notification artifact was
retained. Across the entrant's complete retained submission population, 38 of 49
scored rows returned exactly 0.000 on the private board and all 11 positive rows
came from the confused-deputy `email.send` line, so the public throughput axis that organized
most of the work was worth nothing on the board that decided the prizes; the
mechanism behind that dissociation remains unobserved. ARC-AGI-3 remained
ongoing and unachieved, though its public rank rose to 26 of 2,892 by cutoff-3
on a byte-copy of a public competitor notebook whose byte-identical redraws
spanned 2.45 to 4.31. With no human-only control and unequal, changing case
conditions, the study supports one careful conclusion: agents lowered the
perceived barrier to computational research and executed useful work, but did
not demonstrate dependable scientific autonomy. The resulting governance
protocol emphasizes direct-source verification, falsifiable hypotheses,
matched controls, separate local and external gates, untrusted-memory review,
and human approval for scarce evaluations.

## 1. From Enterprise Architecture to Computational Research

I came to these projects after more than 16 years in consulting: real-time
decisioning and omnichannel AI, including Naive Bayes and gradient-boosting
systems; enterprise and solution architecture across cloud and on-premises
environments; more recent agentic-AI work; and Java development early on. That
background transfers to systems design, integration, and structured problem
solving. It does not make me an expert in agent security, ARC-AGI-3, research
practice, or Kaggle. My own coding was rusty, and most of my Python had been
written with AI help rather than from scratch. So this is not a novice against
an expert, and not a claim that general technical experience substitutes for
knowing a competition domain. It is what happened when an experienced
technologist entered two unfamiliar ones, carrying real strengths and real gaps.

The original experiment was deliberately ambitious. I wanted to see how far an
agent-led process could go if I withheld domain guidance instead of feeding it
hypotheses. In the first case I told the agent to "continue to work in loops and
iterations until you solve the challenge." That licensed persistent
investigation. It did not license changes to shared systems or submissions I had
not seen. My job was to approve, challenge, press for breadth and depth, and
decide when something was ready to leave my machine for a scarce live
evaluation.

None of that was hands-off. Looking back, I estimate 2–5 hours a day spent
reading claims, demanding better tests, redirecting work, and deciding what
could proceed; I did not track the time, so treat the number as testimony. I
also believe the agents let me take part in domains I would otherwise have found
hard to enter, and learn something while doing it. That is how it felt. It is
not a measurement of time saved. There was no human-only control, and neither
project had won anything by the 2026-08-16 cutoff. Neither won a top prize
afterwards either; Section 12 records the final AgentSecurity standing and
Section 13 the state of an ARC-AGI-3 still in progress.

Those distinctions give the paper its title. Access is being able to turn a
question into work that runs: read an unfamiliar codebase, implement a candidate
mechanism, check it, keep the result, design the next test. Autonomy would need
more—picking questions worth asking, designing experiments that can answer
them, reading the answers honestly, contributing something of one's own, and
catching one's own mistakes before a human does. The cases ask which of those
these agents actually had.

## 2. What Counts as an AI Research Agent?

*Agent* covers systems of very different scope. A conversational assistant
answers a bounded prompt. A tool-using LLM agent chases a multi-step objective:
reading files, searching a corpus, editing and running code, checking results,
revising a plan. A closed-loop scientific system goes further, tying hypothesis
selection to real experiments and to the choice of what to try next. Throughout
this paper *AI research agent* means the middle case — an LLM-based system given
enough tools and persistence to do substantial parts of a computational research
workflow. The label describes what the system does. It is not evidence that the
system is a scientist.

Publication status matters to how much weight a source carries, so the studies
below are peer-reviewed articles unless called a preprint.

### 2.1 Bounded robot scientists and autonomous laboratories

Closed-loop automation predates LLM agents. In *Nature* in 2004, King and
colleagues described a robot scientist that generated, selected, and tested
gene-function hypotheses in a yeast metabolic model [1]. The loop was
experimentally real and tightly bounded: deletion mutants, growth assays, a
hand-built logical model. A 2020 *Nature* study reported a mobile robotic
chemist running 688 experiments over eight days inside a ten-variable search
space [2]; humans still set the study, the hypotheses, the objective, the
apparatus, and the space itself. A 2023 *Nature* article described an autonomous
materials laboratory that combined literature-trained models, computation,
robotics, and active learning to realize 36 of 57 targets in 17 days [3]. Humans
chose the target class and the permitted precursors, and inconclusive
measurements needed manual follow-up.

These systems are substantially autonomous *inside an engineered envelope*. That
is not general scientific autonomy, and their constraints differ from a coding
agent's. A laboratory couples a fixed objective to instruments and feedback. An
LLM agent roams between literature, code, conjecture, and prose with no reliable
way to tell whether the resulting chain holds together.

### 2.2 LLM agents across the research workflow

The literature now spans ideation, synthesis, coding, reproduction, review, and
paper generation, and the task boundaries matter as much as the headlines. Park
and colleagues fed GPT-4 materials-science problems and got hypotheses, along
with a high error rate and a need for expert evaluation [4] — a demonstration,
not a validated discovery. ScienceAgentBench (ICLR 2025) turned 102 tasks from
44 papers into verifiable programming problems; baselines solved only a minority
even with repeated attempts and expert hints [5]. These are self-contained
tasks, not research programs. A 2026 *Nature* article on Co-Scientist reported
biomedical hypotheses with preliminary in-vitro validation, with experts in the
loop throughout and the evidence concentrated in one field [6].

The broader claims come from preprints. Data-to-paper linked data, code,
results, and prose well enough to produce simple manuscripts on autopilot, and
its authors reported thin novelty, real errors, and a rising need for human
co-piloting as complexity grew [7]. The AI Scientist ran ideation, small
experiments, writing, and simulated review end to end from seed code, and
reported implementation failures, weak rigor, misleading conclusions, and
occasional invented results [8]. Producing a paper is not the same as making a
discovery.

The benchmarks say much the same. DiscoveryBench found performance falling
sharply as workflow and domain complexity rose, its best system reaching 25% on
the authors' metric within a benchmark that excluded several hard workflow
classes [9]. CORE-Bench put the best agent at 21% on its hardest level, even
though reproducing work from an existing repository is far narrower than doing
new work [10]. PaperBench had its best agent completing 21% of rubric-weighted
requirements across 20 replication tasks, and on a three-paper subset it did not
beat the recruited ML-PhD baseline [11]. Expert reviewers rated LLM-generated
NLP ideas as more novel on average but slightly less feasible than human ones,
though nobody executed the ideas, novelty judgments are subjective, and the
system could not rank its own output reliably [12]. A literature agent did well
on defined retrieval and synthesis tasks while producing context-dependent
contradiction labels and overconfident answers [13]. A multi-agent reviewer beat
its single-agent baselines; its automated alignment had the best recall but
worse precision and Jaccard than human-review alignment, while a nine-participant
study still found more good and specific comments [14]. Those two metrics answer
different questions, and both need someone accountable reading them.

Even the clerical parts need checking. A *Scientific Reports* study of 84
generated literature reviews found fabricated citations, and errors inside real
ones, in the April 2023 ChatGPT snapshots tested [15]. Those rates say nothing
about today's systems. The lesson survives anyway: a citation-shaped string is
not provenance.

Together this supports a capability map, not a single autonomy score. Agents can
do useful pieces of research and can sometimes string many pieces into a long
workflow. They also degrade with complexity, hidden evaluation, broken controls,
unreliable self-assessment, and weak provenance. So this paper treats them as
research executors whose output earns trust one episode at a time, and refuses
to read autonomy off fluency, tool use, conversation volume, tokens, or a
finished manuscript.

## 3. Research Questions and Method

### 3.1 Research questions

1. How far do AI agents lower the entry barrier for an experienced technologist
   moving into an unfamiliar computational-research domain?
2. Which research tasks do they do well?
3. How much scientific direction and originality appears without domain-specific
   human guidance?
4. Where do they fail — confident error, thin due diligence, stale memory,
   imitation, and the gap between local and live results?
5. Which human practices make the work more reliable and more useful?

### 3.2 Comparative N-of-1 design and case boundaries

This is a longitudinal, comparative N-of-1 study of one researcher using several
AI coding agents. AgentSecurityComp is the primary case and ARC-AGI-3 the
comparison. The comparison is analytical, not controlled: the two cases surface
recurring activities and failure modes in different technical settings, but they
were not randomly chosen or run under matched conditions. OpenCode/DeepSeek
supplies supplementary evidence only. It is not a third case and not a
provider-comparison arm.

The corpus combines Claude Code, Codex, and OpenCode/DeepSeek session records
tied to the two repositories; Git history and pinned artifacts; experiment
scripts, logs, and result records; and an approved set of author interview
responses. Repository and transcript evidence establishes what happened in the
projects. Literature and policy sources supply context and prove nothing about
either project; they are limited to primary papers, official publication
records, and official editorial-policy pages already checked in the evidence
ledger.

Four companion documents carry the evidence. The
[evidence ledger](evidence/ai-agents-research-evidence.md) registers every coded
episode and admitted quotation by source ID. The
[public episode ledger](evidence/episode-ledger-public.md) reproduces all 38
episodes with their public locators — commits, submission references, repository
paths, published records — and private trace identifiers redacted, so a reviewer
can check the tallies without access to the controlled histories. The
[source-availability manifest](evidence/source-availability-manifest.md) records
what survived an audit on 2026-09-04: seven of ten canonical Claude files and
all 15 canonical Codex files were present at their recorded paths. Three Claude
originals were missing, so claims resting on them fall back to repository
corroboration, another record, or an explicit testimony label. The
[cutoff-2](evidence/cutoff-2-live-results-2026-09-04.md) and
[cutoff-3](evidence/cutoff-3-live-results-2026-09-08.md) artifacts hold the later
competition observations and their claim limits. The hash manifest was not
re-run at cutoff-3; its 2026-09-04 state stands.

By the author's own account, Claude Code was the main research system, and Codex
and OpenCode/DeepSeek came in mostly to reset perspective when the primary line
looked stuck, repetitive, or settled too early. Tasks, dates, models, budgets,
and exposure all differed. Session and token totals therefore describe usage,
not contribution, quality, or provider merit. (Testimony: author baseline and
interview)

### 3.3 Research episode and coding scheme

The unit of analysis is a bounded research episode, not a message, turn,
subagent, commit, or submission. The corpus is a purposive maximum-variation
sample, not a census. An episode qualified when it carried a proposition
specific enough to adjudicate, evidence traceable before or after the test, an
implementation or experiment or explicit adjudication, and a lesson supported
well enough to code origin and status. Routine debugging, operational work,
duplicate provider continuations, repeated variants raising no new evidentiary
question, and propositions too thin to adjudicate were left out.

Each episode tracks one proposition as far as the record allows: the hypothesis;
whether it appears to originate with a human, an agent, an external source, or a
mix; the evidence cited beforehand; the implementation or experiment; human
review; the local outcome; the live outcome; the final status; when any
correction came; and the lasting lesson. The same inquiry continued in a second
provider stays one episode.

That gives 38 episodes: 17 AgentSecurityComp, 16 ARC-AGI-3, five OpenCode.
Thirty-one were coded at the 2026-08-16 cutoff, two more at cutoff-2
(Section 12), and five at cutoff-3 (Section 13). Origin is coded conservatively
as `human`, `agent`, `external`, or `mixed`; an agent's proposal is not coded as
autonomous discovery when human or external input shaped the same episode.
Status is `confirmed`, `partially supported`, `refuted`, `invalid experiment`,
`superseded`, or `open`, and belongs to that row's proposition alone. Local and
live outcomes stay in separate fields so a working implementation is never
mistaken for a transferred effect.

Codes also cover external-method dependence, infrastructure value, recombination,
experimental validity, calibration, correction, stale memory, human challenge and
approval, provider switching, operational failure, and domain learning. The
coding is interpretive, and no second coder worked blind, so there is no
inter-rater reliability figure. The counts describe this sample. No denominator
of all possible episodes exists, so the status distribution does not generalize
past the rows themselves.

### 3.4 Provenance and deduplication boundaries

Sessions are counted at the level of a provider's top-level conversation.
Subagents, specialists, workflow journals, scratchpad copies, bridge records,
and tool-result derivatives are linked to a parent or kept only for
traceability, never counted again. Imported, forked, and overlapping histories
are not summed. Provider metadata, working directory, timestamps, canonical
identifiers, and content overlap pick the most conservative lineage to retain. A
content match joins a case only when metadata places the work in that repository
or one of its worktrees. The Codex lineage used to write this paper is excluded
from the historical counts.

These rules stop conversation volume from passing as research output. They do
not prove intellectual independence: paraphrase and short copied fragments slip
past exact-content checks, and mutable agent stores can yield a different
inventory on a later extraction. Where several agents, imported histories, or
repeated prompts circle the same question, episode-level deduplication overrides
provider totals.

### 3.5 Evidence classes, quotation, and claim control

Claims are classified internally as source fact, local measurement, live
observation, triangulated finding, inference, retrospective testimony, or open
hypothesis. The prose does not tag every sentence, but it holds the distinctions.
A local result cannot establish live efficacy. A transcript cannot stand in for
code or evaluator output. Author estimates about oversight, value, trust, and
cost stay testimony unless something independent corroborates them.

Private histories are source material, not an appendix. Only short excerpts
bearing on hypothesis formation, confidence, correction, intervention, or
governance may be quoted, each with `authorized` status in the private trace and
with provider, case, session, timestamp, speaker, location, context, and
redaction retained. Secrets, credentials, unrelated personal material, and
misleadingly truncated passages are excluded. Quote identifiers are thematic,
not chronological: Q04 is dated 2026-06-30 and Q02 2026-07-01, so Q04 cannot be
read as retracting Q02. They concern different ceiling claims.

Anything an AI produced — claim, summary, citation, interpretation — needed an
independent source check before it entered the manuscript. ICMJE and Springer
Nature guidance both bar AI tools from authorship and keep accountability with
the human [16,17], though those are general and mutable policies rather than
evidence about this project. Sole authorship and the specific roles of Claude
Code, Codex, and OpenCode/DeepSeek are declared below, and the target venue's
live rules will govern at submission.

### 3.6 Living evidence policy

Section 11.1 sets out what this design cannot support. The short version is that
there is no human-only control, no matched budget, and no stable model baseline,
so nothing here becomes a productivity estimate or a provider ranking.

What belongs here is how the record is kept. This is a living manuscript. The
inventory is pinned to AgentSecurityComp at commit `2ed68e8`
(2026-08-16T10:29:29+03:00) and ARC-AGI-3 at `ebe5b3e`
(2026-08-15T18:41:01+03:00), with the mutable Claude, Codex, and OpenCode stores
extracted at 2026-08-16T08:06:05Z under filters recorded in the private ledger. Pinned
revisions bound repository claims; they do not imply that every transcript
refers to the same revision. Completed, pending, superseded, failed, and
unresolved experiments stay distinct in every later revision. New results get a
new dated cutoff and never silently overwrite a negative or unresolved outcome,
and final rankings, costs, and conclusions are added only once the supporting
records have been checked. Two cutoffs have since been appended: cutoff-2 on
2026-09-04 (Section 12) and cutoff-3 on 2026-09-08 (Section 13). ARC-AGI-3 was
still open at the latest one, so its numbers are a dated mid-competition state
rather than a result.

## 4. Case I: AI Agent Security

**Outcome-evidence note.** The independently retrieved AgentSecurity
live-results artifact is frozen at 2026-08-16T10:56:15Z. Selected rows were
rechecked four times that day, at 11:10:21Z, 11:26:07Z, 11:59:48Z, and
12:44:16Z; none of those rechecks replaces the frozen table. The 11:26 recheck
resolved the early `ERROR` rows discussed below, and the last two tracked the
L31 arms to completion, as described in 4.4. Every live observation postdates
both the repository cutoff at 2026-08-16T07:29:29Z and the mutable-history
snapshot at 2026-08-16T08:06:05Z. (AgentSecurity live-results ledger:
`paper/evidence/working-note-claim-ledger.md`; AI evidence cutoff table)

### 4.1 Entering the executable problem

The case opened on 2026-06-13 with a deliberately broad instruction to keep
iterating toward the objective. The agent worked first against a mock scaffold,
then read the actual SDK and ported the attack onto its real `AttackCandidate`
interface. It also raised the number of candidate attacks, having read the
scorer as additive: more valid candidates, more scored findings. The real path
ran and carried every later submission; the extra volume set a baseline and
solved nothing. Both were competent acts of inspection and implementation. They
are not evidence that the system picked an important direction on its own, and
verification and submission approval stayed with the human. (Episodes
AS-S01-AS-S02; Quote Q01)

On 2026-06-27 the contract itself changed the problem. Fabricated secret-like
strings had stopped scoring, because SDK 3.1.2 wanted a literal `SECRET_MARKER`
or a value genuinely read from the protected file. The agent adopted the
documented marker, checked marker-bearing exfiltration locally, and scoring
resumed. This is why plumbing can be research: a plausible attack was worth
nothing until it obeyed the evaluator's protocol. The repair also came straight
from SDK semantics and a zero score, so executing it well is not the same as
discovering something. (Episode AS-S03)

Two early statements show correction and unstable confidence side by side. On
2026-06-30 the agent withdrew its own approximately 570 boundary once exact
model behavior contradicted it, and the human that day declined to decide and
asked for thorough local verification. On 2026-07-01 the ledger records a fresh
claim that both models were stuck near a 465 boundary and a 44-point ceiling,
which later work weakened. So the June 30 correction comes before the July 1
claim and retracts nothing. The canonical Claude file holding all three extracts
was missing at the 2026-09-04 re-audit; they are prior ledger extracts, not
re-opened originals. (Quotes Q02-Q04; Episode AS-S10; source-availability
manifest)

### 4.2 Practical value through adaptive sizing

The clearest value vignette landed on 2026-07-25, and it was not an invention.
Higher-scoring public solutions reportedly sized their output from time observed
in the live environment. The agent rebuilt that in bounded form: measure how
long accepted candidates take, estimate how many fit the evaluator's budget, and
stop before the whole submission risks timing out. Local replay-safety checks
passed. A later API recheck then found all five L6 rows at status `ERROR`. The
adaptive arm shows 80.145 against a 64.800 control, but a score on an `ERROR`
row is not a completed live effect. What the episode demonstrates is faithful
translation of a public method into this repository, verified locally. Good
engineering, unproven externally, nobody's original idea. (Episode AS-S04;
Source AS-S04)

The throughput work that followed is the reason local and live results are kept
in separate fields. On 2026-07-26, stopping decoding once the tool call closed
cut a local timing from 1.23 to 1.03 seconds; the two matched L7 rows differ by
1.440 points and both are `ERROR`. On 2026-07-27, packing several messages into
one model call again looked good in the local timing model; no live description
matched the planned L8 ladder, and every later L9 packing row is `ERROR`, their
visible scores below the single-post row. The code ran and the measured overhead
moved. Whether either mechanism helped a completed competition run stayed open.
(Episodes AS-S05-AS-S06)

### 4.3 Failure through non-identifying experiments

August brought something worse than negative results: tests that could not
identify the cause they proposed. On 2026-08-04 the agent read Gemma's poor
result as model weakness, but the comparison ran on an under-powered message
frame. That same weak frame drove GPT to zero, and only a faithful
commitment-forge frame later separated the two models. With a broken control the
comparison is an invalid experiment. It neither refuted nor confirmed the model
hypothesis. (Episode AS-S07)

The router ladder on 2026-08-08 showed the same lesson at scale. The agent built
deterministic board routing and workload splitting, and both the router and its
self-measurement worked locally. Live arms scored 42.665-47.865 against a 44.320
baseline, no stable gain. The deeper problem is that the arms overlapped in what
they changed, so their different scores could never isolate routing as the
cause. Several named variants do not make an experiment controlled; the arms
have to move different mechanisms. Status: `invalid experiment`, neither a
breakthrough nor a clean negative. (Episode AS-S08; Source AS-S08; live-results
ledger, the five L20 rows)

### 4.4 Public dependence, human gates, and the late ladders

On 2026-08-09 the agent reproduced the public dimong4/nctuan commitment-forge
method, which pushes a reasoning model to commit several tool posts inside one
candidate. The project record says four posts per candidate fired as designed,
and the live result was 47.850 against 43.600 for the single-post control.
Recombination then paired that borrowed mechanism with dual-board routing and a
Gemma variant: dual arms at 81.985 and 82.660, and an N=600 Gemma isolate at
34.000 against 27.000 for Gemma single. The N=900 follow-up narrowed to 35.000
against 34.605, and the N=1200 forge reached 35.375, so the isolate's early gain
proved neither durable nor scalable. Bounded component behavior was supported;
the stated reproduction target was not reached and the remaining ceiling went
unexplained. Public method, agent execution, and human selection all stay
visible in the attribution. (Episodes AS-S09-AS-S10; live-results ledger, the
L21-L22 rows)

Governance grew more explicit as confident explanations piled up. The human
approved bounded ladders, demanded controls, and on 2026-08-09 told a fresh
system to “do not trust the memnory or recorded info, validate everything”. That
memory-blind audit rechecked code and evidence and produced no completed live
adjudication before the cutoff. Its value was discipline rather than score:
recorded conclusions became claims to revalidate instead of premises to inherit.
The second provider was a reset, under human direction, not corroboration of the
first. (Episode OC-S02; Quote Q05)

The last dated ladders came back mixed or negative. On 2026-08-12 two proposed
throughput knobs collapsed into one effective axis before L27, the project's
label for that controlled ladder, whose *probe-hop* arms ran a one-hop
calibration probe before sizing the candidate set. The human insisted on both
tests and a control; the arms scored 50.295-57.620 against an 88.730 control. On
2026-08-13 the GPU path was made to work, and its best arm scored 50.175 against
an 83.115 historical CPU threshold — refuting that narrow threshold claim, not
establishing anything causal about CPU versus GPU, since no same-batch hardware
control existed. L29 ran on 2026-08-15 at 85.675, under the historical 88.730,
refuting its threshold target without causally rejecting routing. At the frozen
cutoff L31 had four pending *chain-pack* arms, which put several multi-hop
messages inside one candidate; only the companion *fast-emit* arm had run, at
25.145. The 11:59:48Z recheck found one chain-pack arm complete at 73.605 with
three pending and no matched control, and by 12:44:16Z all four were in at
79.985, 79.365, 73.605, and 54.375. All sat below the historical 88.730, and
none of those unmatched comparisons identifies a chain-pack effect. The winning
objective remained unachieved as retrospective testimony. (Episodes
AS-S11-AS-S14; Testimony: living outcomes register; live-results ledger, the
L27-L31 rows)

### 4.5 Case evidence summary

Table 1 separates what the agent executed from what the human governed and what
the work inherited from external systems. Its outcomes are episode
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

**Outcome-evidence note.** Every ARC score in this section is a repository
record — project ledger, protocol, design note, transcript, or result artifact —
identified in the episode source register. Each shows what the project recorded,
not a fresh verification, and the qualification holds for the whole section
rather than being restated at each result. Nothing here was re-queried from the
platform at the 2026-08-16 cutoff. Sections 12.2 and 13.2 later did query it,
and several of these rows now match authenticated public submissions. (Sources
ARC-S01-ARC-S16; AI evidence ledger, known evidence gaps)

### 5.1 Exploration, search, and evaluator boundaries

ARC-AGI-3 posed a different problem: act inside interactive games whose state,
goals, and evaluator lifecycle were only partly visible. Agent-led exploration
had room to run, but its hypotheses still met human challenge, local harness
tests, and scarce external evaluations. On 2026-06-29 the agent proposed a
double reset between plays. An eval-faithful validation that day reported a
2.6-152-fold effect on 15 of 25 games once the no-op was repaired; a handoff on
July 1 recorded a 7-109-fold local range. The two artifacts use different ranges
and contexts, so neither is treated as the definitive local estimate. In
competition mode the second play returned HTTP 400, which made the test invalid
for the deployment setting it claimed. Exploration produced an executable idea
and could not supply the evaluator permission the idea depended on. (Episode
ARC-S03; Source ARC-S03)

On 2026-07-01 the agent noticed that scoring kept the best run and built
search-and-replay: find a solved path, then replay the action sequence cleanly.
The design record says it solved all 25 development games. That is a substantial
harness result, and the scoring trick did not survive external conditions. The
conclusion splits: the solver worked locally, the transfer claim did not. Calling
the development sweep an autonomous solution would erase both the hidden
evaluator boundary and the human insistence on external checks. (Episode
ARC-S02; Source ARC-S02)

### 5.2 Serving identity and development-to-hidden reversal

The sharpest validity failure came on 2026-07-11. A fine-tuned LoRA adapter
appeared to beat its base model at 1.26, and the agent was confident before the
human asked for proof of which model was actually deployed. The audit found the
adapter had never served: generation ran on the base model. Treatment and
control were the same model, so this is an `invalid experiment`, not a failed
fine-tune. The general point is that model serving is part of the experiment
rather than plumbing around it. The canonical Claude file was missing at the
2026-09-04 re-audit, so the diagnosis stands as a prior ledger extract
corroborated by repository evidence. (Episode ARC-S05; Quote Q06; Source
ARC-S05; source-availability manifest)

A failure on 2026-07-12 was valid enough to teach something. Reducing prompt
tokens raised the development mean from 0.89 to 1.96, and the hidden-evaluation
entry came back at 0.73. Unlike the LoRA episode this intervention genuinely
ran; it simply did not generalize. That reversal is what separates a refuted
transfer claim from an invalid comparison, and it is why a large local delta
cannot stand in for a held-out result. (Episode ARC-S08; Source ARC-S08)

An executable-world-model policy, which tested proposed actions against an
internal model before acting, adds a third status. Independent code review on
2026-07-14 found and repaired defects, and later campaigns then displaced the
policy without any durable isolated gain. The implementation got better while
the efficacy claim became `superseded` — neither confirmed nor cleanly refuted.
Keeping that status stops later work from turning a repaired artifact into a
result it never produced. (Episode ARC-S04)

### 5.3 Harness and perception as research infrastructure

The clearest value in this case came from measuring and improving the harness
itself. On 2026-08-01 four same-versus-same replicate pairs showed
root-mean-square variation of 0.707 game levels per pair, a scale summary of the
paired evaluation noise. Two preregistered gates turned out to be under-powered,
so no external-effect claim was made and the protocol was amended. Measuring the
noise before reading small differences turned an unreliable comparison into a
stated instrument limit, and the governance rule followed: every submission is
an experiment with a question, a control, and a decision gate, not an isolated
leaderboard try. (Episode ARC-S06; Source ARC-S06)

Perception work made that concrete. On 2026-08-03 the agent fixed slow-tick
heads-up-display bars by virtually rotating and masking them; retained replay
and regression cases passed, and no leaderboard gain was claimed. On 2026-08-09
the goal-inference input changed from a flat object list to a role-typed,
HUD-masked scene, letting the reasoner tell the controllable object from the
target and the context while volatile status elements were suppressed. The
retained comparison moved from 0/9 to 6/6. Both role typing and HUD masking
changed at once, so nothing isolates which one did the work, and neither has a
separable external attribution. These are real improvements to seeing and
testing, not an end-to-end competition advance. (Episodes ARC-S01, ARC-S07;
Sources ARC-S01, ARC-S07)

### 5.4 Hypothesis closure and public-signal noise

Hypotheses here were closed rather than left alive on plausibility. A structural
plan channel with braking and phase gates ran on 2026-08-09 and stayed inside
the established score band. On 2026-08-10 best-of-N candidate selection worked
in the harness, but the reset it needed was swallowed in competition mode and
the second play failed. A repaired duck-memory namespace strategy also stayed
inside its registered 0.69-1.30 interval — *in-band* — at 0.83. Better
structure, working local selection, and repaired state were all genuine
implementation work, and none of them established the breakthrough proposed.
(Episodes ARC-S09-ARC-S10; Episode OC-S05; Sources ARC-S10, OC-S05)

External signals were not automatically trustworthy either. On 2026-08-09 an
OpenCode/DeepSeek campaign folded nine linked specialist searches into a
research document, and a later audit found the assumed corpus came from the
wrong model. Breadth cannot repair provenance, so the episode is an `invalid
experiment`. Earlier, a proposed duck-sparse 35B arm looked good until a serving
audit showed its path had never executed, and the human killed it before reset —
costing a slot but producing no external negative either. In both, human
challenge closed an attractive but unsupported hypothesis before it ate more
evaluation. (Episodes OC-S03-OC-S04)

The correction became a gate rather than a memory of failure. A later adapter
comparison opened with the rule “Serving identity proven first,” and
deterministic controls established which model was running before anyone read
an outcome. Together with memory-blind reassessment, which treats stored
conclusions as untrusted until rechecked, that made provenance and deployment
identity preconditions for a claim instead of cleanup after a surprising score.
These gates came from human challenge and agent execution together. They do not
make the agent the arbiter of its own validity. (Quote Q07; Episode ARC-S05;
Episode OC-S04)

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

Ordinary accounts of agentic research collapse six different claims into one.
*Access* is getting into an unfamiliar technical domain and starting useful
work. *Execution* is turning a proposed mechanism into code, instruments, and
experiments. *Insight* is an explanation the evidence supports over its rivals.
*Originality* is about where the question or method came from. *Reliability* is
producing valid, calibrated results episode after episode. *Autonomy* would mean
holding all five together dependably, correcting itself and stopping when it
should, without a human spotting the critical mistake first. These cases show
access clearly, execution substantially, insight in places, and not
much dependable originality, reliability, or autonomy. (Episodes AS-S01-AS-S17;
Episodes ARC-S01-ARC-S16; Episodes OC-S01-OC-S05; Testimony Q08-Q09)

The origin codes support that split, with a caveat. Of 38 episodes, 16
propositions are coded `agent`, 18 `mixed`, four `external`, none `human`. No
human-origin rows is a fact about where propositions appeared to start, not
evidence that humans contributed no thinking; the 18 mixed rows and the
intervention column are full of human framing, challenge, approval, demands for
controls, and claim closure. An agent-origin proposition is not automatically
original either. It can recombine inherited methods, chase an already visible
failure, or end up refuted, invalid, superseded, or open. (AI evidence ledger,
descriptive measures and derivations, all 38 episode IDs)

### 6.2 Access without mastery; execution without dependable originality

The strongest cross-case result is access without mastery. The agents found
their way through unfamiliar SDKs, evaluator protocols, model-serving paths,
game harnesses, and experimental artifacts well enough to make both projects
run. That matches the author's sense that the tools allowed real participation
and real learning. It does not show that anyone acquired domain mastery, and
with no human-only control it measures no productivity effect at all. (Episodes
AS-S01-AS-S03; Episodes ARC-S02, ARC-S05-ARC-S07; Testimony Q08; Testimony:
author baseline and interview)

Execution held up better than interpretation. Agents ported interfaces, repaired
parsers, built routers, got a GPU path working, audited which adapter was
serving, wrote controlled runners, and kept result artifacts — several of which
stayed useful after the claim that motivated them failed. A working router did
not identify a routing effect. A working GPU path did not establish a CPU
bottleneck. Repaired policy code did not establish durable superiority. Building
the artifact proves execution; insight needs a comparison that identifies the
cause and a result that survives the evaluation boundary that matters. (Episodes
AS-S01, AS-S08, AS-S12; Episodes ARC-S04-ARC-S05, ARC-S07)

Adaptive sizing and the commitment forge show how to attribute recombination.
Both mechanisms came from outside. The agents brought them into the repository,
tested them, and in the forge case combined the reproduction with board and
model variants. Reuse with its provenance intact is not plagiarism. It is also
not discovery. What is claimed here is implementation, adaptation, and component
testing — not inventing the public mechanism, and not hitting the reproduction
target either. (Episodes AS-S04, AS-S09-AS-S10; Testimony Q09)

### 6.3 Review, confidence, and evidence authority

Human oversight was part of the machine, not a backstop bolted to it. The
author's estimate is 2–5 hours a day of review, challenge, redirection, and
approval. Across the episodes that intervention exposed broken controls, forced
proof of which model was serving, required hidden or competition-mode tests,
kept unresolved arms pending, and stopped an unserved proposal from spending a
live slot. The learning happened in that loop: agent proposals turned
assumptions into something concrete, and adverse review turned them into
reusable gates. This is supervised execution at scale, not hands-off autonomy.
(Episodes AS-S07-AS-S08, AS-S11, AS-S14; Episodes ARC-S05, ARC-S08-ARC-S09;
Episode OC-S03; Testimony: author baseline and interview)

Confidence tracked validity poorly. Q04 records the agent correcting its own
approximately 570 boundary once exact-model evidence contradicted it. Q02, from
the following day, asserts a different 465 boundary and a 44-point ceiling that
later work weakened. Q04 comes first and retracts nothing; what the pair shows
is that one successful self-correction did not prevent the next confident
ceiling claim. The canonical transcript was missing at re-audit, so this
supports the recorded process example and no more. Other confident lines rested
on an adapter that never served, a broken model frame, a reset the evaluator
would not allow, and a corpus for the wrong model. (Quotes Q02, Q04; Episodes
AS-S07, ARC-S03, ARC-S05, ARC-S09; Episode OC-S04; source-availability manifest)

Neither stored memory nor a change of provider produced evidence. A saved
conclusion can carry a stale assumption or a repaired no-op forward, which is
why the memory-blind audit treated memory as claims to recheck. A second
provider could widen the space of explanations or reset a settled line, but
shared repositories, prompts, public methods, and prior conclusions kept that
from being independent corroboration, and unequal tasks, timing, models, and
budgets rule out ranking one provider against another. On efficacy the external
result stayed the authority. Retrieved live rows carry the AgentSecurity scores.
ARC results carried a weaker project-ledger qualification at the first cutoff;
cutoff-2 narrowed that and cutoff-3 closed it for the public axis, where ARC's
rows are now authenticated live observations. Its private axis is still
unqueried because it does not yet exist (§12.2, §13.2). (Episodes OC-S01-OC-S05;
Quote Q05; AgentSecurity live-results ledger; Sources ARC-S01-ARC-S16; AI
evidence ledger, known evidence gaps)

## 7. Where Agents Add Value

The cases support a practical role: agents as research executors. The value was
spread across the workflow rather than concentrated in discovery. (Episodes AS-S01-AS-S17; Episodes ARC-S01-ARC-S16)

- **Navigation and onboarding.** Searching repositories, reading SDKs, and
  working through evaluators turned unfamiliar systems into maps someone could
  act on. This is what the author's sense of access rests on, and it stays
  testimony rather than a measured comparison against working unaided. (Episodes AS-S01-AS-S03; Episodes ARC-S02-ARC-S03; Testimony
  Q08)
- **Implementation and operations.** Proposed mechanisms became attack
  candidates, search-and-replay systems, serving probes, parsers, routers,
  replay-safe sizing, and gated runners. Those artifacts kept their operational
  value even when the score claim behind them was refuted or never adjudicated. (Episodes AS-S04, AS-S08, AS-S12, AS-S14; Episodes
  ARC-S02, ARC-S05, ARC-S07, ARC-S12)
- **Instrumentation.** Timing probes, router self-measurement, serving-identity
  checks, retained replay cases, and A/A noise measurement made hidden
  assumptions observable. ARC's 0.707-level RMS estimate and the later rule
  “Serving identity proven first” are stronger contributions to research
  validity than any leaderboard narrative. The cutoff-3 replication rig turned
  the same capability on the external metric: once byte-identical draws were
  shown to span 2.45 to 4.31, a same-image instrument with pre-registered bands
  was the only way left to read a lever. (Episodes
  AS-S05, AS-S08; Episodes ARC-S05-ARC-S07, ARC-S14-ARC-S16; Quote Q07)
- **Experiment generation.** Agents produced alternative mechanisms and runnable
  arms while the human asked for bounded ladders, controls, and full-game
  verdicts. The ledger holds both working component tests and informative
  closures. Generating testable propositions did not make choosing between them
  or reading them trustworthy. (Episodes AS-S05-AS-S14;
  Episodes ARC-S08-ARC-S12)
- **Literature and method discovery.** Agent search surfaced public strategies,
  model candidates, and specialist syntheses worth reproducing or arguing with.
  It lived or died on source identity: the public forge was useful once
  attributed and tested, while the nine-specialist document was void because its
  corpus was for the wrong model. (Episodes AS-S04, AS-S09; Episode
  OC-S04; Episode ARC-S12)

None of this needs a new finding to be worth having. A parser regression suite,
a deterministic serving probe, a preserved negative ladder, or a runner someone
can rerun all make the next question cheaper to ask. What the agents produced
was research infrastructure and a reviewed record of experiments actually run.
Calling every artifact an insight would erase the causal and provenance work
that turns execution into knowledge.
(Episodes ARC-S04-ARC-S07; Episodes AS-S08, AS-S11-AS-S14)

## 8. Where Agents Struggle

The status spread is a mixed record, not a success rate: of 38 claims, eight
confirmed, ten partially supported, ten refuted, five invalid experiments, one
superseded, four open. The labels sit on different propositions with different
kinds of evidence, so they do not add up to an accuracy score. What they show is
why a result that runs, an effect that transfers, an experiment that is valid,
and a conclusion that lasts have to be judged one at a time. (AI evidence ledger, descriptive measures and
derivations, with all 38 IDs assigned exactly once)

Hypothesis selection and novelty remained weak points. The ledger contains 16
agent-origin propositions, but several pursued throughput, routing, serving,
reset, or turn-cadence explanations that were later refuted or invalidated. The
author could not identify a clear unexpected agent-originated discovery and
assessed the contributions as largely building on other people's work. The
cutoff-3 ARC evidence sharpens rather than softens this: the largest single
improvement in that case's best banked public score came from byte-copying a
named public notebook, while the two agent-origin candidates tested against
pre-registered bands in the same week both returned null. That testimony does
not prove agents cannot originate discoveries; it limits what these two cases
can claim. Agent generation supplied candidates, while worthwhile selection and
independent originality remained unresolved. (Episodes AS-S07-AS-S08,
AS-S12-AS-S14; Episodes ARC-S03, ARC-S08-ARC-S09, ARC-S13, ARC-S15-ARC-S16;
Testimony Q09)

Calibration failed where it mattered most. High local confidence came just
before someone discovered that the treatment never served, that the comparison
frame was under-powered, that the reset was unavailable in competition mode, or
that the research corpus was for the wrong model. None of those is cosmetic;
each changed what kind of experiment had been run. The agents could explain the
mistake afterwards. Human challenge or outright external failure is what made
them look. (Episodes AS-S07; ARC-S03, ARC-S05, ARC-S09; Episode OC-S04; Quotes
Q04, Q06-Q07)

Causal reasoning broke down whenever the arms failed to isolate anything. The
router ladder moved overlapping factors at once, the early Gemma comparison ran
on a broken control, and the LoRA treatment and its base control turned out to
be the same served model. Prompt reduction is the contrast: a real intervention
whose development gain simply reversed on the hidden evaluation. The first three
could not answer the question they posed; the fourth refuted a transfer claim.
Running a non-identifying design more times does not fix it.
(Episodes AS-S07-AS-S08; Episodes ARC-S05, ARC-S08)

The line between local and live evidence also gave way repeatedly. Early close
and packing only ever reached `ERROR` rows. Search-and-replay solved the
development set and not the external one. Prompt reduction reversed. Qwen 3.8
stayed open despite a strong local A/B because nothing external had scored it by
the cutoff. Local tests show that code works, or that something moves inside the
harness. They cannot show that a thing is deployed, that it generalizes, or that
it wins. (Episodes AS-S05-AS-S06; Episodes ARC-S02, ARC-S08-ARC-S09,
ARC-S12)

Knowing when to stop, and what to forget, did not come from the agent by itself.
An appealing line could run on past in-band or adverse results, and a stored
summary could carry last week's assumption into this week's run. The human
bounded the ladders, demanded controls, kept pending things pending, killed the
unserved arm, and commissioned the memory-blind reassessment. Switching provider
reopened the question space and could equally continue the same episode or build
a wider synthesis on premises that were already void. (Episodes AS-S11-AS-S14;
Episodes OC-S02-OC-S05; Episode ARC-S11)

## 9. Governing AI-Assisted Research

The resulting governance framework is a research protocol, not generic advice
to keep a human in the loop. Each control below answers a coded failure and
specifies an operational action that a researcher or IT professional can audit.
(Episodes AS-S01-AS-S17; Episodes ARC-S01-ARC-S16; Episodes OC-S01-OC-S05)

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

Most of the controls above were derived retrospectively from failures. The
cutoff-3 ARC work is the one place in this record where several of them were
applied prospectively, and it is reported for that reason rather than for its
result. Faced with an external metric whose byte-identical draws spanned 2.45 to
4.31, the project built a same-image off-platform instrument, wrote engagement
gates, a primary endpoint, decision bands, safety lines, and void rules before
each launch, and then read two candidates against those locked rules. Both were
recorded as negatives: one engaged its mechanism completely and moved nothing,
the other was engaged-but-flat inside its own dead band. The wave also caught a
defect in its own safety counter and appended the correction rather than editing
it away. The controls did not produce a better score. They produced two
defensible closures and a trustworthy instrument, which is what they are for.
(Episodes ARC-S14-ARC-S16; §13.2)

The framework also settles who owns what. Agents can fill in hypothesis cards,
build controls, keep ledgers, and run first-pass audits. The accountable human
decides whether the design identifies the claim, whether an external gate is
worth spending, and what the evidence actually supports. Tooling can enforce the
same split: immutable experiment manifests, content-addressed artifacts,
deployment-identity probes, permissioned live runners, and approval logs make
those gates inspectable instead of leaving them to conversational memory. (Episodes ARC-S05-ARC-S06, ARC-S12;
Episodes AS-S11-AS-S14; Quote Q07)

## 10. Implications

**Researchers.** Judge an agent by the research role it played and the kind of
evidence it produced, not by one label. Here, access did not bring mastery,
execution did not bring insight, and useful recombination was not originality.
Reporting those separately lets a confirmed parser repair stand on its own
without inflating into a ranking claim, and lets a reproduced public mechanism
keep its value without being called an invention. (Episode ARC-S07; Episodes AS-S04, AS-S09-AS-S10) This separation
aligns with broader evidence: bounded laboratory systems close loops inside
human-engineered envelopes [1-3], while scientific-programming and replication
benchmarks do not establish open-ended research autonomy [5,11].

**IT professionals.** The unit to secure is the path from claim to evidence.
Repository permissions and model access cover operational risk; scientific
reliability also needs versioned inputs, deployment-identity probes, matched
controls, local and external results in separate fields, append-only outcomes,
and live runners behind permission. Memory should keep source, cutoff,
contradiction, and unresolved status instead of compressing a project into its
most flattering narrative. A second model can challenge assumptions, as long as
shared repositories and inherited conclusions stay visible, so that diversity is
never mistaken for independence. (Episodes
ARC-S05-ARC-S06; Episodes OC-S01-OC-S05; Episodes AS-S07-AS-S08)

**Research leaders.** Nothing here supports a staffing multiplier, a provider
ranking, or replacing anyone. What it supports is budgeting agents alongside
human review, scarce external evaluations, evidence curation, and someone with
the authority to stop invalid work. Judge a portfolio by how many claims were
validly closed and how much they mattered, not by conversation volume, tokens,
commits, or manuscripts. This recommendation is case-derived, while the broader
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
38 interpretively coded episodes. The bounded implication is operational: the
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
were selected because the author conducted them, and the 38 episodes were
chosen and interpretively coded by that same authorial research process. No
second coder was blinded to the cases, no inter-rater reliability estimate
exists, and quotations were selected for explanatory value under the stated
privacy rules. Selection bias and single-author interpretation can therefore
affect episode boundaries, origins, statuses, and the salience of failures or
successes. Independent verification is also bounded: because the raw agent
histories are controlled, a reviewer can audit the public locators in the
accompanying redacted ledger but cannot re-derive the coding from the private
traces. The public episode ledger mitigates but does not remove this limit.
Three canonical Claude files and two additional cited Claude continuations were
also absent at the 2026-09-04 re-audit. Prior ledger extracts and repository
corroboration preserve bounded evidence for affected claims, but cannot restore
the missing original transcript context.

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
access and learning value, reported costs, trust judgments, the unachieved
winning objectives, and any judgment about how long the work would have taken
without AI. Costs were not allocated by case or reconciled to receipts,
and subscription amounts were not recorded in the reviewed ledger. The ARC
Stage 2b full-25 verdict has an additional provenance limitation: it was read at
audit time from a mutable file outside the frozen Git revision. Its hash,
modification time, and extraction time are recorded, but the exact bytes cannot
be reconstructed from the cutoff repository alone.

Finally, the outcomes were ongoing at the 2026-08-16 cutoff. Four AgentSecurity
L31 chain-pack rows were pending at the frozen cutoff; a later status-only recheck
found one complete at 73.605 and three still pending, and a second recheck found
all four complete at 79.985, 79.365, 73.605, and 54.375. No ARC external state was
freshly queried, and Qwen 3.8 external transfer remained open. The post-competition
cutoff-2 revision (Section 12, dated 2026-09-04) resolves the AgentSecurity outcome
with an authenticated final standing and a fresh ARC live query; consistent with
this section's rule, that later observation appends dated states and cannot
retroactively convert an invalid experiment into a valid one or erase a negative,
superseded, or unresolved episode. The cutoff-3 revision (Section 13, dated
2026-09-08) appends a third state under the same rule. It carries two further
limits of its own. ARC-AGI-3 was open at that cutoff, so its rank of 26 of 2,892
is mutable, rests on the top draw of a family whose byte-identical draws span
2.45 to 4.31, and cannot be read as a stable position; and the off-platform
replication results cited in Section 13.2 are local measurements on a
same-image rig, which can refute a proposition about that rig but cannot
establish or refute a live competition effect. The live three-draw read on the
`yield900` candidate was incomplete at that cutoff and remains open.

### 11.2 Living-outcomes register

The register records, per item, what is known now and what a later revision may
add. "Not established" is a finished evidence status, not an empty field. The
table carries the latest state only. The dated states behind it are preserved in
Section 12 (cutoff-2), Section 13 (cutoff-3), and the two live-results
artifacts, and nothing here overwrites them.

| Register item | AgentSecurityComp | ARC-AGI-3 | Update constraint |
| --- | --- | --- | --- |
| Evidence cutoff | Cutoff-3, authenticated Kaggle queries on 2026-09-08 between 18:21:51Z and 18:25:29Z. | Cutoff-3, same query window; ARC project repository read at commit `41213de`. | Each stream keeps its own cutoff. A later observation appends a dated state; it never replaces one. |
| Winning objective | Not won. Competition closed 2026-09-01; authenticated standing 171 of 4,186. | Unachieved and still open; deadline 2026-11-02. | The 173 of 4,251 Silver report is author testimony: no notification artifact survived two audits. |
| Public standing | Best banked public score 92.670. | Public rank 26 of 2,892 on a best score of 4.31 (2026-09-07), against a frontier of 11.04. | ARC values are mutable while the competition runs and must stay timestamped. |
| Private board | Fully revealed for this entrant: 38 of 49 scored rows at exactly 0.000, 11 positive, all from the confused-deputy `email.send` line. | Not revealed until the 2026-11-02 close. | The AgentSecurity pattern is complete for submissions actually flown, not for the competition, and does not expose the guardrail. |
| Most recent experiment state | Selected pair: Slot A at 92.670 public and 0.000 private, Slot B at 16.555 public and 16.735 private. | Byte-identical draws span 2.45 to 4.31. Off-platform, the turn-budget knob is null on levels and a pre-registered probe-discipline arm read engaged-but-flat and was recorded dead. | Off-platform rig results are local measurements, not live competition results. The live three-draw read on the knob was unfinished at cutoff-3. |
| Deadlines | Final submission 2026-09-01; optional Working Note 2026-09-08. The note was published on 2026-09-02. | Competition deadline 2026-11-02 23:59 UTC, from the authenticated listing. | Publication is an authenticated observation. The Working Note award outcome is not, and stays reserved. |
| Cost and oversight | Not separated by case. | Not separated by case. | Cross-case testimony only: about USD 100 OpenRouter, USD 30 Modal, unrecorded subscriptions, and 2–5 hours a day of review. Receipt-reconciled cost and measured oversight remain reserved. |
| Reserved fields | Working Note award outcome; receipt-reconciled cost; measured cumulative oversight. | Final status and rank; winning-objective verdict; private-board result; Qwen 3.8 transfer; the completed live three-draw read. | Populate only from a newly cited official record, a preserved project artifact, or explicitly labelled testimony. |

Appendix A.6 specifies the update procedure. It was applied for cutoff-2 in
Section 12 and cutoff-3 in Section 13. Any later update appends another dated
state: pending stays pending and unqueried stays unqueried until direct evidence
changes it.

## 12. Post-Competition Outcomes (cutoff-2, 2026-09-04)

This section performs the Appendix A.6 update procedure for a second dated
cutoff. It appends authenticated final and mid-competition outcomes; it does not
rewrite the 2026-08-16 narrative, whose frozen states are preserved in Sections
4, 5, and 11. AgentSecurityComp concluded on 2026-09-01; ARC-AGI-3 remained an
ongoing competition at this cutoff.

**Evidence provenance.** The [cutoff-2 live-results artifact](evidence/cutoff-2-live-results-2026-09-04.md)
records the authenticated queries and their claim-use limits. The AgentSecurity
submission rows, private and public scores, authenticated user rank,
competition timeline, and the ARC-AGI-3 rows and official deadline below were
retrieved from the Kaggle API on 2026-09-04 and are **live observations**. The
Silver label and 173/4,251 notification value are retrospective author
testimony: the repository records the report, but no screenshot, email, or
archived notification survived the audit. The available private histories used
for the two added episodes are recorded in the
[source-availability manifest](evidence/source-availability-manifest.md); the
episode coding also uses repository artifacts and the companion working note.

### 12.1 AgentSecurityComp: a reported Silver placement without a throughput win

The public-throughput line that dominated the 2026-08-16 narrative did not close
the observed frontier gap. The best banked public score was 92.670 (ref
55766377). A retained authenticated leaderboard query showed that the public
frontier had reached at least 147.530 by 2026-08-29, making the directly observed
top-to-best ratio about 1.59 times. This is not asserted as the exact frontier at
the 2026-09-01 deadline. Every attacker-controllable lever tested in the final
week—commitment-forge wording, adaptive void-safe sizing, inter-hop reasoning
suppression, and probe-hop count—failed to beat about 92.670 or lowered the row,
and the frontier method was absent from every inspected public artifact. This is
a valid family-level negative result, not proof that the gap was unclosable.
(Episode AS-S16)

A different, human-directed line produced the only positive private score among
the selected pair. On the authenticated revealed rows, two high-public EXFIL
submissions scored 0.000 private (ref 55927148 at 89.680 public; ref 55902731 at
91.600 public). Queried confused-deputy `email.send` rows scored approximately
15.8–16.8 private. The author selected Slot A, the banked public best (ref
55766377, public 92.670, private 0.000), and Slot B, a confused-deputy set (ref
55805571, public 16.555, private 16.735). The best private score among the
queried confused-deputy rows was 16.805 (ref 55904213), on a non-selected draw.
These observations confirm a bounded row-level pattern in the revealed sample:
the queried EXFIL rows scored zero while the queried confused-deputy rows scored
positively. They do not expose the private guardrail, prove a universal
`http.post` rule, isolate the scoring component, or establish the platform's
rank calculation. (Episode AS-S15)

The authenticated cutoff-2 competition query returned rank 171 of 4,186
entrants. Separately, the author reported a Silver notification showing 173 of
4,251 on 2026-09-02. The report is preserved in the repository, but the
notification itself was not retained, so the medal label and 173/4,251 remain
testimony. The top-prize objective was not won. The selected-row pattern is
consistent with the rationale for the human-selected private-board hedge, but it
does not by itself establish that hedge as the cause of the final placement.
Read through the paper's categories, the outcome still supports a limited
interpretation: execution and human-governed recombination advanced further than
dependable agent originality, while the private mechanism remains unknown.
(Episodes AS-S15-AS-S16; §6.2; Testimony Q09)

### 12.2 ARC-AGI-3: still open, with a fresh live query

Contrary to the cutoff-1 register, ARC-AGI-3 has an official deadline of
2026-11-02, retrieved from the authenticated ARC Prize 2026 competition listing.
The competition was ongoing at this cutoff and its private board is not revealed
until close. A fresh authenticated query on 2026-09-04 shows that post-cutoff
work continued—a model-swap campaign—and lifted the best public score to 1.94
(ref 55970756, 2026-09-03), above the roughly 0.7–1.9 band of the frozen
narrative; the author's public rank was 374 of 2,779 teams at 16:56:36Z. A
separate authenticated query at 20:12:04Z returned 379 of 2,787, confirming that
the ongoing rank and entrant count were mutable even within the day. No private
score exists yet, and the winning objective is unachieved. The case is therefore
explicitly bounded as a mid-competition snapshot, resolving the freshness
asymmetry noted in Section 11.1: both cases now carry a dated cutoff-2 live query,
with AgentSecurity final and ARC-AGI-3 open. The same fresh query also
corroborated several ARC submission scores that Section 5 could report only as
project-ledger values at cutoff-1—for example the duck-memory row at 0.83 (ref
55488796) and the structural arms at 1.09, 0.78, and 1.03 (refs 55493742,
55450891, 55418633)—which now match the authenticated public rows. (Sources:
authenticated Kaggle competition listing and submission rows, 2026-09-04)

### 12.3 Two added episodes and recomputed tallies

Two AgentSecurityComp episodes are added at this cutoff; no earlier episode's
code is changed.

- **AS-S15** (origin `mixed`; status `confirmed`). Proposition: among the
  revealed tested rows, the two queried high-public EXFIL submissions score
  0.000 private while the queried confused-deputy `email.send` rows score
  positively, including 16.735 for selected Slot B. The human directed the pivot
  and selected the final submissions; the agent and its subagents performed
  source analysis; public write-ups and a mock private-guardrail wheel were
  external inputs. The row-level proposition is confirmed. The private
  guardrail mechanism, universal family behavior, and causal contribution to
  final rank remain unobserved.
- **AS-S16** (origin `agent`; status `refuted`). Proposition: a final-week
  attacker-controllable lever closes the public-throughput gap to the frontier.
  Refuted: no lever beat about 92.670, several lowered the row, and a direct
  query showed that the frontier had reached at least 147.530 by 2026-08-29.
  Lesson: exhausting a family of attacker levers is a valid negative result,
  not evidence that the gap is unclosable.

Recomputed descriptive tallies at cutoff-2: **33 episodes** (16 AgentSecurityComp,
12 ARC-AGI-3, five OpenCode). Status: **five** confirmed, **ten** partially
supported, **eight** refuted, **five** invalid experiments, **one** superseded,
**four** open. Origin: **14** agent, **16** mixed, **three** external, **zero**
human. These remain descriptive of the reviewed corpus, not estimates of
population frequency, and the two additions leave every earlier code unchanged.
Cost and cumulative-oversight fields remain retrospective testimony and are not
populated by this cutoff. (AI evidence ledger, cutoff-2 addendum)

## 13. Continuing Outcomes (cutoff-3, 2026-09-08)

This is the third dated cutoff, taken four days after the second under the
procedure in Appendix A.6. It adds what the platform showed on 2026-09-08 and
leaves the earlier narrative alone. AgentSecurityComp was closed by then.
ARC-AGI-3 was not, so its numbers here are a snapshot of an open competition and
will have moved since.

The queries, identifiers, and per-claim limits sit in the
[cutoff-3 live-results artifact](evidence/cutoff-3-live-results-2026-09-08.md).
Kaggle rows are live observations. The replication results in 13.2 were measured
off the platform, on the project's own rig, and are local measurements
throughout.

### 13.1 What the private board actually paid for

The final standing did not change: rank 171 of 4,186. Searching the repository
again turned up no screenshot or archived copy of the reported Silver
notification, so 173 of 4,251 stays testimony rather than evidence.

What did change is how much of the private board is visible. Section 12.1 could
only cite a handful of revealed rows. The retained submission list was retrieved
in full at this cutoff, with one limit worth stating plainly: the platform
returns only the most recent 50 rows, and those 50 span 2026-08-22 to 2026-09-01,
the final eleven days of a case that opened in June. Earlier submissions fall
outside it. Of the 50, one errored and 49 carry both scores. Thirty-eight
of those 49 scored exactly zero on the private board. The eleven that scored
anything all came from the confused-deputy `email.send` line, between 2.290 and
16.805. Nothing above 50 points of public score earned a single private point,
including the 92.670 row that was selected.

Months of public-throughput work drove most of Section 4. On the board that
decided the prizes it was worth nothing. The only rows that paid came from
a small hedge line that never cleared 16.6 in public.
That holds across every submission still on file, which is a stronger claim than
Section 12.1 could make from a queried sample and a weaker one than a campaign
census. It is still a claim about one entrant's last eleven days. It says nothing about what the guardrail was, why those
rows scored, or whether the hedge is what produced the final rank. (Episode
AS-S17)

One row does not belong to the hedge family. A diversity arm flown for private
predicate coverage, pairing the confused-deputy line with untrusted-to-action,
scored 10.745. It was the only positive row submitted as portfolio coverage
rather than as another draw of the same hedge, and it scored below the hedge.
That is consistent with the portfolio reasoning without vindicating it, and a
success-only reading of the board would have dropped it.

The Working Note is now visible as a published notebook rather than a repository
record. Whether it won anything is unknown; the award had not been announced when
these queries ran, and that field stays reserved.

### 13.2 A better rank on someone else's notebook

ARC-AGI-3 moved from rank 374 of 2,779 to 26 of 2,892, and from a best public
score of 1.94 to 4.31. The leader at the same moment was on 11.04. Taken alone
that is the most encouraging number in this study. Two things about how it
happened matter more than the rank.

The jump came from copying a competitor. On 2026-09-05 the project submitted a
byte-for-byte copy of a public notebook, attributed in the submission itself and
carrying 149 votes at the time of the query. It scored 3.25, against a best
in-house result of 1.94. That single move added 1.31 points, and the comparison
cuts deeper than it first looks. Most of the earlier record-setting steps changed
no code at all: +0.96, +0.31, +0.03, +0.44 and +0.06 were exact-byte
resubmissions, several drawn from a variance yardstick series whose own
description records a mean of 0.918 and a standard deviation of 0.149. The
largest improvement traceable to a change the project originated is +0.14, the
model swap of 2026-08-31. Most of what looked like two months of progress was the
same code drawn again. Everything flown afterwards is that same public notebook,
either unchanged or with one constant altered. The reuse is transparent and it is
the largest improvement in the case.
It is not a discovery, and it sits in the same category as the adaptive-sizing and
commitment-forge work in Section 6.2. (Episode ARC-S13)

The metric also barely holds still. Submitting the identical file three times
returned 3.25, 2.58, and an outright platform error. Two runs of the one-knob candidate returned 4.31 and 2.45. Unchanged code
spans two-thirds of a point; the candidate spans nearly two. Rank 26 rests on the
best draw of that spread, and nothing in the public record distinguishes it from
noise. (Episode ARC-S14)

That instability had a practical consequence. With draws that wide and slots
that scarce, the leaderboard could not settle a one-knob question. The project
tested levers on its own rig instead: same container image, same class of GPU,
25 games a wave. The engagement gate, the primary endpoint, the decision bands,
and the void rules were written down before each launch.

Two candidates went through it. The first was the constant that separated the
4.31 from the base, which had looked promising on two early waves. A larger
comparison ran three waves a side, two on the rig and one from a Kaggle commit
run, so the totals mix two platforms. It came back at 118 levels against 118.
The knob plainly changed how the agent behaved, roughly doubling calls per turn
and cutting actions per game from 143 to 115. None of that reached the score.
(Episode ARC-S15)

The second was the top-ranked proposal from the same analysis: refuse the model's
analysis-only calls after two in a turn and make it test its leading hypothesis.
It engaged on every gate that had been registered for it, and returned 41 levels
against a pooled base of 39.33, well inside the band that had been declared dead
before launch. It was recorded dead. (Episode ARC-S16)

Both readings held because the rule was fixed before the number arrived. In the
second case the mechanism did everything it was designed to do and the result
still did not move, which is the execution-versus-insight distinction of
Section 6.2 showing up prospectively rather than in hindsight. The wave also caught a fault in its own safety counter: a filter written with a
space missed the compact JSON the harness actually writes. It was fixed, tested,
and appended to the summary rather than quietly corrected.

None of that is live evidence. Section 8's boundary cuts both ways: a null on the
rig no more refutes a competition effect than a gain on the rig would establish
one. The live three-draw rule on the knob was also unfinished at this cutoff, at
4.31 and 2.45 against a threshold of 4.0, with the third draw due the following
morning. It is recorded as pending.

Neither headline verdict moves. The AgentSecurity prize was not won and the
standing is unchanged; ARC's objective is unmet and its private board stays
closed until November. Section 6.3 noted that ARC results carried a weaker
qualification because they had never been queried directly. That gap is now
closed on the public side, and remains open on the private side only because no
private result exists yet.

### 13.3 Added episodes and recomputed tallies

Five episodes are added, one from AgentSecurityComp and four from ARC-AGI-3. No
earlier code changes.

- **AS-S17** (`mixed`, `confirmed`). The public and private boards are
  dissociated across the entrant's whole submission population: 38 of 49 scored
  rows at exactly zero, all 11 positive rows from the confused-deputy line, and
  nothing above 50 public earning anything private. The guardrail, the behavior
  of submissions never flown, and the contribution to final rank stay unobserved.
- **ARC-S13** (`external`, `confirmed`). Copying the best public artifact beat
  every in-house arm: 3.25 against 1.78–1.94. No matched control was run, so draw
  variance bounds how firmly the size of that gain can be stated.
- **ARC-S14** (`mixed`, `confirmed`). One public draw cannot settle a one-knob
  change here. Identical submissions returned 3.25, 2.58, and an error; the
  candidate returned 4.31 and 2.45. This is the noise-floor discipline of
  Episode ARC-S06 applied to the external board.
- **ARC-S15** (`agent`, `refuted`). The turn-budget constant produced no step on
  the rig: 118 levels against 118 over 75 runs a side, despite large and verified
  behavioral change. The live read was unfinished and is not treated as closed.
- **ARC-S16** (`agent`, `refuted`). Harness-enforced probe discipline engaged on
  every registered gate and returned 41 levels against a base of 39.33, inside
  its own dead band. Fixing the decision rule in advance is what let an engaged
  but flat result be reported as a negative.

The corpus is now 38 episodes: 17 AgentSecurityComp, 16 ARC-AGI-3, five
OpenCode. Eight confirmed, ten partially supported, ten refuted, five invalid
experiments, one superseded, four open. By origin, 16 agent, 18 mixed, four
external, none human. These describe the reviewed corpus and not population
frequencies, and the five additions leave every earlier code untouched. Cost and
oversight remain testimony and are not populated here.

## Data, Ethics, and Declarations

### Data and materials availability

The manuscript's [public episode ledger](evidence/episode-ledger-public.md)
provides all 38 coding rows, status and origin derivations, and public artifact
locators. The [cutoff-2 live-results artifact](evidence/cutoff-2-live-results-2026-09-04.md)
records the competition observations used in Section 12, and the
[cutoff-3 live-results artifact](evidence/cutoff-3-live-results-2026-09-08.md)
records those used in Section 13, including the repository locators for the
off-platform replication results and the claim-use limit that keeps them
separate from live competition evidence. Private Claude, Codex,
and OpenCode histories are controlled because they can contain credentials,
personal material, and unrelated project content. Their availability and file
digests are reported in the
[source manifest](evidence/source-availability-manifest.md); three canonical
Claude originals were absent at the 2026-09-04 audit. An authorized audit can
inspect surviving private sources under the quotation and redaction rules in
Appendix A, but the private histories are not distributed with the paper.

### Ethics and reflexivity

This retrospective self-study analyzes the author's own agent interactions,
decisions, and project artifacts. It did not recruit external research
participants or publish private third-party conversation content. The author is
simultaneously participant, analyst, and sole coder, creating unavoidable risks
of recall, selection, and interpretation bias. The public ledger, explicit
testimony labels, missing-source disclosures, and narrow claim statuses are
intended to make those risks inspectable rather than eliminate them. Any target
venue's current requirements for self-study or human-participant review must be
checked before submission.

### Funding and competing interests

No external research funding is reported for this study. Direct service costs
are described only as retrospective author testimony because receipts were not
reconciled by case. The author operates BrainMatterStudios and used commercial
AI and compute services named in the Methods. The author declares no provider
sponsorship of the study or manuscript.

### Author affiliation and correspondence

Ahmed Mobasher, BrainMatterStudios, The Hague, Netherlands, and Cairo, Egypt.
Correspondence is available through
[brainmatterstudios.com](https://brainmatterstudios.com).

**Keywords:** AI research agents; computational research; scientific autonomy;
human oversight; research integrity; tool-using language models; N-of-1 study.

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
every included canonical root and linked derivative, checks that all 38 episode
IDs occur exactly once, and reconciles origin and status totals to the row-level
IDs in the evidence ledger. Exact private transcript contents are not required
for the published count; an authorized auditor can inspect the surviving
private locators and the identified substitutes without releasing the
histories. The source-availability manifest records the
audit-time SHA-256 digest of each surviving canonical Claude and Codex file.
Three canonical Claude originals were absent from their expected paths on
2026-09-04; claims tied to those sources must rely on separately identified
surviving evidence and cannot be represented as directly re-opened transcript
claims.

### A.2 Episode construction and coding

Episode construction was purposive and sought variation across cases,
mechanisms, successful and failed outcomes, validity failures, provider
continuations, and governance lessons. It was not an exhaustive sampling frame.
Inclusion required a bounded adjudicable proposition, traceable evidence, an
implementation, experiment, or explicit evidence adjudication, and enough
record to code origin and a final or dated-open status. Routine debugging,
purely operational work, duplicate continuations, repeated variants without a
new evidentiary issue, and propositions lacking an adjudicable record were
excluded. No all-events denominator was constructed.

An included episode begins with a bounded proposition and ends when the reviewed
record supports a final status or a dated open state. The coding row records
case, date, proposition, origin (`human`, `agent`, `external`, or `mixed`),
prior evidence, pre-outcome confidence, human intervention, local outcome,
external outcome, final status, lesson, and source locator. The six final
statuses are `confirmed`, `partially supported`, `refuted`, `invalid
experiment`, `superseded`, and `open`. Status belongs to the proposition, not to
the provider or artifact. A functioning implementation can coexist with a
refuted efficacy claim; a broken control produces `invalid experiment`, not a
negative result.

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
