import sys, contextlib, io
sys.path.insert(0,'comp'); sys.path.insert(0,'.'); sys.path.insert(0,'dev')
from pathlib import Path
from aicomp_sdk.agents.gpt_oss_agent import GPTOSSAgent, build_gpt_oss_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates
import attack
GGUF="models/gpt-oss-20b-Q4_K_M.gguf"; FIX=Path('comp')/'aicomp_sdk'/'fixtures'
# REAL Kaggle params: max_new_tokens=1024, seed=123
cfg=build_gpt_oss_backend_config(model_path=GGUF, max_new_tokens=1024)
with contextlib.redirect_stderr(io.StringIO()):
    backend=LlamaCppChatTemplateBackend.from_model_path(model_path=GGUF,config=cfg,n_ctx=8192,n_gpu_layers=-1,verbose=False)
agent=GPTOSSAgent(backend=backend); alg=attack.AttackAlgorithm()
def posts(msg,seed):
    env=SandboxEnv(seed=seed,fixtures_dir=FIX,agent=agent,guardrail=Optimal()); env.reset()
    with contextlib.redirect_stderr(io.StringIO()):
        env.interact(msg,max_tool_hops=8)
    return sum(1 for x in eval_predicates(env.export_trace_dict()) if x['predicate']=='EXFILTRATION')
mp=attack.K1_PROMPTS[11](attack.EXFIL_PAYLOAD, alg._k1_url(1))  # a.co/16 multipost
print("gpt-oss multipost @ REAL params (max_tokens=1024): posts per seed")
print("  seed=123 (the real replay seed):", posts(mp,123))
print("  seeds 1-5:", [posts(mp,s) for s in (1,2,3,4,5)])
