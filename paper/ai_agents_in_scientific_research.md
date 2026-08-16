# Access Without Autonomy: An Instrumented Case Study of AI Agents in Computational Research

## Abstract

Large-language-model agents can search literature, inspect repositories, write
and execute code, coordinate multi-step workflows, and draft research prose.
Those capabilities make computational research more accessible, but they do
not by themselves establish scientific autonomy, originality, or reliability.
This living, comparative N-of-1 case study examines my use of AI coding agents
in two unfamiliar competition-based research projects: AgentSecurityComp as the
primary case and ARC-AGI-3 as a comparative case. The study draws on
deduplicated agent histories, pinned repository evidence, experiment artifacts,
and retrospective author testimony. Its unit of analysis is a bounded research
episode rather than a provider turn or conversation count. Thirty-one episodes
were coded for hypothesis origin, prior evidence, human intervention, local and
live outcomes, claim status, and methodological lesson. The design has no
human-only control, the providers were used unequally, the platforms and models
changed during the observation period, and competition scores are noisy proxies
for research quality. The manuscript therefore does not estimate a productivity
multiplier or compare providers. It tests a narrower thesis: AI agents can
substantially lower the barrier to executing computational research, while
their most defensible current role remains high-throughput research execution
under skeptical human governance. At the evidence cutoff, both competition
objectives remained unachieved; that status is retrospective testimony pending
verification against final records.

## 1. From Enterprise Architecture to Computational Research

I came to these projects with more than 16 years of consulting experience in
decisioning, omnichannel AI, architecture, and early-career Java development.
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

Benchmark and human-study evidence reinforces that separation. CORE-Bench, a
preprint on computational reproducibility, reported that the best evaluated
agent reached 21% accuracy on its hardest task level, even though reproduction
from an existing repository and data is narrower than new research [9]. The
official PaperBench release, accompanied by a preprint, reported that the best
tested agent completed an average of 21% of rubric-weighted requirements across
20 machine-learning replication tasks and did not exceed its recruited
ML-PhD baseline [10]. A separate preprint found that expert reviewers rated
LLM-generated NLP ideas as more novel on average but slightly less feasible
than human ideas; the ideas were not executed, their novelty judgments were
subjective, and the system's self-ranking was unreliable [11]. Another preprint
reported strong performance for a literature agent on defined retrieval and
synthesis tasks while noting context-dependent contradiction labels and
overconfidence [12]. A multi-agent review preprint found gains over tested
single-agent baselines, but also many low-precision comments and a continuing
need for accountable judgment [13].

Even apparently routine research mechanics require verification. A
peer-reviewed *Scientific Reports* study of 84 generated literature reviews
found fabricated citations and errors in real citations from the April 2023
ChatGPT snapshots it tested [14]. Those rates should not be generalized to
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
not prove what happened in either project.

Claude Code was the primary research system. I introduced Codex and
OpenCode/DeepSeek mainly as perspective resets when the primary line of work
appeared stuck, repetitive, or prematurely settled. Tasks, dates, models,
budgets, and exposure differed. Session or token totals therefore describe use,
not independent intellectual contribution, research quality, or provider
superiority.

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
authorship or tool use [15,16]. Ahmed Mobasher's status as sole author and the
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

## 5. Case II: ARC-AGI-3

## 6. Cross-Case Findings

## 7. Where Agents Add Value

## 8. Where Agents Struggle

## 9. Governing AI-Assisted Research

## 10. Implications

## 11. Limitations and Living Outcomes

## Acknowledgements and AI-Use Disclosure

Ahmed Mobasher is the sole author and is accountable for the manuscript's
claims, citations, originality, integrity, and final wording. Claude Code was
the primary agent used to execute research work across the two cases. Codex and
OpenCode/DeepSeek were used as supplementary perspective resets and challenge
mechanisms; their unequal use does not support a provider ranking. In the
current manuscript collaboration, Codex assisted with evidence-ledger review
and drafting of the opening, background, and method. AI-generated material was
treated as provisional and checked against the reviewed evidence ledger. None
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
9. Siegel, Z. S., Kapoor, S., Nadgir, N., Stroebl, B., and Narayanan, A.
   “CORE-Bench: Fostering the Credibility of Published Research Through a
   Computational Reproducibility Agent Benchmark.” arXiv 2409.11363v2
   (2024; revised 2026). Preprint.
   [arXiv:2409.11363](https://arxiv.org/abs/2409.11363).
10. Starace, G., Jaffe, O., Sherburn, D., et al. “PaperBench: Evaluating AI's
    Ability to Replicate AI Research.” Official benchmark release and
    accompanying preprint, arXiv 2504.01848 (2025).
    [Primary paper](https://arxiv.org/abs/2504.01848).
11. Si, C., Yang, D., and Hashimoto, T. “Can LLMs Generate Novel Research Ideas?
    A Large-Scale Human Study with 100+ NLP Researchers.” arXiv 2409.04109v1
    (2024). Preprint. [arXiv:2409.04109](https://arxiv.org/abs/2409.04109).
12. Skarlinski, M. D., Cox, S., Laurent, J. M., et al. “Language agents achieve
    superhuman synthesis of scientific knowledge.” arXiv 2409.13740v2 (2024).
    Preprint. [arXiv:2409.13740](https://arxiv.org/abs/2409.13740).
13. D'Arcy, M., Hope, T., Birnbaum, L., and Downey, D. “MARG: Multi-Agent
    Review Generation for Scientific Papers.” arXiv 2401.04259v1 (2024).
    Preprint. [arXiv:2401.04259](https://arxiv.org/abs/2401.04259).
14. Walters, W. H., and Wilder, E. I. “Fabrication and errors in the
    bibliographic citations generated by ChatGPT.” *Scientific Reports* 13,
    14045 (2023). Peer-reviewed article.
    [doi:10.1038/s41598-023-41032-5](https://doi.org/10.1038/s41598-023-41032-5).
15. International Committee of Medical Journal Editors. “Use of AI by Authors.”
    Current editorial recommendation checked 2026-08-16.
    [ICMJE guidance](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html).
16. Springer Nature. “AI guidance for researchers and communities.” Current
    publisher policy checked 2026-08-16.
    [Springer Nature guidance](https://group.springernature.com/gp/group/ai/ai-guidance-for-our-researchers-and-communities).

## Appendix A: Evidence and Coding Method
