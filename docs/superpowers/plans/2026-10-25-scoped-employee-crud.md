# Scoped Employee CRUD Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Enable UC1–3 for branch managers within their branch while preserving HR/OWNER access and employee history.

**Architecture:** Extend existing employee and employment-assignment services with explicit scoped authorization. Keep account administration separate; reuse onboarding and existing status/termination flows without schema changes.

**Tech Stack:** Bun/Elysia/Drizzle/PostgreSQL16, Next.js16/React19.

**Spec:** `docs/superpowers/specs/2026-10-25-use-case-delivery-design.md`, Subtask3.

## Global Constraints

- Accounting uses existing HR role; no ACCOUNTING role.
- Employee: own data only. Supervisor: own department. Branch manager: own branch. HR/accounting and owner: all branches, with duties appropriate to the role.
- Apply role scope server-side—never rely on hidden frontend controls.
- Avoid hard deletes for master data or records that affect payroll history; prefer status fields and append-only audit trails.
- Preserve employment-assignment history; no cross-branch transfer or account administration granted to managers.
- No schema or migration changes for this task. No production writes, external messages, pushes or merges.

## Review Focus

- Crafted onboarding requests targeting another branch must fail before any employee is inserted.
- Manager requests with optional account creation must fail without creating an account.
- Sparse team DTOs must not silently erase phone/email/address when editing.
- Termination must preserve history and provide a usable confirmation even if current assignment ends.
- A manager's former employee transferred to another branch must not remain editable through historical assignment.

### Task 1: Branch-scoped employee management vertical slice

**Files:**
- Modify existing `backend/src/features/employee/employee.scope.ts`, `employee.service.ts`, `employee.repository.ts`, `employee.mapper.ts`, `employee.dto.ts` as needed.
- Modify existing employment-assignment/termination service authorization only where required by scoped onboarding/termination.
- Modify `frontend/lib/auth/route-access.ts`, `frontend/app/(dashboard)/employees/page.tsx`, `frontend/features/identity-hr/employees/employee-read-view.tsx`, onboarding and profile controls as needed.
- Extend existing feature tests; create `frontend/e2e/employee-management.e2e.ts` for real UI proof.

**Interfaces:**
- Consumes existing scoped actor grants, `onboardEmployee`, employee update/status and assignment/termination services. Preserve existing public API contracts where possible; document additive DTO fields.
- Produces authorized create/edit/deactivate flows for manager own branch and unchanged HR/OWNER flows. Standalone create lacking assignment remains HR/OWNER-only. No manager bank-account/account-admin capability.

- [ ] Read nearest AGENTS and required Next docs. Inspect existing signatures and tests before edits; record chosen policy for historical terminated visibility.
- [ ] Add focused failing backend tests: manager own-branch onboard/update/terminate succeeds; other branch denied with no writes; employee/supervisor denied; account payload denied; HR/OWNER regressions; audit/history preserved. Run and capture genuine RED.
- [ ] Implement minimal service/repository scoped changes; manager responses include contact/date fields required by existing form without exposing full national/passport/bank data. Keep mapping at controller boundary.
- [ ] Run focused tests and backend typecheck; expect zero failures.
- [ ] Add failing UI capability checks or browser regression, then implement manager controls/route access and restricted onboarding choices. Scope profile capabilities separately from bank/account admin controls.
- [ ] Verify browser create→persisted profile→edit→persisted change→terminate/status confirmation for manager own branch; negative other-branch API and forbidden account payload. HR/OWNER existing access must remain usable. Use disposable fixtures, unique codes, local stack only.
- [ ] Run frontend unit/lint/typecheck; expect zero failures. Root runs full DB/browser suites sequentially after ownership handback.
- [ ] Write report `docs/superpowers/reports/03-scoped-employee-crud.md` with files, decisions, RED/GREEN evidence and limitations. Do not claim browser proof unless actually run. Do not commit unrelated AUTH-01 changes; task-specific commits allowed after tests.
