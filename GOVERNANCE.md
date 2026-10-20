<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: GOVERNANCE.md
# Stage: 06_PLAN
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-GOVERNANCE-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .github/CODEOWNERS, BRANCH_PROTECTION.md, PROVENANCE.md
# EnumType: Doc
# EnumEdges: DEPENDS_ON .github/CODEOWNERS; DEPENDS_ON BRANCH_PROTECTION.md; DEPENDS_ON PROVENANCE.md
# DAG Node: none
# Intent: Make guild accountability and approval authority explicit before protected delivery.
# ───────────────────────────────────────────────────────────────
-->

# Entertainment Guild governance

Owner: Citadel Nexus Inc. Guildmaster: **Director Nexus** (GitLab `director`).
Datadog team handle: `guild-entertainment`.

## Charter

The guild owns public entertainment surfaces, agent pets (Tamagotchi), and the
Entertainment Floor. Its remit includes games, quests, events, lore and public
demos within this repository. Private-stack changes and other guilds' surfaces
require a handoff to their owners.

## Decisions and approvals

Contributors propose changes through an SRS-scoped pull request. Director Nexus
sets guild priorities and approves design, scope and release readiness. Record
material decisions, rationale and dissent in the PR or linked design record.
No self-approval: obtain an independent guild lead when the guildmaster authors
a change. Require at least one guild member review and guildmaster approval
(or a delegate explicitly designated in the PR). SDK public-interface changes
also require `sdk-core` review; coordinate cross-guild changes with affected owners.

The existing `@citadel-nexus/guild-entertainment-leads` team is the GitHub review
route for Director Nexus. An administrator must verify their GitHub username,
team membership and write access. GitLab `director` and the Datadog team name
do not establish a GitHub account or team mapping. Once verified, add the
actual GitHub username to CODEOWNERS if direct review assignment is desired.

GitHub CODEOWNERS accepts approval by any owner on the matching line; it does
not require both the SDK and guild teams, nor specifically the guildmaster.
The merger must check these additional approvals in the PR record. Never use
an unverified GitHub identity or claim these social rules are automatically enforced.

## Escalation

Escalate unresolved decisions, ownership disputes, conflicts of interest or
absence of a qualified independent approver to the **guildmasters group**.
Record the question, options and affected guilds in the PR; the operator routes
it to the group through the established internal dispatch process. Do not invent
a public team handle or endpoint. The group records a resolution or appoints an
independent delegate before merge. Security reports follow SECURITY.md.

## Merge and release controls

Follow BRANCH_PROTECTION.md for default-branch rules. Signed commits and green
checks are required; artifact attestations do not replace commit signing.
Follow PROVENANCE.md to verify the CI distribution. A successful build or
attestation does not authorize a production deployment or package publication.

Changes to this charter, ownership, branch requirements or signing workflow
require the same review rules; reducing protections also requires a recorded
guildmasters-group decision and administrator action. The bootstrap does not
activate remote controls. Administrators must complete the documented setup.
