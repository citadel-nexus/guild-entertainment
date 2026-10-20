<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: BRANCH_PROTECTION.md
# Stage: 06_PLAN
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-GOVERNANCE-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .github/workflows/build-provenance.yml, GOVERNANCE.md
# EnumType: Doc
# EnumEdges: GATES .github/workflows/build-provenance.yml; DEPENDS_ON GOVERNANCE.md
# DAG Node: none
# Intent: Specify enforceable default-branch controls and their administrator prerequisites.
# ───────────────────────────────────────────────────────────────
-->

# Default-branch protection requirements

This repository has no installed settings/ruleset reconciliation mechanism.
This document is the administrator's configuration specification; merging it
**does not change GitHub settings**. No inert settings file is presented as
enforced policy. Existing workflows target `main`; the administrator must
confirm it is the default branch and align workflow triggers if it differs.

## Admin activation

Create an **active branch ruleset** targeting the default branch (GitHub's
`~DEFAULT_BRANCH` selector) or equivalent branch protection:

| Requirement | Setting |
|---|---|
| Pull requests | Require a PR and at least one approving review |
| Ownership | Require review from Code Owners |
| Fresh review | Dismiss stale approvals; require approval of the most recent reviewable push by someone other than the pusher |
| Conversations | Require all review conversations to be resolved |
| Commit provenance | Require signed commits |
| Status checks | Require checks below and require branches up to date before merging |
| History | Block force pushes and branch deletion |
| Exceptions | Apply to administrators; no routine bypass actors |

Use the exact check-run names observed on a PR, with GitHub Actions as the
expected source application where supported:

- `build` — existing CI lint, test and application build.
- `governance-checks` — governance and provenance security contract checks.
- `build-artifact` — the distribution build/package that will be attested.

Do not require `attest` on pull requests: it deliberately runs only after a
successful trusted main-branch build. The existing `docker` job is also not a
PR check. Do not require status names that have never appeared. Security scan
jobs currently have different trigger coverage; adding them as required PR
checks needs a separate workflow change. No merge queue is configured; before
enabling one, add and validate `merge_group` coverage for every required check.

## Ownership prerequisites

The confirmed human code-owner team is `@citadel-nexus/guild-entertainment`;
the guild's GitHub App automation/bot identity is `director-nexus-ent-guildmaster`.
Identity source: the operator's 2026-10-20 update, citing Datadog team
**Entertainment Guild — Director Nexus** (`guild-entertainment`) links.
The identity mapping is resolved. Admins still must validate that
`guild-entertainment` and `sdk-core` are visible GitHub teams with write access
and eligible human reviewers. Validate CODEOWNERS in GitHub. GitHub Apps
cannot be code owners; do not add the App to CODEOWNERS. Code-owner review
cannot enforce two separate team approvals; apply GOVERNANCE.md's additional
human approval procedure.

## Automation actors and bypass limits

Default: no bypass for `director-nexus-ent-guildmaster`. The App may submit or
update PRs under its installed permissions; a bot review is not human approval.
Human code-owner review remains mandatory for `.github/**`, `GOVERNANCE.md`,
`CODEOWNERS` (including `.github/CODEOWNERS`), and workflows.

Only consider adding this App as a ruleset actor or allowed bypass actor when
a specific automation need is justified and approved under GOVERNANCE.md.
For example, a separate rule restricting automation-branch creation might
permit the App without waiving the default branch's review rules. Record the
App installation/actor ID verified in GitHub, the exact rule and branch scope,
human approvers, expiry and audit/revocation plan. Do not invent an actor ID.

A branch ruleset's bypass list applies to its rules, not selected file paths.
Never add the App to the bypass list of a ruleset or legacy protection that
would let it waive required human review on the protected paths. Even a
pull-request-only bypass can waive review requirements; it is not sufficient
protection. Keep human-review rules in an active ruleset with no App bypass,
and validate the combined rules before permitting any separate exception.
If GitHub cannot express that separation, deny the exception. No bypass or
settings change is authorized or applied by this staging update.

## Signing and Actions prerequisites

Contributors must use verified signed commits. Select merge methods that comply
with GitHub's signed-commit rule, and test the chosen method on a staging PR.
The artifact workflow uses short-lived GitHub OIDC credentials and GitHub's
Sigstore-backed artifact attestation service; no stored signing key is needed.
Allow the referenced official Actions and the `id-token: write` and
`attestations: write` permissions on the trusted signing job. Keep the default
workflow token read-only and do not grant write tokens to fork pull requests.
Confirm artifact attestations are available for this repository's visibility
and plan (public repositories are supported; private/internal support depends
on the GitHub plan). No environment approval or settings changes are made here.

## Activation blockers and acceptance

The current scaffold has no npm lockfile, TypeScript configuration, ESLint
configuration or declared TypeScript/Vitest/ESLint tool dependencies. Existing
npm checks fail; `npm ci` cannot run without a lockfile. A separate authorized
build-toolchain change must repair the scaffold. Do not disable required checks
or substitute a source archive for a successful application build.

After repair: run a PR build, observe all required checks, test rejected
unsigned commits and missing owner approval, merge through the protected path,
and verify a main-branch artifact as described in PROVENANCE.md. Confirm PR
runs skip signing. Record results before treating protections and provenance as
operational. Default-branch settings, permissions and team-access validation remain
administrator tasks; this staging change does not claim they are enabled.
