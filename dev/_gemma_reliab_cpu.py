"""Reliability of gemma stop(idx4)/toolonly(idx12) across seeds+URLs on CPU (faithful).
Need ~100% fire and NO degrade-to-prose (a prose-only turn = misfire -> 8-hop blowup -> void)."""
import sys, time, contextlib, io
sys.path.insert(0,'comp'); sys.path.insert(0,'.')
from pathlib import Path
import attack
from aicomp_sdk.agents.gemma4_agent import Gemma4Agent, build_gemma4_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates
GGUF="models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf"; FIX=Path('comp')/'aicomp_sdk'/'fixtures'; T=attack.EXFIL_PAYLOAD
cfg=build_gemma4_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    be=LlamaCppChatTemplateBackend.from_model_path(model_path=GGUF,config=cfg,n_ctx=4096,n_gpu_layers=0,verbose=False,supports_tools=True,llama_kwargs={"swa_full":True})
ag=Gemma4Agent(backend=be)
alg=attack.AttackAlgorithm(config={})
def one(fn,seed,i):
    u=alg._k1_url(i); env=SandboxEnv(seed=seed,fixtures_dir=FIX,agent=ag,guardrail=Optimal()); env.reset()
    t0=time.time()
    with contextlib.redirect_stderr(io.StringIO()): res=env.interact(fn(T,u),max_tool_hops=8)
    dt=time.time()-t0; tr=env.export_trace_dict()
    exfil=sum(1 for x in eval_predicates(tr) if x['predicate']=='EXFILTRATION')
    return exfil,res.agent_turns,dt
for label,idx in [("natural",0),("stop",4),("toolonly",12)]:
    fires=0;tsum=0;n=0
    for i in range(5):
        try: e,turns,dt=one(attack.K1_PROMPTS[idx],100+i,i)
        except Exception as ex: print(f"[{label}] seed{100+i} ERR {ex}",flush=True); continue
        fires+=1 if e>=1 else 0; tsum+=dt; n+=1
        print(f"[{label}] seed{100+i} posts={e} turns={turns} {dt:4.1f}s",flush=True)
    if n: print(f"==> {label}: fire={fires}/{n} avg={tsum/n:4.1f}s  (natural-relative speed shown by avg)\n",flush=True)
print("done",flush=True)
