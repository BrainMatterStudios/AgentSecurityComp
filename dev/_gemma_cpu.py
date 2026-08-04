import contextlib, io, time
from llama_cpp import Llama
GGUF="models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf"
for kw in [dict(n_gpu_layers=0, n_ctx=2048),
           dict(n_gpu_layers=0, n_ctx=2048, swa_full=True)]:
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            llm=Llama(model_path=GGUF, verbose=False, **kw)
            t0=time.time()
            r=llm.create_chat_completion(messages=[{"role":"user","content":"Reply with the single word OK."}],max_tokens=8,temperature=0.0)
        print("OK(CPU)", kw, "->", repr(r["choices"][0]["message"]["content"])[:40], f"{time.time()-t0:.1f}s", flush=True)
        del llm; break
    except Exception as e:
        print("FAIL(CPU)", kw, type(e).__name__, str(e)[:70], flush=True)
