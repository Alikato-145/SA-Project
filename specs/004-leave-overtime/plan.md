# Implementation Plan: Leave and Overtime

**Branch**: `004-leave-overtime` | **Date**: 2026-09-22 | **Spec**: [spec.md](spec.md)

## Summary

B2 delivers scoped leave and OT workflows in the frozen `leave` and `overtime`
features. Leave approval applies quota and attendance effects transactionally;
approval histories are append-only and only explicitly approved OT reaches payroll.

## Technical Context

**Language/Version**: TypeScript 5.9 on Bun 1.3

**Primary Dependencies**: Elysia, Drizzle ORM, Zod, node-postgres

**Storage**: PostgreSQL 16 using frozen feature schemas and migrations

**Testing**: Bun test and opt-in `TEST_DATABASE_URL` checks

**Target Platform**: Containerized Linux service and local Bun development

**Project Type**: Backend feature modules

**Performance Goals**: Interactive request and decision flows with bounded payroll reads

**Constraints**: No schema, migration, shared app, Person A/C, or frontend changes

**Scale/Scope**: `backend/src/features/{leave,overtime}/` only

## Constitution Check

| Gate | Status | Evidence |
|---|---|---|
| Historical integrity | Pass | Append-only approval history and frozen facts. |
| Authorization and atomicity | Pass | Scoped services and transaction-owned leave decision. |
| Feature-first layers | Pass | Feature-owned DTO, mapper, repository, service, controller, route, tests. |
| Frozen model | Pass | Existing tables and constraints only. |
| Focused verification | Pass | Quota, 3-day rule, OT type, explicit-approval tests. |

## Project Structure

```text
specs/004-leave-overtime/
├── plan.md
├── research.md
├── data-model.md
├── contracts/leave-overtime-api.md
└── quickstart.md

backend/src/features/{leave,overtime}/
```

**Structure Decision**: Person B owns implementation files beside frozen schemas.
Person C composes unmounted routes; Person A supplies scoped actor and effective
assignment interfaces.

## Complexity Tracking

No constitution violations require justification.
