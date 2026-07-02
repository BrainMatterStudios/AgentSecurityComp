import sys, time, contextlib, io
sys.path.insert(0,'comp'); sys.path.insert(0,'.'); sys.path.insert(0,'dev')
from pathlib import Path
from aicomp_sdk.agents.gpt_oss_agent import GPTOSSAgent, build_gpt_oss_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates
import attack
GGUF="models/gpt-oss-20b-Q4_K_M.gguf"; FIX=Path('comp')/'aicomp_sdk'/'fixtures'
cfg=build_gpt_oss_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    backend=LlamaCppChatTemplateBackend.from_model_path(model_path=GGUF,config=cfg,n_ctx=8192,n_gpu_layers=-1,verbose=False)
agent=GPTOSSAgent(backend=backend)
def measure(msg,seed,hops):
    env=SandboxEnv(seed=seed,fixtures_dir=FIX,agent=agent,guardrail=Optimal()); env.reset()
    t0=time.time()
    with contextlib.redirect_stderr(io.StringIO()):
        env.interact(msg,max_tool_hops=hops)
    dt=time.time()-t0
    return sum(1 for x in eval_predicates(env.export_trace_dict()) if x['predicate']=='EXFILTRATION'), dt
alg=attack.AttackAlgorithm()
def mp(i): return attack.K1_PROMPTS[11](attack.EXFIL_PAYLOAD, alg._k1_url(i))
def single(i): return attack.K1_PROMPTS[0](attack.EXFIL_PAYLOAD, alg._k1_url(i))
print("gpt-oss @ REAL 8-hop replay cap:")
r=[measure(mp(s+100),s,8) for s in range(1,7)]
print("  multipost posts:", [x[0] for x in r], "avg", round(sum(x[0] for x in r)/6,2))
print("  multipost sec  :", [round(x[1],1) for x in r], "avg", round(sum(x[1] for x in r)/6,1))
rs=[measure(single(s+200),s,8) for s in range(1,4)]
print("  single posts/sec:", [(x[0],round(x[1],1)) for x in rs])
