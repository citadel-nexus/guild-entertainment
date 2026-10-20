<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: .bits/srs/SRS-CN-ENTERTAINMENT-GOVERNANCE-001.md
# Stage: 04_HYPOTHESIZE
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-GOVERNANCE-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .bits/check_governance.py
# EnumType: Doc
# EnumEdges: VERIFIED_BY .bits/check_governance.py
# DAG Node: none
# Intent: Specify reviewable ownership and artifact trust requirements for the guild.
# ───────────────────────────────────────────────────────────────
-->

# SRS-CN-ENTERTAINMENT-GOVERNANCE-001

Entertainment Guild ownership governance and signed build provenance

## Authorization and scope

Operator: Dmitry Richard, mr.nobody@citadel-nexus.com. Seat: BITS-CODEGEN.
Dispatch: DISP-GOVERNANCE-entertainment. Mode: staging. Status: in_progress.

The operator authorized creation of the missing governance prerequisites,
including this local SRS and dispatch. This authorization supersedes the
missing-record bootstrap stop for this work only. No remote VCC status is
claimed. No production, deployment, direct push, settings change or secrets.

## Acceptance

1. Name Director Nexus (GitLab `director`) as guildmaster, document the
   entertainment surfaces, Tamagotchi agent pets and Entertainment Floor,
   preserve SDK ownership, and route GitHub reviews through existing teams
   until the guildmaster's GitHub identity is verified.
2. Document decisions, required guildmaster approval and guildmasters-group
   escalation. Describe admin steps for default-branch review, signed commits,
   required checks, no force pushes and no deletion. No settings automation
   is installed in the repository, so documentation is the supported outcome.
3. Build and package the existing npm distribution, then create a keyless
   signed SLSA v1 provenance attestation for its exact bytes only after trusted
   default-branch builds. No signing for pull requests. No deployment.
4. Provide verification bound to repository, workflow, branch and source SHA.
   Explain that existing Docker images/npm releases are outside this signature.
5. Validate workflow security properties, emit CGRF headers, a three-type
   memory payload and the §15 report. Report npm baseline blockers honestly.

## Gates

CKS target B+/75; CAPS minimum B+; CKS, CAPS and CK pending.
Governance/CI static checks must all pass. Live signed artifact production
requires GitHub execution and the baseline build repair; it is not asserted by
this bootstrap. Acceptance of an operational provenance run remains pending.
