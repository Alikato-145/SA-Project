# B5 Validation

From `backend/`, run `bun run typecheck` and `bun test`. With an explicit disposable migrated `TEST_DATABASE_URL`, rerun the database catalog and feature tests. For end-to-end validation after C integration, approve a leave day, verify its work-day and payroll snapshot; approve OT, advance, and loan; then preview/lock payroll and confirm no pending or reversed entries were used.

Validation on 2026-09-22: `bun run typecheck` passed; `bun test` passed
52 tests and skipped 8 PostgreSQL tests because no disposable
`TEST_DATABASE_URL` was configured. B5's effect and worked-day tests pass.
Frontend lint and TypeScript pass. A webpack production build with a temporary
local font response passed and generated all four B4 routes; the standard
build remains blocked by Turbopack local-port restrictions and the root
layout's external Google font fetch. No A/C shared files were changed.
