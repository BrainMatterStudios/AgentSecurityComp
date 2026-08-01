export const meta = {
  name: 'jed-plan-review',
  description: 'Independent adversarial review of our JED plan + the armed L13 submissions: audit the cost model, the mix, the strategy, and the private endgame against SDK ground truth; verdict on whether we are on the right track',
  phases: [
    { title: 'Review', detail: '4 adversarial strands: cost-model audit, L13 mix audit, strategy/opportunity-cost, private endgame' },
    { title: 'Synthesize', detail: 'weigh strands -> verdict + ranked risks + concrete mix changes' },
    { title: 'Verify', detail: 'adversarially verify the top course-corrections against source' },
  ],
}

const BRIEF = `
You are an INDEPENDENT, ADVERSARIAL reviewer validating a team's plan for the Kaggle competition
"AI Agent Security: Multi-Step Tool Attacks" (slug ai-agent-security-multi-step-tool-attacks). The
prize is the hidden PRIVATE leaderboard ($50k, deadline 2026-09-01); the public LB = mean of two
per-model attack scores (gpt-oss-20b, gemma-4-26B). Reward flattery with nothing — hunt for what is
WRONG, missing, or a waste of scarce daily submission quota (5/day). Verify every claim against the
authoritative SDK source; do not accept the team's memos on faith.

GROUND TRUTH (authoritative rulebook — read directly, cite file:line):
  comp/aicomp_sdk/            scoring.py, core/predicates.py, core/cells.py, guardrails/optimal.py, core/env/*, agents/*
  comp/kaggle_evaluation/jed_attack_134815/   gateway, model servers, response_parsing.py

THE TEAM'S PLAN + CLAIMS TO AUDIT (treat as hypotheses, not facts):
  Memory: /Users/ahmed/.claude/projects/-Users-ahmed-Documents-AgentSecurityComp/memory/*.md
    (jed-scoring-mechanics-verified.md, gemma-lever-structurally-dead.md, jed-private-board-hedge.md, jed-winning-model.md)
  HANDOFF.md ; attack.py (_run_replay_safe, JED_RS_ONLY board-isolation knob, _RS_TEMPLATES, _FP_PROBES)
  Their measurement scripts + LOGS (the evidence for their claims):
    dev/_gemma_native_forge.py + logs/gemma_native_forge.log   (multipost dead: posts/turn caps 0.5)
    dev/_gemma_special_probe.py                                  (gemma control tokens don't round-trip)
    dev/_gemma_kv_probe.py + logs/gemma_kv_probe.log            (KV prefix reuse ON)
    dev/_gemma_prefill_count.py + logs/gemma_prefill_count.log  (schema reused: 1110->28 tok)
    dev/_rs_only_smoke.py + logs/rs_only_smoke.log             (JED_RS_ONLY isolation works)

THE ARMED SUBMISSIONS (fire tonight at 00:00 UTC — dev/_build_l13.py, submission_kernel_l13_*/):
  1 pt-safe  : pool FRAC97, BOTH boards            -> ~89.6 anchor/floor
  2 pt-probe : gpt-only  FRAC97 (JED_RS_ONLY=gpt)  -> publicScore = gpt_row/2
  3 k1nx-1000: gemma-only FRAC97 (JED_RS_ONLY=gemma)-> publicScore = gemma_row/2
  4 k1nx-1200: gpt-only  FRAC99                     -> gpt headroom probe
  5 k1nx-800 : blended FRAC96, both boards          -> conservative climb bet
Best validated public so far = ~89.6. Team thesis: gemma is structurally maxed (~row58); gpt is the
only public lever; the ~110 leaders max gpt; private board likely rewards email.send CONFUSED_DEPUTY
where http.post EXFIL may be blocked.

Your job: is this plan on the right track? Where is it wrong or wasteful? Cite file:line / log lines.`;

const REVIEW_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['strand', 'findings', 'recommendations'],
  properties: {
    strand: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['issue', 'severity', 'evidence'],
        properties: {
          issue: { type: 'string', description: 'a flaw, error, risk, or wasted opportunity in the plan/mix' },
          severity: { type: 'string', enum: ['high', 'medium', 'low'] },
          evidence: { type: 'string', description: 'file:line or log line; or the SDK code that proves it' },
          claim_verdict: { type: 'string', enum: ['confirmed-correct', 'wrong', 'unverifiable', 'n/a'], description: 'if auditing a team claim, does it hold?' },
        },
      },
    },
    recommendations: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['action', 'rationale', 'priority'],
        properties: {
          action: { type: 'string' },
          rationale: { type: 'string' },
          priority: { type: 'string', enum: ['now-before-reset', 'this-week', 'later'] },
        },
      },
    },
  },
};

const SYNTH_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['verdict', 'summary', 'top_risks', 'armed_mix_assessment', 'course_corrections', 'rearm_before_reset'],
  properties: {
    verdict: { type: 'string', enum: ['ON_TRACK', 'MINOR_CORRECTION', 'MAJOR_CORRECTION'] },
    summary: { type: 'string' },
    top_risks: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['risk', 'severity', 'evidence'], properties: {
      risk: { type: 'string' }, severity: { type: 'string', enum: ['high', 'medium', 'low'] }, evidence: { type: 'string' } } } },
    armed_mix_assessment: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['rung', 'decision', 'why'], properties: {
      rung: { type: 'string' }, decision: { type: 'string', enum: ['keep', 'change', 'drop'] }, why: { type: 'string' } } } },
    course_corrections: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['action', 'priority', 'rationale'], properties: {
      action: { type: 'string' }, priority: { type: 'string', enum: ['now-before-reset', 'this-week', 'later'] }, rationale: { type: 'string' } } } },
    rearm_before_reset: { type: 'boolean', description: 'should the armed L13 mix be changed before it fires tonight?' },
  },
};

const VERIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['correction', 'sound', 'reasoning'],
  properties: {
    correction: { type: 'string' },
    sound: { type: 'boolean', description: 'is this course-correction actually correct + better than the current plan, per the SDK code?' },
    reasoning: { type: 'string', description: 'cite file:line' },
    caveats: { type: 'string' },
  },
};

const STRANDS = [
  { key: 'cost-model-audit', prompt:
    `Adversarially re-verify the team's FOUR core claims against SDK source AND their probe logs. Try to REFUTE each: (a) throughput is DECODE-bound and the schema KV prefix is REUSED across candidates (check gguf_model_server persistence, reset_state, the llama.cpp backend, and logs/gemma_kv_probe.log + logs/gemma_prefill_count.log); (b) multipost is structurally dead because response_parsing rejects >1 tool_call/generation (response_parsing.py) — confirm and check whether the ≤32 messages/finding × hops structure offers a DIFFERENT throughput path they dismissed; (c) gemma is maxed at ~row58 (control tokens don't round-trip; logs/gemma_native_forge.log, gemma_special_probe); (d) the gpt board has UNUSED headroom (is gpt actually decode-minimized already, or is there a further decode cut — hop1 wrap-up, tool-call format, terser template?). State which claims hold and which are wrong, with citations.` },
  { key: 'l13-mix-audit', prompt:
    `Audit each of the 5 armed L13 rungs for CORRECTNESS and whether it delivers its intended read. Check attack.py JED_RS_ONLY: does the fingerprint (_FP_PROBES) reliably detect the model on the REAL Kaggle T4 (not just the local smoke), and does returning one benign 'Acknowledged.' candidate make that board score EXACTLY 0 (verify against scoring.py/predicates.py — could the benign candidate fire anything, or cause a fallback)? Is the consistency identity slot1 ≈ slot2+slot3 valid given publicScore = mean/2? Void risk at FRAC99/FRAC96 (does the 9000s total-void apply; is FRAC99 gpt-only safe)? Will any rung produce a MISLEADING number? Is blended FRAC96 (slot5) a wasted slot given ~89.6 is the FRAC97 peak?` },
  { key: 'strategy-review', prompt:
    `Opportunity-cost review. It is ~1 month to the 2026-09-01 deadline; quota is 5 submissions/day. Tonight spends 4 of 5 slots on DIAGNOSTICS (board split + gpt headroom) that will not raise the LB. Is that the best use? Interrogate the central thesis "gpt is the only public lever": if gpt is already decode-minimized (close_ok forge applied), gpt-only FRAC99 will be ~flat and the night confirms a DEAD END — is that worth 4 slots, or should we test an actual gpt decode-cut lever tonight instead? Is the public board simply maxed at ~89.6 and should we pivot effort now? What is the single highest-EV use of tonight's 5 slots? Propose the best alternative mix if you have one.` },
  { key: 'private-endgame', prompt:
    `The prize is the hidden PRIVATE board (persistent_provenance guardrail, unreadable; privateScore hidden until 2026-09-01). Every submission is scored on both boards; Kaggle lets you SELECT final submissions. Review the team's private plan: (1) is "email.send CONFUSED_DEPUTY is the private hedge where http.post EXFIL may be blocked" sound — verify the CONFUSED_DEPUTY predicate + how OptimalGuardrail vs a stricter provenance guardrail would treat http.post data vs email.send (predicates.py, guardrails/optimal.py, core/tools/*)? (2) Given we get NO private feedback before the deadline, are we allocating effort correctly by spending nights on public diagnostics? (3) When and how should private hedges be planted/selected? (4) Is there a judged write-up prize we should be resourcing? Give concrete endgame guidance.` },
];

phase('Review');
const reviews = (await parallel(STRANDS.map(s => () =>
  agent(BRIEF + '\n\n---\nYOUR REVIEW STRAND: ' + s.key + '\n' + s.prompt +
    '\n\nRead the cited files/logs directly. Be adversarial and specific; cite file:line or log lines. Do not rubber-stamp.',
    { label: 'review:' + s.key, phase: 'Review', schema: REVIEW_SCHEMA, effort: 'high' }
  )))).filter(Boolean);

log(`review strands returned: ${reviews.length}/${STRANDS.length}`);

phase('Synthesize');
const packed = reviews.map(r => `## ${r.strand}\nFINDINGS:\n` +
  (r.findings || []).map(f => `- [${f.severity}/${f.claim_verdict || '-'}] ${f.issue}  (${f.evidence})`).join('\n') +
  `\nRECS:\n` + (r.recommendations || []).map(x => `- (${x.priority}) ${x.action} — ${x.rationale}`).join('\n')
).join('\n\n');

const synth = await agent(
  `You are the lead independent reviewer. Weigh the 4 adversarial strands below and deliver a decisive verdict on whether the team is ON THE RIGHT TRACK. You may re-check any claim against comp/ SDK or the memory/attack.py/L13 files (cite file:line). Be honest and adversarial — the team values hard critique over reassurance.\n\nDeliver: (1) verdict ON_TRACK / MINOR_CORRECTION / MAJOR_CORRECTION; (2) the top risks with evidence; (3) a keep/change/drop call on EACH of the 5 armed L13 rungs; (4) prioritized course-corrections; (5) whether the armed mix should be re-armed BEFORE it fires tonight at 00:00 UTC.\n\n=== STRAND REVIEWS ===\n${packed}`,
  { label: 'synthesize', phase: 'Synthesize', schema: SYNTH_SCHEMA, effort: 'high' }
);

phase('Verify');
const corr = (synth.course_corrections || []).slice(0, 3);
const verified = (await parallel(corr.map(c => () =>
  agent(`Adversarially verify ONE proposed course-correction to the team's JED plan against the REAL SDK code (comp/). Is it actually correct AND better than the current plan, or does the code/economics defeat it? Default to sound=false if unproven. Cite file:line.\n\nCORRECTION: ${c.action}\nRATIONALE: ${c.rationale}`,
    { label: 'verify:' + (c.action || 'x').slice(0, 24), phase: 'Verify', schema: VERIFY_SCHEMA, effort: 'high' })
))).filter(Boolean);

return { verdict: synth.verdict, summary: synth.summary, top_risks: synth.top_risks,
  armed_mix_assessment: synth.armed_mix_assessment, course_corrections: synth.course_corrections,
  rearm_before_reset: synth.rearm_before_reset, verifications: verified };
