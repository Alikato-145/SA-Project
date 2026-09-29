# Tasks: C4 Operations Integration and Usability

**Input**: Design documents from `specs/010-c4-operations-integration/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [operations contract](contracts/operations-http.md)

## Phase 1: Foundation

- [X] T001 Add a focused integration-access test matrix in `backend/src/features/operations-integration/operations-integration.service.test.ts`.
- [X] T002 Implement a feature-owned repository for scoped assignment, branch, shop, operation-context, and locked-payroll lookups in `backend/src/features/operations-integration/operations-integration.repository.ts`.
- [X] T003 Implement the authenticated actor conversion and server-side scope/operation guards in `backend/src/features/operations-integration/operations-integration.service.ts`.
- [X] T004 Compose request ID, authentication, CSRF protection, stable error envelopes, and the existing Person B controllers/routes in `backend/src/features/operations-integration/operations-integration.routes.ts`.
- [X] T005 Register concrete operations dependencies and routes in `backend/src/app.ts` and cover mounted workflow routes in `backend/src/features/operations-integration/operations-integration.app.test.ts`.

**Checkpoint**: All exposed operations requests receive an authenticated server actor and existing business services remain the only owners of workflow rules.

## Phase 2: User Story 1 - Operate daily workflows safely (Priority: P1) 🎯 MVP

**Goal**: Release scoped, authenticated operations routes without altering business histories.

**Independent Test**: A role matrix permits in-scope read/mutation attempts and safely denies cross-scope attempts for each workflow family.

- [X] T006 [US1] Add shared typed operations API requests and envelope/error handling in `frontend/lib/operations/operations-api.ts` with tests in `frontend/lib/operations/operations-api.test.ts`.
- [X] T007 [US1] Move attendance, leave, overtime, and finance pages onto the shared operations client in `frontend/app/(dashboard)/{attendance,leave,overtime,finance}/page.tsx`.
- [X] T008 [US1] Release role-aware operation destinations and extend route-policy tests in `frontend/lib/auth/route-access.ts` and `frontend/lib/auth/route-access.test.ts`.

**Checkpoint**: An authorized user can open and use the intended daily-workflow page; direct server calls remain scope-enforced.

## Phase 3: User Story 2 - Scan and act in the operations workspace (Priority: P2)

**Goal**: Make workflow purpose, status, filters, and actions clear at operational density.

**Independent Test**: At 360px and 1280px, each released page has a visible task heading, primary action, clear state feedback, and no horizontal page scrolling.

- [X] T009 [US2] Refine the shared operations feedback, form, status, and table patterns in `frontend/app/(dashboard)/{attendance,leave,overtime,finance}/page.tsx` using the existing dashboard tokens.
- [X] T010 [US2] Add focused UI state/access tests for released operations paths in `frontend/lib/auth/route-access.test.ts` and `frontend/lib/operations/operations-api.test.ts`.

**Checkpoint**: Operations pages are high-signal, accessible, and visually consistent without a new design system.

## Phase 4: User Story 3 - Understand the signed-in workspace (Priority: P3)

**Goal**: Replace placeholder session context with an understandable account shell and sign-out.

**Independent Test**: A signed-in role sees safe account identity and permitted navigation, then sign-out redirects to login.

- [X] T011 [US3] Add logout to `frontend/lib/auth/auth-api.ts` and its focused request test in `frontend/lib/auth/auth-api.test.ts`.
- [X] T012 [US3] Pass the current actor into the shell and add safe identity/sign-out behavior in `frontend/components/dashboard-access-guard.tsx` and `frontend/components/application-shell.tsx`.

## Phase 5: Validation and handoff

- [X] T013 Run backend `bun run typecheck` and `bun test`, frontend `bun test`, `bun run lint`, and `bun run build`; record results in `specs/010-c4-operations-integration/quickstart.md`.
- [X] T014 Run the Impeccable detector over changed frontend targets and address its actionable findings.
- [ ] T015 Perform the live PostgreSQL role smoke in `specs/010-c4-operations-integration/quickstart.md` when a Docker-enabled database is available; record evidence or the environment blocker.

## Dependencies and execution order

`T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → T010 → T011 → T012 → T013 → T014 → T015`

The backend foundation is the release blocker. Frontend API work can begin once
the contract in T004 is fixed; page and shell refinement follow without changing
business rules.
