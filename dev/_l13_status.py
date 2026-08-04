"""Clean structured read of L13 submission scores."""
import kaggle
api = kaggle.KaggleApi(); api.authenticate()
subs = api.competition_submissions("ai-agent-security-multi-step-tool-attacks")
for s in subs[:8]:
    ref = str(s.ref)
    pub = s.publicScore
    print(f"{ref}  {str(s.status):26s}  pub={pub!r:>10}  | {(s.description or '')[:48]}")
