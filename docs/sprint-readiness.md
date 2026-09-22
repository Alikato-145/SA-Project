# Sprint readiness

Validated on 2026-09-22 for the [two-week plan](two-week-three-person-plan.md).
The local baseline is ready for A1, B1, and C1. Authentication, attendance,
payroll, and business UI features remain the sprint packages' responsibility.

## Baseline and branches

- Backend base: `f3e5862` (PostgreSQL); frontend base: `d17b768` (standalone image).
- Preparation commits: backend `e9dc03f`, frontend `87d34da`.
- All three repositories use the `codex/sprint-readiness` publication branch.
  The root branch records these exact submodule commits for reproducible checkout.
- Original `develop`/`main` branches remain unchanged. These preparation branches
  still need team review and merging before they become the shared sprint base.
- Publishing preparation does not start A1, B1, or C1; sprint feature work is paused.
- Another auth commit exists on the locally known backend `origin/develop`.
  Person A should review it for A1 reuse; it is outside this tested baseline.

Do not run a blanket submodule update over uncommitted work. To check this preparation branch in a fresh clone:

```bash
git clone --branch codex/sprint-readiness --recurse-submodules \
  https://github.com/Alikato-145/SA-Project.git
```

Existing clean clones can select the published root branch and run
`git submodule update --init --recursive` to use its recorded versions.

## Development setup

Requires Bun 1.3.x and Docker with Compose v2. Initial image/package downloads and
the starter's Google Fonts require network access during builds.

From the repository root:

```bash
test -f .env || cp .env.example .env
test -f backend/.env || cp backend/.env.example backend/.env
docker compose up --build -d --wait
docker compose ps
```

Choose free `HTTP_PORT` and `POSTGRES_PORT` values in root `.env`; match the database
port in `backend/.env` for host Bun commands. This workspace uses **18080** and
**55432** because another application already uses port 80:

- UI: <http://localhost:18080>
- API: <http://localhost:18080/api>
- Gateway liveness: <http://localhost:18080/healthz>
- Host database: `127.0.0.1:55432`, database `haris_payroll`.

The UI is still the starter page. Check Compose health and `/api` as well as
`/healthz`: the latter only proves gateway liveness. Source changes reload in
development containers. `docker compose down` stops this project and preserves data.

Run package commands in their own directories:

```bash
cd backend
bun install --frozen-lockfile
bun run typecheck
bun test
```

```bash
cd frontend
bun install --frozen-lockfile
bun run lint
bun run build
```

Without `TEST_DATABASE_URL`, `bun test` runs five database-independent checks and
skips five database checks. Skips do not prove database readiness. Use a disposable
database for the full suite: fixtures roll back, but identity sequences can advance.
For host backend development, run `bun run db:up`, `bun run db:migrate`, then
`bun run dev`; containers already migrate before startup. Use Docker for same-origin
frontend `/api` routing until C1 configures the shared API client.

## Repeatable isolated validation

The following project has its own ports, network, and volumes. It can run alongside
normal development. Pick other free ports if necessary.

```bash
POSTGRES_PORT=55433 HTTP_PORT=18082 docker compose --env-file .env.example \
  -p haris-payroll-check up --build -d --wait

docker compose --env-file .env.example -p haris-payroll-check exec -T \
  -e TEST_DATABASE_URL=postgresql://postgres:postgres@postgres:5432/haris_payroll \
  backend bun test

docker compose --env-file .env.example -p haris-payroll-check exec -T \
  backend bun run db:migrate

curl --fail http://127.0.0.1:18082/healthz
curl --fail http://127.0.0.1:18082/api
curl --fail --output /dev/null http://127.0.0.1:18082/

# Removes only this disposable test project and its volumes.
docker compose --env-file .env.example -p haris-payroll-check down -v
```

Production-like validation uses `compose.production.yaml`, an explicit `--env-file`,
a separate `-p` project, and a free HTTP port. See the root README for its required
environment fields. Never commit credentials.

## Evidence

| Check | Result on 2026-09-22 |
|---|---|
| Locked package installs, backend typecheck, frontend lint | Passed |
| Drizzle generation | No schema changes or new migration |
| Clean development stack | Four healthy services; `/`, `/api`, `/healthz` passed |
| Development full backend suite | 10 passed, 0 skipped, 0 failed |
| Migration repeat | Passed; catalog retained one migration |
| Production frontend image | Next.js compile, typecheck and static generation passed |
| Production-like stack | Four healthy services; all three HTTP checks passed |
| Production full backend suite | 10 passed, 0 skipped, 0 failed |
| Schema parity | Schema-only dumps matched after removing generated dump guard tokens |
| Database baseline | 36 tables, 22 enums, bigint PKs; required exclusion/history objects checked |
| Behavior checks | Audit update/delete rejected; shared schedule end date rejected; next day allowed |

Host Turbopack encountered a sandbox port-binding restriction; the production
Docker build passed without UI/font changes. This verifies the infrastructure
baseline, not every payroll rule or a production release. Detailed schema/reference
audit work remains tracked in infrastructure spec 001.

## Day 1 handoffs

| Owner | First deliverable | Consumers |
|---|---|---|
| A / A1 | Actor/scope contract, account DTO and initial account provisioning approach | B, C |
| A / A2–A3 | Organization/employee/assignment service signatures and fixtures | B1, C2 |
| B / B1 | Attendance input contract, work date and historical branch snapshot | C2 |
| B / B2–B3 | Approved leave/OT and finance input contracts and fixture cases | C2 |
| C / C1 | API/error conventions, ID representation, transaction interface, route/navigation integration | A, B |

Each package starts with a spec, plan and tasks. Public persistence fields use
`snake_case`, business dates use ISO date strings, and money stays decimal strings.
A/C must agree on safe ID serialization: the current Drizzle bigint number mapping
must never silently accept unsafe integers. Cross-feature access uses services.

Day 5 checks a minimal employee/attendance backend flow; Day 7 integrates B3 finance;
Day 8 checks payroll/payslips; Day 9 checks the full UI flow. Audit writes, scope
enforcement and transaction/history protections remain mandatory in each package.
