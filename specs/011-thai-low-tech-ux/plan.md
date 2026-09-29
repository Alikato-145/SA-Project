# Implementation Plan: Thai Low-Tech UX Across the Application

**Branch**: `codex/c4-operations-integration` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

## Summary

Refine every current Haris Payroll screen into a consistent Thai operational workspace for staff with limited technical confidence. Reuse the established dashboard palette and native controls; add shared page guidance, status labels, feedback states, role-aware context, responsive list/table treatment, and plain-language vocabulary. Preserve all existing server authorization, transactions, audit history, and payroll data rules.

## Technical Context

**Language/Version**: TypeScript 5, React 19, Next.js 16; Bun backend services

**Primary Dependencies**: Next.js App Router, Tailwind CSS 4, Elysia, Drizzle

**Storage**: Existing PostgreSQL through the backend; no schema changes

**Testing**: Bun unit tests, frontend ESLint and production build, focused browser checks at 360 and 1280 pixel widths

**Target Platform**: Responsive desktop and mobile web used inside a restaurant or back-office operations environment

**Project Type**: Web application with frontend and backend submodules

**Performance Goals**: No new client dependency; preserve current request patterns and avoid page-level horizontal overflow

**Constraints**: Thai-first content, 44px minimum interactive controls where practical, visible keyboard focus, no raw identifiers as the primary user label, no UI-only authorization, no changes to domain rules or persistence

**Scale/Scope**: All current login and dashboard routes, including nested employee and account pages; five fixed roles

## Constitution Check

| Gate | Status | Evidence |
|---|---|---|
| Historical payroll integrity | Pass | No historical record, approval decision, debt, payroll, or schema change is planned. |
| Server-enforced authorization | Pass | UI visibility derives from session role/context only; routes and services continue to enforce every request. |
| Feature-first backend | Pass | Backend changes are limited to any existing public presentation contract required for a safe UX; no business logic moves to the frontend. |
| Data and contract discipline | Pass | Existing response contracts remain the source of truth; only safe labels/messages may be added when needed. |
| Focused verification and minimal change | Pass | Reuse current shell, API client, request state, and native controls; add targeted route and responsive checks. |

**Post-design check**: Pass. The design adds no database entities, migrations, or authority changes.

## Research Decisions

See [research.md](research.md). The key decisions are:

1. Keep the incumbent green dashboard identity and adopt its semantic tokens consistently instead of applying a new visual theme.
2. Use a shared Thai page frame and shared status/feedback primitives so all routes gain the same predictable language without duplicating state markup.
3. Treat server scope as final; client role context removes irrelevant controls but never makes authorization decisions for mutations.
4. Use native input, select, date, button, table, and details elements before adding custom widgets or dependencies.

## Project Structure

### Documentation

```text
specs/011-thai-low-tech-ux/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/ui-behavior.md
├── quickstart.md
└── tasks.md
```

### Source Code

```text
frontend/
├── app/
│   ├── login/
│   └── (dashboard)/             # every current user-facing route
├── components/                  # application shell and employee selection
├── features/identity-hr/        # existing HR page views and shared primitives
└── lib/                          # API client, current-user context, route policy

backend/
└── src/features/                # existing feature routes/services remain the
                                  # authority for scope, state, and business rules
```

**Structure Decision**: Retain the current frontend App Router and feature folders. Place presentation-only reuse near the current shared components; only update backend presentation contracts if an existing route cannot return a safe label or state needed by the UI.

## Complexity Tracking

No constitution violation or new architectural layer is required.
