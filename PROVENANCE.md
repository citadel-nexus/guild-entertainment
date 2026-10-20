<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: PROVENANCE.md
# Stage: 06_PLAN
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-GOVERNANCE-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .github/workflows/build-provenance.yml
# EnumType: Doc
# EnumEdges: DEPENDS_ON .github/workflows/build-provenance.yml
# DAG Node: none
# Intent: Let artifact consumers verify both archive integrity and the authorized build identity.
# ───────────────────────────────────────────────────────────────
-->

# Signed build provenance

## Artifact and trust boundary

The `Build provenance` workflow validates governance, then runs `npm ci`, lint,
tests and the existing TypeScript build. It packages `dist/`, package metadata,
README and LICENSE into `guild-entertainment-dist.tar.gz`. The archive is a build
distribution, not a container or published npm release; dependencies are not
bundled. Existing Docker and npm publication workflows are outside this scope.

PR builds exercise the same packaging without signing permissions. Only a
successful `push` to this repository's `main` branch can run the separate
`attest` job. It downloads the artifact from that same run and uses
`actions/attest-build-provenance` to produce a signed in-toto statement with
SLSA provenance v1 for the archive digest. GitHub OIDC supplies a short-lived
Sigstore signing identity. This signs the artifact **by its digest** in the
attestation; no separate long-lived key or detached archive signature is needed.
There is no deployment or package/registry publication step.

Download the `entertainment-dist` artifact for the archive and
`entertainment-provenance` for its Sigstore JSONL verification bundle. The bundle
is also recorded in GitHub's attestation service. Artifact retention is 30 days,
subject to repository limits; preserve the archive, bundle, run URL and source
SHA together if needed longer. Do not verify the outer ZIP produced by GitHub's
artifact download UI; extract it and verify the inner `.tar.gz` bytes.

## Verify before use

Use a current GitHub CLI with `gh attestation verify` support and access to
this repository. Select a successful **main-branch push** run from the protected
repository, inspect its workflow and source commit, and pin that independently
reviewed commit. Do not derive trust solely from metadata supplied with an
untrusted downloaded artifact.

```bash
REPO=citadel-nexus/guild-entertainment
RUN_ID=123456789             # replace with the selected trusted push run
EXPECTED_COMMIT=REPLACE_WITH_REVIEWED_FULL_COMMIT_SHA

gh run view "$RUN_ID" --repo "$REPO" \
  --json event,headBranch,headSha,conclusion,workflowName
# Require push, main, the reviewed SHA, success, and Build provenance.
gh run download "$RUN_ID" --repo "$REPO" --name entertainment-dist --dir verified-dist
gh run download "$RUN_ID" --repo "$REPO" --name entertainment-provenance --dir verified-provenance

gh attestation verify verified-dist/guild-entertainment-dist.tar.gz \
  --repo "$REPO" \
  --signer-workflow "$REPO/.github/workflows/build-provenance.yml" \
  --source-ref refs/heads/main \
  --source-digest "$EXPECTED_COMMIT" \
  --predicate-type https://slsa.dev/provenance/v1 \
  --deny-self-hosted-runners
```

Require a successful exit. Review the verified predicate's source repository
and commit against your approved change. A checksum alone is not proof of
identity. A valid attestation from a different workflow, branch, source commit
or repository is not accepted by this policy.

To verify using the downloaded bundle, repeat the same command adding
`--bundle verified-provenance/provenance.jsonl`; retain every identity and
source restriction. Use GitHub CLI's supported trust-root handling; do not
disable signature or transparency verification. This is not a promise of
fully offline verification.

As an admin acceptance test, verify the untouched archive successfully, then
copy it, append a byte and require verification of the copy to fail. Also
require failure when using an unrelated expected source SHA. Never consume or
deploy the deliberately corrupted copy. These live tests have not been run
in this sandbox.

## Limits and prerequisites

See BRANCH_PROTECTION.md for administrator activation and the pre-existing
build-toolchain blockers. No signed artifact is produced until the real build
succeeds. GitHub OIDC identity is not a Director Nexus personal signature and
artifact signing does not satisfy the signed-commit rule. SLSA v1 is the
predicate format; this change makes no independently assessed SLSA level claim.
The trust boundary includes the reviewed workflow, versioned official Actions,
GitHub-hosted runners, dependency inputs and repository controls. Review action
updates as code-owner changes; this follows the repo's major-version action
convention and does not claim immutable action revisions or reproducible builds.
