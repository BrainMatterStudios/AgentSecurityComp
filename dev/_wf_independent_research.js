export const meta = {
  name: 'jed-independent-research',
  description: 'Clean-room independent research on the AI-Agent-Security tool-attack Kaggle comp: derive scoring, cost, and top strategies from SDK ground truth + web, with zero access to the prior team\'s analysis',
  phases: [
    { title: 'Research', detail: '5 blind strands: SDK scoring, SDK cost/throughput, comp web-meta, attack techniques, scored-model internals' },
    { title: 'Synthesize', detail: 'dedup + rank candidate strategies against SDK ground truth' },
    { title: 'Verify', detail: 'adversarial feasibility check of each top strategy against the real scoring/guardrail/cost code' },
  ],
}

// ---- Neutral brief (objective facts only; NO prior conclusions) ----
const BRIEF = `
You are researching a live Kaggle competition: "AI Agent Security: Multi-Step Tool Attacks"
(competition slug: ai-agent-security-multi-step-tool-attacks). It is an OFFENSIVE red-team
competition: entrants submit an attack policy that drives two tool-using LLM agents to take
unsafe actions; a scoring gateway replays the attack against each model under guardrails and
awards points. The public leaderboard is the mean of two per-model public scores. The two
scored models and all scoring/guardrail/gateway rules are DEFINED IN CODE in this repo under:
  comp/aicomp_sdk/            (the competition SDK: scoring.py, core/predicates.py, core/cells.py,
                               guardrails/, core/env/, agents/)
  comp/kaggle_evaluation/jed_attack_134815/  (the gateway + per-model servers)
This SDK is the AUTHORITATIVE, objective rulebook. Read it directly.

HARD FIREWALL — to keep this investigation independent, you MUST NOT read, open, grep, or rely
on ANY of the following (they contain a prior team's analysis and would bias you):
  - any *.md file (HANDOFF.md, STRATEGY.md, COMPETITION.md, README.md, etc.)
  - attack.py, run_smoke_test.py, mock_env/, agentsec/
  - anything under dev/, submission_kernel_*/, refkernels/, notebooks/, out_*/, research_kernel_*/
  - EXPERIMENT_REPORT.html, and any memory/ directory
If you accidentally open one, discard it and note that you did. Base every claim ONLY on the SDK
source under comp/ and on your own web research. Cite file:line for code claims.

GOAL: independently determine (a) exactly how score is computed and what maximizes it, (b) the
real per-attack cost/throughput and time-budget structure that bounds how much you can score,
and (c) the highest-leverage concrete attack STRATEGIES to maximize the public leaderboard mean.
Think like a fresh strong competitor. Do not assume the prior team was right about anything.`;

const FIND_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['strand', 'findings', 'strategies'],
  properties: {
    strand: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['claim', 'evidence'],
        properties: {
          claim: { type: 'string' },
          evidence: { type: 'string', description: 'file:line citation or URL/source' },
          confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
        },
      },
    },
    strategies: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['name', 'mechanism', 'expected_leverage'],
        properties: {
          name: { type: 'string' },
          mechanism: { type: 'string', description: 'concretely how it raises score, tied to the scoring/cost code' },
          expected_leverage: { type: 'string', description: 'rough size of the win and why' },
          how_to_test: { type: 'string' },
        },
      },
    },
  },
};

const SYNTH_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['scoring_model', 'cost_model', 'ranked_strategies'],
  properties: {
    scoring_model: { type: 'string', description: 'the independently-derived score formula + what maximizes it, with citations' },
    cost_model: { type: 'string', description: 'the independently-derived per-attack cost / time-budget structure, with citations' },
    ranked_strategies: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['rank', 'name', 'mechanism', 'expected_effect', 'novelty', 'risk'],
        properties: {
          rank: { type: 'integer' },
          name: { type: 'string' },
          mechanism: { type: 'string' },
          expected_effect: { type: 'string' },
          novelty: { type: 'string', description: 'how non-obvious this is' },
          risk: { type: 'string' },
        },
      },
    },
  },
};

const VERDICT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['strategy', 'actually_scores', 'reasoning', 'verdict'],
  properties: {
    strategy: { type: 'string' },
    actually_scores: { type: 'boolean', description: 'given the REAL scoring+guardrail+cost code, does this raise the LB mean?' },
    reasoning: { type: 'string', description: 'cite the SDK code that makes it work or fail' },
    expected_magnitude: { type: 'string' },
    blockers: { type: 'string' },
    verdict: { type: 'string', enum: ['PROMISING', 'MARGINAL', 'DEAD'] },
  },
};

const STRANDS = [
  { key: 'sdk-scoring', web: false, prompt:
    `Read ONLY comp/aicomp_sdk/scoring.py, comp/aicomp_sdk/core/predicates.py, comp/aicomp_sdk/core/cells.py, and whatever they import. Independently derive the EXACT score formula: what events earn points, severity/weights, any dedup or per-cell/per-finding bonuses, caps, and normalization. State precisely what an attacker must maximize to raise the per-model score, and how the public LB mean is formed. Propose concrete strategies that follow directly from the scoring code. Cite file:line for everything.` },
  { key: 'sdk-cost', web: false, prompt:
    `Read ONLY comp/kaggle_evaluation/jed_attack_134815/*.py (gateway, inference server, model servers) and comp/aicomp_sdk/core/env/* and comp/aicomp_sdk/agents/* . Independently derive the COST/THROUGHPUT structure that bounds scoring: any per-phase time budget / deadline, how many attack candidates can be replayed, what each candidate costs (generation, tool hops, model prefill/decode), whether the model KV cache or prompt prefix is reused across candidates or re-computed each time, and what happens on timeout (partial credit vs total void). This determines how many scoring events you can fit. Verify the KV/prefix-reuse question directly from the llama.cpp backend + reset semantics — do not assume. Propose strategies that increase the number of scoring events within the budget. Cite file:line.` },
  { key: 'web-comp', web: true, prompt:
    `Web research ONLY (plus, if needed, identify the two scored model names from comp/ model-server files). Find everything public about the Kaggle competition "AI Agent Security: Multi-Step Tool Attacks": its leaderboard shape and top scores, any public notebooks/kernels, forum/discussion threads, host clarifications, and known winning approaches or write-ups. Summarize what top competitors appear to be doing and any published score ceilings. Cite URLs. Propose strategies grounded in what the field is actually doing.` },
  { key: 'web-technique', web: true, prompt:
    `Web research ONLY. Survey state-of-the-art techniques for: driving tool-using LLM agents to perform unsafe actions (prompt injection, indirect/tool-result injection, multi-step tool attacks), forcing/steering model generation via chat-template control tokens or assistant-prefix forcing, maximizing the count of harmful tool calls a single agent turn emits, and gaming replay-based scoring harnesses. Focus on techniques that would raise the number of successful unsafe tool-call events. Cite URLs. Propose concrete strategies.` },
  { key: 'web-models', web: true, prompt:
    `First identify the two scored models from comp/ (their GGUF paths in the model-server files) — do NOT read any *.md or attack.py. Then web-research those exact models (e.g. gpt-oss-20b and the gemma variant): their chat template + special/control tokens, tool-calling output format, whether the tokenizer round-trips control tokens typed as text (relevant to prefix-forcing), reasoning vs non-reasoning behavior, and decode-speed/latency characteristics on a T4-class GPU. Identify per-model tricks to force many tool calls cheaply. Cite URLs and file:line for the model identity.` },
];

phase('Research');
const research = (await parallel(STRANDS.map(s => () =>
  agent(BRIEF + '\n\n---\nYOUR STRAND: ' + s.key + '\n' + s.prompt +
    (s.web ? '\n\nUse web search/fetch: call ToolSearch with query "select:WebSearch,WebFetch" first to load them, then research.' : '\n\nThis is a code-reading strand: use Read/Grep on comp/ only.'),
    { label: 'research:' + s.key, phase: 'Research', schema: FIND_SCHEMA, effort: 'high' }
  )))).filter(Boolean);

log(`research strands returned: ${research.length}/${STRANDS.length}`);

phase('Synthesize');
const packed = research.map(r => `## strand ${r.strand}\nFINDINGS:\n` +
  (r.findings || []).map(f => `- [${f.confidence || '?'}] ${f.claim}  (${f.evidence})`).join('\n') +
  `\nSTRATEGIES:\n` + (r.strategies || []).map(s => `- ${s.name}: ${s.mechanism} | leverage: ${s.expected_leverage} | test: ${s.how_to_test || ''}`).join('\n')
).join('\n\n');

const synth = await agent(
  `You are the independent synthesis lead. Below are findings + candidate strategies from 5 blind research strands on the Kaggle competition "AI Agent Security: Multi-Step Tool Attacks". You may re-check any claim against the SDK under comp/ (cite file:line). You MUST NOT read any *.md, attack.py, dev/, memory/, or submission_kernel_* — stay independent.\n\nProduce: (1) the independently-derived SCORING model, (2) the independently-derived COST/throughput model, (3) a de-duplicated, ranked list of the highest-leverage concrete strategies to maximize the public LB mean. Rank by expected effect × feasibility. Prefer strategies grounded in the actual scoring/cost code over speculation. Note novelty and risk for each.\n\n=== STRAND OUTPUTS ===\n${packed}`,
  { label: 'synthesize', phase: 'Synthesize', schema: SYNTH_SCHEMA, effort: 'high' }
);

phase('Verify');
const top = (synth.ranked_strategies || []).slice(0, 4);
const verdicts = (await parallel(top.map(s => () =>
  agent(
    `Adversarially verify ONE proposed competition strategy against the REAL rules. Read the relevant SDK code under comp/ (scoring.py, predicates.py, cells.py, guardrails/, the gateway, env, agents, llama.cpp backend) and decide whether this strategy would ACTUALLY raise the public leaderboard mean, or whether the scoring/guardrail/cost code defeats it. Be skeptical; default to DEAD if the code doesn't clearly support it. Do NOT read any *.md, attack.py, dev/, memory/, or submission_kernel_*. Cite file:line.\n\nSTRATEGY: ${s.name}\nMECHANISM: ${s.mechanism}\nCLAIMED EFFECT: ${s.expected_effect}`,
    { label: 'verify:' + (s.name || 'x').slice(0, 24), phase: 'Verify', schema: VERDICT_SCHEMA, effort: 'high' }
  ).then(v => ({ ...v, rank: s.rank }))
))).filter(Boolean);

return {
  scoring_model: synth.scoring_model,
  cost_model: synth.cost_model,
  ranked_strategies: synth.ranked_strategies,
  verdicts,
};
