<!--
# ─── CGRF Header ───────────────────────────────────────────────
# File: .bits/out/DISP-BUILD-entertainment/report.md
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .bits/queue/DISP-BUILD-entertainment.md
# EnumType: Doc
# EnumEdges: DEPENDS_ON .bits/queue/DISP-BUILD-entertainment.md
# DAG Node: none
# Intent: Record the verified staging outcomes and unresolved connected-environment gates.
# ───────────────────────────────────────────────────────────────
-->

# Staging dispatch report

## §1 SUMMARY

Status: PARTIAL (implementation complete; live acceptance blocked)
Dispatch: DISP-BUILD-entertainment
Seat: BITS-CODEGEN
SRS: SRS-CN-ENTERTAINMENT-BUILD-001
Branch: bits/SRS-CN-ENTERTAINMENT-BUILD-001-governance
Tasks: 3/4 (connected acceptance pending)
Smoke: 8/14 build gates; combined static 30/30; npm + mypy 0/6
CKS Gate: B+/75; CKS: pending; CAPS minimum: B+; CAPS: pending; CK: pending
Commits: capture after final bookkeeping with `git log --oneline origin/main..HEAD`.
Base: 246dda4f23e18e24af175d03060cd1f63562ea4f (updated main, PRs #13 and #15).

This continuation is locally authorized by the current operator directive;
it does not assert remote VCC approval. The directive explicitly combines both
SRS scopes in one staging branch/PR. No publication was performed in-session.

## §2 TASK RESULTS

- Task A — Build configuration: PASS (static), PARTIAL (execution). Node 22,
  strict source/test typing, production-only compilation and flat ESLint are
  declared. Verify: `python .bits/check_build.py BuildContract.test_runtime_and_real_build`.
  Files: package/config/Docker files. CKET: 11_COMMIT.
- Task B — Isolated tests: PARTIAL. Six Vitest cases mock SDK/NATS and cover
  health, startup, listener, task result and failure paths. No production
  connections; enforced coverage thresholds are 80%. Runtime execution and
  coverage measurement require dependencies. Verify: `npm test`.
  Files: tests/*, vitest.config.ts. CKET: 11_COMMIT.
- Task C — Workflow repair: PASS (offline), PARTIAL (live). Manual-only lockfile
  refresh validates before an isolated PR writer; full-SHA action pins,
  scoped package reads, proper GHCR expressions and BuildKit secrets are set.
  Signing remains successful-trusted-main-only with exact same-run artifact.
  Verify: `python .bits/check_build.py && python .bits/check_governance.py`.
  Files: workflows, BUILD.md, PROVENANCE.md. CKET: 11_COMMIT/06_PLAN.
- Task D — Operational acceptance: PARTIAL. Real lockfile, npm gates, Docker
  build and cryptographic positive/negative verification require GitHub/registry
  access. BUILD.md documents bootstrap sequencing and prerequisites. Reports and
  memory are complete; no fabricated lockfile or runtime/signing result.
  Verify: `test ! -e package-lock.json && python -m json.tool .bits/out/DISP-BUILD-entertainment/memory.json >/dev/null`.
  Files: dispatch output. CKET: 11_COMMIT.

## §3 SMOKE TEST RESULTS

| Command | Expected | Actual | Result / cause |
|---|---|---|---|
| `python .bits/check_build.py` | 8 pass | 8 pass | PASS |
| `python .bits/check_governance.py` | 10 pass | 10 pass | PASS |
| `python .bits/check_governance.py --mutations` | 12 rejected | 12 rejected | PASS |
| `npm ci --offline --ignore-scripts` | install succeeds | exit 1 | BLOCKED: no real lockfile |
| `npm run lint` | lint succeeds | exit 2 | BLOCKED: @eslint/js not installed |
| `npm run typecheck` | strict types pass | exit 127 | BLOCKED: tsc not installed |
| `npm test` | Vitest + 80% coverage | exit 127 | BLOCKED: vitest not installed |
| `npm run build` | compiled dist | exit 127 | BLOCKED: tsc not installed |
| `mypy --strict .bits/check_governance.py .bits/check_build.py` | typecheck passes | exit 1 | BLOCKED: types-PyYAML absent |
| `python -m pip install --no-index types-PyYAML==6.0.12.20250915` | cached stubs install | exit 1 | BLOCKED: no offline distribution |
| `ruff check .bits/check_governance.py .bits/check_build.py` | no findings | exit 0 | PASS |
| `node --check eslint.config.mjs` | valid JS syntax | exit 0 | PASS |
| `python -m py_compile .bits/check_governance.py .bits/check_build.py` | valid Python syntax | exit 0 | PASS |

Remediation: declared tools/configuration and pinned Python checking requirements;
the authenticated workflow generates the real lockfile and reruns the five npm
gates. Never skip tests or synthesize SDK type declarations to mask installation
failure. The available sandbox is Node 24.13.0/npm 11.6.2; Node 22 was not installed.
Strict mypy still needs registry access; no suppression or fake stubs were added.

Pytest initially failed collection because its separate Python environment lacked
PyYAML. Reusing the already-installed PyYAML resolved that environment issue:

```bash
PYTHONPATH="$(python -c 'import yaml; from pathlib import Path; print(Path(yaml.__file__).parent.parent)')" pytest -q .bits/check_governance.py .bits/check_build.py
```

Result: 18 passed. The twelve mutation scenarios also passed separately.
The verification shell was exercised with five fake-gh scenarios: correct,
reject-all, accept-all, accept-tampered and accept-wrong-signer. Only correct
succeeds. This tests control flow, not real attestations. GitHub CLI help confirms
all configured verification flags exist; no signed subject was available locally.

The installed Prettier TypeScript parser accepted all eight TS files (four
production files, three test files and Vitest configuration). This is syntax-only,
not TypeScript checking. Reproduce with the installed global parser or the
connected `npm run typecheck` gate. pytest-cov is unavailable; measured coverage
is deferred. Docker/registry and cryptographic verification were not executed.

## §4 MEMORY INGEST

Type A count: 28; Type B count: 40; Type C count: 2.
IOO compliance: true. DKG orphans: 0. Payload: .bits/out/DISP-BUILD-entertainment/memory.json.
Verify: `python -m json.tool .bits/out/DISP-BUILD-entertainment/memory.json >/dev/null`.
Events use observed UTC timestamps; no uncreated commit SHA is fabricated.

## §5 CKET FILING

- 06_PLAN: BUILD.md
- 04_HYPOTHESIZE: .bits/srs/SRS-CN-ENTERTAINMENT-BUILD-001.md
- 11_COMMIT: .bits/check_build.py; .bits/out/DISP-BUILD-entertainment/memory.cgrf.yaml; .bits/out/DISP-BUILD-entertainment/memory.json; .bits/out/DISP-BUILD-entertainment/report.md; .bits/queue/DISP-BUILD-entertainment.md; .bits/requirements-checks.txt; .dockerignore; .github/workflows/ci.yml; .github/workflows/lockfile-refresh.yml; .github/workflows/release.yml; .gitignore; .nvmrc; .nvmrc.cgrf.yaml; docker/Dockerfile; eslint.config.mjs; package-lock.json.cgrf.yaml; package.json; package.json.cgrf.yaml; tests/automation.test.ts; tests/health.test.ts; tests/startup.test.ts; tsconfig.build.json; tsconfig.build.json.cgrf.yaml; tsconfig.json; tsconfig.json.cgrf.yaml; vitest.config.ts
- 13_SAVE: none

CGRF headers and JSON/data companions cover every new file. Stages are logical
per repository conventions and the current build directive. REFLEX is deferred
to the external post-merge pipeline; no CK/CAPS/CKS result is fabricated.
Verify changed-file coverage with `git diff --name-only origin/main HEAD` after capture.

## §6 GOVERNANCE

Entity: Citadel Nexus Inc. (Delaware C-Corp).
License posture: existing LICENSE retained; no license change in this dispatch.
Hard-NO scan: no changes to protected code, notify workflow, settings or secrets.
Secret scan: changed-file prefix scan passed without printing matched values.
Stripe mode: not applicable; no checkout/payment code touched.
Human code-owner review remains mandatory; App automation cannot substitute.
No production endpoints were contacted. No new runtime modules or SAKE stubs.
CodeQL and secret scanning retained unchanged; verify with
`git diff origin/main -- .github/workflows/security-scan.yml LICENSE src` (empty).

## §7 NEXT ACTIONS

Blockers: authenticated lockfile generation, installed Node 22 toolchain, SDK
package availability/types, strict mypy stubs, live Docker/attestation acceptance.
Administrators must validate package access, signed-bot-commit acceptance,
rulesets and attestations/OIDC permissions per BUILD.md. None changed here.
Handoffs requested: none. Bugs filed out of scope: none.
Suggested next dispatch: complete DISP-BUILD-entertainment connected acceptance
with a real lockfile and the positive/tampered/wrong-signer verification run.
PR publication requires the coding-agent UI; no direct PR creation or push occurs.
