# AI Agents in Scientific Research Case Study Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a living, wide-audience Markdown case study evaluating how AI coding agents enabled and constrained Ahmed Mobasher's participation in two unfamiliar computational-research competitions.

**Architecture:** Build a privacy-safe evidence ledger from both repositories, agent histories, live results, and the author interview. Code representative research episodes, synthesize them against primary AI-for-science literature, and draft from verified cross-case findings rather than a retrospective success narrative.

**Tech Stack:** Markdown, Git, `rg`, `jq`, SQLite, Kaggle CLI, Claude Code JSONL, Codex JSONL, OpenCode SQLite, DOI/arXiv/OpenReview sources

**Spec:** `docs/superpowers/specs/2026-08-16-paper-revision-and-agent-research-design.md`

## Global Constraints

- Ahmed Mobasher is sole author; disclose AI assistance in methods and acknowledgements.
- Use AgentSecurityComp as primary case and ARC-AGI-3 as comparative case.
- Treat OpenCode/DeepSeek as supplementary evidence, not a balanced comparison.
- Do not claim autonomous discovery, measured productivity gains, or provider superiority.
- Label retrospective testimony and counterfactual judgments.
- Deduplicate imported, continued, parent, and subagent sessions before counts.
- Quote only short, authorized, context-preserving excerpts; exclude secrets and unrelated personal content.
- Treat both competitions as ongoing and use a dated evidence cutoff.
- Do not modify the ARC-AGI-3 working tree.
- Do not submit, publish, push, deploy, or alter shared competition state.
- Keep current deliverables in Markdown; defer PDF and HTML.

## File Structure

- Create `paper/evidence/ai-agents-research-evidence.md`: provenance inventory, coded episodes, counts, quote ledger, literature matrix, and living outcomes.
- Create `paper/ai_agents_in_scientific_research.md`: wide-audience comparative case-study manuscript with references.

---

### Task 1: Build the Research Provenance Inventory

**Files:**
- Create: `paper/evidence/ai-agents-research-evidence.md`

**Interfaces:**
- Consumes: Claude, Codex, and OpenCode stores; both Git repositories; interview; approved spec.
- Produces: deduplicated evidence-source map and privacy rules.

- [ ] **Step 1: Record repository boundaries**

Run:

```bash
git -C /Users/ahmed/Documents/AgentSecurityComp rev-parse HEAD
git -C /Users/ahmed/Documents/AgentSecurityComp log -1 --format='%H %cI %s'
git -C /Users/ahmed/Documents/ArcAGI3 rev-parse HEAD
git -C /Users/ahmed/Documents/ArcAGI3 log -1 --format='%H %cI %s'
```

Expected: one hash and dated commit for each repository; no writes to ARC-AGI-3.

- [ ] **Step 2: Inventory Claude sessions**

Run:

```bash
find /Users/ahmed/.claude/projects/-Users-ahmed-Documents-AgentSecurityComp \
  /Users/ahmed/.claude/projects/-Users-ahmed-Documents-ArcAGI3 \
  -type f -name '*.jsonl' -print | sort
```

Classify paths as primary session, subagent, workflow journal, scratchpad copy, or tool-result derivative. Exclude tool-result derivatives from conversation counts.

- [ ] **Step 3: Inventory Codex sessions**

Run:

```bash
rg -l 'AgentSecurityComp|/Users/ahmed/Documents/ArcAGI3' \
  /Users/ahmed/.codex/sessions -g '*.jsonl' | sort
```

Inspect metadata to separate native Codex work from imported or continued history.

- [ ] **Step 4: Inventory OpenCode without reading credentials**

Run:

```bash
sqlite3 -header -column /Users/ahmed/.local/share/opencode/opencode.db \
  "select id, datetime(time_created/1000,'unixepoch') created, directory, title, model, tokens_input, tokens_output from session where lower(directory) like '%agentsecuritycomp%' or lower(directory) like '%arcagi3%' order by time_created;"
```

Record parent and specialist sessions separately. Never query or export the `credential` table.

- [ ] **Step 5: Create the evidence ledger**

Use:

```markdown
# AI Agents in Research Evidence Ledger

## Evidence cutoff and repository revisions
## Privacy and quotation rules
## Session provenance and deduplication
## Author baseline and interview testimony
## AgentSecurityComp chronology
## ARC-AGI-3 chronology
## Coded research episodes
## Quote ledger
## Descriptive measures and derivations
## Literature claim matrix
## Living outcomes register
## Known evidence gaps
```

- [ ] **Step 6: Record approved author testimony**

Record as retrospective testimony:

```text
16+ consulting years in decisioning, omnichannel AI, architecture, and early Java.
Rusty independent coding; Python mainly with AI assistance.
Goal: test agent-led research with little domain guidance.
Role: approve, challenge, and encourage depth/breadth rather than supply hypotheses.
Oversight: 2-5 hours/day.
Direct spend: about USD 100 OpenRouter, USD 30 Modal, plus Colab Pro and Claude/Codex subscriptions.
Value: enabled meaningful participation and accelerated contextual learning.
Current outcome: neither winning objective achieved.
Trust issue: confident claims often weakened after challenge; stale records propagated errors.
No clear unexpected agent-originated discovery came to mind.
```

- [ ] **Step 7: Verify privacy and placeholders**

Run:

```bash
rg -n -i 'api[_ -]?key|authorization:|bearer |password[=:]|token[=:]' paper/evidence/ai-agents-research-evidence.md
rg -n '\b(TBD|TODO|FIXME|XXX)\b|<[^>]+>' paper/evidence/ai-agents-research-evidence.md
git diff --check -- paper/evidence/ai-agents-research-evidence.md
```

Expected: no secret values, placeholders, or diff errors.

- [ ] **Step 8: Commit provenance inventory**

```bash
git add paper/evidence/ai-agents-research-evidence.md
git commit -q \
  -m "docs: create AI research evidence ledger" \
  -m "- inventory agent and repository provenance
- record interview testimony and privacy rules
- define deduplication and living outcomes

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 2: Code Representative Research Episodes

**Files:**
- Modify: `paper/evidence/ai-agents-research-evidence.md`

**Interfaces:**
- Consumes: provenance inventory.
- Produces: cross-case table supporting claims about value, autonomy, failure, and governance.

- [ ] **Step 1: Define episode schema**

Use:

```markdown
| Case | Date | Episode | Origin | Prior evidence | Agent confidence | Human intervention | Local outcome | Live outcome | Final status | Lesson | Source IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|
```

Allowed origins: `human`, `agent`, `external`, `mixed`. Allowed statuses: `confirmed`, `partially supported`, `refuted`, `invalid experiment`, `superseded`, `open`.

- [ ] **Step 2: Code at least 12 AgentSecurityComp episodes**

Include SDK scaffold, volume hypothesis, SECRET_MARKER change, adaptive sizing, close_ok, message packing, Gemma test correction, router failure, commitment forge, dual/Gemma forge, L27, GPU, and L29/L31.

- [ ] **Step 3: Code at least 12 ARC-AGI-3 episodes**

Include role-typed perception, search-replay, reset correction, EWM reversal, fine-tune serving failure, leaderboard-noise doctrine, HUD correction, token-diet reversal, best-of-N, structural campaign, Stage 2b, and Qwen 3.8 adoption.

- [ ] **Step 4: Code OpenCode/DeepSeek episodes**

Include the primary AgentSecurityComp investigation and principal ARC-AGI-3 investigations. Link specialist sessions to parent orchestrations instead of treating them as independent projects.

- [ ] **Step 5: Derive descriptive counts**

Count episodes by origin and final status. Record exact ledger row identifiers used in every count so the derivation is reproducible.

- [ ] **Step 6: Select and verify 8-12 quotes**

Cover original goal, confident claim, human challenge, retraction, memory-blind instruction, invalid experiment, evidence gate, and Ahmed's value/originality assessment. Record session ID, locator, date, speaker, and context.

- [ ] **Step 7: Check table completeness**

Run:

```bash
rg -n '^\|' paper/evidence/ai-agents-research-evidence.md | wc -l
rg -n 'confirmed|partially supported|refuted|invalid experiment|superseded|open' paper/evidence/ai-agents-research-evidence.md
git diff --check -- paper/evidence/ai-agents-research-evidence.md
```

Expected: at least 24 episode rows, documented status values, and no diff errors.

- [ ] **Step 8: Commit coded cases**

```bash
git add paper/evidence/ai-agents-research-evidence.md
git commit -q \
  -m "docs: code comparative AI research episodes" \
  -m "- trace hypotheses through implementation and outcome
- distinguish human, agent, external, and mixed origins
- record corrections and governance lessons

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 3: Build and Verify the Literature Matrix

**Files:**
- Modify: `paper/evidence/ai-agents-research-evidence.md`

**Interfaces:**
- Consumes: opened primary papers and official policy pages.
- Produces: claim-level source matrix and verified reference inventory.

- [ ] **Step 1: Verify peer-reviewed anchors**

Open and record DOI, title, venue, year, supported finding, and limitation for:

```text
10.1038/nature02236
10.1038/s41586-020-2442-2
10.1038/s41586-023-06734-w
10.1016/j.jmat.2023.08.007
10.1038/s41598-023-41032-5
ScienceAgentBench, OpenReview 6z4YKr0GK6
10.1038/s41586-026-10644-y
```

- [ ] **Step 2: Verify preprints and official releases**

Open and label status for data-to-paper (`2404.17605`), The AI Scientist (`2408.06292`), DiscoveryBench (`2407.01725`), CORE-Bench (`2409.11363`), PaperQA2 (`2409.13740`), LLM research ideas (`2409.04109`), MARG (`2401.04259`), and PaperBench.

- [ ] **Step 3: Verify disclosure policy**

Open current ICMJE AI guidance and Springer Nature's LLM authorship/disclosure policy. Record only supported policy claims.

- [ ] **Step 4: Populate literature matrix**

Use:

```markdown
| Source | Status | Scientific task | Supported finding | Limitation | Manuscript claim |
|---|---|---|---|---|---|
```

Paraphrase findings; keep any direct quotation below 25 words per source.

- [ ] **Step 5: Validate identifiers and links**

Run:

```bash
rg -o 'https?://[^ )]+' paper/evidence/ai-agents-research-evidence.md | sort -u
rg -n '10\.1038/|10\.1016/|arXiv|OpenReview|PaperBench|ICMJE' paper/evidence/ai-agents-research-evidence.md
git diff --check -- paper/evidence/ai-agents-research-evidence.md
```

Open every listed URL and confirm it resolves to the primary or official source.

- [ ] **Step 6: Commit literature matrix**

```bash
git add paper/evidence/ai-agents-research-evidence.md
git commit -q \
  -m "docs: verify AI-for-science literature matrix" \
  -m "- separate peer-reviewed work from preprints
- map sources to bounded claims
- record limitations and authorship guidance

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 4: Draft Opening, Background, and Method

**Files:**
- Create: `paper/ai_agents_in_scientific_research.md`
- Consult: `paper/evidence/ai-agents-research-evidence.md`

**Interfaces:**
- Consumes: verified baseline, case evidence, and literature.
- Produces: framing, questions, methods contract, and disclosure.

- [ ] **Step 1: Create manuscript skeleton**

Use:

```markdown
# Access Without Autonomy: An Instrumented Case Study of AI Agents in Computational Research

## Abstract
## 1. From Enterprise Architecture to Computational Research
## 2. What Counts as an AI Research Agent?
## 3. Research Questions and Method
## 4. Case I: AI Agent Security
## 5. Case II: ARC-AGI-3
## 6. Cross-Case Findings
## 7. Where Agents Add Value
## 8. Where Agents Struggle
## 9. Governing AI-Assisted Research
## 10. Implications
## 11. Limitations and Living Outcomes
## Acknowledgements and AI-Use Disclosure
## References
## Appendix A: Evidence and Coding Method
```

- [ ] **Step 2: Draft opening narrative**

Introduce Ahmed's background, unfamiliar domains, limited independent Python practice, original autonomy experiment, and 2-5 hours/day oversight. Do not equate architecture expertise with domain-science expertise.

- [ ] **Step 3: Draft AI-for-science background**

Contrast bounded robot scientists and autonomous laboratories with LLM agents performing literature, coding, ideation, and paper generation. Keep publication status visible.

- [ ] **Step 4: Draft research questions and method**

State the five approved questions. Describe comparative N-of-1 design, data, episode unit, coding, evidence tiers, deduplication, quote authorization, and living policy.

- [ ] **Step 5: State limitations early**

Name no human-only control, changing platforms, unequal use, noisy competition proxies, and retrospective testimony.

- [ ] **Step 6: Draft AI-use disclosure**

Name Ahmed as sole author. Describe Claude Code as primary, Codex/DeepSeek as perspective resets, and this Codex collaboration's evidence/drafting role. Retain Ahmed's accountability.

- [ ] **Step 7: Verify opening sections**

Run:

```bash
rg -n 'autonomous|prove|productivity|better than|sole author|2-5|16 years' paper/ai_agents_in_scientific_research.md
git diff --check -- paper/ai_agents_in_scientific_research.md
```

Expected: bounded claims, accurate testimony, and no diff errors.

- [ ] **Step 8: Commit framed manuscript**

```bash
git add paper/ai_agents_in_scientific_research.md
git commit -q \
  -m "docs: frame AI research case study" \
  -m "- establish audience, questions, and method
- distinguish access from scientific autonomy
- disclose AI roles and limitations

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 5: Draft the Two Competition Cases

**Files:**
- Modify: `paper/ai_agents_in_scientific_research.md` case sections
- Consult: `paper/evidence/ai-agents-research-evidence.md`

**Interfaces:**
- Consumes: coded episodes and quotes.
- Produces: two evidence-backed narratives that remain analytically distinct.

- [ ] **Step 1: Draft AgentSecurityComp chronology**

Cover entry, SDK changes, score progression, adaptive sizing, public-method dependence, local/live failures, router invalidity, late ladders, and unachieved goal.

- [ ] **Step 2: Add three AgentSecurityComp vignettes**

Use adaptive sizing for practical value, router or premature breakthrough for failure, and evidence gates for governance. Cite transcript, commit, and live result where available.

- [ ] **Step 3: Draft ARC-AGI-3 chronology**

Cover autonomous exploration, search/replay and perception, serving/evaluation failures, hypothesis closure, public-signal noise, external methods/models, and unachieved goal.

- [ ] **Step 4: Add three ARC-AGI-3 vignettes**

Use harness/perception for value, fine-tune serving or dev-hidden reversal for failure, and “every submission is an experiment” plus memory-blind reassessment for governance.

- [ ] **Step 5: Add provider-switching account**

Describe fresh systems as diversity/reset mechanisms, not independent corroboration or a ranking.

- [ ] **Step 6: Add case evidence tables**

For each case use:

```markdown
| Phase | Agent contribution | Human contribution | External dependence | Outcome | Lesson |
```

- [ ] **Step 7: Trace every paragraph**

Associate each case paragraph with at least one ledger row or testimony entry. Remove untraceable claims or label them retrospective interpretation.

- [ ] **Step 8: Commit case narratives**

```bash
git add paper/ai_agents_in_scientific_research.md
git commit -q \
  -m "docs: draft comparative AI research cases" \
  -m "- trace both competitions from hypothesis to outcome
- distinguish agent, human, and external contributions
- document correction and unachieved goals

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 6: Synthesize Findings and Governance

**Files:**
- Modify: `paper/ai_agents_in_scientific_research.md` synthesis sections
- Consult: `paper/evidence/ai-agents-research-evidence.md`

**Interfaces:**
- Consumes: case narratives and coded evidence.
- Produces: main analysis and practical guidance.

- [ ] **Step 1: Draft cross-case findings**

Cover access without mastery, execution without dependable originality, external recombination, substantial oversight, learning through review, overconfidence, memory contamination, provider switching, and live evidence as authority.

- [ ] **Step 2: Draft where agents add value**

Use observed evidence for navigation, implementation, instrumentation, experiment generation, operations, literature discovery, and onboarding. Distinguish artifacts from scientific insight.

- [ ] **Step 3: Draft where agents struggle**

Use evidence for hypothesis selection, novelty, calibration, due diligence, causal inference, validity, stopping, stale memory, and local-live transfer.

- [ ] **Step 4: Derive governance framework**

Include direct-source verification, falsifiable hypotheses, matched controls, local/live gates, untrusted memory, memory-blind review, model switching for diversity, human approval, preserved negatives, pre-outcome confidence, and stopping/escalation rules.

- [ ] **Step 5: Relate findings to literature**

Contrast the cases with engineered closed loops, ScienceAgentBench/PaperBench, data-to-paper provenance, literature agents, citation fabrication, and AI Scientist audits.

- [ ] **Step 6: Check frequency claims**

Every `often`, `most`, `rarely`, or `consistently` statement must cite coded counts or become a case-bounded qualitative observation.

- [ ] **Step 7: Commit synthesis**

```bash
git add paper/ai_agents_in_scientific_research.md
git commit -q \
  -m "docs: synthesize AI research findings" \
  -m "- distinguish access, execution, and originality
- derive failures from both cases
- turn observed controls into governance guidance

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 7: Complete Living Outcomes, References, and Appendix

**Files:**
- Modify: `paper/ai_agents_in_scientific_research.md`
- Modify: `paper/evidence/ai-agents-research-evidence.md`

**Interfaces:**
- Consumes: all sections and evidence.
- Produces: complete Markdown review draft with explicit open outcomes.

- [ ] **Step 1: Draft implications**

Address researchers, IT professionals, research leaders, and tool builders. Mark which lessons are case-specific and which align with broader evidence.

- [ ] **Step 2: Complete limitations**

Include N-of-1, no control, testimony, selection bias, changing models, unequal use, overlapping histories, competition metrics, hidden evaluators, external dependence, and ongoing outcomes.

- [ ] **Step 3: Create living-outcomes register**

Record evidence cutoff, current scores/status, deadlines, confirmed costs, oversight estimate, and categories reserved for final post-competition revision. Do not leave blank placeholders.

- [ ] **Step 4: Write abstract last**

Use 250-350 words covering problem, method, cases, findings, governance, and limitations without inventing final outcomes.

- [ ] **Step 5: Add verified references**

Use consistent Markdown citations with DOI or official URL. Verify author, year, title, venue/status, and identifier.

- [ ] **Step 6: Add Appendix A**

Describe deduplication, coding, evidence tiers, quotes, cost accounting, and final-outcome update procedure.

- [ ] **Step 7: Run rhetoric and mechanical checks**

Run:

```bash
rg -n '\b(TBD|TODO|FIXME|XXX)\b|<[^>]+>' paper/ai_agents_in_scientific_research.md paper/evidence/ai-agents-research-evidence.md
rg -n 'prove|autonomous scientist|replaced researchers|more productive|best model|superior model|discovery' paper/ai_agents_in_scientific_research.md
rg -n 'often|most|rarely|consistently|always|never' paper/ai_agents_in_scientific_research.md
git diff --check -- paper/ai_agents_in_scientific_research.md paper/evidence/ai-agents-research-evidence.md
wc -w paper/ai_agents_in_scientific_research.md
```

Expected: no placeholders, bounded strong/frequency claims, no diff errors, and recorded word count.

- [ ] **Step 8: Commit review draft**

```bash
git add paper/ai_agents_in_scientific_research.md paper/evidence/ai-agents-research-evidence.md
git commit -q \
  -m "docs: complete living AI research manuscript" \
  -m "- add implications, limitations, and living outcomes
- verify references and disclosure
- prepare Markdown for author review

Co-Authored-By: Codex <noreply@openai.com>"
```

---

### Task 8: Independent Final Verification

**Files:**
- Review: `paper/ai_agents_in_scientific_research.md`
- Review: `paper/evidence/ai-agents-research-evidence.md`
- Review: `docs/superpowers/specs/2026-08-16-paper-revision-and-agent-research-design.md`

**Interfaces:**
- Consumes: complete manuscript and ledger.
- Produces: verified Markdown ready for Ahmed's review, not publication.

- [ ] **Step 1: Trace every quotation**

Confirm speaker, date, context, and character-level accuracy. Confirm redactions preserve meaning.

- [ ] **Step 2: Trace every quantity**

Verify duration, commits, submissions, scores, costs, oversight, sessions, and episode counts. Distinguish query results from estimates.

- [ ] **Step 3: Audit literature claims**

Open every cited primary or official source and confirm direct support for the adjacent claim. Remove decorative citations.

- [ ] **Step 4: Audit contradictions**

Ensure the paper does not pair autonomy claims with substantial oversight, rank providers, state ongoing outcomes as final, or relabel adaptation as original discovery.

- [ ] **Step 5: Run privacy and mechanical checks**

Run:

```bash
rg -n -i '(api[_ -]?key|authorization:|bearer |password[=:]|token[=:])' paper/ai_agents_in_scientific_research.md paper/evidence/ai-agents-research-evidence.md
rg -n '\b(TBD|TODO|FIXME|XXX)\b' paper/ai_agents_in_scientific_research.md paper/evidence/ai-agents-research-evidence.md
git diff --check 04af340..HEAD -- paper/ai_agents_in_scientific_research.md paper/evidence/ai-agents-research-evidence.md
git status --short --branch
```

Expected: no secret values, placeholders, or diff errors; only known unrelated changes remain.

- [ ] **Step 6: Prepare author-review handoff**

Report evidence cutoff, word count, source count, episode count, quotes used, open outcomes, commits, and verification commands. Stop before publication, submission, PDF, or HTML work.
