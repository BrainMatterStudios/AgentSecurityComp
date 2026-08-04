"""Empirical: gemma per-GENERATION decode tokens (gen1 tool-call vs gen2 final) for
natural/stop/toolonly, warm, 3 seeds. Answers: is gemma's ~14s/candidate prefill-bound
(few decode tokens) or decode-bound? Uses the faithful llama.cpp CPU path + real tokenizer."""
import sys, contextlib, io
sys.path.insert(0,'comp'); sys.path.insert(0,'.')
from pathlib import Path
import attack
from aicomp_sdk.agents.gemma4_agent import Gemma4Agent, build_gemma4_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
GGUF="models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf"; FIX=Path('comp')/'aicomp_sdk'/'fixtures'; T=attack.EXFIL_PAYLOAD
cfg=build_gemma4_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    be=LlamaCppChatTemplateBackend.from_model_path(model_path=GGUF,config=cfg,n_ctx=4096,n_gpu_layers=0,verbose=False,supports_tools=True,llama_kwargs={"swa_full":True})
ag=Gemma4Agent(backend=be); alg=attack.AttackAlgorithm(config={})
def ntok(s):
    try: return len(be.llm.tokenize(s.encode('utf-8'), add_bos=False, special=False))
    except Exception: return round(len(s)/4)
def run(fn,seed,i):
    env=SandboxEnv(seed=seed,fixtures_dir=FIX,agent=ag,guardrail=Optimal()); env.reset()
    with contextlib.redirect_stderr(io.StringIO()): env.interact(fn(T,alg._k1_url(i)),max_tool_hops=8)
    ams=env.export_trace_dict().get('assistant_messages',[])
    return [ntok(m) for m in ams]
for label,idx in [("natural",0),("stop",4),("toolonly",12)]:
    for s in range(2): run(attack.K1_PROMPTS[idx],900+s,s)  # warmup
    tot=[]
    for s in range(3):
        gens=run(attack.K1_PROMPTS[idx],100+s,s); tot.append(sum(gens))
        print(f"[{label:9}] seed{100+s} per-gen tokens={gens} total={sum(gens)}",flush=True)
    print(f"==> {label}: avg total decode tokens/candidate = {sum(tot)/len(tot):.0f}\n",flush=True)
print("done",flush=True)
