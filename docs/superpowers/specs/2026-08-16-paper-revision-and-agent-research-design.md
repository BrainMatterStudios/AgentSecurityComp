# Competition Working Note Revision and AI-Agents-in-Research Paper Design

**Date:** 2026-08-16

**Status:** Approved in conversation; awaiting review of this written specification

**Author:** Ahmed Mobasher

**Primary repository:** `/Users/ahmed/Documents/AgentSecurityComp`

**Comparative repository:** `/Users/ahmed/Documents/ArcAGI3`

## 1. Objective

Produce two evidence-led Markdown manuscripts:

1. Revise the existing Kaggle competition Working Note so its claims, results,
   methodology, and limitations match the current SDK, repository history, and
   live submission evidence.
2. Create a living, wide-audience paper about Ahmed's use of AI coding agents in
   computational research, using the AgentSecurityComp project as the primary
   case and ARC-AGI-3 as a comparative case.

The manuscripts serve different purposes. The Working Note is a competition
submission about agent-security methodology and findings. The second paper is a
longitudinal case study of human-agent research collaboration. The latter will
not be inserted into the former except for a concise AI-use disclosure.

## 2. Approved Scope

### 2.1 Deliverables in the current phase

- Revised `paper/working_note.md`.
- New Markdown manuscript at a clear path under `paper/`.
- A Markdown evidence appendix or companion evidence file if the main paper
  would otherwise become unreadable.
- A verified bibliography in Markdown or BibTeX-compatible form, depending on
  what best fits the manuscript source.

### 2.2 Deferred deliverables

The following will be generated only after the manuscripts are finalized:

- PDF editions.
- HTML editions.
- Visual timelines or interactive evidence companions.
- Word-processing formats.

### 2.3 Living-manuscript policy

Both competitions are ongoing. The second paper will therefore:

- state a dated evidence cutoff in every released revision;
- preserve current uncertainty rather than retroactively rewriting it;
- distinguish completed, pending, and superseded experiments;
- receive a final outcomes section after the competition results are known;
- report final rankings, costs, lessons, and retrospective judgments only when
  supported by the final records.

The Working Note will use the same dated-cutoff discipline, with a final pass
before the Kaggle Working Note deadline on 2026-09-08.

## 3. Audience and Writing Style

The second paper is intended for researchers, IT professionals, and interested
general readers. It should be:

- rigorous enough that researchers can assess the evidence and limitations;
- concrete enough that architects and practitioners can apply its governance
  lessons;
- readable without prior knowledge of either competition;
- candid about failure, uncertainty, external-method dependence, and the
  continuing role of human judgment;
- free of promotional claims about any AI vendor or model.

The prose will combine a first-person research narrative with evidence tables,
short transcript excerpts, and clearly labeled analysis. Technical details will
be introduced in plain language before specialist terminology is used.

## 4. Author and AI Disclosure

Ahmed Mobasher will be the sole author. The paper may identify him and describe
his background. Claude Code, Codex, and OpenCode/DeepSeek will not be listed as
authors. Their roles will be disclosed in the methods and acknowledgements.

Ahmed has authorized short quotations from the local agent transcripts. Quotes
must be:

- relevant to hypothesis formation, confidence, correction, intervention, or
  research governance;
- short enough to preserve readability and privacy;
- accompanied by enough context to avoid misleading attribution;
- stripped of secrets, credentials, and unrelated personal information.

The manuscript remains Ahmed's responsibility. AI-generated prose, citations,
and interpretations must be independently checked before inclusion.

## 5. Author Baseline and Research Context

The paper will characterize Ahmed's starting position accurately:

- more than 16 years in consulting;
- experience with real-time decisioning and omnichannel marketing using AI and
  statistical models, including Naive Bayes and gradient-boosted models;
- enterprise- and solution-architecture experience across cloud and on-premise
  technologies;
- experience with agentic AI and early-career Java development;
- some Python exposure, primarily with AI assistance rather than independent
  greenfield implementation;
- strong systems, architecture, integration, and value-delivery skills;
- limited prior expertise in agent security, ARC-AGI-3, scientific research
  practice, and Kaggle competition mechanics.

This is not a novice-versus-expert story. It is a case of an experienced
technologist entering unfamiliar research domains with relevant transferable
skills but meaningful domain and implementation gaps.

## 6. Second Paper: Positioning and Thesis

### 6.1 Paper type

The second paper will be an instrumented, longitudinal, comparative N-of-1 case
study. AgentSecurityComp is the primary case; ARC-AGI-3 is the comparative case.
OpenCode/DeepSeek is a limited supplementary evidence source, not a balanced
model-comparison arm.

### 6.2 Central thesis

> AI agents can substantially lower the barrier to participating in
> computational research, but access should not be confused with autonomy,
> originality, or reliability. Their strongest present role is as
> high-throughput research executors operating under skeptical human governance.

### 6.3 Claims the paper may support

Subject to evidence verification, the paper may argue that agents helped Ahmed:

- enter two technically demanding competitions without first completing a long
  domain-upskilling period;
- navigate unfamiliar code and competition infrastructure;
- synthesize public methods and adapt them into testable implementations;
- build experiment harnesses, submission ladders, operational automation, and
  reproducibility artifacts;
- learn enough domain context to challenge and steer later recommendations;
- maintain a breadth of investigation that would have been impractical under
  Ahmed's available time.

### 6.4 Claims the paper must not make

The paper will not claim that:

- the cases measure general AI scientific capability;
- the agents independently produced a validated scientific discovery;
- AI reduced human involvement to a nominal review step;
- one model or provider was demonstrably better than another;
- a measured productivity multiplier exists without a human-only control;
- leaderboard performance can be causally attributed to an individual agent;
- Ahmed would certainly have needed a specific amount of time without AI.

Ahmed's view that independent progress would likely have required at least a
month of upskilling may be reported as retrospective testimony, clearly labeled
as a counterfactual judgment rather than a measured result.

## 7. Research Questions

1. How much can AI agents lower the entry barrier for an experienced
   technologist entering unfamiliar computational-research domains?
2. Which research tasks do the agents perform effectively?
3. How much scientific direction and originality emerges without
   domain-specific human guidance?
4. Where do agents fail, particularly through confident error, incomplete due
   diligence, stale memory, external imitation, and local-to-live transfer?
5. Which human governance practices improve reliability and research value?

## 8. Evidence Model

### 8.1 Data sources

- Claude Code transcripts associated with both repositories.
- Codex session records associated with both repositories.
- OpenCode/DeepSeek session records associated with both repositories.
- Git history, including commit messages, diffs, and dates.
- Experiment scripts, logs, notebooks, and result artifacts.
- Live Kaggle submission histories and leaderboard records.
- Competition SDK and evaluator source.
- Official competition rules, evaluation criteria, and timelines.
- Ahmed's interview responses in the current collaboration.
- Financial records or user-confirmed estimates for direct costs.
- Primary research literature and official publishing-policy sources.

### 8.2 Research episode as the unit of analysis

Each analyzed episode will include, where available:

1. the question or hypothesis;
2. its apparent origin: human, agent, external source, or mixed;
3. the evidence cited before implementation;
4. the implementation or experiment proposed;
5. the human review or intervention;
6. the local result;
7. the live or external result;
8. whether the claim was confirmed, weakened, refuted, or left unresolved;
9. whether the agent corrected itself before or only after challenge;
10. the durable methodological lesson.

### 8.3 Evidence tiers

Every substantive claim in both papers will be classified internally as one of:

- **Source fact:** directly established by authoritative code or official rules.
- **Local measurement:** produced in a controlled local or cloud replica.
- **Live observation:** returned by the actual competition evaluator.
- **Triangulated finding:** supported by at least two independent evidence types.
- **Inference:** a reasoned interpretation that is not directly observed.
- **Retrospective testimony:** Ahmed's recollection or judgment.
- **Open hypothesis:** not yet resolved.

The manuscripts need not display a label beside every sentence, but their prose
and tables must preserve these distinctions.

### 8.4 Qualitative coding categories

- hypothesis origin;
- external-method dependence;
- implementation and infrastructure value;
- novel recombination;
- experimental validity;
- confidence and calibration;
- retraction or correction;
- stale-memory propagation;
- human challenge or approval;
- model/provider switching;
- local-to-live transfer;
- operational failure;
- domain learning;
- achieved and unachieved goals.

### 8.5 Quantitative descriptors

Where reliably measurable, the paper may report:

- project duration and active days;
- commits and experiment artifacts;
- submission counts, statuses, and score trajectories;
- numbers of hypotheses confirmed, refuted, or unresolved;
- human interventions and agent retractions in a coded sample;
- direct financial costs;
- Ahmed's estimated oversight time of two to five hours per day;
- evidence of repeated versus novel experiments.

Counts must be deduplicated across imported or overlapping Claude, Codex, and
subagent records. Token counts are descriptive of usage, not measures of thought
quality or research contribution.

## 9. Comparative Case Logic

### 9.1 AgentSecurityComp

This case emphasizes:

- source-grounded reverse engineering;
- public-method adaptation;
- experiment ladders under scarce submission slots;
- local-to-T4/leaderboard transfer failures;
- repeated premature breakthrough narratives;
- eventual adoption of a two-gate evidence discipline;
- meaningful participation without achievement of the winning objective.

### 9.2 ARC-AGI-3

This case emphasizes:

- broad agent autonomy in choosing research directions;
- memory-blind and cross-domain research requests;
- many hypotheses killed or reversed by measurement;
- experiment governance supplied by Ahmed rather than domain-specific advice;
- external-agent, competitor, and model dependence;
- persistent-memory benefits and hazards;
- meaningful participation without achievement of the winning objective to
  date.

### 9.3 Provider comparison

Claude Code was the primary system. Codex and DeepSeek were often introduced
when Claude Code appeared stuck, repetitive, or prematurely ready to give up.
This switching may be analyzed as a diversity and reset mechanism. Because
usage, tasks, model versions, budgets, and timing were unequal, the paper will
not rank the providers. Ahmed's current assessment is that none has proved
meaningfully superior overall, although Codex has recently appeared somewhat
better without a large or controlled difference.

## 10. Second Paper Structure

1. Opening narrative: an enterprise architect enters two unfamiliar research
   competitions with AI agents.
2. The experiment and its original autonomy question.
3. What an AI research agent is, contrasted with tool assistance and genuinely
   autonomous closed-loop science.
4. Method, evidence, coding scheme, costs, and limitations.
5. Case I: AgentSecurityComp.
6. Case II: ARC-AGI-3.
7. Cross-case findings.
8. Where agents add practical value.
9. Where agents struggle.
10. A governance framework for researchers and IT professionals.
11. Implications for AI agents in science.
12. Limitations, living outcomes, and final retrospective.
13. Methods and evidence appendix.

The manuscript will use short narrative scenes, evidence tables, and restrained
technical excerpts. It will not reproduce raw transcripts wholesale.

## 11. Working Note Revision Design

### 11.1 Recommended positioning

The Working Note will be reframed around two defensible contributions:

1. a source-derived guardrail-predicate asymmetry analysis; and
2. an empirical account of local-to-leaderboard transfer failure and
   evidence-gated red-team experimentation.

A working title is:

> Guardrail-Predicate Asymmetry and the Limits of Local-to-Leaderboard Transfer
> in Multi-Step Agent Red-Teaming

### 11.2 Required factual corrections

- Update the evidence cutoff beyond the 2026-08-10 draft.
- Replace resolved L25 pending language with the actual results.
- Treat the Gemma forge as initially positive at matched N=600 but near-null in
  the stronger N=900 comparison.
- Report L26 public-kernel reproduction attempts as failures to reproduce the
  expected frontier score.
- Add the strong L27 same-batch negative result.
- Report L28 reasoning-effort results as inconclusive or negative.
- Report GPU submissions as failing to establish the proposed lever.
- Report L29 as below the strongest control/high-water mark.
- Report the L31 fast-emit result as negative and leave the chainpack results
  pending only while the live records remain pending.
- Replace universal hardware-ceiling language with the narrower observation
  that no monotonic gain was observed in the tested candidate range.
- Do not infer the hidden private guardrail's behavior from its module name.
- Treat competitor-mechanism statements as artifact observations unless exact
  revisions and board transfer are documented.
- Explain the 9,000-second generation budget and separate 9,000-second replay
  windows accurately.
- Flag official-documentation discrepancies where evaluator source differs.

### 11.3 Evidence and reproducibility improvements

- Pin the SDK version and relevant source revision.
- Use full repository-relative source paths and verified line citations.
- Add submission IDs, dates, statuses, configurations, and scores.
- Separate `ERROR`-status historical scores from `COMPLETE` results.
- Add a competitor-artifact audit table with repository/kernel revision IDs.
- Add threats to validity: run variance, hidden hardware, contaminated controls,
  unknown aggregation, evaluator changes, and absent private-guardrail source.
- Add a claim-status table distinguishing facts, observations, inferences, and
  open hypotheses.
- Add relevant scholarly references rather than relying exclusively on source
  citations.

### 11.4 Competition-award alignment

The rewrite will explicitly optimize for the official Working Note criteria:

- technical clarity and reproducibility;
- methodological contribution;
- security insight;
- usefulness to the benchmark community;
- responsible communication.

Leaderboard rank will be treated as supporting evidence, not the note's central
claim of value.

## 12. Literature Strategy for the Second Paper

The related-work section will distinguish:

1. closed-loop robot scientists and self-driving laboratories operating in
   tightly specified hypothesis spaces;
2. LLM agents for literature synthesis, hypothesis generation, coding,
   reproduction, experimentation, and paper generation;
3. benchmarks showing limited end-to-end scientific-task performance;
4. evidence about citation fabrication, calibration, provenance, and the limits
   of agent self-review;
5. authorship and disclosure policies that retain human accountability.

Priority sources include peer-reviewed work on Robot Scientist, the mobile
robotic chemist, A-Lab, scientific-hypothesis generation, citation fabrication,
and ScienceAgentBench, plus clearly labeled preprints or official releases for
PaperQA2, data-to-paper, The AI Scientist, CORE-Bench, DiscoveryBench, and
PaperBench. Every reference must be opened and checked against the claim it is
used to support.

## 13. Practical Governance Framework

The second paper will derive a practical framework from the cases. The framework
will cover:

- evidence before confidence;
- direct-source verification;
- explicit hypothesis and falsification criteria;
- separation of local and live validation;
- independent or memory-blind review;
- controlled model switching for perspective diversity;
- treatment of persistent memory as untrusted until revalidated;
- human approval for costly, shared, or irreversible actions;
- preservation of negative results;
- clear stopping and escalation rules;
- disclosure and provenance for AI-assisted work.

The framework must arise from observed case evidence and relevant literature,
not from a decorative acronym invented in advance.

## 14. Risks and Mitigations

### 14.1 Post-hoc storytelling

**Risk:** The final narrative selects only memorable successes and failures.

**Mitigation:** Use dated transcripts, commits, submissions, and preregistered or
pre-arm experiment documents; preserve unresolved claims in each snapshot.

### 14.2 Double-counted histories

**Risk:** Imported sessions and subagent records inflate activity counts.

**Mitigation:** Deduplicate by session provenance, timestamp, parent-child
relationships, and matching content.

### 14.3 Provider-ranking temptation

**Risk:** Unequal usage is mistaken for comparative evidence.

**Mitigation:** Report provider differences as observations only and analyze
switching as workflow diversity.

### 14.4 Confidentiality and credential exposure

**Risk:** Raw transcripts contain secrets or operational details.

**Mitigation:** Quote selectively, redact secrets, and publish derived evidence
tables rather than raw databases.

### 14.5 Overclaiming originality

**Risk:** Recombination of public work is described as autonomous discovery.

**Mitigation:** Code hypothesis origin explicitly and distinguish reproduction,
adaptation, recombination, and novel validated finding.

### 14.6 Competition-specific metric gaming

**Risk:** Leaderboard optimization is conflated with general scientific value.

**Mitigation:** Treat the competitions as bounded research environments and
separate benchmark insight from real-world generalization.

## 15. Verification and Completion Criteria

Before either manuscript is described as complete:

- all competition claims must be checked against current live records;
- all code-mechanics claims must be checked against pinned source;
- every scholarly citation must resolve and support the associated claim;
- quotes must be traced to their source record and checked for context;
- quantitative counts must have a reproducible derivation;
- claims based on Ahmed's recollection must be labeled accordingly;
- current pending experiments must be updated or preserved as pending with a
  dated cutoff;
- both manuscripts must pass a contradiction, placeholder, and unsupported-
  superlative review;
- the final paper must disclose AI assistance and retain Ahmed as the accountable
  sole author.

## 16. Implementation Boundary

This specification authorizes manuscript and evidence-file changes only after
Ahmed reviews and approves the written design. It does not authorize:

- new Kaggle submissions;
- changes to competition code or experiment configurations;
- pushes, deployments, publication, or submission of either paper;
- edits to the ARC-AGI-3 working tree;
- disclosure of raw private transcripts.

Publication, competition submission, and other shared-state actions require a
separate explicit approval.
