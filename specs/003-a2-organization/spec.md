# Feature Specification: A2 Organization Management

**Feature Branch**: `003-a2-organization`

**Created**: 2026-09-22

**Status**: Draft

**Input**: User description: "Continue Person A with A2 organization: shops, branches, departments, and positions; Owner/HR manage all branches, scoped users read only their authorized organization, deactivate instead of delete, and audit every action."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse authorized organization structure (Priority: P1)

Authenticated users browse only the organization records their current grants authorize. Owner and HR see all shops, branches, departments, and positions. A branch manager sees the granted branch, its parent shop, its departments, and positions belonging to that shop. A supervisor sees the granted department, its parent branch and shop, and positions belonging to that shop.

**Why this priority**: Employee onboarding, role-scope forms, attendance, and payroll cannot select or validate organization context without a safe organization catalog.

**Independent Test**: Give each fixed role representative grants and verify list/detail results for own department, own branch, other branches, inactive records, filters, and pagination without performing any mutation.

**Acceptance Scenarios**:

1. **Given** Owner or HR with an active all-scope grant, **When** organization lists are requested, **Then** records from every shop and branch within the supplied filters are returned.
2. **Given** a branch manager, **When** branches and departments are requested, **Then** only the granted branch and its departments are returned.
3. **Given** a supervisor, **When** organization data is requested, **Then** only the granted department plus its required parent branch/shop and shop positions are returned.
4. **Given** a role grant that is revoked or inactive, **When** the next organization request executes, **Then** it grants no access.
5. **Given** an Employee self-scope grant without an A3 assignment context, **When** an organization list is requested, **Then** access is denied rather than widened; A3 may later supply an explicit dated employee context.

---

### User Story 2 - Manage shops and branches (Priority: P1)

Owner and HR create and update shops and branches across all locations. Shop codes are globally unique, branch codes are unique within their shop, and a branch can be created only under an active shop.

**Why this priority**: Branch and shop identities are parents for every remaining organization and employee record.

**Independent Test**: Create two shops, reuse a branch code in different shops, reject a duplicate within one shop, update safe fields, reject an inactive parent, and verify one audit outcome per invocation.

**Acceptance Scenarios**:

1. **Given** an authorized administrator and a unique shop code, **When** a shop is created, **Then** it is active and available to authorized reads.
2. **Given** an active shop, **When** a branch with a unique code in that shop is created, **Then** the branch retains its shop relationship and configured timezone.
3. **Given** an existing shop code or a branch code already used within the same shop, **When** a duplicate is submitted, **Then** the action fails without changing existing data.
4. **Given** an inactive shop, **When** a new branch is submitted under it, **Then** creation is rejected with a stable state-conflict reason.
5. **Given** a non-HR/non-Owner account, **When** it attempts a shop or branch mutation, **Then** the server denies the action regardless of client controls.

---

### User Story 3 - Manage departments and positions (Priority: P1)

Owner and HR create and update departments within branches and positions within shops. Department codes are unique within a branch and position codes are unique within a shop. New children require active parents.

**Why this priority**: Employee assignment history requires a valid branch, department, and position combination.

**Independent Test**: Create departments and positions under active parents, reject duplicate sibling codes and inactive parents, and prove that the selected department belongs to the expected branch and the position to the expected shop.

**Acceptance Scenarios**:

1. **Given** an active branch, **When** an administrator creates a department with a unique branch-local code, **Then** the department is active and remains linked to that branch.
2. **Given** an active shop, **When** an administrator creates a position with a unique shop-local code, **Then** the position is active and remains linked to that shop.
3. **Given** an inactive branch or shop, **When** a new department or position is submitted, **Then** creation is rejected.
4. **Given** a duplicate department code in one branch or position code in one shop, **When** creation or code update is attempted, **Then** the action fails without overwriting the existing record.
5. **Given** the same child code under different valid parents, **When** records are created, **Then** both are accepted.

---

### User Story 4 - Deactivate organization records without erasing history (Priority: P1)

Owner and HR deactivate organization master records instead of deleting them. Existing historical references remain readable, while inactive records cannot be selected for new children or future employee assignments.

**Why this priority**: Payroll and employment history must continue to explain past records after organization changes.

**Independent Test**: Deactivate each entity, verify historical detail remains readable, verify no hard-delete path exists, reject new children under inactive parents, and inspect the correlated audit facts.

**Acceptance Scenarios**:

1. **Given** an active organization record, **When** an authorized administrator deactivates it with a reason, **Then** it becomes inactive without being deleted.
2. **Given** an already inactive record, **When** deactivation is repeated, **Then** the action returns a stable state conflict and does not create a second business mutation.
3. **Given** an inactive record referenced by historical data, **When** an authorized historical detail is requested, **Then** the record remains readable and clearly marked inactive.
4. **Given** any organization resource, **When** clients inspect the public API, **Then** no hard-delete action exists.
5. **Given** a successful or failed read/write action, **When** it completes, **Then** exactly one redacted audit outcome is correlated by request identifier.

### Edge Cases

- Simultaneous creation of the same unique code must result in one success and one stable duplicate conflict.
- Code comparisons follow the canonical database uniqueness behavior; surrounding whitespace is removed before validation and persistence.
- A branch timezone must be a valid IANA timezone; the default is `Asia/Bangkok` when omitted.
- Deactivating a parent does not cascade status changes to existing children; children remain historical facts but cannot be used as an active path while their parent is inactive.
- Updating a child never changes its parent; moving a branch, department, or position is outside A2 because it would rewrite organization identity and historical meaning.
- Inactive records are excluded from selection lists by default but can be included through an explicit status filter for authorized users.
- Empty search results return an empty page rather than a not-found error.
- Invalid, unsafe, or overlong decimal identifiers are rejected without numeric coercion at the API boundary.
- Authenticated detail reads outside the actor's scope return `RESOURCE_NOT_FOUND` so record existence is not disclosed.
- Lists use stable ascending `(code, id)` ordering; `is_active=false` selects inactive-only records.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide paginated, searchable, filterable list and safe detail access for shops, branches, departments, and positions.
- **FR-002**: Owner and HR with active all-scope grants MUST be able to read and administer every organization record across all branches.
- **FR-003**: Branch managers and supervisors MUST read only the branch/department scope granted to them plus the minimum required parent and shop-position context; Employee self scope MUST fail closed until an explicit assignment context is supplied.
- **FR-004**: Every protected action MUST use current account status and active grants supplied by the A1 authenticated actor boundary.
- **FR-005**: Shop codes MUST be non-empty, at most 30 characters, and globally unique; shop names MUST be non-empty and at most 150 characters.
- **FR-006**: Branch codes MUST be non-empty, at most 30 characters, and unique within a shop; branch names MUST be non-empty and at most 150 characters.
- **FR-007**: Branch addresses MAY be absent and MUST be at most 500 characters when supplied; branch timezone MUST be a valid IANA timezone of at most 50 characters and defaults to `Asia/Bangkok` when omitted.
- **FR-008**: Department codes MUST be non-empty, at most 30 characters, and unique within a branch; department names MUST be non-empty and at most 100 characters.
- **FR-009**: Position codes MUST be non-empty, at most 30 characters, and unique within a shop; position names MUST be non-empty and at most 100 characters.
- **FR-010**: New branches and positions MUST require an existing active shop; new departments MUST require an existing active branch whose shop remains active.
- **FR-011**: Update operations MUST NOT change the parent shop of a branch/position or the parent branch of a department.
- **FR-012**: Organization records MUST NOT have a public hard-delete operation.
- **FR-013**: Authorized administrators MUST deactivate active records through explicit actions carrying a non-empty reason, and repeated deactivation MUST return a stable state conflict.
- **FR-014**: Deactivation MUST preserve the record and all historical relationships and MUST NOT cascade-delete or silently deactivate children.
- **FR-015**: Inactive parents or children MUST NOT be accepted for new downstream organization paths or employee assignments, while authorized historical reads MAY include them explicitly.
- **FR-016**: Duplicate-code and state-conflict failures MUST use stable public error codes without leaking persistence details.
- **FR-017**: Every organization endpoint success and applicable failure MUST produce exactly one correlated, redacted audit outcome; successful mutations and their audit facts MUST commit atomically.
- **FR-018**: Audit snapshots MUST contain only organization identifiers, codes, names, active state, safe parent identifiers, timezone, and address where applicable.
- **FR-019**: Public identifiers MUST be decimal strings and persistence/API fields MUST preserve the approved snake-case contract.
- **FR-020**: The feature MUST use the existing approved schema and migrations without adding, renaming, or deleting organization fields.
- **FR-021**: The feature MUST export independently composable routes and MUST NOT edit the shared application composition file.
- **FR-022**: Focused automated tests MUST cover authorization scope, unique-code boundaries, inactive parents, timezone validation, immutable parents, deactivation, atomic audit behavior, pagination, filters, safe errors, and absence of delete routes.
- **FR-023**: Search text and deactivation reasons MUST be trimmed and limited to 150 and 500 characters respectively; a deactivation reason MUST remain non-empty after trimming.
- **FR-024**: List pagination MUST use deterministic ascending code and identifier ordering.

### Key Entities *(include if feature involves data)*

- **Shop**: Top-level restaurant organization with globally unique code, name, active state, branches, and positions.
- **Branch**: Physical operating location belonging to one immutable shop, with shop-local code, name, optional address, timezone, and active state.
- **Department**: Organizational unit belonging to one immutable branch, with branch-local code, name, and active state.
- **Position**: Shop-level job title belonging to one immutable shop, with shop-local code, name, and active state; compensation is explicitly outside this entity.
- **Authenticated Actor**: A1 request-time account and current grant projection used to determine all, branch, or department visibility.
- **Audit Fact**: Append-only, redacted evidence of one organization action outcome.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An authorized administrator can create a shop, branch, department, and position and verify their hierarchy in under five minutes.
- **SC-002**: All tested unauthorized cross-branch and cross-department reads and writes are denied, with zero records disclosed outside the actor's active scope.
- **SC-003**: All tested duplicate and inactive-parent cases return a stable business reason and leave existing organization data unchanged.
- **SC-004**: One hundred percent of registered A2 endpoint success and applicable failure fixtures produce exactly one correlated audit outcome with zero prohibited secrets.
- **SC-005**: Deactivating any organization entity preserves one hundred percent of its existing historical references and exposes no public hard-delete path.
- **SC-006**: Lists containing at least 1,000 organization records return a correct filtered page within two seconds in the standard test environment.

## Assumptions

- A1 authentication, authorization primitives, request correlation, stable errors, transactions, and audit observers are available and remain the shared boundary.
- The approved PostgreSQL/Drizzle organization schema is frozen for A2.
- Owner and HR are the only organization writers; branch managers and supervisors are scoped readers.
- Employee self-scope organization context depends on A3 dated assignment data and therefore fails closed in standalone A2 list endpoints.
- Parent changes are represented by creating a new correctly parented master record and deactivating the old record when business identity truly changes.
- Organization UI work is part of A4; A2 delivers backend contracts and independently composable routes.
