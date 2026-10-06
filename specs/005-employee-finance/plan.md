# Implementation Plan: Employee Finance

**Branch**: `005-employee-finance` | **Date**: 2026-09-22 | **Spec**: [spec.md](spec.md)

## Summary

Person B will implement advance eligibility and decisions, loan installment
schedules, and an append-only debt ledger in the three B3 feature folders.
Services enforce scope and money rules; repositories own PostgreSQL operations.
Payroll receives approved and unsettled inputs through service readers.

## Technical Context

**Language/Version**: TypeScript 5.9 on Bun 1.3

**Primary Dependencies**: Elysia, Drizzle ORM, PostgreSQL driver

**Storage**: PostgreSQL 16, frozen feature-owned schemas

**Testing**: Bun tests plus opt-in disposable PostgreSQL fixtures

**Target Platform**: Existing backend service

**Project Type**: Backend feature modules

**Performance Goals**: Bounded monthly reads and interactive decision flows

**Constraints**: No schema, migration, shared app, Person A/C, or frontend changes;
money uses exact cent arithmetic.

**Scale/Scope**: `backend/src/features/{advance,loan,debt}/`

## Constitution Check

| Gate | Status | Evidence |
|---|---|---|
| Historical integrity | Pass with handoff | Debt entries append; the frozen settlement-column conflict is documented for the schema owner. |
| Authorization | Pass | Services require injected effective scope checks. |
| Atomic decisions | Pass | Approval and settlement operations use repository transaction boundaries. |
| Feature-first layers | Pass | Each concrete finance feature owns its files. |
| Frozen schema | Pass | Existing tables, indexes, and checks are used unchanged. |
| Focused verification | Pass | Date/workday/salary/net thresholds, cent allocation, duplicate settlement, and debt reversal tests. |

## Project Structure

```text
specs/005-employee-finance/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/finance-api.md
├── quickstart.md
└── tasks.md

backend/src/features/
├── advance/    # frozen schema plus route/controller/service/repository/DTO/mapper/tests
├── loan/       # frozen schema plus route/controller/service/repository/DTO/mapper/tests
└── debt/       # frozen schema plus route/controller/service/repository/DTO/mapper/tests
```

**Structure Decision**: Person B exports unmounted route factories and service
readers. Person C owns shared composition, payroll lock/settlement, and the shared
error boundary; Person A owns actor and employee context.

## Complexity Tracking

No constitution violations require justification.
