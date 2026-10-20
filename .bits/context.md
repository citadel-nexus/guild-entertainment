<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: .bits/context.md
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-GOVERNANCE-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .bits/queue/DISP-GOVERNANCE-entertainment.md
# EnumType: ConfigDoc
# EnumEdges: DEPENDS_ON .bits/queue/DISP-GOVERNANCE-entertainment.md
# DAG Node: none
# Intent: Bound the staging session and expose prerequisites before implementation.
# ───────────────────────────────────────────────────────────────
-->

# Current staging context

- Active SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001.
- Dispatch: DISP-GOVERNANCE-entertainment, status `in_progress`.
- Operator: authenticated Dmitry Richard, mr.nobody@citadel-nexus.com.
- Seat: BITS-CODEGEN; mode: staging.
- Authorization: the operator's governance-bootstrap directive in this session.
- Scope: bootstrap records, ownership, charter, default-branch policy,
  signed build provenance and verification documentation.
- Existing living-world SRS remains planned and outside this dispatch.
- CKS target: B+/75; CAPS minimum: B+; scores and CK stamps: pending.

Do preserve existing SDK ownership and package behavior. Do require review
and fail closed when a build or attestation fails. Do record admin activation
work and build prerequisites. Do not deploy, publish packages, alter settings,
introduce secrets, or perform unrelated runtime repairs.

Baseline lacks a lockfile, TypeScript config, ESLint config and declared build/
test tools. These block existing npm CI and the new build job until resolved
in a separate authorized change. GitHub identity for GitLab `director` needs
admin confirmation. Existing CI targets `main`; remote default-branch metadata
could not be queried with this sandbox's repository CLI configuration.
