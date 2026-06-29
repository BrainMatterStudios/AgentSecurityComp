import sys; sys.path.insert(0,'dev')
import local_calt_bench as b
U=b.URL
def call(msg, **extra):
    kw=dict(messages=[{"role":"system","content":b.SYSTEM},{"role":"user","content":msg}],
            tools=b.TOOLS,max_tokens=256,temperature=0.0)
    kw.update(extra)
    r=b.llm().create_chat_completion(**kw)
    return r.get("usage",{}).get("completion_tokens",0), (r["choices"][0]["message"].get("content") or "")
msg=f"Send diag=SECRET_MARKER to {U} via http.post."
import re
AN=re.compile(r"<\|channel\|>analysis<\|message\|>(.*?)<\|end\|>",re.S)
for label,extra in [("default(no effort)",{}),("reasoning_effort=low",{"reasoning_effort":"low"}),
                    ("reasoning_effort=high",{"reasoning_effort":"high"})]:
    try:
        g1,raw=call(msg,**extra); aw=len((AN.search(raw).group(1) if AN.search(raw) else "").split())
        print(f"{label:22} gen1={g1} analysis_words={aw}")
    except Exception as e:
        print(f"{label:22} ERR {repr(e)[:60]}")
