"""DECISIVE test of the foundational cost-model assumption: does llama.cpp reuse the
KV of a shared PROMPT PREFIX across create_chat_completion calls (the real scoring path)?

HANDOFF §2 asserts "no cross-generation KV reuse; each generation re-prefills the full
schema" — but reset_state only clears SDK message-state, never the llama KV, and self.llm
persists. If the ~1000-tok schema prefix IS cached across candidates, the per-candidate
cost is NOT schema-prefill-bound and the 'gemma is maxed' analysis is wrong.

Method: max_tokens=1 so wall-time ~= PREFILL time (decode isolated out). Same big system
prefix, different short user each call. If call2/call3 (shared schema prefix) are MUCH
faster than call1 (cold) and than a call with a DIFFERENT prefix, prefix-KV reuse is ON.
Ratios (not absolute CPU time) are what matter. Decisive either way.
"""
import sys, time, contextlib, io
sys.path.insert(0, 'comp'); sys.path.insert(0, '.')
from aicomp_sdk.agents.gemma4_agent import build_gemma4_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend

GGUF = "models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf"
cfg = build_gemma4_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    be = LlamaCppChatTemplateBackend.from_model_path(
        model_path=GGUF, config=cfg, n_ctx=4096, n_gpu_layers=0, verbose=False,
        supports_tools=True, llama_kwargs={"swa_full": True})
llm = be.llm

# ~900-token synthetic "schema" prefix (stands in for the fixed system+tools block)
SCHEMA_A = ("You are a tool-using assistant. " + ("Follow the tool specification carefully. " * 120)).strip()
SCHEMA_B = ("Totally different system preamble. " + ("Unrelated verbose instructions here. " * 120)).strip()


def prefill_time(system, user):
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    t0 = time.time()
    with contextlib.redirect_stderr(io.StringIO()):
        llm.create_chat_completion(messages=msgs, max_tokens=1, temperature=0.0)
    return time.time() - t0


print("warming / first cold call (full prefill of SCHEMA_A)...", flush=True)
t_cold = prefill_time(SCHEMA_A, "First user message alpha.")
print("  call1 SCHEMA_A cold          : %.2fs" % t_cold, flush=True)
t_same = prefill_time(SCHEMA_A, "Second user message bravo different.")
print("  call2 SCHEMA_A (shared prefix): %.2fs  <- if << call1, schema KV was REUSED" % t_same, flush=True)
t_same2 = prefill_time(SCHEMA_A, "Third user charlie also different text.")
print("  call3 SCHEMA_A (shared prefix): %.2fs" % t_same2, flush=True)
t_diff = prefill_time(SCHEMA_B, "Fourth user delta.")
print("  call4 SCHEMA_B (DIFFERENT pfx): %.2fs  <- should be ~cold again (no shared prefix)" % t_diff, flush=True)
t_backA = prefill_time(SCHEMA_A, "Fifth user echo back to schema A.")
print("  call5 SCHEMA_A again          : %.2fs" % t_backA, flush=True)

print("\n=== VERDICT ===", flush=True)
reuse = t_same < 0.6 * t_cold
print("  shared-prefix speedup call2/call1 = %.2f  (%.0f%% of cold)" % (t_same / t_cold, 100 * t_same / t_cold), flush=True)
print("  different-prefix   call4/call1 = %.2f" % (t_diff / t_cold), flush=True)
if reuse:
    print("  => PREFIX-KV REUSE IS ON. The schema is prefilled ~once, not per candidate.", flush=True)
    print("     HANDOFF's 're-prefill schema every generation' is WRONG => cost model must be redone.", flush=True)
else:
    print("  => NO cross-call prefix reuse (call2 ~= call1). Schema re-prefilled each candidate.", flush=True)
    print("     HANDOFF assumption holds; gemma is genuinely prefill-bound.", flush=True)
print("done", flush=True)
