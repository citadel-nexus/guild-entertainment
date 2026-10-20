<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: BUILD.md
# Stage: 06_PLAN
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .github/workflows/lockfile-refresh.yml, BRANCH_PROTECTION.md, PROVENANCE.md
# EnumType: Doc
# EnumEdges: DEPENDS_ON .github/workflows/lockfile-refresh.yml; DEPENDS_ON BRANCH_PROTECTION.md; DEPENDS_ON PROVENANCE.md
# DAG Node: none
# Intent: Explain authenticated lockfile bootstrap and administrator gates without claiming offline build success.
# ───────────────────────────────────────────────────────────────
-->

# Entertainment Guild build

Use Node 22 (`.nvmrc`, package engines, setup-node and Docker agree on the major).
Run `nvm install && nvm use` in a connected development environment. No lockfile
is included in this repair: dependency resolution must come from the registry.
The staging sandbox has Node 24 and no installed project dependencies; it is not
an authoritative runtime build environment.

## Dependency access

The public SDK scope `@citadel-guilds` is configured for GitHub Packages using
setup-node's `registry-url` and `scope`. All other packages use the normal npm
registry. A package administrator must confirm the SDK exists at that registry,
that its published package exports TypeScript declarations compatible with this
consumer, and grant this repository's Actions access to read it. Package-level
access is distinct from `packages: read` on the job token. Do not add private
CNWB imports or fabricate declarations to mask an unavailable SDK.

Actions uses its ephemeral GITHUB_TOKEN as NODE_AUTH_TOKEN; no new secret is
created or requested. Fork PRs must have read access to public dependencies:
if organization policy blocks their package reads, the build must fail closed.
Do not use pull_request_target to expose a write token to fork code. Check
registry placement/access before activating the flow. The dependency scope is
an explicit configuration choice; no live registry lookup occurred here.

## Manual lockfile refresh

After this workflow is on main, a maintainer selects **Lockfile refresh** in
Actions and runs workflow_dispatch on main. Other refs are deliberately skipped.
The validation job has only contents/read and packages/read permissions. It:

1. Reads Node from .nvmrc and configures scoped registry authentication.
2. Runs `npm install --package-lock-only --ignore-scripts` against the registry.
3. Runs `npm ci && npm run lint && npm run typecheck && npm test && npm run build`.
4. Uploads only package-lock.json if every gate succeeds.

A separate job, dependent on validation success, has contents/write and
pull-requests/write. It checks out the same source SHA, downloads only the
validated lockfile from the same run and opens/updates `bits/lockfile-refresh`
against main. It cannot run npm or dependency lifecycle scripts. There is no
main push or automatic merge. Action revisions are pinned to full commit SHAs.
No PR is opened if resolution or any validation fails, or if nothing changed.

GITHUB_TOKEN-created PRs do not automatically trigger other Actions workflows.
A human maintainer must close and reopen the PR to generate a fresh
pull_request event, then wait for all required checks and independent owner
review. Do not interpret the generating run as a substitute for required PR
checks. The refresh action signs its own commits with GitHub's supported bot
signing; administrators must confirm this satisfies the configured ruleset.
The PR branch is reserved for this automation; do not add unrelated work there.

### Bootstrap sequencing

The repair PR itself still cannot pass npm ci until a real lockfile exists.
A manual-only workflow cannot be dispatched until present on the default branch.
If required checks block that bootstrap, an administrator must choose a documented,
minimal, one-time bootstrap exception with independent human owner review (per
GOVERNANCE.md), or generate and supply a genuine validated lockfile through an
approved connected environment before merging. This session applies no exception,
changes no ruleset and does not claim the PR is ready to merge. Never fabricate
a lockfile or weaken tests to resolve this dependency.

## Local/CI validation

```bash
npm ci
npm run lint
npm run typecheck
npm test
npm run build
python -m pip install -r .bits/requirements-checks.txt
python .bits/check_governance.py
python .bits/check_governance.py --mutations
python .bits/check_build.py
mypy --strict .bits/check_governance.py .bits/check_build.py
```

TypeScript checks source, tests and Vitest configuration; tsconfig.build.json
emits only src into dist. ESLint uses the flat configuration. Vitest mocks the
SDK and NATS modules before imports, never calls production, and enforces 80%
line/function/branch/statement coverage on src. Coverage is an enforced CI
threshold, not a local coverage claim. No tests were removed or relaxed.

The Docker build receives package authentication via a BuildKit secret and a
temporary in-memory npm configuration, never an ARG, ENV token or copied npmrc.
It copies compiled output plus production dependencies into a non-root runtime.
The existing trusted-main GHCR publication and tag-based npm release remain;
this staging session runs neither. CodeQL and secret scanning are retained.

## Administrator prerequisites

- Confirm the team mapping and active review/signed-commit ruleset described in
  BRANCH_PROTECTION.md. The App is automation only, never a human code owner.
- Allow pinned actions, manual workflow runs, and Actions to create pull
  requests. Ensure policy permits the dedicated bot branch and signed bot commits.
- Grant package read access to this repository and confirm registry reachability
  (`npm.pkg.github.com` and `registry.npmjs.org`, including registry tarball hosts).
- Enable artifact attestations for the repository/plan and allow id-token OIDC
  and attestations/write only in the trusted-main signer job. Keep fork tokens
  read-only and use GitHub-hosted runners.
- Require observed `build`, `governance-checks` and `build-artifact` PR check names.
  Do not require main-only `attest` or `docker` on PRs.
- After merging a real lockfile, observe clean PR builds and a protected-main
  provenance run, including positive and both negative verification controls.

No settings, secrets, production endpoints or deployments are changed here.
Real installs, package availability, Docker execution and cryptographic
attestation acceptance remain connected-environment acceptance gates.
