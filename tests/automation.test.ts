/*
# ─── CGRF Header ───────────────────────────────────────────────
# File: tests/automation.test.ts
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: src/automation/cml-bridge.ts, src/automation/nats-listener.ts, vitest.config.ts
# EnumType: Test
# EnumEdges: DEPENDS_ON src/automation/cml-bridge.ts; DEPENDS_ON src/automation/nats-listener.ts; DEPENDS_ON vitest.config.ts
# DAG Node: none
# Intent: Exercise NATS listener and task result failure paths without production connections.
# ───────────────────────────────────────────────────────────────
*/

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const bus = vi.hoisted(() => ({ connect: vi.fn(), subscribe: vi.fn(), publish: vi.fn() }));
vi.mock('nats', () => ({
  connect: bus.connect,
  StringCodec: () => ({
    encode: (text: string) => new TextEncoder().encode(text),
    decode: (data: Uint8Array) => new TextDecoder().decode(data),
  }),
}));
import { startCmlBridge } from '../src/automation/cml-bridge.js';
import { startListener } from '../src/automation/nats-listener.js';

async function* messages(body = '{"task_id":"unit-task"}') {
  yield { subject: 'unit.subject', data: new TextEncoder().encode(body) };
}

describe('automation without production connections', () => {
  beforeEach(() => {
    vi.resetAllMocks();
    vi.stubEnv('NATS_URL', 'nats://127.0.0.1:1');
    vi.spyOn(console, 'log').mockImplementation(() => undefined);
    bus.connect.mockResolvedValue(bus);
    bus.subscribe.mockImplementation(() => messages());
  });
  afterEach(() => { vi.restoreAllMocks(); vi.unstubAllEnvs(); });

  it('consumes listener messages through the mocked connection', async () => {
    await startListener();
    expect(bus.connect).toHaveBeenCalledWith({ servers: 'nats://127.0.0.1:1' });
    expect(bus.subscribe).toHaveBeenCalledWith('citadel.ent.>');
    expect(console.log).toHaveBeenCalledWith('[entertainment] unit.subject: {"task_id":"unit-task"}');
  });
  it('publishes a task result with its original correlation identifier', async () => {
    await startCmlBridge();
    expect(bus.subscribe).toHaveBeenCalledWith('citadel.ent.cml.task');
    expect(bus.publish).toHaveBeenCalledWith('citadel.ent.cml.result', expect.any(Uint8Array));
    expect(JSON.parse(new TextDecoder().decode(bus.publish.mock.calls[0][1] as Uint8Array)))
      .toEqual({ task_id: 'unit-task', status: 'done', output: 'ok' });
  });
  it('reports publication errors on the failure result path', async () => {
    bus.publish.mockImplementationOnce(() => { throw new Error('unit publish failure'); });
    await startCmlBridge();
    expect(bus.publish).toHaveBeenCalledTimes(2);
    expect(JSON.parse(new TextDecoder().decode(bus.publish.mock.calls[1][1] as Uint8Array)))
      .toEqual({ task_id: 'unit-task', status: 'failed', error: 'Error: unit publish failure' });
  });
  it('propagates connection failure instead of claiming success', async () => {
    bus.connect.mockRejectedValue(new Error('unit connection failure'));
    await expect(startListener()).rejects.toThrow('unit connection failure');
    await expect(startCmlBridge()).rejects.toThrow('unit connection failure');
    expect(bus.publish).not.toHaveBeenCalled();
  });
});
