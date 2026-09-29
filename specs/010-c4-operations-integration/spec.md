# Feature Specification: C4 Operations Integration and Usability

**Feature Branch**: `010-c4-operations-integration`

**Created**: 2026-09-28

**Status**: Draft

**Input**: User description: "Complete Person C final integration: make the delivered Operations workflows usable through the existing dashboard, preserve server-side authorization, and improve scanability and action clarity without redesigning the product."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Operate daily workflows safely (Priority: P1)

An authorized employee, supervisor, branch manager, HR user, or owner opens an available daily-workflow destination and can only read or act on records in their assigned scope.

**Why this priority**: The delivered attendance, leave, overtime, and employee-finance workflows cannot support payroll until they are available through the application with their scope rules enforced.

**Independent Test**: Sign in with representative role assignments, perform one permitted operation for each workflow, and verify an out-of-scope operation receives a safe denial without disclosing protected facts.

**Acceptance Scenarios**:

1. **Given** a signed-in user with permission for a workflow, **When** the user opens its dashboard destination, **Then** the destination is available and requests run using the active session.
2. **Given** a user without permission for a record or action, **When** the user submits a direct request, **Then** the system denies it on the server with a stable public reason.
3. **Given** a successful or rejected daily-workflow action, **When** the result returns, **Then** the user sees an immediate, clear status that explains the next action without exposing internal details.

---

### User Story 2 - Scan and act in the operations workspace (Priority: P2)

An operations user can identify the current task, key status, records requiring attention, and the primary next action without navigating through extra screens.

**Why this priority**: The dashboard is used repeatedly during day-to-day operations, so dense information must remain easy to scan and act on.

**Independent Test**: At desktop and narrow mobile widths, open each released operations screen and verify a user can locate the page purpose, filter input, primary action, result state, and pending decision controls without horizontal page scrolling.

**Acceptance Scenarios**:

1. **Given** a workflow page with no selected records, **When** it loads, **Then** it explains what data to select or create and presents the primary action visibly.
2. **Given** records with pending, approved, rejected, or locked-related states, **When** they are displayed, **Then** their status is visually distinct and understandable at a glance.
3. **Given** an error, warning, empty result, loading state, or successful update, **When** it occurs, **Then** the page presents a consistent, accessible message near the relevant task area.

---

### User Story 3 - Understand the signed-in workspace (Priority: P3)

A signed-in user sees their actual account identity, relevant navigation, and a clear way to end their session rather than placeholder account information.

**Why this priority**: Accurate session context increases trust and helps users understand why certain destinations or actions are available.

**Independent Test**: Sign in with one role, verify the shell displays that account and only permitted destinations, then sign out and confirm protected destinations return to sign-in.

**Acceptance Scenarios**:

1. **Given** a signed-in account, **When** the dashboard shell renders, **Then** it displays safe account identity information rather than placeholder content.
2. **Given** the account's current role assignments, **When** navigation renders, **Then** it includes only destinations the role can access.
3. **Given** a signed-in user, **When** the user signs out, **Then** the session ends and protected dashboard destinations require sign-in again.

### Edge Cases

- A user has more than one role assignment; visibility is the union of valid assignments but never expands beyond any permitted scope.
- A user opens a direct unavailable or unauthorized URL; the shell remains available and the page gives a clear, safe explanation.
- A mutation is submitted twice while the first request is in progress; the interface prevents duplicate local submissions and reports the final server outcome.
- A table has more columns than the narrow viewport; the data remains readable without horizontal page-level scrolling.
- A session expires while an operations page is open; the user is returned to sign-in instead of receiving an ambiguous failed state.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST expose the delivered attendance, schedule, holiday, leave, overtime, advance, loan, and debt workflows through the application composition without changing their business rules or persistence model.
- **FR-002**: The system MUST authenticate every exposed operations request and enforce the actor's role scope on the server for every read and mutation.
- **FR-003**: The system MUST map operations failures to stable public error codes and messages and MUST not disclose unauthorized record existence or internal persistence details.
- **FR-004**: The system MUST preserve transactional leave, overtime, finance, and payroll-lock protections when workflows are exposed through the application.
- **FR-005**: The dashboard MUST make released operations destinations available only to roles that can use them; server enforcement remains authoritative.
- **FR-006**: The dashboard MUST reuse its existing visual language while making page purpose, primary action, record status, filters, and feedback states easy to scan.
- **FR-007**: The dashboard MUST provide visible loading, empty, success, warning, validation, forbidden, and error states for released workflow pages.
- **FR-008**: The dashboard MUST show safe signed-in account context and provide session termination.
- **FR-009**: Released workflow pages MUST remain usable at 360-pixel and 1280-pixel viewport widths without horizontal page scrolling.
- **FR-010**: The feature MUST add focused automated checks for application composition, role access, operation error handling, and released navigation behavior.
- **FR-011**: The feature MUST NOT change database schema, migrations, historical payroll facts, approved attendance, approval history, or debt transaction history.

### Key Entities

- **Authenticated actor**: The current signed-in account, linked employee where present, and its active scoped role assignments.
- **Operations workflow**: Attendance, schedules, holidays, leave, overtime, advances, loans, and debt actions available to an authorized actor.
- **Dashboard feedback state**: A loading, empty, success, warning, forbidden, validation, or error condition that guides the user's next action.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every released operations workflow responds through the authenticated application path and has at least one focused composition or role-access check.
- **SC-002**: The tested role matrix allows 100% of intended actions and denies 100% of tested out-of-scope actions without revealing protected record details.
- **SC-003**: A user can locate the page purpose, primary action, current result state, and pending decision controls within one viewport at 1280 pixels for each released operations screen.
- **SC-004**: Released operations screens have no horizontal page scrolling at 360-pixel and 1280-pixel widths.
- **SC-005**: A signed-in user can identify their account and complete sign-out without entering a URL manually.
- **SC-006**: Backend typecheck and tests plus frontend tests, lint, and production build pass before handoff; live-database checks are recorded separately when a database is available.

## Assumptions

- Existing delivered Person B services and routes are the source of business behavior; this feature adds only the composition and usability work needed to release them.
- Existing fixed roles determine operation visibility: employees act on self-service requests, supervisors act within a department, branch managers act within a branch, and HR/owners administer authorized all-branch work.
- The existing dashboard visual system, color tokens, components, and familiar native form controls remain the design authority.
- Full external time-clock, OCR, and email-provider behavior remain outside scope.
