---
description: "Dependency-ordered A4 Identity and HR frontend tasks"
---

# Tasks: A4 Identity and HR Frontend

**Input**: Design artifacts in `specs/005-a4-identity-hr-frontend/`

**Scope**: Implement feature-owned presentation and preview routes now. Shared API client, auth-cookie integration, dashboard shell, root navigation, and live E2E remain Person C integration tasks.

## Phase 1: Setup

- [X] T001 Create A4 feature directories under `frontend/features/identity-hr/` and thin preview routes under `frontend/app/`.
- [X] T002 [P] Define safe A1-A3 frontend view models and replaceable operation-port types in `frontend/features/identity-hr/contracts/types.ts`.
- [X] T003 [P] Export A4 route/navigation metadata for Person C in `frontend/features/identity-hr/route-metadata.ts`.

## Phase 2: Foundation

- [X] T004 Build feature-local visual tokens and accessible primitives in `frontend/features/identity-hr/ui/identity-hr.module.css` and `frontend/features/identity-hr/ui/primitives.tsx`.
- [X] T005 [P] Add safe development fixtures without secrets in `frontend/features/identity-hr/fixtures/preview-data.ts`.
- [X] T006 Implement reusable loading, empty, forbidden, conflict, retry, confirmation, and success presenters in `frontend/features/identity-hr/ui/request-states.tsx`.
- [X] T007 Add feature preview frame and section navigation without modifying shared dashboard layout in `frontend/features/identity-hr/ui/preview-frame.tsx`.

## Phase 3: User Story 1 — Sign in

- [X] T008 [US1] Implement login form state and safe error mapping in `frontend/features/identity-hr/auth/login-form.tsx`.
- [X] T009 [US1] Add responsive login preview route in `frontend/app/login/page.tsx`.

## Phase 4: User Story 2 — Accounts and organization

- [X] T010 [P] [US2] Implement account list/detail/create presenters and role-scope form in `frontend/features/identity-hr/accounts/account-views.tsx`.
- [X] T011 [P] [US2] Implement organization tabs, parent context, active state, forms, and deactivation confirmation in `frontend/features/identity-hr/organization/organization-views.tsx`.
- [X] T012 [US2] Add thin account routes in `frontend/app/(dashboard)/accounts/`.
- [X] T013 [US2] Add thin organization route in `frontend/app/(dashboard)/organization/page.tsx`.

## Phase 5: User Story 3 — Employee discovery

- [X] T014 [US3] Implement scoped employee filters, responsive result list, status and pagination in `frontend/features/identity-hr/employees/employee-list.tsx`.
- [X] T015 [US3] Implement field-presence-safe employee profile and history navigation in `frontend/features/identity-hr/employees/employee-profile.tsx`.
- [X] T016 [US3] Add thin employee list/detail routes in `frontend/app/(dashboard)/employees/`.

## Phase 6: User Story 4 — Onboarding and history

- [X] T017 [US4] Implement two-step onboarding reducer, validation, transient bank handling, optional sections, and atomic-result messaging in `frontend/features/identity-hr/onboarding/onboarding-form.tsx`.
- [X] T018 [P] [US4] Implement assignment timeline and effective-date change presenter in `frontend/features/identity-hr/employees/assignment-history.tsx`.
- [X] T019 [P] [US4] Implement masked bank lifecycle presenter in `frontend/features/identity-hr/employees/bank-accounts.tsx`.
- [X] T020 [P] [US4] Implement weekly-holiday history presenter in `frontend/features/identity-hr/employees/weekly-holidays.tsx`.
- [X] T021 [P] [US4] Implement explicit deferred documents presenter without upload action in `frontend/features/identity-hr/employees/documents.tsx`.
- [X] T022 [US4] Add thin onboarding and employee-history routes under `frontend/app/(dashboard)/employees/`.

## Phase 7: Polish and verification

- [X] T023 [US5] Complete responsive, visible-focus, keyboard, aria-live, reduced-motion, and long-Thai-text pass across A4 components.
- [X] T024 Scan A4 source and fixtures for full bank numbers, passwords, tokens, hashes, direct fetch, or QueryClient creation.
- [X] T025 Run `bun run lint` and `bun run build` in `frontend/`, fix failures, and record results in `specs/005-a4-identity-hr-frontend/quickstart.md`.
- [X] T026 Document deferred Person C integration tasks and changed route manifest in `specs/005-a4-identity-hr-frontend/quickstart.md`.

## Dependencies

`Setup → Foundation → US1/US2/US3 → US4 → Polish`. After Foundation, US1, account UI, organization UI, and employee list UI may proceed in parallel.

## Phase 8: Live integration after shared shell

- [X] T027 Connect account and organization screens to the mounted A1/A2 endpoints with server errors, role scopes, and audited mutations.
- [X] T028 Connect employee list, profile, assignment, bank, and holiday reads and writes to A3 endpoints with server-scoped data.
- [X] T029 Connect atomic onboarding to `/v1/employees/onboard`, including organization choices and one-time password handling.
- [X] T030 Mount A4 navigation in the shared shell, apply role-aware route access, and preserve backend pagination metadata.
- [X] T031 Run frontend tests, lint, typecheck, production build, and document the remaining live environment verification.
