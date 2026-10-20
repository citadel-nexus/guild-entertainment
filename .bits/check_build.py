# ─── CGRF Header ───────────────────────────────────────────────
# File: .bits/check_build.py
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: .github/workflows/lockfile-refresh.yml, .github/workflows/build-provenance.yml, package.json
# EnumType: Test
# EnumEdges: DEPENDS_ON .github/workflows/lockfile-refresh.yml; DEPENDS_ON .github/workflows/build-provenance.yml; DEPENDS_ON package.json
# DAG Node: none
# Intent: Reject unsafe lockfile automation and verify provenance rejection control flow offline.
# ───────────────────────────────────────────────────────────────

"""Check build workflow boundaries without contacting registries or production."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def workflow(name: str) -> dict[str, Any]:
    """Load a workflow without YAML 1.1 boolean coercion."""
    result: dict[str, Any] = yaml.load(
        (ROOT / f".github/workflows/{name}.yml").read_text(), Loader=yaml.BaseLoader
    )
    return result


class BuildContract(unittest.TestCase):
    """Guard the manual lockfile and provenance verification paths."""

    def test_runtime_and_real_build(self) -> None:
        """Require one Node major and production-only compiler output."""
        package = json.loads((ROOT / "package.json").read_text())
        self.assertEqual((ROOT / ".nvmrc").read_text().strip(), "22")
        self.assertEqual(package["engines"]["node"], ">=22 <23")
        self.assertEqual(package["scripts"]["build"], "tsc -p tsconfig.build.json")
        self.assertEqual(package["scripts"]["typecheck"], "tsc --noEmit -p tsconfig.json")
        base = json.loads((ROOT / "tsconfig.json").read_text())
        build = json.loads((ROOT / "tsconfig.build.json").read_text())
        self.assertTrue(base["compilerOptions"]["strict"])
        self.assertEqual(build["include"], ["src/**/*.ts"])
        self.assertEqual(build["compilerOptions"]["outDir"], "dist")
        docker = (ROOT / "docker/Dockerfile").read_text()
        self.assertEqual(docker.count("FROM node:22-alpine"), 2)
        self.assertIn("type=secret,id=node_auth_token,required=true", docker)
        self.assertNotIn("ARG NODE_AUTH_TOKEN", docker)

    def test_manual_refresh_and_minimal_permissions(self) -> None:
        """Keep registry resolution unprivileged and the PR writer dependent on success."""
        w = workflow("lockfile-refresh")
        self.assertEqual(w["on"], {"workflow_dispatch": ""})
        self.assertEqual(w["permissions"], {"contents": "read"})
        validate = w["jobs"]["validate"]
        self.assertEqual(validate["permissions"], {"contents": "read", "packages": "read"})
        self.assertEqual(validate["if"], "github.ref == 'refs/heads/main' && "
                         "github.repository == 'citadel-nexus/guild-entertainment'")
        runs = [s["run"] for s in validate["steps"] if "run" in s]
        self.assertEqual(runs, ["npm install --package-lock-only --ignore-scripts",
                               "npm ci && npm run lint && npm run typecheck && npm test && npm run build"])
        writer = w["jobs"]["pull-request"]
        self.assertEqual(writer["needs"], "validate")
        self.assertNotIn("if", writer)
        self.assertEqual(writer["permissions"], {"contents": "write", "pull-requests": "write"})
        self.assertFalse(any("run" in s for s in writer["steps"]))
        checkout, download, create = writer["steps"]
        self.assertEqual(checkout["with"]["ref"], "${{ github.sha }}")
        self.assertEqual(download["with"], {"name": "validated-lockfile", "path": "."})
        self.assertEqual(create["with"]["branch"], "bits/lockfile-refresh")
        self.assertEqual(create["with"]["base"], "main")
        self.assertEqual(create["with"]["add-paths"], "package-lock.json")
        self.assertEqual(create["with"]["sign-commits"], "true")

    def test_action_pins_and_failure_propagation(self) -> None:
        """Reject mutable actions and suppressed errors in repaired workflows."""
        for name in ("ci", "release", "build-provenance", "lockfile-refresh"):
            w = workflow(name)
            self.assertNotIn("pull_request_target", w["on"])
            for job in w["jobs"].values():
                self.assertNotIn("continue-on-error", job)
                for step in job["steps"]:
                    self.assertNotIn("continue-on-error", step)
                    if "uses" in step:
                        self.assertRegex(step["uses"], r"^[\w/-]+@[0-9a-f]{40}$")
                    if step.get("uses", "").startswith("actions/checkout@"):
                        self.assertEqual(step["with"]["persist-credentials"], "false")

    def test_registry_auth_and_node_file(self) -> None:
        """Require matching authenticated Node setup on every npm build."""
        for name in ("ci", "release", "build-provenance", "lockfile-refresh"):
            for job in workflow(name)["jobs"].values():
                for step in job["steps"]:
                    if step.get("uses", "").startswith("actions/setup-node@"):
                        self.assertEqual(step["with"]["node-version-file"], ".nvmrc")
                        self.assertEqual(step["with"]["registry-url"], "https://npm.pkg.github.com")
                        self.assertEqual(step["with"]["scope"], "@citadel-guilds")
                        self.assertEqual(job["env"]["NODE_AUTH_TOKEN"], "${{ secrets.GITHUB_TOKEN }}")
                        self.assertIn(job["permissions"]["packages"], ("read", "write"))

    def test_docker_publication_boundary(self) -> None:
        """Keep the existing publication path confined to trusted main pushes."""
        job = workflow("ci")["jobs"]["docker"]
        self.assertEqual(job["needs"], "build")
        self.assertIn("github.event_name == 'push'", job["if"])
        self.assertIn("github.ref == 'refs/heads/main'", job["if"])
        login = job["steps"][1]["with"]
        self.assertEqual(login["username"], "${{ github.actor }}")
        self.assertEqual(login["password"], "${{ secrets.GITHUB_TOKEN }}")
        self.assertEqual(login["registry"], "ghcr.io")
        self.assertEqual(job["permissions"], {"contents": "read", "packages": "write"})

    def test_security_scans_retained(self) -> None:
        """Retain CodeQL and secret scanning rather than waiving them for builds."""
        jobs = workflow("security-scan")["jobs"]
        self.assertIn("codeql", jobs)
        self.assertIn("secret-scan", jobs)
        self.assertTrue(any(s.get("uses", "").startswith("github/codeql-action/analyze@")
                            for s in jobs["codeql"]["steps"]))
        self.assertTrue(any(s.get("uses", "").startswith("trufflesecurity/trufflehog@")
                            for s in jobs["secret-scan"]["steps"]))

    def test_embedded_shell_syntax(self) -> None:
        """Parse every repaired shell block with Bash."""
        for name in ("ci", "release", "build-provenance", "lockfile-refresh"):
            for job in workflow(name)["jobs"].values():
                for step in job["steps"]:
                    if "run" in step:
                        result = subprocess.run(["bash", "-n"], input=step["run"],
                                                text=True, capture_output=True, check=False)
                        self.assertEqual(result.returncode, 0, result.stderr)

    def test_verifier_positive_and_negative_control_flow(self) -> None:
        """Exercise rejection logic using a local fake CLI, never claim cryptographic proof."""
        script = workflow("build-provenance")["jobs"]["attest"]["steps"][-1]["run"]
        fake = r"""#!/usr/bin/env python3
import os
from pathlib import Path
import sys
args = sys.argv[1:]
assert args[:2] == ['attestation', 'verify']
for flag in ('--repo', '--signer-workflow', '--source-ref', '--source-digest', '--bundle', '--predicate-type', '--deny-self-hosted-runners'):
    assert flag in args
mode = os.environ['VERIFY_TEST_MODE']
if mode == 'reject-all':
    sys.exit(1)
if mode == 'accept-all':
    sys.exit(0)
artifact = Path(args[2]).read_bytes()
signer = args[args.index('--signer-workflow') + 1]
if artifact != b'original' and mode != 'accept-tampered':
    sys.exit(1)
if not signer.endswith('/build-provenance.yml') and mode != 'accept-wrong-signer':
    sys.exit(1)
sys.exit(0)
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "artifacts").mkdir()
            (root / "artifacts/guild-entertainment-dist.tar.gz").write_bytes(b"original")
            (root / "gh").write_text(fake)
            (root / "gh").chmod(0o700)
            for mode, expected in (("correct", 0), ("reject-all", 1), ("accept-all", 1),
                                   ("accept-tampered", 1), ("accept-wrong-signer", 1)):
                with self.subTest(mode=mode):
                    env = dict(os.environ, PATH=f"{root}:{os.environ['PATH']}",
                               EXPECTED_COMMIT="local-test-only", VERIFY_TEST_MODE=mode)
                    result = subprocess.run(["bash", "-c", script], cwd=root, env=env,
                                            text=True, capture_output=True, check=False)
                    self.assertEqual(result.returncode, expected, result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
