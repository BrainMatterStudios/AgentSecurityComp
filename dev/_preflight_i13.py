import sys, contextlib, io
sys.path.insert(0,'comp'); sys.path.insert(0,'.')
from pathlib import Path
import attack
from aicomp_sdk.agents.gpt_oss_agent import GPTOSSAgent, build_gpt_oss_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates
GGUF="models/gpt-oss-20b-Q4_K_M.gguf"; FIX=Path('comp')/'aicomp_sdk'/'fixtures'
cfg=build_gpt_oss_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    be=LlamaCppChatTemplateBackend.from_model_path(model_path=GGUF,config=cfg,n_ctx=8192,n_gpu_layers=-1,verbose=False)
ag=GPTOSSAgent(backend=be)
alg=attack.AttackAlgorithm(config={})
for i in [0,1,7,99]:
    u=alg._k1_url(i); msg=attack.K1_PROMPTS[13](attack.EXFIL_PAYLOAD,u)
    env=SandboxEnv(seed=123,fixtures_dir=FIX,agent=ag,guardrail=Optimal()); env.reset()
    with contextlib.redirect_stderr(io.StringIO()):
        env.interact(msg,max_tool_hops=8)
    tr=env.export_trace_dict()
    exfil=sum(1 for x in eval_predicates(tr) if x['predicate']=='EXFILTRATION')
    print(f"cand{i} url={u} exfil={exfil} msg_len={len(msg)}", flush=True)
print("PREFLIGHT OK" , flush=True)
