# Technical plan

1. Create `codex/sprint-readiness` in each submodule at the root-recorded commit.
2. Install locked dependencies; restore the existing frontend development image.
3. Scope Compose networks to each project so isolated validation cannot share DNS
   with normal development. Keep all persistent application data untouched.
4. Reconcile documentation and local development configuration with PostgreSQL.
5. Validate the existing migration on an isolated PostgreSQL 16 database, including
   repeat application, catalog checks, and representative history protections.
6. Run frontend lint/build and development/production-like HTTP smoke checks.
7. Record evidence and Day 1 handoff requirements in the sprint documentation.

Constitution check: preserves history and schema, adds no business behavior,
keeps feature ownership and scoped authorization requirements intact, and uses
existing dependencies and infrastructure.
