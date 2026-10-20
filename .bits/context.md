<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: .bits/context.md
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001, SRS-CN-ENTERTAINMENT-BUILD-001
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

- Active SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001 and SRS-CN-ENTERTAINMENT-BUILD-001.
- Build dispatch: DISP-BUILD-entertainment, status `in_progress`.
- Current operator directive authorizes both parts in one staging branch/PR.
- Governance identity work continues under its existing dispatch; build repair
  is authorized under the new build dispatch, including new configs and tests.
- Dispatch: DISP-GOVERNANCE-entertainment, status `in_progress`.
- Operator: authenticated Dmitry Richard, mr.nobody@citadel-nexus.com.
- Seat: BITS-CODEGEN; mode: staging.
- Authorization: the current operator directive for the identity continuation
  and build repair in this staging session.
- Scope: identity continuation, npm toolchain repair, isolated tests, manual
  lockfile refresh, build provenance verification and administrator documentation.
- Existing living-world SRS remains planned and outside this dispatch.
- CKS target: B+/75; CAPS minimum: B+; scores and CK stamps: pending.

Do preserve existing SDK ownership and package behavior. Do require review
and fail closed when a build or attestation fails. Do record admin activation
work and build prerequisites. Do not deploy, publish packages, alter settings,
introduce secrets, or perform unrelated runtime repairs.

The current directive authorizes repair of the missing toolchain. A real lockfile
must be generated with authenticated registry access, never fabricated offline.
The Datadog team Entertainment Guild — Director Nexus links human owner
@citadel-nexus/guild-entertainment and automation App director-nexus-ent-guildmaster.
Remote ruleset activation and access validation remain administrator tasks.
