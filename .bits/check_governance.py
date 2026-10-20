# ─── CGRF Header ───────────────────────────────────────────────
# File: .bits/check_governance.py
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-GOVERNANCE-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-GOVERNANCE-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .github/workflows/build-provenance.yml, .github/CODEOWNERS, .bits/srs/SRS-CN-ENTERTAINMENT-GOVERNANCE-001.md
# EnumType: Test
# EnumEdges: VALIDATES .github/workflows/build-provenance.yml; VALIDATES .github/CODEOWNERS; VALIDATES .bits/srs/SRS-CN-ENTERTAINMENT-GOVERNANCE-001.md
# DAG Node: none
# Intent: Prevent widening the artifact signing boundary or losing ownership requirements.
# ───────────────────────────────────────────────────────────────

"""Validate the governance records and provenance workflow trust boundary.

Run with Python 3.11+ and PyYAML 6.0.3. These are static contract tests;
GitHub execution and cryptographic verification remain separate acceptance gates.
"""

import copy
import io
from pathlib import Path
import sys
from typing import Any, Callable
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRS = "SRS-CN-ENTERTAINMENT-GOVERNANCE-001"
DISPATCH = "DISP-GOVERNANCE-entertainment"
# BaseLoader keeps GitHub's YAML `on` key a string instead of a YAML 1.1 boolean.
WORKFLOW = yaml.load(
    (ROOT / ".github/workflows/build-provenance.yml").read_text(),
    Loader=yaml.BaseLoader,
)


class GovernanceContract(unittest.TestCase):
    """Check ownership, authorization and artifact signing boundaries."""

    def test_authorized_scope(self) -> None:
        """Require the registered SRS and explicit staging authorization."""
        registry = yaml.safe_load((ROOT / ".bits/srs_registry.yml").read_text())
        self.assertIn("SRS-CN-ENTERTAINMENT-LIVINGWORLD-001", registry)
        self.assertEqual(registry[SRS]["dispatch"], DISPATCH)
        dispatch = (ROOT / f".bits/queue/{DISPATCH}.md").read_text()
        for required in ("status: in_progress", "mode: staging", "authorization_source:"):
            self.assertIn(required, dispatch)
        self.assertTrue((ROOT / f".bits/srs/{SRS}.md").is_file())
        for path in ("AGENTS.md", "CLAUDE.md", ".bits/context.md"):
            self.assertTrue((ROOT / path).is_file())

    def test_ownership_preserves_sdk(self) -> None:
        """Retain the existing review teams and explicit guildmaster identity."""
        owners = (ROOT / ".github/CODEOWNERS").read_text()
        rules = [line.split() for line in owners.splitlines()
                 if line.strip() and not line.startswith("#")]
        self.assertEqual(rules, [
            ["*", "@citadel-nexus/guild-entertainment-leads"],
            ["src/index.ts", "@citadel-nexus/sdk-core",
             "@citadel-nexus/guild-entertainment-leads"],
        ])
        charter = (ROOT / "GOVERNANCE.md").read_text()
        for term in ("Director Nexus", "Tamagotchi", "Entertainment Floor", "guildmasters group"):
            self.assertIn(term, charter)

    def test_unprivileged_events(self) -> None:
        """Reject privileged PR triggers or broad signing entry points."""
        self.assertEqual(WORKFLOW["on"], {
            "push": {"branches": ["main"]},
            "pull_request": {"branches": ["main"]},
        })
        self.assertEqual(WORKFLOW["permissions"], {"contents": "read"})

    def test_signer_boundary(self) -> None:
        """Restrict signing to successful builds of this repository's main branch."""
        signer = WORKFLOW["jobs"]["attest"]
        self.assertEqual(signer["needs"], "build-artifact")
        self.assertEqual(signer["if"],
                         "github.event_name == 'push' && github.ref == 'refs/heads/main' "
                         "&& github.repository == 'citadel-nexus/guild-entertainment'")
        self.assertEqual(signer["permissions"], {
            "contents": "read", "id-token": "write", "attestations": "write",
        })
        self.assertNotIn("continue-on-error", signer)
        self.assertFalse(any("checkout@" in s.get("uses", "") for s in signer["steps"]))

    def test_build_has_no_signing_permissions(self) -> None:
        """Keep PR and build code away from the OIDC signing token."""
        for name, job in WORKFLOW["jobs"].items():
            self.assertEqual(job["runs-on"], "ubuntu-latest")
            if name != "attest":
                self.assertEqual(job.get("permissions", WORKFLOW["permissions"]),
                                 {"contents": "read"})
            for step in job["steps"]:
                if step.get("uses", "").startswith("actions/checkout@"):
                    self.assertEqual(step["with"]["persist-credentials"], "false")
                self.assertNotIn("continue-on-error", step)

    def test_real_build_before_packaging(self) -> None:
        """Require all application gates before archiving the compiled output."""
        job = WORKFLOW["jobs"]["build-artifact"]
        self.assertEqual(job["needs"], "governance-checks")
        self.assertNotIn("if", job)
        self.assertNotIn("continue-on-error", job)
        runs = [s["run"] for s in job["steps"] if "run" in s]
        self.assertEqual(runs[:4], ["npm ci", "npm run lint", "npm test", "npm run build"])
        self.assertIn("set -euo pipefail", runs[4])
        self.assertIn("test -f dist/index.js", runs[4])
        self.assertIn("tar -czf artifacts/guild-entertainment-dist.tar.gz dist ", runs[4])

    def test_same_run_artifact(self) -> None:
        """Bind the signed subject to the exact same-run distribution upload."""
        jobs = WORKFLOW["jobs"]
        upload = jobs["build-artifact"]["steps"][-1]
        download = jobs["attest"]["steps"][0]
        self.assertEqual(upload["uses"], "actions/upload-artifact@v4")
        self.assertEqual(download["uses"], "actions/download-artifact@v4")
        self.assertEqual(upload["with"]["if-no-files-found"], "error")
        self.assertEqual(download["with"], {"name": "entertainment-dist", "path": "artifacts"})
        self.assertEqual(upload["with"]["name"], download["with"]["name"])
        signer = jobs["attest"]["steps"][1]
        self.assertEqual(signer["uses"], "actions/attest-build-provenance@v3")
        self.assertEqual(signer["with"], {"subject-path": upload["with"]["path"]})

    def test_bundle_preserved_without_expression_in_shell(self) -> None:
        """Pass the generated bundle path through the environment before copying."""
        steps = WORKFLOW["jobs"]["attest"]["steps"]
        self.assertEqual(len(steps), 4)
        self.assertEqual(steps[2]["env"], {"BUNDLE_PATH": "${{ steps.provenance.outputs.bundle-path }}"})
        self.assertNotIn("${{", steps[2]["run"])
        self.assertIn('cp -- "$BUNDLE_PATH" provenance/provenance.jsonl', steps[2]["run"])
        self.assertEqual(steps[3]["with"]["path"], "provenance/provenance.jsonl")
        self.assertEqual(steps[3]["with"]["if-no-files-found"], "error")

    def test_verification_identity_constraints(self) -> None:
        """Require consumer verification to pin artifact and source identities."""
        doc = (ROOT / "PROVENANCE.md").read_text()
        for flag in ("--repo", "--signer-workflow", "--source-ref refs/heads/main",
                     "--source-digest", "--predicate-type https://slsa.dev/provenance/v1",
                     "--deny-self-hosted-runners", "--bundle"):
            self.assertIn(flag, doc)

    def test_required_checks_exist_on_prs(self) -> None:
        """Keep required new checks reachable on every targeted pull request."""
        jobs = WORKFLOW["jobs"]
        for name in ("governance-checks", "build-artifact"):
            self.assertIn(name, jobs)
            self.assertNotIn("if", jobs[name])
        doc = (ROOT / "BRANCH_PROTECTION.md").read_text()
        for phrase in ("Require signed commits", "Require review from Code Owners",
                       "`governance-checks`", "`build-artifact`", "`build`"):
            self.assertIn(phrase, doc)


def run_mutation_checks() -> bool:
    """Confirm that unsafe workflow variants fail the security contract."""
    original = copy.deepcopy(WORKFLOW)
    mutations: dict[str, Callable[[dict[str, Any]], None]] = {
        "privileged PR trigger": lambda w: w["on"].update({"pull_request_target": {}}),
        "PR signing token": lambda w: w["permissions"].update({"id-token": "write"}),
        "unconditional signer": lambda w: w["jobs"]["attest"].update({"if": "always()"}),
        "cross-run download": lambda w: w["jobs"]["attest"]["steps"][0]["with"].update({"run-id": "1"}),
        "wrong subject": lambda w: w["jobs"]["attest"]["steps"][1]["with"].update({"subject-path": "other.tar.gz"}),
        "ignored build failure": lambda w: w["jobs"]["build-artifact"].update({"continue-on-error": "true"}),
    }
    passed = True
    try:
        for name, mutate in mutations.items():
            WORKFLOW.clear()
            WORKFLOW.update(copy.deepcopy(original))
            mutate(WORKFLOW)
            result = unittest.TextTestRunner(stream=io.StringIO()).run(
                unittest.defaultTestLoader.loadTestsFromTestCase(GovernanceContract)
            )
            rejected = bool(result.failures) and not result.errors
            print(f"{'PASS' if rejected else 'FAIL'}: reject {name}")
            passed = passed and rejected
    finally:
        WORKFLOW.clear()
        WORKFLOW.update(original)
    return passed


if __name__ == "__main__":
    if sys.argv[1:] == ["--mutations"]:
        raise SystemExit(0 if run_mutation_checks() else 1)
    unittest.main(verbosity=2)
