/*
# ─── CGRF Header ───────────────────────────────────────────────
# File: tests/startup.test.ts
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: src/index.ts, vitest.config.ts
# EnumType: Test
# EnumEdges: DEPENDS_ON src/index.ts; DEPENDS_ON vitest.config.ts
# DAG Node: none
# Intent: Verify guild startup configuration without connecting the production SDK.
# ───────────────────────────────────────────────────────────────
*/

import { expect, it, vi } from 'vitest';

const sdk = vi.hoisted(() => ({ start: vi.fn(), options: vi.fn() }));
vi.mock('@citadel-guilds/sdk', () => ({
  default: class {
    constructor(options: unknown) { sdk.options(options); }
    start = sdk.start;
  },
}));

it('starts the configured guild through a mocked SDK', async () => {
  await import('../src/index.js');
  expect(sdk.options).toHaveBeenCalledWith({
    name: 'entertainment', natsPrefix: 'citadel.ent', port: 8400,
  });
  expect(sdk.start).toHaveBeenCalledOnce();
});
