<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: .bits/queue/DISP-GOVERNANCE-entertainment.md
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-GOVERNANCE-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .bits/srs/SRS-CN-ENTERTAINMENT-GOVERNANCE-001.md
# EnumType: ConfigDoc
# EnumEdges: DEPENDS_ON .bits/srs/SRS-CN-ENTERTAINMENT-GOVERNANCE-001.md
# DAG Node: none
# Intent: Record the operator authorization and bounded task gates for this bootstrap.
# ───────────────────────────────────────────────────────────────
-->

# DISP-GOVERNANCE-entertainment

- srs: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
- guild: entertainment
- guildmaster: Director Nexus (GitLab director)
- datadog_team: guild-entertainment
- seat: BITS-CODEGEN
- mode: staging
- status: in_progress
- branch: bits/SRS-CN-ENTERTAINMENT-GOVERNANCE-001-bootstrap
- authorization_source: authenticated operator directive in this Bits AI session
- operator: Dmitry Richard, mr.nobody@citadel-nexus.com
- authorization_recorded: 2026-10-20

## Authorization source

The operator's directive: "create those". The accompanying directive explicitly
authorizes creating AGENTS.md and missing governance prerequisites, this SRS
and dispatch, and the ownership/governance/provenance work from the initial
request. It restricts this work to one branch and PR for this SRS, with no
production, deploy, push to main, changes to GitHub settings, or secrets.
This is a local authorization record, not an invented remote VCC approval.
No Memory Brief was provided. No sibling repositories are locally available.

## Task table

| Phase | Task | Gate |
|---|---|---|
| A | Bootstrap agent context, SRS and dispatch | Registered scope and authorization exist |
| B | Charter, ownership and default-branch policy | Guildmaster named; SDK owner retained; admin requirements explicit |
| C | Build artifact, keyless SLSA provenance and verification | Security contract checker passes |
| D | Validation, report and memory | Static smoke passes; live/build blockers reported |

## Smoke checks

```bash
python .bits/check_governance.py
npm test
npm run lint
npm run build
```

The baseline npm commands currently fail. Do not waive their required GitHub
checks or expand this dispatch into runtime repairs. Static phase gates and
full smoke results are reported separately; never describe the overall smoke
as passing when baseline checks fail. A follow-up build-toolchain dispatch and
admin activation are required before live provenance acceptance.
