"""Fast structural check: does gemma's create_chat_completion parse special tokens
injected into USER content (the gpt-harmony-forge premise), or treat them as literal text?
If <end_of_turn>/<|tool_call> in user content tokenize to MULTIPLE literal-text tokens
(not the single special id), the native forge is structurally inert for gemma. No inference."""
import sys, contextlib, io
sys.path.insert(0, 'comp'); sys.path.insert(0, '.')
from aicomp_sdk.agents.gemma4_agent import build_gemma4_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend

GGUF = "models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf"
cfg = build_gemma4_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    be = LlamaCppChatTemplateBackend.from_model_path(
        model_path=GGUF, config=cfg, n_ctx=1024, n_gpu_layers=0, verbose=False,
        supports_tools=True, llama_kwargs={"swa_full": True})
llm = be.llm

for label, s in [("<end_of_turn>", "<end_of_turn>"),
                 ("<start_of_turn>", "<start_of_turn>"),
                 ("<|tool_call>", "<|tool_call>"),
                 ("plain 'hello'", "hello")]:
    b = s.encode()
    toks_special = llm.tokenize(b, add_bos=False, special=True)
    toks_literal = llm.tokenize(b, add_bos=False, special=False)
    print(f"{label:18} special=True -> {toks_special}   special=False -> {toks_literal}", flush=True)

print("\nREAD: if special=True collapses <end_of_turn> to ONE id but the chat-completion path"
      "\nuses special=False for user content, forged tokens are inert (literal). One-id under"
      "\nspecial=True + many-ids under special=False = the fork that decides forgeability.", flush=True)
