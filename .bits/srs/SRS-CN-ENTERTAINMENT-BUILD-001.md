<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: .bits/srs/SRS-CN-ENTERTAINMENT-BUILD-001.md
# Stage: 04_HYPOTHESIZE
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .bits/queue/DISP-BUILD-entertainment.md
# EnumType: Doc
# EnumEdges: DEPENDS_ON .bits/queue/DISP-BUILD-entertainment.md
# DAG Node: none
# Intent: Define the authorized build repair acceptance gates and its bounded staging exception.
# ───────────────────────────────────────────────────────────────
-->

# SRS-CN-ENTERTAINMENT-BUILD-001

Status: in_progress. Dispatch: DISP-BUILD-entertainment. Seat: BITS-CODEGEN.
Mode: staging. Authorization: Dmitry Richard's current operator directive.
This is a local record, not a claim of remote VCC registration.

Repair the existing TypeScript guild build with Node 22, strict TypeScript,
ESLint and Vitest using mocked production clients. Preserve runtime behavior,
existing security scanning and review requirements. Never fabricate a lockfile.
Generate it only with authenticated registry access through a manual-only
workflow, validate ci/lint/typecheck/test/build, then open a reviewed branch PR.
Attest only successfully compiled output; verify the real artifact and reject
tampering and a wrong signer workflow. Document admin prerequisites.

The operator explicitly combines this build SRS and the governance identity
continuation in one branch/PR. Existing root layout remains; build configs,
tests and scripts use logical CKET 11_COMMIT, docs 06_PLAN, specs 04_HYPOTHESIZE.
No production connections, deployment, settings/secrets changes or main push.
CKS target B+/75; CAPS minimum B+; CKS/CAPS/CK pending.

Acceptance: all governance/build static checks and negative tests pass;
report every offline npm outcome and defer real install/signing to GitHub.
