<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: .bits/queue/DISP-BUILD-entertainment.md
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .bits/srs/SRS-CN-ENTERTAINMENT-BUILD-001.md
# EnumType: ConfigDoc
# EnumEdges: DEPENDS_ON .bits/srs/SRS-CN-ENTERTAINMENT-BUILD-001.md
# DAG Node: none
# Intent: Record the current operator authorization and phase gates for the build repair.
# ───────────────────────────────────────────────────────────────
-->

# DISP-BUILD-entertainment

- srs: SRS-CN-ENTERTAINMENT-BUILD-001
- status: in_progress
- mode: staging
- seat: BITS-CODEGEN
- operator: Dmitry Richard, mr.nobody@citadel-nexus.com
- authorization_source: current operator directive, 2026-10-20
- branch: bits/SRS-CN-ENTERTAINMENT-BUILD-001-governance

Local staging authorization only; no remote VCC status asserted. One branch/PR
with the governance continuation is explicitly authorized. The supplied source
conversation records PR #15 merged, unpublished identity work and missing build
tools. No separate Memory Brief was supplied.

| Phase | Task | Gate |
|---|---|---|
| A | Governance identity continuation | 10 static checks; 12 mutations rejected |
| B | Node/config/test/build repair | Static build contract and isolated tests |
| C | Manual lock refresh and attestation verification | Workflow security tests |
| D | Report and memory | Evidence recorded without invented lockfile/signing |

```bash
python .bits/check_governance.py
python .bits/check_governance.py --mutations
python .bits/check_build.py
mypy --strict .bits/check_governance.py .bits/check_build.py
npm ci --offline --ignore-scripts
npm run lint
npm run typecheck
npm test
npm run build
```

Registry-dependent failures block live acceptance, not honest reporting of
completed offline work. Do not weaken tests to satisfy the smoke target.
