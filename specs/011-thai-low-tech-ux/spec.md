# Feature Specification: Thai Low-Tech UX Across the Application

**Feature Directory**: `specs/011-thai-low-tech-ux`

**Created**: 2026-09-29

**Status**: Ready for planning

**Input**: Improve the UX/UI of the whole Haris Payroll application after reviewing the existing specifications, frontend, and backend. The primary audience is Thai staff with limited technical confidence. Preserve the established dashboard identity and all server-side authorization and payroll safeguards.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - An employee completes only their own work (Priority: P1)

An Employee can sign in, understand the available workspaces, submit and review
their own requests, and view their own released information without encountering
another employee selector or an action that their role cannot complete.

**Why this priority**: A self-service user is most likely to be confused or
concerned when presented with staff-wide controls and identifiers.

**Independent Test**: Sign in as an Employee and visit every destination made
available to that role. Confirm that the page names the user’s own context,
shows only usable actions, and explains any unavailable information in Thai.

**Acceptance Scenarios**:

1. **Given** an Employee opens a self-service page, **When** the page needs an
   employee context, **Then** it uses their own record and does not ask them to
   search for or enter another employee.
2. **Given** an Employee has no records yet, **When** they open a workspace,
   **Then** they see a plain-language empty state explaining what will appear
   there and the next available action.
3. **Given** an Employee lacks permission for a management action, **When**
   the page renders, **Then** that action is not offered.

---

### User Story 2 - A supervisor or manager resolves daily work safely (Priority: P1)

A Supervisor or Branch Manager can identify what needs attention, select only
records in their scope, and complete an approval or correction with a visible
outcome and no ambiguous technical wording.

**Why this priority**: Daily operational decisions affect attendance, leave,
overtime, and payroll preparation; a mistaken or repeated action is costly.

**Independent Test**: Sign in with representative Supervisor and Branch
Manager roles, load one operational list, complete one permitted decision, and
try one unavailable action.

**Acceptance Scenarios**:

1. **Given** a page contains pending work, **When** an authorized manager
   opens it, **Then** the pending status, record context, and next action are
   distinguishable without decoding IDs or English status names.
2. **Given** a manager’s scope excludes a record, **When** they search or
   submit a direct request, **Then** the interface does not imply success and
   explains the access boundary safely.
3. **Given** an operation succeeds or is blocked, **When** the response
   returns, **Then** the message describes the outcome and a sensible next
   step in Thai.

---

### User Story 3 - HR and Owner perform administration without guessing (Priority: P1)

An HR or Owner user can work through organization, employee, account, payroll,
payslip, report, and settings pages using clear page purpose, grouped fields,
plain Thai labels, and one obvious primary action.

**Why this priority**: These pages contain the highest density of sensitive,
interdependent information and are used by staff who may not know payroll
terminology or technical identifiers.

**Independent Test**: For every administration page, a reviewer can identify
the page purpose, required information, current state, primary action, and
where to get help before entering data.

**Acceptance Scenarios**:

1. **Given** a user opens a form, **When** information is required, **Then**
   each field has a Thai label, relevant help before entry, and an error beside
   the field or action that needs correction.
2. **Given** a page lists records, **When** it contains statuses or dates,
   **Then** the user can scan the meaning without relying on raw codes, IDs, or
   colour alone.
3. **Given** an action cannot be used in the current state, **When** the page
   renders, **Then** it is hidden or explained before the user attempts it.

---

### User Story 4 - Every page is understandable and responsive (Priority: P1)

Any signed-in user can move through the dashboard, direct links, and nested
detail pages on a phone or desktop without horizontal page scrolling, blank
areas, unexplained jargon, or lost navigation.

**Why this priority**: Shared clarity prevents the same usability problem from
being repeated in each business workflow.

**Independent Test**: Review login plus every current dashboard route at 360
and 1280 pixel widths, including denied, loading, empty, error, and populated
states where available.

**Acceptance Scenarios**:

1. **Given** a user opens any current route directly, **When** it loads,
   **Then** the page presents a Thai purpose statement and preserves a clear
   route back to available work.
2. **Given** a page is narrow, **When** tables or forms need more space,
   **Then** content remains readable without horizontal page scrolling and
   controls remain comfortably tappable.
3. **Given** loading, success, warning, denied, or error states, **When**
   they appear, **Then** they have consistent wording and visual treatment
   across the application.

---

### User Story 5 - Users understand payroll vocabulary and consequences (Priority: P2)

A user encountering payroll, leave, overtime, finance, payslip, or report
terms can understand the term, its current status, and whether an action will
change a pending item or a historical record.

**Why this priority**: Payroll terms such as leave type, locked period, and
deduction can otherwise lead to avoidable support requests and unsafe
assumptions.

**Independent Test**: Open each domain workspace and confirm that unfamiliar
terms, disabled actions, and immutable states carry a short Thai explanation
at the point of use.

**Acceptance Scenarios**:

1. **Given** a user sees a domain term or status, **When** its meaning is not
   plain from the label, **Then** concise Thai explanatory text is available
   next to it.
2. **Given** a payroll-related item is final or locked, **When** it is shown,
   **Then** the page clearly distinguishes it from a pending item and explains
   the permitted correction path.

### Edge Cases

- A signed-in account has no linked employee record; pages explain the missing
  setup without showing another employee’s information.
- An account has more than one role; navigation and controls show the union of
  available roles but never bypass record-level scope.
- A session expires while a form is open; the user receives a safe Thai sign-in
  recovery path and the form is not presented as saved.
- A list has no results because of a filter versus because no data exists; the
  page distinguishes the two conditions.
- A service returns a safe public error; the UI preserves its specific Thai
  explanation rather than replacing it with generic technical language.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every current user-facing route, including login, dashboard,
  account, organization, employee and employee-detail pages, attendance,
  leave, overtime, finance, payroll, payslip, report, settings, and denied
  pages, MUST have Thai page purpose and user-facing controls.
- **FR-002**: Each route MUST offer only actions that are meaningful for the
  signed-in role and the displayed record state; the server remains the
  authority for every authorization decision.
- **FR-003**: Employee self-service routes MUST use the signed-in employee
  context and MUST NOT expose general employee search or selection controls.
- **FR-004**: Management pages MAY provide scoped record selection, but MUST
  explain what is being selected in Thai and avoid requiring raw identifiers
  where a recognizable name is available.
- **FR-005**: Forms MUST use visible Thai labels, describe required or
  consequential information before submission, prevent duplicate submissions,
  and place recovery guidance near validation or server feedback.
- **FR-006**: Tables, cards, and lists MUST show readable Thai status labels;
  status meaning MUST not rely on colour, an English code, or a numeric ID
  alone.
- **FR-007**: Every route MUST provide consistent loading, empty, no-result,
  success, warning, denied, and error states when those conditions are
  applicable to the page.
- **FR-008**: The shared navigation and account context MUST help users
  understand where they are, what their role permits, and how to return or
  sign out without entering a URL.
- **FR-009**: Current routes MUST remain usable at 360 and 1280 pixel widths
  with no horizontal page scrolling, visible keyboard focus, and controls that
  can be operated by touch.
- **FR-010**: The interface MUST explain immutable or historical payroll,
  attendance, leave, overtime, and debt data without offering an edit action
  that cannot succeed.
- **FR-011**: This work MUST preserve existing business rules, server-side
  authorization, audit history, approved records, locked payroll records, and
  database schema.
- **FR-012**: The completed application MUST have route-by-route Thai UX and
  role-flow verification covering the five fixed roles and representative
  loading, empty, error, and responsive states.

### Key Entities

- **User role and scope**: The permitted work context for Employee,
  Supervisor, Branch Manager, HR, and Owner.
- **Page state**: A page’s loading, empty, no-result, success, warning,
  denied, error, pending, or final condition.
- **Operational record**: An attendance, leave, overtime, finance, payroll,
  payslip, report, account, organization, or employee item shown to a user.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of current user-facing routes provide Thai page purpose,
  user-facing labels, and a recoverable loading, empty, denied, or error state
  where relevant.
- **SC-002**: In a route-by-role review, 100% of disallowed actions are absent
  from the interface and 100% of attempted direct server requests remain
  denied.
- **SC-003**: A representative user can identify the primary task and next
  action on every populated page within 10 seconds without using a raw ID.
- **SC-004**: 100% of reviewed pages fit 360 and 1280 pixel widths without
  horizontal page scrolling or obscured keyboard focus.
- **SC-005**: All representative form submissions show a clear Thai result,
  prevent an immediate duplicate submission, and point users to the item that
  needs attention on failure.

## Assumptions

- The current feature set and route access policy define the user-facing scope;
  unimplemented business capabilities are described clearly rather than mocked.
- Existing Thai domain terminology is retained where it is already clear, with
  short contextual help added for terms that low-tech users may not recognize.
- Existing native form controls and dashboard styling remain the visual basis;
  this is a usability refinement, not a new product design language.
- All five existing roles remain the authorization model, and the frontend does
  not become an authorization boundary.
