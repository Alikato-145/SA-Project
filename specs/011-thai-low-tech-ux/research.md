# Research: Thai Low-Tech UX Across the Application

## Decision: Operate as a dense, calm Thai dashboard

**Rationale**: The application is a repeated-work operational tool, not a marketing experience. The existing green palette, bordered sections, and native controls already support a calm and familiar workflow. The UI/UX review recommends a dense dashboard treatment with high-contrast semantic feedback and Thai-readable typography. This satisfies the user’s request without replacing the product identity.

**Alternatives considered**:

- A new visual theme or a card-heavy redesign: rejected because it disrupts established patterns and does not solve role, terminology, or feedback problems.
- Adding a component framework: rejected because the existing stack and native controls cover the required interactions.

## Decision: Make role and record context visible before actions

**Rationale**: Existing server scope checks correctly reject cross-employee requests, but some pages still expose a general employee picker to employees. The client will derive display context from the active session: Employee sees their own record, while management roles see a scoped search. Backend scope checks remain mandatory for every request.

**Alternatives considered**:

- Hide controls only after a rejected request: rejected because it wastes user effort and makes the page appear broken.
- Trust a frontend-only role guard: rejected by the project constitution.

## Decision: Use shared Thai feedback and field guidance

**Rationale**: The audit found mixed English labels, raw status codes, generic errors, and inconsistent loading/empty states. A reusable presentation layer will use a Thai title, short purpose statement, status label, recovery-focused message, and native `role=status`/`role=alert` semantics. Forms keep visible labels and show contextual help before consequential inputs.

**Alternatives considered**:

- A toast-only system: rejected because it is easy to miss and cannot identify the field or action that needs recovery.
- Translating only headings: rejected because it leaves task completion and error recovery unclear.

## Decision: Adapt lists before adding custom table tooling

**Rationale**: Responsive guidance requires no page-level horizontal overflow. Short operational rows can become labelled stacked rows on small screens; genuinely wide tables keep a contained horizontal wrapper with clear headers. This uses existing CSS and semantic HTML, without a table dependency.

**Alternatives considered**:

- Force every column to fit a phone: rejected because it makes payroll and attendance data unreadable.
- Add a data-grid library: rejected because current list size and feature scope do not justify it.

## Decision: Preserve existing API mutation pattern for this refinement

**Rationale**: Existing authenticated API routes already own validation, authorization, transactional workflow behavior, and public errors. Moving mutations to a new interaction mechanism would not improve low-tech usability and risks duplicate behavior. The frontend will instead improve disabled, loading, result, and recovery states around the existing calls.

**Alternatives considered**:

- Replace every operation with a new mutation architecture: rejected as unrelated rework.
