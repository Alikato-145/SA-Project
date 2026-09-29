# Research: C4 Operations Integration and Usability

## Decisions

### Authenticated operations boundary

**Decision**: Create one small application-owned operations integration adapter
that derives a safe feature actor from the existing authenticated session and
asserts scope before existing Person B services perform their work.

**Rationale**: Person B services already contain business rules but accept small
feature actor types and dependency ports. Directly registering their route
factories would leave no concrete production access implementation. One adapter
keeps composition and scope conversion out of controllers and avoids copying
authorization decisions into eight features.

**Alternatives considered**:

- Register routes with permissive no-op access ports — rejected because it
  violates server-enforced authorization.
- Rebuild every Person B feature around the A1 actor type — rejected because it
  expands the change beyond C4 and creates unnecessary merge risk.

### Public operations contract

**Decision**: Wrap released operations routes with the established request ID,
authentication, CSRF-origin, and public error-envelope behavior.

**Rationale**: Existing frontend API helpers already expect the shared envelope;
consistent safe errors are required for actionable feedback and auditability.

**Alternatives considered**:

- Keep raw domain errors and direct JSON responses — rejected because it leaks
  implementation-specific behavior and duplicates frontend error handling.

### Dashboard release and visual direction

**Decision**: Preserve the current dashboard's restrained visual system, use the
shared API client, release role-appropriate navigation, and improve hierarchy
through compact section headers, semantic status badges, grouped filters/actions,
and consistent feedback states.

**Rationale**: This is an operational tool. Familiar controls and state clarity
reduce cognitive load more than a visual redesign.

**Alternatives considered**:

- Introduce a new component library or visual system — rejected because it
  conflicts with the brief and adds no workflow value.
- Keep every operation page unavailable until visual polish is complete —
  rejected because the primary blocker is secure integration, not decoration.

### Live validation

**Decision**: Run package checks locally and document the live role smoke
sequence for a PostgreSQL-enabled environment.

**Rationale**: Current local test runs skip database-bound checks when a test
database is unavailable. The release must distinguish green package checks from
live workflow proof.

**Alternatives considered**:

- Treat skipped database tests as release proof — rejected because constraints,
  transactions, and composed routes require live evidence.
