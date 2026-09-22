# Implementation Plan: Person B Payroll Handoff

**Branch**: `main` | **Date**: 2026-09-22 | **Spec**: [spec.md](spec.md)

**Input**: B5 integration support for attendance, leave/OT, and finance payroll inputs.

## Summary

Add a B-owned attendance service adapter that LeaveService can call inside its existing transaction; count accepted work days for AdvanceService using the existing attendance service/repository. Verify B readers, record contracts and blockers for C, and leave C-owned composition untouched.

## Technical Context

**Language/Version**: TypeScript on Bun
**Primary Dependencies**: Existing Drizzle ORM and Elysia backend
**Storage**: Frozen PostgreSQL 16 feature tables
**Testing**: Focused Bun tests, backend typecheck/full suite; optional disposable database tests
**Target Platform**: Backend service integration
**Project Type**: Web service
**Performance Goals**: Bounded employee/date queries
**Constraints**: No schema, migrations, shared application or Person A/C files
**Scale/Scope**: B1 attendance extension and integration contract

## Constitution Check

- Historical attendance branch is preserved; conflicting worked/holiday days are rejected.
- Leave effect uses the caller's transaction, so quota, decision history, and attendance roll back together.
- Access and payroll locks remain server-side dependencies.
- No debt settlement update is attempted against the append-only trigger.

## Project Structure

```text
backend/src/features/attendance/attendance-leave-effect.service.ts
backend/src/features/attendance/attendance-leave-effect.repository.ts
backend/src/features/attendance/attendance-leave-effect.test.ts
backend/src/features/attendance/attendance.service.ts
backend/src/features/attendance/attendance.test.ts
specs/007-person-b-payroll-handoff/{spec.md,plan.md,research.md,data-model.md,contracts/,quickstart.md,tasks.md}
```

## Phase 0: Research

B1 exposes a bounded payroll work-day reader but not a leave attendance effect or worked-day count. B2 LeaveService already passes its repository transaction to an injected attendance effect. B3 AdvanceService expects an injected eligibility provider. C payroll code and A actor/assignment services are not yet present; use explicit adapters, not speculative implementations in their files.

## Phase 1: Design

The attendance effect queries a dated employee row under lock. For absent/leave it retains the branch and writes `leave` with final deduction flag. For a missing row it asks A's historical assignment service for that date, then inserts a snapshot. Present, late, and holiday rows are conflicts. The repository uses the transaction passed by LeaveService. The attendance worked-day count reads an employee range, counts only present and late, and is exposed through a B-owned adapter satisfying B3's eligibility interface.

## Phase 2: Implementation

Write focused tests, implement the effect and count, run typecheck and suite. Audit each B reader's approved/due filter and document C's route/auth/transaction/settlement responsibilities. Do not mount routes or alter payroll feature.
