# Implementation Plan: Schedules and Attendance

**Branch**: `003-schedules-attendance` | **Date**: 2026-09-22 | **Spec**: [spec.md](spec.md)

## Summary

Person B will deliver B1's backend modules for effective-dated branch schedules,
one-date overrides, shop holiday entries, and manual daily attendance. Each module
follows route → controller → service → repository. The frozen PostgreSQL model
already protects unique dates, clock ordering, and overlapping schedules; services
add input validation, stable conflict errors, and authorization hooks supplied by
Persons A and C.

## Technical Context

**Language/Version**: TypeScript 5.9 on Bun 1.3

**Primary Dependencies**: Elysia, Drizzle ORM, Zod, node-postgres

**Storage**: PostgreSQL 16 using frozen feature-owned schemas and migration

**Testing**: Bun test; database tests opt in with `TEST_DATABASE_URL`

**Target Platform**: Containerized Linux service and local Bun development

**Project Type**: Web application backend feature modules; B1 has no UI work

**Performance Goals**: Interactive schedule lookup and bounded attendance reads

**Constraints**: No schema, migration, shared app, Person A, Person C, or frontend
changes. Dates remain ISO strings, timestamps remain UTC instants, and historical
branch values remain stored facts.

**Scale/Scope**: The three B-owned feature folders only: `branch-schedule`,
`holiday-calendar`, and `attendance`.

## Constitution Check

| Gate | Status | Evidence |
|---|---|---|
| Historical payroll integrity | Pass | Attendance stores the submitted branch snapshot; corrections retain it. |
| Server-side authorization | Planned dependency | Services receive actor/scope guards from A/C; routes remain unmounted until provided. |
| Feature-first layering | Pass | Each B feature has DTO, mapper, repository, service, controller, route and test files. |
| Frozen PostgreSQL model | Pass | No schema or migration work; existing protections remain authoritative. |
| Focused verification | Pass | Resolver, override, conflict, clock and snapshot service tests; opt-in database checks. |

No unresolved clarification remains. Person C must confirm the actor/scope,
public-error, payroll-lock, and route-composition contracts in
[integration.md](contracts/integration.md) before routes are enabled.

## Project Structure

### Documentation

```text
specs/003-schedules-attendance/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── attendance-api.md
│   └── integration.md
└── tasks.md
```

### Source Code

```text
backend/src/features/
├── branch-schedule/
│   ├── branch-schedule.schema.ts          # existing, frozen
│   ├── branch-schedule.dto.ts
│   ├── branch-schedule.mapper.ts
│   ├── branch-schedule.repository.ts
│   ├── branch-schedule.service.ts
│   ├── branch-schedule.controller.ts
│   ├── branch-schedule.routes.ts
│   └── branch-schedule.test.ts
├── holiday-calendar/
│   ├── holiday-calendar.schema.ts         # existing, frozen
│   ├── holiday-calendar.dto.ts
│   ├── holiday-calendar.mapper.ts
│   ├── holiday-calendar.repository.ts
│   ├── holiday-calendar.service.ts
│   ├── holiday-calendar.controller.ts
│   ├── holiday-calendar.routes.ts
│   └── holiday-calendar.test.ts
└── attendance/
    ├── attendance.schema.ts                # existing, frozen
    ├── attendance.dto.ts
    ├── attendance.mapper.ts
    ├── attendance.repository.ts
    ├── attendance.service.ts
    ├── attendance.controller.ts
    ├── attendance.routes.ts
    └── attendance.test.ts
```

**Structure Decision**: Person B owns only the listed files. Repositories use the
feature schemas directly. Routes are exported for Person C to compose in
`backend/src/app.ts`; B does not edit that shared file.

## Complexity Tracking

No constitution violations require justification.
