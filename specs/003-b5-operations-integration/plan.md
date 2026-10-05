# Implementation Plan: B5 Operations and Payroll Integration

**Branch**: Existing checkouts; no branch switch | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

**Input**: `specs/003-b5-operations-integration/spec.md`

## Summary
Connect the eight existing Person B features to authenticated application routes and screens. Preserve dated employee context, enforce actual grant scope, protect mutations against payroll locks, record transactional audit evidence, and correct payroll input projection. Reuse existing services and shared transport conventions; no schema or migration changes.

## Technical Context

**Language/Version**: TypeScript, Bun 1.3.x; Next.js 16.3.4 / React 19.2.8.
**Primary Dependencies**: Existing Elysia, Drizzle, pg, jose, React and shared API client; no new runtime libraries.
**Storage**: PostgreSQL 16, frozen feature-owned schema and migrations.
**Testing**: Bun service/route/database tests, frontend client tests, lint/build, isolated PostgreSQL journey and browser walkthrough.
**Target Platform**: Web browser and existing local/Compose server.
**Project Type**: Web application with backend/frontend Git submodules.
**Performance Goals**: Repeat prepared two-branch journey within 30 minutes; preserve existing bounded payroll calculation performance check.
**Constraints**: Exact decimal money, string public IDs with safe persistence conversion, server scope checks, append-only history, atomic approvals/settlements/audit. Serialize operational input mutations with payroll final projection. Existing ignored local feature pointer locates this spec.
**Scale/Scope**: Eight backend features, four existing operations pages and necessary schedule/holiday controls, payroll integration fixes and handoff evidence.

## Constitution Check

Pre-research and post-design: PASS. I: close prior schedule rows and create successors; preserve approval/debt/locked facts. II: trusted actors and matching grants, origin checks, service-owned transactions and safe audits. III: feature-prefixed service/repository adapters; routes delegate to controllers, mappers format DTOs; cross-feature access uses services. IV: frozen PostgreSQL schema, snake_case/string IDs/decimal strings. V: focused boundary, runtime and integration checks, no dependencies or deferred external integrations.

No architecture exception is authorized. Frozen debt settlement metadata cannot be updated: derive settlement from existing locked payroll source evidence; report the mismatch in schema-owner-handoff.md. Business queries remain in owning repositories; lock/projection capabilities are exposed through payroll services. Shared application files are changed serially for integration, reflecting Person C ownership.

## Project Structure

### Documentation (this feature)

```text
specs/003-b5-operations-integration/
  spec.md
  plan.md
  research.md
  data-model.md
  contracts/operations.md
  quickstart.md
  tasks.md
  validation.md
```

### Source Code (repository root)

```text
backend/src/app.ts
backend/src/core/{auth,db,errors,audit}/
backend/src/features/{employee,branch-schedule,holiday-calendar,attendance,leave,overtime,advance,loan,debt,payroll}/
backend/src/test/                 # disposable integrated journey
frontend/lib/operations/         # shared typed operations client
frontend/app/(dashboard)/{attendance,leave,overtime,finance}/
frontend/lib/auth/route-access.ts
frontend/components/             # existing navigation
```

**Structure Decision**: Keep concrete features singular and feature-owned. The application composes feature plugins and concrete service dependencies only. Frontend reuses shared session/API facilities and existing layouts.

## Delivery Phases

1. Research existing runtime, transactions, permissions and frontend; capture decisions below.
2. Design unchanged entities and public contracts; generate tasks and analyze coverage.
3. Foundation: trusted transport, scoped historical context, transactional lock and audit adapters.
4. US1: mount attendance/schedules/holidays, safe input validation and dated schedule behavior.
5. US2: leave/OT runtime, atomic quota/history/attendance, matching-grant approval authority.
6. US3: advance projection/thresholds, loans/debt and exact finance deductions.
7. US4: payroll shop scope, approved leave protection, reversals, final serialization and repeatable integration evidence.
8. Validate package checks, isolated database journey and UI. Record limitations without treating skipped checks as passing.
