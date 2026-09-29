# Tasks: Thai Low-Tech UX Across the Application

**Input**: Design documents from `/specs/011-thai-low-tech-ux/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/ui-behavior.md`, and `quickstart.md`

**Tests**: Add focused tests where role context or public error behavior changes; validate every route through lint, build, and the route review in `quickstart.md`.

## Phase 1: Setup and audit baseline

- [X] T001 Record every current route, role policy, safe backend scope boundary, and present UX gap in `specs/011-thai-low-tech-ux/route-audit.md`.
- [X] T002 Review and document the current global visual tokens, form rules, keyboard focus, responsive behavior, and Thai terminology in `frontend/app/globals.css` and `specs/011-thai-low-tech-ux/route-audit.md`.

## Phase 2: Shared foundations

- [X] T003 Create shared Thai page heading, feedback, status-label, domain-vocabulary, and state-explanation primitives in `frontend/components/workspace-ui.tsx`.
- [X] T004 Update semantic tokens, touch-friendly controls, focus treatment, Thai-readable typography, and motion reduction in `frontend/app/globals.css`.
- [X] T005 Update shared navigation, account context, mobile menu, sign-out feedback, and route orientation in `frontend/components/application-shell.tsx`.
- [X] T006 Add focused tests for shared status labels, feedback semantics, and role context in `frontend/components/workspace-ui.test.ts`.

**Checkpoint**: Every feature page can reuse one Thai heading, feedback, and status vocabulary without changing server authorization.

## Phase 3: User Story 1 - Employee self-service is self-scoped (Priority: P1) 🎯 MVP

**Goal**: An Employee sees only their own context and can understand their available work without raw employee identifiers.

**Independent Test**: Sign in as an Employee and verify Leave, Overtime, Payslips, dashboard, and denied routes do not expose an employee selector or unavailable mutation action.

- [ ] T007 [US1] Extend self-versus-management employee context handling in `frontend/components/employee-picker.tsx` and `frontend/lib/auth/auth-api.ts` without widening API authority.
- [X] T008 [US1] Refine employee Leave flow, edit flow, Thai status labels, and self-only context in `frontend/app/(dashboard)/leave/page.tsx`.
- [X] T009 [US1] Refine employee Overtime flow, Thai status labels, self-only context, and approved/rejected feedback in `frontend/app/(dashboard)/overtime/page.tsx`.
- [X] T010 [US1] Refine employee Payslip reading, empty state, final-state explanation, and Thai vocabulary in `frontend/app/(dashboard)/payslips/page.tsx`.
- [ ] T011 [US1] Add role-context and self-service regression checks in `frontend/lib/auth/route-access.test.ts` and `frontend/lib/payslip/payslip-api.test.ts`.

## Phase 4: User Story 2 - Scoped daily operations are clear (Priority: P1)

**Goal**: Supervisors and Branch Managers can identify pending work and act only within their existing server-enforced scope.

**Independent Test**: Sign in as Supervisor and Branch Manager, load Attendance/Leave/Overtime, and confirm pending actions and error recovery are clear in Thai while direct out-of-scope requests remain denied.

- [X] T012 [US2] Refine Attendance filters, Thai statuses, record selection, correction flow, field guidance, and responsive table presentation in `frontend/app/(dashboard)/attendance/page.tsx`.
- [ ] T013 [US2] Refine management Leave decision controls, pending/final explanation, change-type guidance, and scoped employee search in `frontend/app/(dashboard)/leave/page.tsx`.
- [ ] T014 [US2] Refine management Overtime decision controls, pending/final explanation, and scoped employee search in `frontend/app/(dashboard)/overtime/page.tsx`.
- [ ] T015 [US2] Verify no client-only scope assumption changes operation authorization in `backend/src/features/operations-integration/operations-integration.routes.ts` and add/extend focused scope tests in `backend/src/features/operations-integration/operations-integration.service.test.ts`.

## Phase 5: User Story 3 - HR and Owner administration is approachable (Priority: P1)

**Goal**: HR and Owner can complete setup and financial administration with Thai labels, named records, explained consequences, and visible primary actions.

**Independent Test**: Open each administration route as Owner or HR and identify the purpose, required inputs, current record state, primary action, and recovery path without entering an ID as the primary discovery method.

- [X] T016 [US3] Refine Dashboard orientation, permitted-work guidance, and unavailable-work explanations in `frontend/app/(dashboard)/dashboard/page.tsx`.
- [ ] T017 [P] [US3] Refine account pages and account preview states in `frontend/app/(dashboard)/accounts/page.tsx`, `frontend/app/(dashboard)/accounts/[accountId]/page.tsx`, `frontend/app/(dashboard)/accounts/new/page.tsx`, and `frontend/features/identity-hr/accounts/account-views.tsx`.
- [ ] T018 [P] [US3] Refine organization setup and preview states in `frontend/app/(dashboard)/organization/page.tsx` and `frontend/features/identity-hr/organization/organization-views.tsx`.
- [ ] T019 [P] [US3] Refine employee list, detail, employment, bank, weekly-holiday, document, and onboarding pages in `frontend/app/(dashboard)/employees/` and `frontend/features/identity-hr/employees/`.
- [X] T020 [P] [US3] Refine Finance request/approval visibility, Thai status and currency/date context, confirmation copy, and immutable-ledger explanation in `frontend/app/(dashboard)/finance/page.tsx`.
- [ ] T021 [P] [US3] Refine Payroll configuration, preview, lock, adjustment, loading/error, and immutable-period explanation in `frontend/app/(dashboard)/payroll/page.tsx`.
- [X] T022 [P] [US3] Refine Settings, Reports, and Payslip administration with Thai terminology, named selection where available, export guidance, and result states in `frontend/app/(dashboard)/settings/page.tsx`, `frontend/app/(dashboard)/reports/page.tsx`, and `frontend/app/(dashboard)/payslips/page.tsx`.
- [ ] T023 [US3] Add or update focused public-error and role-visibility regression checks in `frontend/lib/api/client.test.ts`, `frontend/lib/auth/route-access.test.ts`, and the affected backend feature tests.

## Phase 6: User Story 4 - Whole application navigation and responsive states (Priority: P1)

**Goal**: Login and every current route remain readable, recoverable, and navigable on desktop and narrow mobile screens.

**Independent Test**: Review login plus every dashboard route at 360px and 1280px; confirm no page-level horizontal overflow, visible focus, and a clear recovery route for denied/error states.

- [ ] T024 [US4] Refine Thai login labels, help, validation recovery, password-manager semantics, and narrow-screen layout in `frontend/app/login/page.tsx`, `frontend/app/login/login.module.css`, and `frontend/features/identity-hr/auth/login-form.tsx`.
- [X] T025 [US4] Refine forbidden, loading, error, and nested-layout copy and recovery links in `frontend/app/(dashboard)/dashboard/forbidden/page.tsx`, `frontend/app/(dashboard)/dashboard/loading.tsx`, `frontend/app/(dashboard)/dashboard/error.tsx`, `frontend/app/(dashboard)/payroll/loading.tsx`, `frontend/app/(dashboard)/payroll/error.tsx`, `frontend/app/(dashboard)/settings/loading.tsx`, and `frontend/app/(dashboard)/settings/error.tsx`.
- [ ] T026 [US4] Ensure nested HR preview and request-state screens use clear Thai current/illustrative-data language, semantic feedback, and responsive overflow handling in `frontend/features/identity-hr/ui/preview-frame.tsx`, `frontend/features/identity-hr/ui/request-states.tsx`, `frontend/features/identity-hr/ui/primitives.tsx`, and `frontend/features/identity-hr/ui/identity-hr.module.css`.

## Phase 7: User Story 5 - Domain vocabulary and final-state clarity (Priority: P2)

**Goal**: A user can understand payroll-related terms and knows which records are pending versus historical.

**Independent Test**: Open every operational and financial workspace and confirm that unfamiliar terms, raw codes, and final states have concise Thai explanations at the point of use.

- [ ] T027 [US5] Apply shared Thai status, money, date, leave-type, attendance, overtime, finance, payroll, and final-state labels to `frontend/app/(dashboard)/attendance/page.tsx`, `frontend/app/(dashboard)/leave/page.tsx`, `frontend/app/(dashboard)/overtime/page.tsx`, `frontend/app/(dashboard)/finance/page.tsx`, `frontend/app/(dashboard)/payroll/page.tsx`, `frontend/app/(dashboard)/payslips/page.tsx`, and `frontend/app/(dashboard)/reports/page.tsx`.

## Phase 8: Polish and validation

- [X] T028 Run the Web Interface Guidelines audit against every changed frontend file and document remediated findings in `specs/011-thai-low-tech-ux/route-audit.md`.
- [ ] T029 Run the UI/UX responsive and role checklist from `specs/011-thai-low-tech-ux/quickstart.md` and record credential-free results in `specs/011-thai-low-tech-ux/route-audit.md`.
- [X] T030 Run backend typecheck and focused tests plus frontend tests, lint, and production build; record commands and results in `specs/011-thai-low-tech-ux/route-audit.md`.
- [X] T031 Run the Impeccable detector on all changed frontend UI files and resolve findings before handoff.

## Dependencies & Execution Order

`T001 → T006 → (T007–T027 by story) → T028–T031`

- User Stories 1–5 all depend on the shared foundation.
- User Stories 1 and 2 share Leave/Overtime and must be completed sequentially in those files.
- User Story 3 page groups marked `[P]` can be worked independently after shared labels exist.
- Validation follows every completed story and the final cross-cutting pass.

## Implementation Strategy

1. Build the shared Thai presentation and account-context foundation.
2. Make self-service unambiguous first, then daily management flows.
3. Apply the same language and interaction rules to every administrative page.
4. Audit every route in two fixed viewport passes, resolve the findings, and stop.
