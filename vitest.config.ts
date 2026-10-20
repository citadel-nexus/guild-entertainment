/*
# ─── CGRF Header ───────────────────────────────────────────────
# File: vitest.config.ts
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: package.json
# EnumType: Test
# EnumEdges: DEPENDS_ON package.json
# DAG Node: none
# Intent: Enforce isolated runtime tests and minimum coverage before artifacts can be signed.
# ───────────────────────────────────────────────────────────────
*/

import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    include: ['tests/**/*.test.ts'],
    clearMocks: true,
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts'],
      reporter: ['text', 'json-summary'],
      thresholds: { lines: 80, functions: 80, branches: 80, statements: 80 },
    },
  },
});
