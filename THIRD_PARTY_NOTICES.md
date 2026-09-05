# Third-Party Notices

The MIT license in [`LICENSE`](LICENSE) covers the original work in this repository
authored by Ahmed Mobasher (BrainMatter Studios). It does **not** cover the
third-party material listed below, which is included for reproducibility and
remains under its own terms and copyright.

---

## 1. `aicomp-sdk` — competition SDK (`comp_310_backup/`)

- **Version bundled:** 3.1.0 (`comp_310_backup/aicomp_sdk-3.1.0.dist-info/`)
- **Copyright:** 2026 Competition Organizers
- **License:** MIT — full text at
  `comp_310_backup/aicomp_sdk-3.1.0.dist-info/licenses/LICENSE`
- **Upstream:** https://github.com/mbhatt1/competitionscratch

Redistributed under the MIT terms granted by its authors. This includes the
scoring and guardrail sources cited by the working note
(`guardrails/optimal.py`, `core/predicates.py`, `scoring.py`) and the harness
fixtures under `aicomp_sdk/fixtures/`.

**Note on fixtures.** Files such as `fixtures/file_seed/api_keys.txt`,
`credentials.json`, and `secret.txt` contain **synthetic bait values** — they are
the benchmark's honeypot data, not real credentials. They use documented
placeholders (e.g. AWS's `AKIAIOSFODNN7EXAMPLE`, Slack's `T00000000/...`
webhook form) and RFC 2606 reserved domains. Automated secret scanners will
flag them; they carry no access to any system.

**Version caveat.** The working note pins its code citations to `aicomp-sdk
3.1.2`, which is *not* redistributed here. The copy bundled at
`comp_310_backup/` is 3.1.0. Line numbers and minor details may differ; obtain
3.1.2 from the competition's Data page or upstream to verify §4 exactly.

## 2. Competitor reference kernels (`refkernels_new/`)

Four publicly published Kaggle kernels by other competition participants,
retained because the working note (§5) pins each as a frozen source artifact by
git blob hash. Each is cited in the paper by its public Kaggle URL and analyzed
as a **source observation only, with no score attribution**.

| Path | Author | Source |
|---|---|---|
| `refkernels_new/dimong4_ai-agent-security/` | dimong4 | https://www.kaggle.com/code/dimong4/ai-agent-security |
| `refkernels_new/nctuan_jed-slow-multipost/` | nctuan | https://www.kaggle.com/code/nctuan/jed-slow-multipost |
| `refkernels_new/tetsutani_ai-agent-sec-adaptive-uniform-two-probe-recovery/` | tetsutani | https://www.kaggle.com/code/tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery |
| `refkernels_new/paul720810_hermes-attack-v72-m112-20260721-151926/` | paul720810 | https://www.kaggle.com/code/paul720810/hermes-attack-v72-m112-20260721-151926 |

Copyright remains with the respective authors, under whatever terms they
published on Kaggle. They are included under an academic-citation rationale, not
relicensed. **If you authored one of these and would prefer it not be mirrored
here, open an issue and it will be removed** — the paper's citations resolve via
the public Kaggle URLs and the git blob hashes recorded in §5 regardless.

## 3. Fonts (`paper/html/fonts/`)

Bundled for offline rendering of the HTML manuscripts. All under the SIL Open
Font License 1.1, with full license text alongside each file:

| Font | Copyright | License file |
|---|---|---|
| Fraunces | The Fraunces Project Authors | `OFL-Fraunces.txt` |
| Geist | 2024 The Geist Project Authors | `OFL-Geist.txt` |
| JetBrains Mono | The JetBrains Mono Project Authors | `OFL-JetBrains-Mono.txt` |
