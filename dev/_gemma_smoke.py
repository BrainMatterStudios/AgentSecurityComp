import sys, contextlib, io, time
from llama_cpp import Llama
GGUF="models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf"
for kw in [dict(swa_full=True,n_batch=512),
           dict(swa_full=True,n_batch=512,flash_attn=True),
           dict(flash_attn=True,n_batch=256)]:
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            llm=Llama(model_path=GGUF,n_ctx=8192,n_gpu_layers=-1,verbose=False,**kw)
            t0=time.time()
            r=llm.create_chat_completion(messages=[{"role":"user","content":"Reply with the single word OK."}],max_tokens=16,temperature=0.0)
        print("OK", kw, "->", repr(r["choices"][0]["message"]["content"])[:60], f"{time.time()-t0:.1f}s", flush=True)
        del llm
        break
    except Exception as e:
        print("FAIL", kw, type(e).__name__, str(e)[:80], flush=True)
