# Research: B5 Integration

## Runtime and transport
Decision: Mount all eight B feature plugins under `/api/v1`, use the existing request authenticator, origin validation, request IDs and public error boundary. Controllers return envelopes and mappers produce snake_case/string-ID DTOs.
Rationale: Existing B plugins are unmounted and rely on injected fake-tested ports; the shared actor uses trusted string IDs and associated scoped grants.
Alternatives considered: Permissive adapters, raw/camelCase responses or a parallel auth layer would leave scope and client handling inconsistent.

## Authorization and effective context
Decision: Resolve dated employment through employee/assignment services. Match permission and scope from the same grant for each target. Leave approval authority is derived from that matching grant, never an unrelated widest grant. Shop-wide holidays require global HR/owner authority; branch managers manage their branch schedules.
Rationale: Multi-grant actors and transfers make current-assignment and widest-scope shortcuts unsafe.
Alternatives considered: UI-only authorization and client-provided roles are rejected.

## Transactions, history and lock races
Decision: Use transaction-scoped repositories and service-owned orchestration; expose payroll mutation guards as a service and serialize final payroll projection with operational mutations. Audits write alongside mutations. Schedule changes close the prior effective row and insert a successor.
Rationale: Separate guard/write operations and final source row locks alone do not prevent phantom input inserts or partial audits.
Alternatives considered: Nontransactional guards or in-memory locks do not work across processes.

## Payroll and finance
Decision: Exclude reversed originals from debt inputs; constrain assignments/pending approval checks to period shop; approved leave creates no absence/lateness deduction. Reuse payroll calculation for advance projected net and subtract the candidate once. Configure advance eligibility at application configuration level with current 20/20/half defaults, without adding frozen schema keys.
Rationale: Direct inspection identified reversed debt and cross-shop input defects; existing approval uses nontransactional projection and hardcoded thresholds.
Alternatives considered: A second payroll calculator and schema migrations add drift or breach sprint freeze.

## Frontend
Decision: Typed operations client uses shared apiRequest; IDs stay strings, money stays strings. Enable current operations navigation, expose existing schedule/override/holiday operations in attendance screen, and distinguish session/forbidden/conflict/loading/empty outcomes.
Rationale: Four pages duplicate raw fetch and shared route access currently marks them unavailable.
Alternatives considered: A new UI framework, library or visual redesign is outside B5.

## Verification
Decision: Reuse focused tests and add transport/scope/race/projection regressions plus disposable two-branch journey.
Rationale: Most B services currently test fake ports; neither production adapters nor the full employee-to-payroll handoff are demonstrated.
Alternatives considered: Treating schema-only or skipped database checks as integration proof is insufficient.

All technical unknowns resolved through local code research. Research was delegated independently for operations, payroll, and frontend.

## Frozen debt settlement mismatch
Decision: Derive settlement from immutable locked payroll source items, preserving debt rows.
Rationale: Real validation showed the frozen append-only trigger rejects settlement metadata UPDATE; source evidence already exists and supports exact-once exclusion and reversal guards.
Alternatives considered: Changing the trigger/migration is frozen and requires schema owner coordination. See [schema-owner handoff](schema-owner-handoff.md).
