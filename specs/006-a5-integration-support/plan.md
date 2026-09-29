# Implementation Plan: A5 Integration Support

**Branch**: codex/a5-integration-support | **Date**: 2026-09-29 | **Spec**: spec.md

## Summary

Freeze the employee operation-context contract, test historical authorization and compensation integration, check audit completeness/redaction, and supply a truthful demo handoff. Fix only defects proven by checks.

## Technical Context

**Stack**: TypeScript, Bun/Elysia backend; TypeScript/Next.js frontend.
**Dependencies**: Existing application only; no new runtime package.
**Storage**: Existing PostgreSQL/Drizzle schema; no migrations.
**Tests**: Bun tests, backend typecheck, frontend tests/lint/build. Database-gated checks only with a dedicated TEST_DATABASE_URL.
**Scope**: Person A integration boundary plus attendance/payroll contract; no new endpoint.

## Constitution Check

- Historical integrity: assert dated context, do not rewrite history.
- Authorization: test backend decisions, not hidden UI controls.
- Audit: check registered actions and redaction.
- Feature-first: tests and fixes stay in owning layers.
- Schema/contracts: no new migration or API.
- Verification: regression tests for confirmed defects; report unavailable DB checks accurately.

No exception planned.

## Sequence
