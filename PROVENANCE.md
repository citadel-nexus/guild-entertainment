<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: PROVENANCE.md
# Stage: 06_PLAN
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001, SRS-CN-ENTERTAINMENT-BUILD-001
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
typecheck, tests and a clean TypeScript build. It packages `dist/`, package metadata,
the registry-generated lockfile, README and LICENSE into `guild-entertainment-dist.tar.gz`. The archive is a build
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

The main-only signing job performs the same `gh attestation verify` check
against its saved bundle, expected source SHA and signer workflow. It then
appends a byte to a temporary copy and requires verification to fail. It also
verifies the original archive with the wrong signer identity
`citadel-nexus/guild-entertainment/.github/workflows/ci.yml` and requires failure.
Either unexpected success fails the job. A final positive verification detects
persistent service/trust-root failures; the temporary corrupted copy is deleted.
These are real cryptographic checks when run on GitHub, not checksum comparisons.

The local build contract executes the shell with a fake gh command to test
success/failure propagation, including a verifier that accepts tampering or the
wrong signer. This is only control-flow evidence. Live signing and cryptographic
negative checks have not been run in this sandbox. Administrators should also
check that an unrelated expected source SHA fails, retaining all other flags.

## Limits and prerequisites

See BRANCH_PROTECTION.md for administrator activation and the pre-existing
lockfile and package-access prerequisites in BUILD.md. No signed artifact is
produced until the real build succeeds. GitHub OIDC identity is not a Director Nexus personal signature and
artifact signing does not satisfy the signed-commit rule. SLSA v1 is the
predicate format; this change makes no independently assessed SLSA level claim.
The trust boundary includes the reviewed workflow, full-SHA-pinned Actions,
GitHub-hosted runners, dependency inputs and repository controls. Review action
updates as human code-owner changes. Immutable action references do not establish
reproducible builds or prove registry contents; the reviewed lockfile and actual
build gates remain necessary. Only a newly compiled distribution is packaged;
failed installs, tests or builds cannot produce an attestation.
