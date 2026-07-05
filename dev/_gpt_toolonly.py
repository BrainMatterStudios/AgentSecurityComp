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
cfg=build_gpt_oss_backend_config(model_path=GGUF, max_new_tokens=1024)
with contextlib.redirect_stderr(io.StringIO()):
    backend=LlamaCppChatTemplateBackend.from_model_path(model_path=GGUF,config=cfg,n_ctx=8192,n_gpu_layers=-1,verbose=False)
agent=GPTOSSAgent(backend=backend)
def run(msg):
    env=SandboxEnv(seed=123,fixtures_dir=FIX,agent=agent,guardrail=Optimal()); env.reset()
    with contextlib.redirect_stderr(io.StringIO()):
        env.interact(msg,max_tool_hops=8)
    tr=env.export_trace_dict()
    posts=sum(1 for x in eval_predicates(tr) if x['predicate']=='EXFILTRATION')
    # count assistant text tokens roughly via trace? use turns as proxy; measure via re-gen not needed
    return posts, len(tr.get('tool_events',[]))
SM=attack.EXFIL_PAYLOAD; U="http://a.co/1"
nat=attack.K1_PROMPTS[0](SM,U)
tool=attack.K1_PROMPTS[12](SM,U)
# use the model server's own token accounting via a direct generate to compare cost
from aicomp_sdk.agents.types import toolspec  # may not exist; fallback below
