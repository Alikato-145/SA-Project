# Sprint readiness

Created: 2026-09-22

Prepare the current workspace to start `docs/two-week-three-person-plan.md`.
Reuse the PostgreSQL backend and frontend baseline commits already recorded by
the root repository. Preserve existing branches, local work, and database volumes.

Acceptance criteria:

- Project guidance consistently identifies PostgreSQL and feature-owned schemas.
- A clean isolated development stack starts, applies the existing migration, and
  serves the frontend, API root, and gateway health endpoint.
- Backend typechecking and database checks pass; frontend lint and build pass.
- A production-like stack uses the same migration and reaches healthy status.
- Developers have explicit Day 1 ownership, dependency handoffs, and reproducible
  setup/check commands. Feature packages remain separate work.

No business endpoints or UI flows are added. Do not change the frozen schema or
migrations; report a discovered domain mismatch for the schema owner. Do not update
root gitlinks or publish changes without authorization.

Publication authorized by the user on 2026-09-22: commit and push preparation
branches for both submodules and record those commits on the root preparation
branch. Sprint feature implementation remains paused.
