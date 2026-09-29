# Feature Specification: A4 Identity and HR Frontend

**Feature Branch**: `codex/a4-identity-hr`

**Created**: 2026-09-27

**Status**: Implemented; live integration verification pending against a running backend

**Input**: User description: "Implement the A4 Identity/HR frontend work that can proceed before Person C finishes shared shell integration."

## User Scenarios & Testing

### User Story 1 - Sign in with actionable states (Priority: P1)

A payroll user signs in and receives a clear result for success, invalid credentials, temporary lock, disabled account, validation failure, or service failure.

**Why this priority**: Every protected HR journey begins with a safe and understandable sign-in experience.

**Independent Test**: Submit valid and invalid credentials and verify pending, field validation, locked, disabled, generic failure, and success behavior without exposing internal details.

**Acceptance Scenarios**:

1. **Given** a valid active account, **When** the user signs in, **Then** the user sees a successful transition into the HR workspace.
2. **Given** an invalid, locked, or disabled account, **When** sign-in fails, **Then** the page explains the safe business reason and provides an appropriate next action.
3. **Given** a keyboard-only or mobile user, **When** using the form, **Then** all controls remain labeled, reachable, and usable.

---

### User Story 2 - Administer accounts and organization (Priority: P1)

An Owner or HR user reviews accounts, roles, shops, branches, departments, and positions; creates or updates permitted records; and deactivates records with confirmation instead of deleting history.

**Why this priority**: Employee administration depends on valid organization and access-control masters.

**Independent Test**: Use account and organization screens with loading, empty, forbidden, conflict, validation, and success outcomes and verify parent relationships remain visible.

**Acceptance Scenarios**:

1. **Given** an authorized administrator, **When** viewing accounts or organization masters, **Then** searchable, paged, active/inactive information is understandable.
2. **Given** a scoped or unauthorized user, **When** opening an administrative action, **Then** the interface communicates that access is unavailable while the server remains authoritative.
3. **Given** a deactivation action, **When** the user confirms it with a reason, **Then** the interface never presents the action as permanent deletion.

---

### User Story 3 - Find and understand employees (Priority: P1)

A user finds employees within their authorized scope and opens a profile showing only the sections and fields returned for that role.

**Why this priority**: Employee search and detail are the central HR workflows and the entry point for history management.

**Independent Test**: Exercise Employee, Supervisor, Branch Manager, HR, and Owner views and verify scoped lists, masked values, empty results, and private-field absence.

**Acceptance Scenarios**:

1. **Given** a role-scoped user, **When** filtering employees, **Then** only authorized results are shown and the current filters remain visible.
2. **Given** a safe employee response, **When** opening detail, **Then** the page renders only fields present in that response and never invents hidden values.
3. **Given** no visible results or a hidden record, **When** the request completes, **Then** the user receives a safe empty or not-found state without existence disclosure.

---

### User Story 4 - Onboard and maintain employment history (Priority: P1)

An HR or Owner user completes employee identity, first assignment, optional bank, weekly holidays, and optional account creation as one guided workflow, then reviews assignment, bank, and holiday history.

**Why this priority**: This is the primary Person A demo journey and must preserve the backend's atomic and historical behavior.

**Independent Test**: Complete onboarding with all optional sections, force a component failure, and verify one success or one failure message with no misleading partial-success state.

**Acceptance Scenarios**:

1. **Given** valid employee and assignment information, **When** onboarding succeeds, **Then** created resource identifiers and any one-time password are shown clearly.
2. **Given** any failed onboarding component, **When** the server rejects the request, **Then** the interface states that no partial onboarding was saved.
3. **Given** employment history, **When** adding an assignment or weekly holiday period, **Then** the interface describes effective dates and historical preservation rather than editing the old fact.
4. **Given** bank data, **When** reading an account, **Then** only masked digits appear; plaintext entered for mutation is cleared after completion.

---

### User Story 5 - Work reliably across devices and integration states (Priority: P2)

Users operate the same critical HR workflows on desktop and mobile, including loading, empty, validation, conflict, forbidden, retry, confirmation, and success states.

**Why this priority**: Operational staff use mixed devices and integration with the shared shell will happen after feature work.

**Independent Test**: Verify all A4 routes at narrow and wide widths with keyboard navigation, visible focus, reduced motion, and a replaceable integration boundary.

**Acceptance Scenarios**:

1. **Given** a 360-pixel viewport, **When** completing a critical workflow, **Then** no required field or action is hidden or clipped.
2. **Given** a delayed or failed request, **When** state changes, **Then** focus and status messaging make the result understandable.
3. **Given** the shared shell becomes available, **When** A4 is integrated, **Then** feature routes and navigation metadata can be adopted without rewriting business screens.

### Edge Cases

- Session expires while a protected screen is open.
- Server returns an unknown stable error code or malformed payload.
- Filter changes produce an empty page after a later pagination page.
- Optional onboarding sections are omitted or dynamically enabled.
- One-time password is dismissed; the UI must not persist or redisplay it.
- A bank number or password must not remain in logs, URL state, or long-lived client cache.
- A record becomes inactive between loading detail and submitting an action.
- Long Thai names, organization names, and validation messages wrap on narrow screens.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST provide sign-in with pending, success, invalid-credential, locked, disabled, validation, and retryable failure states.
- **FR-002**: The system MUST provide account administration views for list, detail, create, password reset, status, and scoped role assignment when authorized.
- **FR-003**: The system MUST provide organization views for shops, branches, departments, and positions with parent filters and active/inactive state.
- **FR-004**: The system MUST represent removal-like master actions as deactivation with confirmation and reason, never hard deletion.
- **FR-005**: The system MUST provide scoped employee list, filters, pagination, detail, and own-profile presentation.
- **FR-006**: The system MUST render only fields supplied by the authorized employee response and MUST never infer or placeholder-fill protected values.
- **FR-007**: The system MUST provide a guided onboarding flow covering employee, assignment, optional bank, weekly holidays, and optional account.
- **FR-008**: The system MUST communicate onboarding as one atomic decision and MUST not show partial success when any component fails.
- **FR-009**: The system MUST show one-time credentials only in the immediate successful result and MUST not persist them after dismissal or navigation.
- **FR-010**: The system MUST provide assignment, bank, and weekly-holiday history views and mutation forms using effective-date language.
- **FR-011**: The system MUST display only masked bank account values outside a bank mutation input and clear plaintext after completion.
- **FR-012**: The system MUST provide loading, empty, validation, conflict, forbidden, not-found, retry, confirmation, and success states.
- **FR-013**: The system MUST be keyboard usable, expose visible focus, support reduced motion, and preserve required actions at mobile widths.
- **FR-014**: UI capability hints MAY hide irrelevant actions for usability but MUST state that the backend remains the authorization boundary.
- **FR-015**: The feature MUST publish route and navigation metadata and mount it in the shared shell once that shell is available.
- **FR-016**: The feature MUST use the shared API client for live requests without creating a second network or query provider.
- **FR-017**: The attachment section MUST explicitly state that document upload is outside this demo and MUST NOT provide a fake upload action.
- **FR-018**: Automated verification MUST cover primary journeys, protected-value handling, error mapping, responsive structure, lint, and production build.

### Key Entities

- **Current user**: Safe authenticated account and active role grants used only for capability presentation.
- **Account**: Login identity, status, linked employee, and scoped roles; never contains a password hash.
- **Organization resource**: Shop, branch, department, or position with parent relationship and active state.
- **Employee summary/profile**: Role-safe employee fields supplied by the backend.
- **Onboarding draft**: Short-lived form state for employee, assignment, optional bank, holidays, and account.
- **Employment history item**: Effective-dated assignment or weekly holiday fact.
- **Bank account summary**: Metadata, active/primary state, and last four digits only.
- **UI request state**: Idle, loading, empty, validation error, forbidden, conflict, retryable error, or success.

## Success Criteria

### Measurable Outcomes

- **SC-001**: A trained HR user can complete the full onboarding flow in under five minutes without external instructions.
- **SC-002**: All seven A4 work areas expose a usable loading, empty or success state and a safe failure state.
- **SC-003**: Five role personas complete their permitted employee-view journeys with zero protected-field disclosures.
- **SC-004**: Critical login, employee search, onboarding, and history flows remain usable at 360 pixels and with keyboard-only navigation.
- **SC-005**: Every submitted failure maps to one understandable user message and offers a next action where retry is safe.
- **SC-006**: Automated lint and production build complete with zero errors.
- **SC-007**: The feature uses the shared shell, API client, and navigation manifest without duplicating authentication or query providers.

## Assumptions

- Existing A1-A3 backend contracts remain canonical and server authorization remains authoritative.
- Person C's shared API client, cookie authentication, and dashboard shell became available on `frontend/develop` before the 2026-09-29 integration pass.
- A4 routes now use the shared request boundary and dashboard navigation; the backend still decides record scope and mutation rights.
- The initial implementation targets modern desktop and mobile browsers with network connectivity.
- Attachments, OCR, live time-clock integration, payroll questions, and schema changes remain outside A4.
