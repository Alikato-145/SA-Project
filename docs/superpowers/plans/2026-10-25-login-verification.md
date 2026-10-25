# Login and Role Verification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete Subtask 2 by preparing an isolated verification stack and verifying Login, session handling and scoped access for existing roles, including accounting mapped to HR.

**Architecture:** Reuse `scripts/verify.sh`, Compose verification overrides, guarded release fixture and existing auth/Playwright suites. This subtask primarily prepares and verifies existing functionality; modify application code only if a reproduced failure requires a separately recorded fix. Do not mix new payment/loan/schema implementation into Login verification.

**Tech Stack:** Existing Next.js 16 frontend, Bun/Elysia backend, PostgreSQL 16, Docker Compose and Playwright Chromium.

**Spec:** `docs/superpowers/specs/2026-10-25-use-case-delivery-design.md`

## Global Constraints

- ฝ่ายบัญชีใช้ HR grant เดิม ไม่เพิ่ม ACCOUNTING role ในงานชุดนี้
- Database tests and release seeds must target the disposable verification database only; `DATABASE_URL` must equal explicit `TEST_DATABASE_URL` and `RELEASE_DISPOSABLE_DB=1` for fixture seeding.
- No changes to schema, migrations or submodule pointers in this subtask.
- Preserve current source changes and main development databases/volumes; do not reset or stop unrelated containers.
- Do not equate listed tests or passing unit tests with successful browser verification.
- SMTP verification uses local Mailpit only; no external email sends.

## Review Focus

1. A combined HR/OWNER grant can hide a scoped role bug: use existing single-role fixture accounts and assert returned grants.
2. A new account without a grant can login but must not access business pages: exercise existing no-role onboarding scenario.
3. A disabled account with an old session must lose protected access: exercise existing disable/session scenario.
4. Wrong-password/lockout boundaries must not be inferred from happy-path Login: run focused auth/lockout tests and record browser coverage separately.
5. Network errors during logout must not imply session ended: exercise existing mobile logout recovery browser scenario.

## Task 1 Establish repeatable isolated runtime

**Files:**
- Reuse: `compose.yaml`, `compose.verify.yaml`, `.env.example`, `scripts/verify.sh`
- Reuse: `backend/src/db/seed.ts`, `backend/src/db/release-fixture.ts`
- Create: `docs/superpowers/plans/2026-10-25-login-verification-results.md`

**Interfaces:**
- Consumes: Docker daemon, Compose configuration and local ports.
- Produces: verification project `haris-payroll-verify`, base URL `http://localhost:18083`, PostgreSQL host port `55440`, Mailpit `18025`; synthetic September 2026 fixture.

- [x] Check `docker info` and inspect running projects/port conflicts. If daemon is stopped, start installed Docker Desktop without changing global configuration.
- [x] Run `HTTP_PORT=18083 POSTGRES_PORT=55440 docker compose --env-file .env.example -p haris-payroll-verify -f compose.yaml -f compose.verify.yaml config --quiet`; expected exit 0.
- [x] Reuse `VERIFY_BROWSER=0 sh scripts/verify.sh` to build/start only the verification project, seed twice idempotently and run unit/database/static checks. Expected healthy services and no failed checks. Record exact results, including skips.
- [x] Check `/api/v1/auth/me` without a session returns 401, `/healthz` and frontend login route are reachable. Do not proceed against a different or unseeded database.

## Task 2 Verify roles and session behavior

**Files:**
- Reuse: `frontend/e2e/scope.e2e.ts`, `frontend/e2e/flow.e2e.ts`, `frontend/e2e/global-setup.ts`, `frontend/playwright.config.ts`
- Reuse: `backend/src/features/user-account/user-account.lockout.test.ts`, `backend/src/features/user-account/auth.routes.test.ts`, `frontend/lib/auth/route-access.test.ts`
- Update: results document with source-derived and actually executed evidence separately.

**Interfaces:**
- Consumes: Task 1 base URL and guarded synthetic accounts.
- Produces: results for EMPLOYEE, SUPERVISOR, BRANCH_MANAGER, HR (including accounting actor), OWNER; session and own/department/branch/all scope evidence.

- [x] Run focused backend auth and lockout tests using `bun test src/features/user-account/auth.routes.test.ts src/features/user-account/user-account.lockout.test.ts src/features/user-account/user-account.service.test.ts src/core/auth/authorization.test.ts`; expected 0 failures. Read test assertions before claiming disabled/wrong-password boundaries are covered.
- [x] Run `bun test lib/auth/route-access.test.ts lib/auth/auth-api.test.ts` in frontend; expected 0 failures and all canonical post-login destinations covered.
- [x] Run existing scope browser file with `E2E_BASE_URL=http://localhost:18083 bun run test:e2e e2e/scope.e2e.ts`; expected all five role cases pass, including correct denial outside scope.
- [x] Run existing no-role/onboarding, named role/password/disabled-session and mobile/logout recovery scenarios from `flow.e2e.ts` using Playwright grep. Record any steps performed via page.request rather than UI and do not relabel them as UI button tests.
- [x] Inspect per-role screenshots/trace on failure; classify runtime, fixture or product cause before changing source. Additional tests/fixes require a narrow red-to-green check and preserve current architecture.

## Task 3 Record handover baseline

**Files:**
- Update: results document and design checklist.

**Interfaces:**
- Consumes: command exit statuses, test summaries and browser artifacts from Tasks 1–2.
- Produces: a reproducible baseline for employee CRUD and remaining Use Cases.

- [x] Record five-role/accounting mapping, exact executed tests, environment readiness, fixture month and unresolved coverage.
- [x] Mark Subtask 2 complete only if runtime plus required browser cases ran successfully. If environment prevents execution, retain incomplete checkboxes and document the exact blocker without claiming product failure or success.
- [x] Verify only intended documentation/test changes exist and no schema or submodule pointer was changed. No automatic commit/push is required for this verification task.

## Self-review

The spec's Login/accounting mapping is covered. Payment, loan, adjustment and PDF implementation remain separate later subtasks. All commands refer to existing files and scripts; runtime project/ports and fixture parameters match current verification tooling. No new helper, dependency or framework is required merely to run this subtask.

## Execution note

Runtime and the selected 8 browser scenarios passed. An additional replay probe exposed AUTH-01: copied JWT still authorizes after logout. Full session acceptance remains open; see the results document. No application/schema changes were made to hide or fix this finding within the verification step.

Closure after authorized AUTH-01 implementation: complete, backend `dea8d64`/frontend `6e1b14f`. Migrated DB484pass,frontend45pass,logout browser2pass,live5role/restart checks pass,independent review clean. Browser full22/23 plus isolated previously-throttled case1/1; see results/report for production nginx pacing caveat. Prior no-schema-change baseline statement is historical; additive revocation migration was implemented and tested afterward with explicit authorization.
