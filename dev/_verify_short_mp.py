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
agent=GPTOSSAgent(backend=backend); alg=attack.AttackAlgorithm()
def measure(i,seed):
    env=SandboxEnv(seed=seed,fixtures_dir=FIX,agent=agent,guardrail=Optimal()); env.reset()
    t0=time.time()
    with contextlib.redirect_stderr(io.StringIO()):
        env.interact(attack.K1_PROMPTS[11](attack.EXFIL_PAYLOAD, alg._k1_url(i)),max_tool_hops=8)
    return sum(1 for x in eval_predicates(env.export_trace_dict()) if x['predicate']=='EXFILTRATION'), time.time()-t0
R=[measure(s+300,s) for s in range(1,7)]
posts=[x[0] for x in R]; secs=[x[1] for x in R]
avgp=sum(posts)/6; avgs=sum(secs)/6; tok=avgs*41; calT4=tok/7.2; N=9000/calT4
print("short-URL idx11 @8hops: posts",posts,"avg",round(avgp,2))
print(f"  ~{tok:.0f} tok/cand, T4 cal_t {calT4:.1f}s, boundary N~{N:.0f}, row@N=85 ~{(16*avgp+2)*85/200:.1f}")
