/*
# ─── CGRF Header ───────────────────────────────────────────────
# File: eslint.config.mjs
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: package.json
# EnumType: ConfigDoc
# EnumEdges: DEPENDS_ON package.json
# DAG Node: none
# Intent: Catch TypeScript defects consistently with the declared ESLint flat configuration.
# ───────────────────────────────────────────────────────────────
*/

import js from '@eslint/js';
import globals from 'globals';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['dist/**', 'node_modules/**', 'coverage/**'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  { files: ['**/*.ts'], languageOptions: { globals: globals.node } },
);
