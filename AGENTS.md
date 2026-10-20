<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: AGENTS.md
# Stage: 04_HYPOTHESIZE
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-GOVERNANCE-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .bits/context.md, GOVERNANCE.md
# EnumType: ConfigDoc
# EnumEdges: DEPENDS_ON .bits/context.md; DEPENDS_ON GOVERNANCE.md
# DAG Node: none
# Intent: Define the authorized public guild workflow without importing private monorepo assumptions.
# ───────────────────────────────────────────────────────────────
-->

# Entertainment Guild agent instructions

This is `citadel-nexus/guild-entertainment`, the public Entertainment Guild
repository owned by Citadel Nexus Inc. It is a TypeScript guild scaffold, not
the CNWB mirror. Follow existing package scripts and public SDK conventions.

## Read order and authorization

Read AGENTS.md, CLAUDE.md, .bits/context.md, .bits/srs_registry.yml, the active
SRS document, then its .bits/queue dispatch. A dispatch must be authorized and
`in_progress` or `ready` before implementation. The operator explicitly
approved the governance bootstrap recorded in DISP-GOVERNANCE-entertainment;
this is a local staging authorization, not a claim of remote VCC registration.
No Memory Brief was supplied for this dispatch; do not invent prior art.

Keep each change scoped to one SRS and one feature branch. Do not change
production, deploy, push to main, change GitHub settings, or handle secrets.
No private CNWB imports, tenant material, private endpoints or private-stack
changes. Do not modify notify-citadel.yml, signing-key logic, protected ledger
or audit code. Do not fabricate CK, CAPS or CKS results.

## Ownership and layout

Director Nexus (GitLab `director`) is guildmaster; the Datadog team is
`guild-entertainment`. See GOVERNANCE.md and .github/CODEOWNERS for review.
Preserve SDK team ownership and request a guildmaster approval on every PR.
A GitLab username is not proof of a GitHub identity.

Retain this repository's root documents, .bits records and .github workflows;
do not relocate them into physical CKET directories. CGRF stages are logical
classifications here: governance documents use 06_PLAN, agent/spec documents
04_HYPOTHESIZE, and .bits automation/dispatch/output plus workflows 11_COMMIT.
This repo-specific layout applies to the authorized bootstrap. New files need
CGRF headers (HTML comments in Markdown; sibling .cgrf.yaml for JSON), pending
CK/CAPS, and matching Type A/B/C memory records.

## Validation and delivery

Use `npm test`, `npm run lint`, and `npm run build` for application changes.
The governance checker is `python .bits/check_governance.py` (PyYAML 6.0.3).
Do not add Python application infrastructure or change the guild runtime for
this bootstrap. Record unavailable checks as failures; never claim coverage
or successful signing from static validation. CI signing must occur only
for a successful build of the protected default branch, on GitHub-hosted runners.

Use conventional commits with Phase, Files, Smoke, SRS, Dispatch and CK footers.
Produce the dispatch report and three-type memory payload. Post-merge CK and
REFLEX validation are external; report them as deferred. New runtime modules
require SAKE stubs; this bootstrap introduces no runtime modules.
