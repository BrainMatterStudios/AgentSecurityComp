# Claude and Codex Source-Availability Manifest

**Audit date:** 2026-09-04  
**Scope:** every canonical Claude Code and Codex history source listed in the
cutoff-1 evidence map, plus the later history files used for author testimony,
the public-frontier observation, and cutoff-2 live queries.

This is an availability and integrity manifest, not a public transcript dump.
Hashes identify the files present during this audit. Agent-history stores are
mutable; a later extraction can legitimately produce a different digest. Three
of the ten canonical Claude files were absent from their recorded project
paths. Their absence is reported rather than silently treating derivative
quotations as surviving originals.

## 1. Canonical Claude Code sources

| Case | Canonical ID | Audit state | SHA-256 or surviving substitute |
| --- | --- | --- | --- |
| ARC-AGI-3 | `2c317a12-f48d-4a3f-8ddc-8b48615ad490` | present | `955875b52b6b42bdec99d8bb307cb91eaf2b814a351f4870f9fccdedfe967a22` |
| ARC-AGI-3 | `32add479-d332-44f0-ae03-8ed849c86377` | present | `d9b1c7b879ed57d48c17b084d80974b64df3024586835fd7d0cde60b69a1a687` |
| ARC-AGI-3 | `573f46bd-f297-4c15-8028-9676d148ba1b` | **absent at recorded path** | Q06 survives only through the controlled quote ledger and repository corroboration; do not represent it as a re-openable original transcript. |
| ARC-AGI-3 | `626c7722-330b-4125-b1de-439d21bef0a0` | present | `a4fca61f5464b35b28d73b9d9f1059980386ae705f2c8b2093d50d86eb64c88e` |
| ARC-AGI-3 | `de216582-726c-415f-9dd5-71c05fb4d2c3` | present | `ef580b71ff437e70d13b8e5e23dc0d7fc57fdb067f58b981d3b3973206f02b74` |
| AgentSecurityComp | `0385f350-248c-431f-a9f2-1604c96b5ce2` | present | `9d6c94b8eec5e6f5ff8bc3cd8c9a9947bdd6b19176d80bdac05db38238a4faa2` |
| AgentSecurityComp | `42258c4d-4471-458b-a3c0-757cf6791024` | present | `2cf9d704c9f5a9554b33d37114d97e8f1a6d822a331a1c9505b6d733c44b0f84` |
| AgentSecurityComp | `a809e3ce-6bd5-4997-914a-1100fe705967` | present | `9c9211307ea8db55aaff201f8bbc8798d5af8d96c4ec6282c63f4652a9552a16` |
| AgentSecurityComp | `d02227a2-1ed0-471c-abb2-994217974264` | **absent at recorded path** | Q01's original user instruction survives in `~/.claude/history.jsonl` (entry 2983 at audit time); Q02-Q04 survive only as prior controlled-ledger extracts and derivative copies. |
| AgentSecurityComp | `f1ef3669-1d5f-4caf-ab9b-c4eedf643569` | **absent at recorded path** | Relevant claims survive through the controlled quote ledger and repository evidence; do not represent the original transcript as available. |

## 2. Canonical Codex sources

| Case | Canonical ID | Audit state | SHA-256 |
| --- | --- | --- | --- |
| ARC-AGI-3 | `019ed1da-2605-7a63-b99e-69db1f12161b` | present | `e4cc6995aa8be4c796ab0a675e3a4dc566313d873f5e17df528f00af4c1ada40` |
| ARC-AGI-3 | `019ed98f-89e6-7530-bcf1-c453709e4434` | present | `9bfd65a282b7b17326ea2f1ac14c8d9cd99401eefb982fb518c2fd86486e999b` |
| ARC-AGI-3 | `019ed98f-8a24-7bb2-8aa4-1f14fd24088b` | present | `c5b428b3a2280920ecc70bee61222e567a6eac36cfbdc4664005dc09f6b97207` |
| ARC-AGI-3 | `019fce51-2e83-73b1-92d9-2a24d75c102a` | present | `a6952152f8de1f54090e907df7059f1c09dbc150140eac594a4492f4ac32f5bc` |
| ARC-AGI-3 | `01a005ec-999c-7573-9626-e89e51ad4f6b` | present | `16caf38f19ecf4f0e1454c92f63ddf0ab82f7f1fb49e7f7eecdb7086d036d940` |
| AgentSecurityComp | `019ed259-af2a-7020-9160-0b55c823dac1` | present | `83ce878a374479086ea133cae55e23ae61518b6f7cd33096e3bd97b9b5ce558d` |
| AgentSecurityComp | `019ed25a-827c-7202-81f7-f635cc301017` | present | `ed5938441760da685ea3537c5fadf9e58a330bf0005aa52237409cb188c4f57d` |
| AgentSecurityComp | `019ed98f-8976-7c43-a9c1-5ca274e2de36` | present | `2d6de8e3f4a394864001398da4adda326a6311a72a1f7e8438c9ba426d0067a9` |
| AgentSecurityComp | `019fad04-b6b5-7370-b5ac-bfbf870e1c16` | present | `babad4cd6ca16e12afa1d212ad868a0b5182371f5805a8933777777a63f74f44` |
| AgentSecurityComp | `019fad19-326f-7503-90a8-0df3753259d3` | present | `f1d1153288eb2e5e9d2429e796573628265a87caa539045b2cdcfa19c669a77a` |
| AgentSecurityComp | `019fad7d-427a-7d00-9818-33698703ce2c` | present | `e3ef6fa72372ed209c7f0f5f2838a8846406c48f27880996b63139086b7e26d5` |
| AgentSecurityComp | `019fad85-1933-7f80-804a-e3395635559b` | present | `a51e37615d17b5b7bc0f85d779ca9f09b948afcd8b3a19899f1523301ace307a` |
| AgentSecurityComp | `019fce03-3854-79b1-a5ed-c0cd803a0575` | present | `01ae6031177844a11e7f586056a5cceb01121c5c01bb9fae0f4fe12731ae61c3` |
| AgentSecurityComp | `019fce29-2147-70b1-a1f1-054e020cd692` | present | `ab494234e51f9d59772b1f6bd10046d4ce605580071ddcc1e0ea3c49dee491ff` |
| AgentSecurityComp | `01a005ed-b434-76a0-95e0-5fe82f4dc768` | present | `9018fe7e0ecb2a2dbccb4b0cfafa8a13f4759666c718481a803733e7f5b9313b` |

## 3. Supplemental Claude and Codex sources used after cutoff-1

| Purpose | Source ID | Audit state | SHA-256 |
| --- | --- | --- | --- |
| Cutoff-2 authenticated competition queries | Claude `a8b27783-6519-42d5-bcd6-6440c6d602ab` | present | `8e5612fd5cacb37415b4d28641779815596d10339c6ca37a6c5bf9dcc96c5147` |
| Public-frontier authenticated query | Codex `01a04f0a-0694-7301-b343-f082024a492c` | present | `11d6533b4564ede9e3434f0eff1f56449e2d76cb4df343f6070a78b0a936d5da` |
| Retrospective Q08/Q09 interview | Codex `01a0091e-6c06-72e0-ba1c-e5499447d566` | present | `9a7bbe67fa42b8f467731ff76d3337645bdbfd5c765a4cb507f0f03920e10b13` |
| Final-week AgentSecurity research | Claude `df7d67d1-357d-45df-a458-63a4e741d054` | present | `06752430494b46b12f07046a6356f6b9f62eefcb4e9f57cb4c3bac3bf695241a` |
| Private-hedge digest | Claude `d28017de-3f65-488c-8c50-38facf2b5534` | present | `ad0169b0c6c29fa17e9c5907765106c0127c5af83748ed2f93f897be300c208a` |
| Surviving Q01 prompt history | Claude global `history.jsonl` | present, mutable | `384b791c290174ead3e2509ce7bc633706724b9c8adc677259e4f0d45c6174d8` |

## 4. Additional Claude continuation locators cited by the episode register

| Source ID | Audit state | SHA-256 or consequence |
| --- | --- | --- |
| `25c84940-5ede-4850-a639-5579fdef6ebe` | **absent at recorded path** | AS-S05 and AS-S06 retain repository and live-row evidence; the continuation itself is not re-openable. |
| `9d0f25c3-7d3c-4eaf-a219-001b44ea5ec4` | present | `ad8c88b26ff18072b26fc6386c0bae6dd85593b5358d37463e4ae1941ad9efae` |
| `9f138e71-bfaa-49fa-93aa-e6cf5f592493` | present | `b1bcffa08be269f58fa2e32aa7417a2482e51042a5269c19fb008d72425a6de4` |
| `38ec9bae-690c-4713-aa14-c3245497ca9e` | **absent at recorded path** | ARC-S04 retains commit-level evidence; the continuation itself is not re-openable. |

## 5. Audit consequence

Seven of ten canonical Claude files and all 15 canonical Codex files were
present at their recorded paths. Three Claude originals were not. Claims tied
to those missing originals require surviving repository evidence, a separate
available session, or an explicit derivative/testimony label. This manifest
does not upgrade derivative evidence into an original transcript.
