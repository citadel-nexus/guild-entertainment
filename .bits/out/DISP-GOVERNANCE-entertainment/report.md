<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: .bits/out/DISP-GOVERNANCE-entertainment/report.md
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-GOVERNANCE-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .bits/queue/DISP-GOVERNANCE-entertainment.md, .bits/out/DISP-GOVERNANCE-entertainment/memory.json
# EnumType: Doc
# EnumEdges: DEPENDS_ON .bits/queue/DISP-GOVERNANCE-entertainment.md; DEPENDS_ON .bits/out/DISP-GOVERNANCE-entertainment/memory.json
# DAG Node: none
# Intent: Preserve validation limits and admin handoff requirements for the staging change.
# ───────────────────────────────────────────────────────────────
-->

# Dispatch report

## §1 SUMMARY

- Status: PARTIAL — local implementation complete; operational acceptance pending.
- Dispatch: DISP-GOVERNANCE-entertainment
- Seat: BITS-CODEGEN; mode: staging.
- SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
- Branch: dd/bits/SRS-CN-ENTERTAINMENT-GOVERNANCE-001-bootstrap
- Tasks: 4/4 local phases; live provenance/admin acceptance pending.
- Smoke: prior application smoke remains 1/4 dispatch commands passing (25%).
- Current continuation: 10/10 static checks passed; 12/12 unsafe variants rejected.
- Identity resolved: human owner team `@citadel-nexus/guild-entertainment`;
  automation GitHub App `director-nexus-ent-guildmaster` (not a code owner).
- Identity source: operator's 2026-10-20 update citing Datadog team
  **Entertainment Guild — Director Nexus** (`guild-entertainment`) links.
- CKS Gate: B+/75; CKS: pending; CAPS minimum: B+; CAPS: pending; CK: pending.
- Commits: resolve the focused session change with the command below; no synthetic SHA.

```bash
git log --format='%h %s' c84a02bab9f9b7a34c4afe9ad3304e8318a42ace..HEAD
```

## §2 TASK RESULTS

| Task | Status | Output | Verify | Files / CKET |
|---|---|---|---|---|
| A — Bootstrap | PASS | Local staging authorization, registry and spec | `python .bits/check_governance.py GovernanceContract.test_authorized_scope` | AGENTS.md, CLAUDE.md, .bits/context.md, registry, SRS, queue / 04_HYPOTHESIZE and 11_COMMIT |
| B — Ownership | PASS | Confirmed human guild team, SDK ownership retained, App bypass limits documented | `python .bits/check_governance.py GovernanceContract.test_ownership_preserves_sdk GovernanceContract.test_required_checks_exist_on_prs` | .github/CODEOWNERS, GOVERNANCE.md, BRANCH_PROTECTION.md / 06_PLAN |
| C — Provenance | PARTIAL | Main-only signing workflow and consumer verification; live run pending | `python .bits/check_governance.py` and PROVENANCE.md verification procedure | workflow, checker, PROVENANCE.md / 11_COMMIT and 06_PLAN |
| D — Report/memory | PASS | Evidence and linked three-type payload | `python -m json.tool .bits/out/DISP-GOVERNANCE-entertainment/memory.json` | .bits/out/DISP-GOVERNANCE-entertainment/ / 11_COMMIT |

Static phase gates A/B/C pass; C's live acceptance is deferred. D records the
failed application smoke explicitly rather than presenting static success as
an operational build or a completed remote dispatch.

## §3 SMOKE TEST RESULTS

The static suite and unsafe variants below were rerun for the identity update.
Application failures are retained from the bootstrap; npm commands were not
rerun because this continuation changes only governance, records and checker
coverage. No build-toolchain or application changes were made.

| Command | Expected | Actual | Result |
|---|---|---|---|
| `python .bits/check_governance.py` | All static contracts pass | 10/10 passed | PASS |
| `npm test` | Vitest tests pass | `vitest: not found` | FAIL |
| `npm run lint` | ESLint clean | ESLint configuration missing | FAIL |
| `npm run build` | Compiled dist output | `tsc: not found` | FAIL |

Root cause: the pre-existing scaffold lacks a lockfile, declared development
tools, TypeScript configuration and ESLint configuration. No runtime fix was
applied: it is outside this SRS. Follow-up must provision a reproducible npm
toolchain and tests, then rerun all four commands and `npm ci`. Do not relax
required checks. No application coverage percentage is claimed; pytest and
actionlint are unavailable here. `mypy --strict .bits/check_governance.py` is
blocked by missing PyYAML type stubs. No dependency installation was attempted
in the sandbox, and no real build artifact or signature was produced.

Additional reproducible security check:
`python .bits/check_governance.py --mutations` rejects 12 unsafe variants:
privileged PR trigger, PR signing token, unconditional signing, another run's
artifact, wrong signed subject, ignored build failure, bare GitHub App owner,
App account owner, placeholder guild lead team, placeholder owner, missing
human owner, and App alongside the human owner. A passing baseline is required
before the negative checks, so an unrelated failure cannot count as rejection.
Strict mypy was rerun and remains blocked only by missing PyYAML type stubs.
During the bootstrap, workflow shell blocks were parsed with `bash -n` and
verification flags were checked against
`gh attestation verify --help`. Live artifact tamper and signer-verification tests remain unrun.

## §4 MEMORY INGEST

- Type A count: 15; Type B count: 23; Type C count: 3.
- IOO compliance: true; DKG orphans: 0.
- Payload: .bits/out/DISP-GOVERNANCE-entertainment/memory.json; JSON CGRF metadata: .bits/out/DISP-GOVERNANCE-entertainment/memory.cgrf.yaml.
- Verify counts/links against the payload summary. No Memory MCP call made.

## §5 CKET FILING

Logical stages retain the repository's existing layout, as specified in AGENTS.md.

- 06_PLAN: .github/CODEOWNERS, GOVERNANCE.md, BRANCH_PROTECTION.md, PROVENANCE.md.
- 04_HYPOTHESIZE: AGENTS.md, CLAUDE.md, .bits/srs/SRS-CN-ENTERTAINMENT-GOVERNANCE-001.md.
- 11_COMMIT: .bits/context.md, .bits/srs_registry.yml,
  .bits/queue/DISP-GOVERNANCE-entertainment.md, .bits/check_governance.py,
  .github/workflows/build-provenance.yml, this report, memory.json and its sidecar.
- 13_SAVE: none.
- CGRF: all 15 touched files have session-authored metadata (JSON via sidecar);
  13 files are new. REFLEX check: deferred to the private post-merge validator.

## §6 GOVERNANCE

- Entity: Citadel Nexus Inc. (Delaware C-Corp).
- License posture: existing MIT license retained; no license migration authorized.
- Hard-NO scan: no protected paths changed; prior headers were not modified.
- Secret scan: no forbidden credential prefixes in changed files.
- Stripe mode: not applicable; no checkout or Stripe logic touched.
- GitHub settings and production: not changed. The session records PR #15 as
  merged; this continuation stays on the same branch and does not open another
  PR or claim to add code to the completed merge. Revised PR metadata is prepared
  for the UI; the published PR description has not been directly edited.
- Default branch assumed main from existing workflows; repository CLI default-
  branch lookup was unavailable due to host/remote configuration mismatch.
- Remote VCC registration and sibling-repo comparison: not performed.

## §7 NEXT ACTIONS

- Admin: confirm default branch and visible write-enabled owner teams;
  enable rulesets/branch protection, code-owner review, signed commits and required
  checks; allow official Actions, OIDC and artifact attestations. See
  BRANCH_PROTECTION.md for exact controls and activation tests.
- Automation: identity mapping is resolved. No bypass is granted. Any proposed
  exception for `director-nexus-ent-guildmaster` requires documented human
  approval and must never waive human code-owner review for `.github/**`,
  `GOVERNANCE.md`, `CODEOWNERS` or workflows.
- Build maintainer: repair existing npm build/test/lint prerequisites in a
  separate authorized dispatch, then perform a real main-branch build and
  positive/tampered/wrong-source verification from PROVENANCE.md.
- Handoffs requested: none; no private-stack implementation required.
- Suggested next dispatch: DISP-BUILD-entertainment (proposed only) — repair the
  existing public npm toolchain and exercise provenance end to end.
- Bugs filed: none; no issue was supplied and provider writes are unavailable.
- PR labels to apply at creation: bits:codegen,
  srs:srs-cn-entertainment-governance-001,
  dispatch:disp-governance-entertainment, verified:manual-review.
