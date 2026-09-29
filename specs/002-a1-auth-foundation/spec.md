# Feature Specification: A1 Authentication Foundation

**Feature Branch**: `002-a1-auth-foundation`

**Created**: 2026-09-22

**Status**: Ready for planning

**Input**: User description: "Implement work package A1 Authentication Foundation from the approved Person A plan. Include login, logout, current actor, account lockout, scoped roles, account administration, owner and HR all-branch management, and an audit observer on every backend action. Do not change the frozen database schema or migrations."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sign in safely and identify the current actor (Priority: P1)

An active account holder signs in with a username and password, remains signed in
for the working session, signs out when finished, and can inspect the safe account,
employee, role, and scope information that the application uses for access decisions.

**Why this priority**: Every protected business flow depends on the system being able
to identify an active actor reliably without exposing credentials or internal account data.

**Independent Test**: Create one active account with a valid role, sign in, request
the current-actor view, access one protected operation, sign out, and confirm that the
same protected operation is no longer available.

**Acceptance Scenarios**:

1. **Given** an active account with valid credentials, **When** the user signs in, **Then** the sign-in succeeds and subsequent protected actions identify that account as the actor.
2. **Given** a signed-in user, **When** the user requests their current account context, **Then** the response contains only safe account, linked-employee, role, scope, and capability information.
3. **Given** a signed-in user, **When** the user signs out, **Then** the application removes its active browser session and subsequent protected actions require sign-in.
4. **Given** an inactive, disabled, or locked account, **When** valid credentials are submitted, **Then** sign-in is denied with a stable public reason and no sensitive internal detail.

---

### User Story 2 - Limit repeated credential guessing (Priority: P1)

The system tracks failed sign-in attempts and temporarily locks an account after five
consecutive failures so that repeated guessing is slowed without requiring manual
intervention for an ordinary temporary lock.

**Why this priority**: Credential protection is part of the minimum safe authentication
boundary and is explicitly shown in the approved sign-in flow.

**Independent Test**: Submit four invalid passwords, verify that the account is not
locked, submit the fifth invalid password, verify a 15-minute lock, and then verify
that a successful sign-in after the lock expires clears the failure state.

**Acceptance Scenarios**:

1. **Given** an active account with fewer than four consecutive failures, **When** another invalid password is submitted, **Then** the failure is recorded without locking the account.
2. **Given** an active account with four consecutive failures, **When** the fifth invalid password is submitted, **Then** the account is locked for 15 minutes.
3. **Given** an account within its lock period, **When** any password is submitted, **Then** sign-in is denied without evaluating or revealing whether the submitted password was correct.
4. **Given** a lock period that has expired, **When** valid credentials are submitted, **Then** sign-in succeeds and the failure count and temporary lock are cleared.

---

### User Story 3 - Enforce role scope on every protected action (Priority: P1)

Each protected action checks the actor's current role grants and concrete scope so an
employee is limited to self, a supervisor to one department, a branch manager to one
branch, and HR or Owner to all branches. Owner and HR can manage all A1-A3 data.

**Why this priority**: Hidden controls are not an authorization boundary; later
attendance, payroll, and employee features rely on the same server-enforced scope.

**Independent Test**: Execute the same protected read and write action as each of the
five roles against own, same-department, same-branch, and other-branch targets and
verify the approved authorization matrix.

**Acceptance Scenarios**:

1. **Given** an employee grant, **When** the account accesses another employee's protected data, **Then** access is denied.
2. **Given** a supervisor grant for a branch and department, **When** the account accesses a target in that department, **Then** permitted basic actions succeed, while another department is denied.
3. **Given** a branch-manager grant, **When** the account accesses a target in that branch, **Then** permitted branch actions succeed, while another branch is denied.
4. **Given** an HR or Owner grant, **When** the account performs an A1-A3 management action in any branch, **Then** the action is permitted subject to the action's business validation.
5. **Given** a role grant that has been revoked or deactivated, **When** the account makes its next request, **Then** the revoked authority is no longer effective.

---

### User Story 4 - Administer accounts and scoped roles (Priority: P2)

An authorized HR or Owner user creates an account, optionally links it to one employee,
issues a one-time temporary password, changes account status, unlocks it, resets its
password, and grants or revokes one of the five fixed roles with a valid scope.

**Why this priority**: The application cannot onboard employees or managers without a
controlled account-administration flow, but authentication and enforcement remain
independently useful before the administration screens are complete.

**Independent Test**: As HR or Owner, create and link an account, grant each valid
scope combination, reject invalid combinations, reset the password, unlock or disable
the account, revoke a grant, and verify that the next protected request reflects the change.

**Acceptance Scenarios**:

1. **Given** an employee without an account, **When** HR or Owner creates and links an account, **Then** the employee has exactly one linked account and receives a temporary password that is shown only once.
2. **Given** a fixed role, **When** HR or Owner submits the scope fields required by that role, **Then** the grant is created and becomes effective on the next request.
3. **Given** a department-scoped role, **When** its department does not belong to its branch, **Then** the grant is rejected.
4. **Given** an account that already links the employee or a username that already exists, **When** another conflicting account is created, **Then** the operation is rejected without altering the existing account.
5. **Given** an account administrator, **When** that user attempts to grant authority broader than their own current authority, **Then** the grant is rejected.
6. **Given** a disabled account, **When** HR or Owner re-enables it, **Then** it may sign in again subject to credential and lockout rules.
7. **Given** an HR account, **When** it attempts to grant or revoke Owner, **Then** the operation is rejected; only Owner can administer Owner grants.
8. **Given** the final active Owner account or grant, **When** an administrator attempts to disable or revoke it, **Then** the operation is rejected so the system retains an administrator.

---

### User Story 5 - Audit every backend action without leaking secrets (Priority: P1)

Every backend use case records an auditable action outcome. Successful mutations
record the actor, action, target, request identifier, and redacted before/after facts
atomically with the business change. Reads and failed actions are also observable,
including authentication failures where no actor is known.

**Why this priority**: Payroll and employee administration require later inspection,
and the owner explicitly requires an observer to be embedded in every action.

**Independent Test**: Exercise every A1 endpoint once successfully and once through
an applicable failure path, then confirm that each invocation has a correlated,
append-only audit record and that no prohibited secret appears in stored audit data.

**Acceptance Scenarios**:

1. **Given** a successful state-changing action, **When** its business transaction commits, **Then** the corresponding redacted domain audit record commits in the same transaction.
2. **Given** a state-changing action whose audit record cannot be stored, **When** the operation is attempted, **Then** the business change is rolled back.
3. **Given** an action that fails validation, authorization, authentication, or persistence, **When** its business transaction rolls back, **Then** the failed outcome is still recorded after rollback with a stable reason and request identifier.
4. **Given** any read or list action, **When** it completes or fails, **Then** the observer records its action code, outcome, actor when known, and redacted target information.
5. **Given** credentials, tokens, password hashes, bank-account secrets, or full personal identifiers in an action, **When** the action is audited, **Then** none of those prohibited values are stored in the audit record.
6. **Given** an audit record, **When** ordinary application flows execute later, **Then** they cannot update or delete that audit fact.
7. **Given** one observed endpoint invocation, **When** its outcome is persisted, **Then** exactly one canonical audit row represents that invocation and observer layers do not duplicate it.

### Edge Cases

- Simultaneous invalid sign-in attempts must not lose increments or permit a sixth attempt before lockout becomes effective.
- A valid session belonging to an account disabled after sign-in must be rejected on the next protected request.
- A valid session must not preserve a role that was revoked after the session began.
- An account may exist without an employee link, but one employee may link to at most one account.
- A user may hold multiple non-conflicting role grants; each request uses the union of currently active grants without widening an individual grant's scope.
- Self and all-scoped roles reject branch and department values; branch scope requires a branch and no department; department scope requires a matching branch and department.
- A temporary lock expiry must not silently change a permanently disabled account back to active.
- An audit failure must not leave a successful business mutation without evidence.
- Failed authentication auditing must not reveal whether a username exists.
- Repeated requests carrying the same client request identifier must still create distinct audit facts while preserving the correlation identifier.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST authenticate active accounts with username and password without exposing whether a submitted username exists on failed authentication.
- **FR-002**: The system MUST maintain a browser sign-in state for no longer than eight hours and MUST remove that state when the user signs out.
- **FR-003**: The system MUST return a safe current-actor view containing only account identity, optional linked-employee summary, active role grants, scopes, and derived capabilities.
- **FR-004**: The system MUST count consecutive failed sign-in attempts atomically and lock the account for 15 minutes on the fifth consecutive failure.
- **FR-005**: The system MUST clear the failed-attempt count and expired temporary lock after a successful sign-in while preserving any permanent disabled state.
- **FR-006**: The system MUST load current account status and role grants for every protected action so status and grant changes apply by the next request.
- **FR-007**: The system MUST enforce self, department, branch, and all scopes on the server for every protected action.
- **FR-008**: The system MUST treat Owner and HR as all-scope administrators for A1-A3 data in every branch.
- **FR-009**: The system MUST limit role types to the five fixed roles Employee, Supervisor, Branch Manager, HR, and Owner; custom role creation is outside this feature.
- **FR-010**: The system MUST validate each role grant's required branch and department combination and reject a department that is outside the selected branch.
- **FR-011**: The system MUST prevent an account administrator from granting authority broader than the administrator's current authority.
- **FR-012**: Authorized HR and Owner users MUST be able to create, link, enable, disable, unlock, and reset passwords for accounts.
- **FR-013**: The system MUST allow at most one account per employee and MUST require unique usernames.
- **FR-014**: A generated temporary password MUST be shown only in the successful creation or reset result and MUST never be retrievable afterward.
- **FR-015**: Passwords, password hashes, session tokens, cookies, authorization values, full bank-account values, bank ciphertext, and full national or passport identifiers MUST NOT appear in responses, logs, errors, or audit payloads.
- **FR-016**: Every backend use case MUST pass through a common action observer that records action code, outcome, request identifier, target, and actor when known.
- **FR-017**: Every successful mutation MUST append a redacted before/after domain audit fact in the same transaction as the business change and MUST roll back if the audit append fails.
- **FR-018**: Every failed action and every read action MUST append a redacted audit outcome even when the main business transaction rolls back or no actor can be identified.
- **FR-019**: Audit records MUST be append-only through ordinary application access.
- **FR-020**: Public errors MUST use stable codes and messages and include a request identifier without exposing internal failures.
- **FR-021**: Sign-in and cookie-authenticated state-changing actions MUST reject untrusted cross-origin requests.
- **FR-022**: Sign-out MUST remove the browser's active authentication state; server-side token revocation and multi-device session management are outside this feature.
- **FR-023**: The feature MUST NOT change the approved database schema or migration history; discovered mismatches are reported to the schema owner.
- **FR-024**: The feature MUST expose independently composable routes or handlers so the shared application composer can register them without moving business logic into the composition file.
- **FR-025**: Each critical lockout, role-scope, privilege-escalation, revocation, secret-redaction, audit atomicity, and unauthorized-access boundary MUST have a runnable automated test.
- **FR-026**: HR MUST NOT grant or revoke the Owner role; only an active Owner may administer Owner grants.
- **FR-027**: The system MUST reject any account-status or role-grant change that would leave no active Owner capable of administration.
- **FR-028**: Exactly one canonical audit outcome MUST represent each observed endpoint invocation; a successful mutation's transactional domain audit is the canonical row and MUST NOT be duplicated by a transport observer.
- **FR-029**: Required observation covers A1 business endpoints and their validation/authentication/authorization failures, but excludes health checks, preflight requests, static files, unknown routes, and the audit insert operation itself.
- **FR-030**: A protected read MUST NOT disclose its result when its required audit outcome cannot be persisted.
- **FR-031**: Controlled setup MUST idempotently provision or validate the five fixed role masters and MUST provide a secure path for provisioning the initial Owner before ordinary administration begins.

### Key Entities

- **User Account**: Login identity with optional employee link, unique username, credential hash, status, failed-attempt state, temporary lock time, and last successful sign-in time.
- **Role**: One of five fixed permission types with its required general scope category.
- **Account Role Grant**: A role assigned to an account with its concrete branch and department scope, grantor, and grant time.
- **Authenticated Actor**: Safe request-time representation of the active account, optional employee identity, current grants, and capabilities.
- **Audit Fact**: Append-only evidence of an action containing actor when known, stable action code, target, redacted old/new facts, outcome reason, occurrence time, and request correlation identifier.
- **Employee**: Optional human-resource identity linked one-to-zero-or-one with a user account; detailed employee management belongs to A3.
- **Branch and Department**: Organization records used to validate and enforce concrete role scopes; their management belongs to A2.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of protected A1 actions reject unauthenticated requests and out-of-scope actors in the automated authorization matrix.
- **SC-002**: The fifth consecutive invalid password attempt results in a 15-minute lock in every boundary and concurrency test run.
- **SC-003**: A role revocation or account disablement is effective by the user's next protected request without requiring the eight-hour sign-in state to expire.
- **SC-004**: HR or Owner can create an account, grant a valid scoped role, sign in as that account, and verify its effective scope in under three minutes during the demo.
- **SC-005**: 100% of registered A1 actions produce an audit outcome for successful and applicable failure paths.
- **SC-006**: Automated secret-scanning assertions find zero credentials, hashes, tokens, cookie values, full personal identifiers, full bank-account values, or bank ciphertext in responses, errors, logs, and audit payloads.
- **SC-007**: A forced audit-write failure leaves zero committed business mutations in every tested state-changing A1 use case.
- **SC-008**: All generated A1 responses and errors contain a request correlation identifier so a demo action can be traced to its audit evidence.
- **SC-009**: The focused A1 automated suite and backend type check complete successfully from a clean supported development environment.

## Assumptions

- PostgreSQL infrastructure, the current Drizzle schema, and the canonical migration are complete and frozen before implementation begins.
- The five role master records are provisioned by controlled setup or seed data outside the role-management user flow.
- HR may administer Employee, Supervisor, Branch Manager, and HR grants but may not grant or revoke Owner; active Owners administer Owner grants.
- The final active Owner account and grant are protected from disablement or revocation.
- Sign-in state is a signed, HTTP-only browser cookie with an eight-hour lifetime; no refresh token or persistent server-side session is included in the demo sprint.
- Sign-out removes the browser cookie but cannot invalidate a copied stateless token before its eight-hour expiry; server-side revocation is a post-demo schema decision.
- Failed actions and reads are audit actions, but UI interactions that do not invoke a backend use case are not separate audit facts.
- Exactly one canonical audit row is stored per observed endpoint invocation; internal audit writes are excluded to prevent recursion.
- Employee attachments, forgot-password email, multi-factor authentication, session-device management, and customizable permissions are outside A1.
- The shared transaction helper, application route composer, and public response envelope are coordinated with Person C; A1 consumes or exports their contracts without taking ownership of shared composition files.
