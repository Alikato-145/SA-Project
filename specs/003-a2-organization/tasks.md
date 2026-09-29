# Tasks: A2 Organization Management

**Input**: Design documents from `/specs/003-a2-organization/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/organization-api.md`, `quickstart.md`

**Tests**: Required by FR-022. Tests are written before their corresponding
implementation and must fail for the intended reason before production code is
added.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: May run in parallel because it changes different files and has no
  unfinished dependency.
- **[Story]**: Maps the task to one independently testable user story.

## Phase 1: Setup

**Purpose**: Establish feature-owned locations without changing schema,
migrations, frontend, or shared application composition.

- [X] T001 Create the organization coordination feature skeleton in `backend/src/features/organization/`
- [X] T002 [P] Create layered Shop feature file skeletons in `backend/src/features/shop/`
- [X] T003 [P] Create layered Branch feature file skeletons in `backend/src/features/branch/`
- [X] T004 [P] Create layered Department feature file skeletons in `backend/src/features/department/`
- [X] T005 [P] Create layered Position feature file skeletons in `backend/src/features/position/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared organization contracts, authorization, errors, audit safety,
and validation required by every story.

- [X] T006 Add `DUPLICATE_CODE` public error code, status, and safe message in the existing unified registry `backend/src/core/errors/error-codes.ts`
- [X] T007 [P] Add duplicate-code error boundary tests in `backend/src/core/errors/error-boundary.test.ts`
- [X] T008 Define organization domain records, list/page inputs, visibility filters, and repository executor types in `backend/src/features/organization/organization.types.ts`
- [X] T009 Implement trimmed text, decimal bigint identifier, pagination, boolean filter, and IANA timezone validation in `backend/src/features/organization/organization.validation.ts`
- [X] T010 [P] Add validation boundary tests in `backend/src/features/organization/organization.validation.test.ts`
- [X] T011 Implement fail-closed grant-to-organization visibility projection for Owner, HR, Branch Manager, Supervisor, and Employee in `backend/src/features/organization/organization.scope.ts`
- [X] T012 [P] Add all/branch/department/revoked/self-scope tests in `backend/src/features/organization/organization.scope.test.ts`
- [X] T013 Add organization snapshot allowlists and redaction tests in `backend/src/core/audit/audit-redaction.ts` and `backend/src/core/audit/audit-redaction.test.ts`
- [X] T014 Register all 20 organization transport audit actions and test unique route/action coverage in `backend/src/core/audit/a2-transport-audit.plugin.ts` and `backend/src/core/audit/a2-transport-audit.plugin.test.ts`

**Checkpoint**: Shared A2 behavior is tested and no user-story code needs to
reinterpret grants, validation, errors, or audit fields.

---

## Phase 3: User Story 1 — Browse authorized organization (Priority: P1) 🎯 MVP

**Goal**: Authenticated users list and read only the organization graph allowed
by their current active grants.

**Independent Test**: Mount read routes in a test-only Elysia app and prove
Owner/HR all-scope, branch-manager branch scope, supervisor department scope,
revoked grants, employee fail-closed behavior, filters, pagination, and hidden
cross-scope detail.

### Tests for User Story 1

- [X] T015 [P] [US1] Add Shop scoped repository/service read tests in `backend/src/features/shop/shop.read.test.ts`
- [X] T016 [P] [US1] Add Branch scoped repository/service read tests in `backend/src/features/branch/branch.read.test.ts`
- [X] T017 [P] [US1] Add Department scoped repository/service read tests in `backend/src/features/department/department.read.test.ts`
- [X] T018 [P] [US1] Add Position scoped repository/service read tests in `backend/src/features/position/position.read.test.ts`
- [X] T019 [US1] Add list/detail route contract and audit-outcome tests for all resources in `backend/src/features/organization/organization.read.routes.test.ts`

### Implementation for User Story 1

- [X] T020 [P] [US1] Implement scoped Shop list/detail persistence in `backend/src/features/shop/shop.repository.ts`
- [X] T021 [P] [US1] Implement scoped Branch list/detail persistence in `backend/src/features/branch/branch.repository.ts`
- [X] T022 [P] [US1] Implement scoped Department list/detail persistence in `backend/src/features/department/department.repository.ts`
- [X] T023 [P] [US1] Implement scoped Position list/detail persistence in `backend/src/features/position/position.repository.ts`
- [X] T024 [P] [US1] Define Shop read DTOs and pure response mapper in `backend/src/features/shop/shop.dto.ts` and `backend/src/features/shop/shop.mapper.ts`
- [X] T025 [P] [US1] Define Branch read DTOs and pure response mapper in `backend/src/features/branch/branch.dto.ts` and `backend/src/features/branch/branch.mapper.ts`
- [X] T026 [P] [US1] Define Department read DTOs and pure response mapper in `backend/src/features/department/department.dto.ts` and `backend/src/features/department/department.mapper.ts`
- [X] T027 [P] [US1] Define Position read DTOs and pure response mapper in `backend/src/features/position/position.dto.ts` and `backend/src/features/position/position.mapper.ts`
- [X] T028 [P] [US1] Implement Shop scoped list/detail use cases in `backend/src/features/shop/shop.service.ts`
- [X] T029 [P] [US1] Implement Branch scoped list/detail use cases in `backend/src/features/branch/branch.service.ts`
- [X] T030 [P] [US1] Implement Department scoped list/detail use cases in `backend/src/features/department/department.service.ts`
- [X] T031 [P] [US1] Implement Position scoped list/detail use cases in `backend/src/features/position/position.service.ts`
- [X] T032 [P] [US1] Implement thin Shop read controller and routes in `backend/src/features/shop/shop.controller.ts` and `backend/src/features/shop/shop.routes.ts`
- [X] T033 [P] [US1] Implement thin Branch read controller and routes in `backend/src/features/branch/branch.controller.ts` and `backend/src/features/branch/branch.routes.ts`
- [X] T034 [P] [US1] Implement thin Department read controller and routes in `backend/src/features/department/department.controller.ts` and `backend/src/features/department/department.routes.ts`
- [X] T035 [P] [US1] Implement thin Position read controller and routes in `backend/src/features/position/position.controller.ts` and `backend/src/features/position/position.routes.ts`

**Checkpoint**: All four resources are independently readable with exact scope,
pagination, search, active filtering, response mapping, and one action audit.

---

## Phase 4: User Story 2 — Manage shops and branches (Priority: P1)

**Goal**: Owner and HR create and safely update shops and branches while codes,
active parents, immutable relationships, timezones, and audit atomicity hold.

**Independent Test**: Create shops and branches, reuse a branch code only across
different shops, reject inactive parents and invalid timezones, deny scoped
writers, and force audit failure to prove mutation rollback.

### Tests for User Story 2

- [X] T036 [P] [US2] Add Shop create/update service and database integration tests in `backend/src/features/shop/shop.write.test.ts`
- [X] T037 [P] [US2] Add Branch create/update service and database integration tests in `backend/src/features/branch/branch.write.test.ts`
- [X] T038 [US2] Add Shop/Branch mutation route, authorization, immutable-parent, duplicate, and audit tests in `backend/src/features/organization/organization.shop-branch.routes.test.ts`

### Implementation for User Story 2

- [X] T039 [P] [US2] Add Shop insert/update persistence and unique-conflict translation in `backend/src/features/shop/shop.repository.ts`
- [X] T040 [P] [US2] Add Branch parent lookup, insert/update persistence, and unique-conflict translation in `backend/src/features/branch/branch.repository.ts`
- [X] T041 [P] [US2] Add Shop create/update request DTO validation in `backend/src/features/shop/shop.dto.ts`
- [X] T042 [P] [US2] Add Branch create/update request DTO validation and timezone default in `backend/src/features/branch/branch.dto.ts`
- [X] T043 [US2] Implement transactional Shop create/update use cases with Owner/HR authorization and domain audit in `backend/src/features/shop/shop.service.ts`
- [X] T044 [US2] Implement transactional Branch create/update use cases with active-Shop validation and domain audit in `backend/src/features/branch/branch.service.ts`
- [X] T045 [P] [US2] Add Shop mutation handlers and route schemas in `backend/src/features/shop/shop.controller.ts` and `backend/src/features/shop/shop.routes.ts`
- [X] T046 [P] [US2] Add Branch mutation handlers and route schemas in `backend/src/features/branch/branch.controller.ts` and `backend/src/features/branch/branch.routes.ts`

**Checkpoint**: Shops and branches satisfy create/update contract without
schema, migration, parent, or shared-composition changes.

---

## Phase 5: User Story 3 — Manage departments and positions (Priority: P1)

**Goal**: Owner and HR create and safely update departments and positions using
branch-local and shop-local uniqueness and active parent chains.

**Independent Test**: Create both child types, reuse codes under different
parents, reject same-parent duplicates and inactive parent chains, deny scoped
writers, and verify audit rollback.

### Tests for User Story 3

- [X] T047 [P] [US3] Add Department create/update service and database integration tests in `backend/src/features/department/department.write.test.ts`
- [X] T048 [P] [US3] Add Position create/update service and database integration tests in `backend/src/features/position/position.write.test.ts`
- [X] T049 [US3] Add Department/Position mutation route, authorization, immutable-parent, duplicate, and audit tests in `backend/src/features/organization/organization.department-position.routes.test.ts`

### Implementation for User Story 3

- [X] T050 [P] [US3] Add Department active parent-chain lookup, insert/update persistence, and conflict translation in `backend/src/features/department/department.repository.ts`
- [X] T051 [P] [US3] Add Position active parent lookup, insert/update persistence, and conflict translation in `backend/src/features/position/position.repository.ts`
- [X] T052 [P] [US3] Add Department create/update request DTO validation in `backend/src/features/department/department.dto.ts`
- [X] T053 [P] [US3] Add Position create/update request DTO validation in `backend/src/features/position/position.dto.ts`
- [X] T054 [US3] Implement transactional Department create/update use cases with active Branch/Shop validation and domain audit in `backend/src/features/department/department.service.ts`
- [X] T055 [US3] Implement transactional Position create/update use cases with active Shop validation and domain audit in `backend/src/features/position/position.service.ts`
- [X] T056 [P] [US3] Add Department mutation handlers and route schemas in `backend/src/features/department/department.controller.ts` and `backend/src/features/department/department.routes.ts`
- [X] T057 [P] [US3] Add Position mutation handlers and route schemas in `backend/src/features/position/position.controller.ts` and `backend/src/features/position/position.routes.ts`

**Checkpoint**: Department and position management is independently complete
and preserves parent identity.

---

## Phase 6: User Story 4 — Deactivate without erasing history (Priority: P1)

**Goal**: Owner and HR deactivate each organization entity without deletion or
cascade while preserving historical reads and atomic audit evidence.

**Independent Test**: Deactivate each entity, repeat it, query inactive detail,
attempt new children under inactive parents, force audit rollback, and prove the
public route table contains no `DELETE` action.

### Tests for User Story 4

- [X] T058 [P] [US4] Add resource deactivation service tests in `backend/src/features/organization/organization.deactivation.test.ts`
- [X] T059 [P] [US4] Add inactive-parent-chain and non-cascade database integration tests in `backend/src/features/organization/organization.history.test.ts`
- [X] T060 [US4] Add deactivation route, reason, repeated-state, atomic audit, and no-DELETE contract tests in `backend/src/features/organization/organization.deactivation.routes.test.ts`

### Implementation for User Story 4

- [X] T061 [P] [US4] Add conditional active-to-inactive persistence methods to all four resource repositories in `backend/src/features/shop/shop.repository.ts`, `backend/src/features/branch/branch.repository.ts`, `backend/src/features/department/department.repository.ts`, and `backend/src/features/position/position.repository.ts`
- [X] T062 [US4] Implement transactional deactivation use cases and state conflicts in all four resource services under `backend/src/features/`
- [X] T063 [P] [US4] Add deactivation request/response controller handling to all four resource controllers under `backend/src/features/`
- [X] T064 [P] [US4] Add `POST /:id/deactivate` routes and reason schemas to all four resource route files under `backend/src/features/`

**Checkpoint**: Every organization master has a one-way, audited, non-cascading
deactivation path and no hard-delete path.

---

## Phase 7: Polish and Cross-Cutting Verification

- [X] T065 Export a dependency-injected A2 route bundle without editing `backend/src/app.ts` in `backend/src/features/organization/organization.routes.ts`
- [X] T066 [P] Add route-bundle composition tests for exactly 20 endpoints and no `DELETE` methods in `backend/src/features/organization/organization.routes.test.ts`
- [X] T067 Add 1,000-row filtered pagination performance fixture and assertion in `backend/src/features/organization/organization.performance.test.ts`
- [X] T068 Run formatter and `bun run typecheck` from `backend/` and resolve A2-introduced findings
- [X] T069 Run focused A2 unit/contract tests and isolated PostgreSQL integration tests from `backend/`
- [X] T070 Run the complete backend regression suite and record commands/results in `specs/003-a2-organization/handoff.md`
- [X] T071 Validate all scenarios in `specs/003-a2-organization/quickstart.md` and document Person C composition instructions in `specs/003-a2-organization/handoff.md`

---

## Dependencies and Execution Order

### Phase dependencies

- Setup → Foundational → all user stories.
- US1 establishes scoped reads used by the later mutation stories.
- US2 Shop behavior precedes Branch behavior; Branch behavior precedes US3
  Department behavior. Position work depends only on Shop behavior.
- US4 depends on complete repositories and services from US1–US3.
- Polish and full verification depend on all stories.

### Parallel opportunities

- T002–T005 create different feature folders.
- Foundational tests T007, T010, and T012 target different contracts.
- Within US1, resource-specific test, repository, DTO/mapper, service, and
  transport files can proceed by resource after their direct dependencies.
- Shop and Branch tests may be authored together; implementation remains Shop
  before Branch where parent behavior is involved.
- Department and Position slices may proceed in parallel after their respective
  parent slices.
- Deactivation repository/controller/route work is resource-local after T060.

## Implementation Strategy

1. Complete and verify the shared foundation.
2. Deliver US1 as the first independently runnable read-only MVP.
3. Add Shop then Branch writes; verify before proceeding.
4. Add Department and Position writes.
5. Add one-way deactivation across all resources.
6. Compose only through the feature-owned route bundle and hand it to Person C;
   do not edit the shared application composition file.

## Phase 8: Convergence

- [X] T072 Expand Shop and Position public identifier route schemas to accept canonical positive PostgreSQL `bigint` identifiers up to 19 digits and add route-boundary coverage per FR-019 (partial)

## Phase 9: Convergence

- [X] T073 Restore the documented safe-decimal identifier boundary for Shop and Position routes and cover `Number.MAX_SAFE_INTEGER` plus the first unsafe integer per the API contract and FR-019 (contradicts)
