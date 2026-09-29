# Research: A2 Organization Management

## Decision 1: Parent identity is immutable

**Decision**: Create commands include the parent ID; update commands cannot change it.

**Rationale**: Re-parenting silently changes historical organization meaning. A genuine identity change uses a new record and deactivates the old one.

**Alternatives considered**: Direct FK update; effective-dated organization masters requiring unapproved schema changes.

## Decision 2: Deactivation does not cascade

**Decision**: Deactivating a parent changes only that row. A child is usable for new work only when it and its full parent chain are active.

**Rationale**: Existing children and historical references must remain factual and inspectable.

**Alternatives considered**: Cascade deactivation; reject deactivation while children exist; hard delete.

## Decision 3: Scoped reads fail closed

**Decision**: All grants see all data; branch grants see their branch, its departments, parent shop, and shop positions; department grants see their department plus parent branch/shop and shop positions. Self grants alone see no A2 list data until A3 supplies explicit dated assignment context.

**Rationale**: A1 self grants do not contain organization IDs, so widening visibility would be unsafe.

**Alternatives considered**: Public active catalog; reading assignments before A3 exists.

## Decision 4: Database uniqueness is authoritative

**Decision**: Services may pre-check duplicates, but repositories translate PostgreSQL unique-constraint failures to one duplicate signal exposed as `DUPLICATE_CODE`.

**Rationale**: Pre-checks alone race under simultaneous requests.

**Alternatives considered**: Pre-check only; exposing constraint names.

## Decision 5: IANA timezone validation

**Decision**: Validate timezones against the runtime IANA database; default to `Asia/Bangkok` only when omitted on create.

**Rationale**: Branch timezone affects attendance day boundaries and must not accept arbitrary strings.

**Alternatives considered**: Fixed enum; unchecked strings; external lookup.

## Decision 6: Audit coverage

**Decision**: Every service method uses A1 `ActionObserver`; successful mutations append allowlisted domain snapshots in the same transaction. Actions use `organization.<resource>.<verb>`.

**Rationale**: This preserves the every-action observer rule and exactly-one canonical outcome.

**Alternatives considered**: Route-only logs; triggers only; post-commit mutation audit.

## Decision 7: No schema/migration expansion

**Decision**: Use the four existing tables and their current unique/FK constraints unchanged.

**Rationale**: The supplied DBML and executable Drizzle schema already represent A2.

**Alternatives considered**: Version columns, soft-delete timestamps, effective ranges.

## Decision 8: Make disclosure and pagination deterministic

**Decision**: Authenticated out-of-scope detail reads return
`RESOURCE_NOT_FOUND`; list queries sort by ascending code then identifier;
`is_active=false` returns inactive-only rows. Search is limited to 150
characters, branch address and deactivation reason to 500 characters.

**Rationale**: This prevents record-existence disclosure, makes pagination
stable under test, and bounds values that participate in filtering or audit.

**Alternatives considered**: Returning `FORBIDDEN_SCOPE` for hidden records,
undefined database ordering, or an ambiguous include-inactive flag.

## Decision 9: Keep create audit targets compatible with A1

**Decision**: A create request begins with the A1 `unknown` record sentinel.
The generated record ID is present in the allowlisted `new_data.id` snapshot
written atomically with the insert.

**Rationale**: A1 establishes action context before persistence generates the
identifier; changing observer identity mid-action would expand shared audit
scope unnecessarily.
