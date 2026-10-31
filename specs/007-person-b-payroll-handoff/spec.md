# Feature Specification: Person B Payroll Handoff

**Feature Branch**: `main`

**Created**: 2026-09-22

**Status**: Draft

**Input**: Complete Person B work package B5 from `docs/two-week-three-person-plan.md` without changing Person C files.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Approved leave updates attendance (Priority: P1)

When a scoped approver confirms leave, its daily attendance effect is applied in the same decision so payroll sees the approved day correctly.

**Why this priority**: A missing or conflicting work-day record can change daily deductions.

**Independent Test**: Approve leave for an absent day and see a leave work-day; a present day blocks approval and rolls back the decision.

**Acceptance Scenarios**:

1. **Given** an absent day, **When** leave is approved, **Then** that day is marked leave with the approved deduction state and original branch retained.
2. **Given** no work-day record, **When** leave is approved, **Then** the historical assignment branch is recorded for that date.
3. **Given** a present or late day, **When** leave approval attempts to replace it, **Then** approval fails without changing attendance or quota.

---

### User Story 2 - Count worked days for advance (Priority: P2)

Finance checks actual accepted worked days in the request month before approving an advance.

**Why this priority**: The 20-day threshold must come from attendance, not a guessed calendar count.

**Independent Test**: Only present and late records are counted in a bounded employee/month range.

**Acceptance Scenarios**:

1. **Given** 19 present/late work days, **When** finance checks eligibility, **Then** approval is denied.
2. **Given** 20 present/late work days, **When** finance checks eligibility, **Then** the worked-day check passes.

---

### User Story 3 - Payroll receives approved inputs (Priority: P3)

Person C can consume clearly defined, scoped B1–B3 readers and know which integration decisions remain.

**Why this priority**: Payroll must exclude pending decisions and avoid double deductions.

**Independent Test**: Inspect each reader contract and run focused checks for approved/due/unsettled status filters.

**Acceptance Scenarios**:

1. **Given** mixed request statuses, **When** payroll reads B inputs, **Then** only approved leave/OT/advances and due loans are returned.
2. **Given** unsettled debt, **When** payroll prepares deduction, **Then** the unresolved append-only settlement conflict is reported before lock.

### Edge Cases

- A historical assignment cannot be found for a leave date.
- A concurrent manual attendance write wins a unique date slot.
- The advance request is made before month end or month changes.
- Payroll retry sees a deducted installment or a reversed debt entry.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Approved leave MUST apply attendance changes within its approval transaction.
- **FR-002**: The attendance effect MUST preserve an existing historical branch or use the branch effective on the leave date.
- **FR-003**: The effect MUST refuse to overwrite present, late, or holiday attendance as ordinary leave approval.
- **FR-004**: Finance MUST be able to count present and late work days in a bounded request-month range.
- **FR-005**: B-owned payroll readers MUST clearly filter unapproved or already-deducted records.
- **FR-006**: Integration requirements that need Person C's files or a schema-owner decision MUST be documented, not silently worked around.

### Key Entities *(include if feature involves data)*

- **Work-day record**: Dated employee attendance with historical branch and deduction flag.
- **Approved leave day**: Dated final leave type and deduction values.
- **Finance input**: Approved advance, due installment, or eligible debt transaction.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Focused tests cover existing absence, no work-day, conflicting presence, and worked-day counting.
- **SC-002**: Backend typecheck and full test suite pass apart from database tests lacking a configured disposable database.
- **SC-003**: Person C has an explicit checklist for route mounts, auth adapters, payroll readers, and debt settlement.

## Assumptions

- Person A supplies historical assignment lookup and actor scope; Person C supplies payroll locks and shared app composition.
- The frozen schema's append-only debt trigger remains unchanged.
