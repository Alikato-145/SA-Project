# Sprint release checklist

Person C coordinates this checklist. Infrastructure evidence is in
[sprint-readiness.md](sprint-readiness.md); feature checks remain pending.

## Baseline verified on 2026-09-22

- [x] PostgreSQL runtime, migration generation without drift, 36 tables/22 enums.
- [x] Clean development and production-like stacks and HTTP smoke checks.
- [x] Backend typecheck/database tests, frontend lint and production image build.
- [x] Schema parity and migration idempotence.
- [x] Commit preparation changes and record exact submodule versions on the publication branch.
- [x] Owner authorized merging the preparation baseline into all three `main` branches (2026-09-22).

## Demo freeze — Day 10

- [ ] Login/logout/current user and scoped role matrix verified.
- [ ] Organization/employee creation and effective-dated employment history work through UI/API.
- [ ] Attendance complete; historical branches and duplicate protection verified.
- [ ] Leave quotas, overlap, 3-vs-4-day approvals and corrected types tested.
- [ ] All OT types require explicit approval and preserve decision history.
- [ ] Advance date/worked-day/cap/net-pay boundaries tested; loan/debt history preserved.
- [ ] Daily payroll, decimal rounding and social-security base tested.
- [ ] Lock rejects missing attendance, pending approvals and negative net pay.
- [ ] Locked snapshots remain immutable; tracked adjustments work.
- [ ] Payslip access is scoped; mock delivery attempts logged individually.
- [ ] Bank-transfer and social-security CSV exports match locked payroll.
- [ ] Repeatable fixtures demonstrate the complete UI/API flow.
- [ ] Final lint, typecheck, tests, build and deployment rehearsal recorded below.

## Final evidence

Record merged submodule commits, commands/results, demo date, known limitations,
and the person accepting the demo. Infrastructure readiness does not check off
unimplemented feature behavior.
