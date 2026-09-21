# Haris Payroll — Two-Week Plan for Three Developers

เป้าหมายคือ demo ที่เดิน flow ครบภายใน 10 วันทำงาน ไม่ใช่ production-ready release

## กติกากลาง

- PostgreSQL schema และ migration ถือว่า freeze ระหว่าง sprint; หากพบ schema mismatch ให้เปิด issue และให้ schema owner แก้คนเดียว
- แต่ละคนเป็นเจ้าของ folder feature ของตัวเองทั้ง backend และ frontend
- `backend/src/app.ts`, frontend layout/navigation และ shared API client ให้ Person C เป็นผู้รวม เพื่อลด merge conflict
- ทุก work package ต้องมีอย่างน้อยหนึ่ง runnable service/integration test สำหรับ business rule สำคัญ
- ใช้ CSV, local attachment storage, manual attendance และ mock email adapter ก่อน

## Person A — Identity, organization, and employees

### A1: Authentication foundation — Day 1–2

- Typed errors, error boundary, password/session handling, authenticated actor
- Role scope: self, department, branch, all
- Login, logout, `/me`, account lockout, role assignment
- Files: `backend/src/core/{errors,auth}/`, `backend/src/features/{user-account,role}/`

### A2: Organization — Day 3

- CRUD shops, branches, departments, positions
- Unique codes, inactive records, scoped authorization
- Files: `backend/src/features/{shop,branch,department,position}/`

### A3: Employees and employment history — Day 4–6

- Employee CRUD
- Assignment/transfer/promotion/salary history using effective dates
- Bank accounts and weekly holidays
- Files: `backend/src/features/{employee,employment-assignment,employee-bank-account,employee-weekly-holiday}/`

### A4: Identity/HR frontend — Day 7–8

- Login, organization screens, employee list/detail/form/history
- Files: `frontend/app/login/`, `frontend/app/(dashboard)/{organization,employees}/`

### A5: Integration support — Day 9–10

- Authorization matrix checks
- Fix employee/payroll integration issues
- Help Person C complete demo flow

## Person B — Attendance, approvals, and employee finance

### B1: Schedules and attendance — Day 1–3

- Branch schedules, overrides, holidays
- Manual work-day records with historical branch snapshot
- Files: `backend/src/features/{branch-schedule,holiday-calendar,attendance}/`

### B2: Leave and overtime — Day 4–5

- Leave request, quota, overlap, 3-day supervisor rule, approval history
- OT request and explicit approval for all three OT types
- Files: `backend/src/features/{leave,overtime}/`

### B3: Advances, loans, and debt — Day 6–7

- Advance eligibility and approval
- Loan installments
- Append-only debt transactions
- Files: `backend/src/features/{advance,loan,debt}/`

### B4: Operations/finance frontend — Day 8–9

- Attendance, leave, OT, advance, loan, and debt screens
- Files: `frontend/app/(dashboard)/{attendance,leave,overtime,finance}/`

### B5: Integration support — Day 10

- Verify approved attendance/leave/OT/finance inputs are available to payroll
- Fix integration blockers with Person C

## Person C — Shared frontend, payroll, payslips, and reports

### C1: Shared application shell — Day 1–2

- Transaction helper, shared API contracts, API client
- Dashboard layout/navigation, loading/error/forbidden states
- Compose all exported feature routes in `backend/src/app.ts`
- Files: `backend/src/core/db/transaction.ts`, `backend/src/shared/http/`, `frontend/lib/api/`, `frontend/app/(dashboard)/`, `backend/src/app.ts`

### C2: Payroll — Day 3–6

- Payroll configuration and periods
- Decimal-safe daily calculation, deductions, approved leave/OT, finance inputs
- Preview, lock preconditions, immutable snapshot, adjustments
- Files: `backend/src/features/payroll/`, `frontend/app/(dashboard)/payroll/`

### C3: Payslips and exports — Day 7–8

- Payslip generation and own-payslip authorization
- Mock email delivery log
- Bank-transfer and social-security CSV exports
- Files: `backend/src/features/{payslip,reports}/`, `frontend/app/(dashboard)/{payslips,reports}/`

### C4: Final integration — Day 9–10

- Merge route registrations and navigation
- Run the complete employee-to-payslip demo
- Production build and deployment rehearsal
- Record results in `docs/release-checklist.md`

## Daily synchronization

```text
09:00  Pull/rebase own branch and announce today's package
13:00  Share API contract changes; no surprise route/DTO changes afterward
17:00  Push branch, post tests run and blockers
Day 5  Integration checkpoint: auth → employee → attendance
Day 8  Integration checkpoint: attendance → payroll → payslip
Day 10 Demo freeze; bug fixes only
```

## SpecKit workflow for each work package

Run these as prompts inside Codex from the repository root. Create one spec per
work package (`A1`, `A2`, `B1`, etc.), not one spec per source file.

### 1. Create the specification

```text
$speckit-specify

Implement work package A1 Authentication Foundation from
docs/two-week-three-person-plan.md. Follow AGENTS.md and the PostgreSQL domain
model. Implement only A1 scope. Do not modify database schema or migrations.
```

Replace `A1` with the package being claimed.

### 2. Clarify only when a business decision is missing

```text
$speckit-clarify
```

Skip this when the spec has no unresolved business choice.

### 3. Generate the technical plan

```text
$speckit-plan
```

### 4. Generate executable tasks

```text
$speckit-tasks
```

### 5. Check for conflicts before implementation

```text
$speckit-analyze
```

Use this for payroll, leave, authorization, or packages touching shared files.
For simple CRUD packages, skip it if the plan/tasks are already clear.

### 6. Implement and validate

```text
$speckit-implement
```

### 7. Run package checks

Backend:

```bash
cd backend
bun run typecheck
bun test
```

Frontend:

```bash
cd frontend
bun run lint
bun run build
```

Full stack:

```bash
docker compose up --build -d
docker compose ps
curl --fail http://127.0.0.1/healthz
```

## Git workflow

Because `backend/` and `frontend/` are submodules, create and commit branches in
the submodule actually changed.

```bash
git pull --recurse-submodules
git submodule update --init --recursive
```

Backend example:

```bash
cd backend
git switch main
git pull
git switch -c feature/a1-auth-foundation
# implement and test
git add src package.json bun.lock
git commit -m "feat(auth): add authentication foundation"
git push -u origin feature/a1-auth-foundation
```

Frontend example:

```bash
cd frontend
git switch main
git pull
git switch -c feature/a4-employee-ui
# implement, lint, and build
git add app components lib
git commit -m "feat(employees): add employee management UI"
git push -u origin feature/a4-employee-ui
```

Do not update root submodule pointers from a feature branch. After backend/frontend
PRs are merged, one coordinator updates both pointers in the root repository and
runs the final Compose validation.

## Definition of done for the sprint

```text
login
→ organization setup
→ employee creation and assignment
→ attendance + leave/OT approval
→ advances/loans/debt
→ payroll preview and lock
→ payslip
→ CSV exports
```

Each arrow must work through the UI and backend. Comprehensive edge-case coverage,
real email, cloud attachments, OCR, biometric integration, advanced dashboards,
and visual polish are deferred.
