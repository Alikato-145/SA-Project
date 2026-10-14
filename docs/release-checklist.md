# Sprint release checklist

Person C coordinates this checklist. Infrastructure evidence is in
[sprint-readiness.md](sprint-readiness.md); latest feature evidence is in [completion-progress.md](completion-progress.md).

## Baseline verified on 2026-09-22

- [x] PostgreSQL runtime, migration generation without drift, 36 tables/22 enums.
- [x] Clean development and production-like stacks and HTTP smoke checks.
- [x] Backend typecheck/database tests, frontend lint and production image build.
- [x] Schema parity and migration idempotence.
- [x] Commit preparation changes and record exact submodule versions on the publication branch.
- [x] Owner authorized merging the preparation baseline into all three `main` branches (2026-09-22).

## Demo freeze — Day 10

- [x] Login/logout/current user and scoped role matrix verified.
- [x] Organization/employee creation and effective-dated employment history work through UI/API.
- [x] Attendance complete; historical branches and duplicate protection verified.
- [x] Leave quotas, overlap, 3-vs-4-day approvals and corrected types tested.
- [x] All OT types require explicit approval and preserve decision history.
- [x] Advance date/worked-day/cap/net-pay boundaries tested; loan/debt history preserved.
- [x] Daily payroll, decimal rounding and social-security base tested.
- [x] Lock rejects missing attendance, pending approvals and negative net pay.
- [x] Locked snapshots remain immutable; tracked adjustments work.
- [x] Payslip access is scoped; mock delivery attempts logged individually.
- [x] Bank-transfer and social-security CSV exports match locked payroll.
- [x] Repeatable fixtures demonstrate the complete UI/API flow.
- [x] Final lint, typecheck, tests, build and local deployment rehearsal recorded below.

## Final evidence

Record merged submodule commits, commands/results, demo date, known limitations,
and the person accepting the demo. Infrastructure readiness does not check off
unimplemented feature behavior.

Latest publication evidence: [release-verification-2026-10-14.md](release-verification-2026-10-14.md). Human acceptance and production provider configuration remain separate gates.

Corrected application source passed [Linux CI run 38577475119](https://github.com/Alikato-145/SA-Project/actions/runs/38577475119): full root verification, WebKit role recovery and both production image builds. This does not sign off real hosting or the unresolved vendor image findings.
