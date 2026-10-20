/*
# ─── CGRF Header ───────────────────────────────────────────────
# File: tests/health.test.ts
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: src/routes/health.ts, vitest.config.ts
# EnumType: Test
# EnumEdges: DEPENDS_ON src/routes/health.ts; DEPENDS_ON vitest.config.ts
# DAG Node: none
# Intent: Detect changes to the public health response and its clock-derived timestamp.
# ───────────────────────────────────────────────────────────────
*/

import { afterEach, describe, expect, it, vi } from 'vitest';
import { healthCheck } from '../src/routes/health.js';

describe('health contract', () => {
  afterEach(() => vi.useRealTimers());
  it('reports the guild identity and current ISO timestamp', () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-10-20T12:00:00Z'));
    expect(healthCheck()).toEqual({
      guild: 'entertainment', status: 'healthy', version: '0.1.0',
      nats_prefix: 'citadel.ent.*', timestamp: '2026-10-20T12:00:00.000Z',
    });
  });
});
