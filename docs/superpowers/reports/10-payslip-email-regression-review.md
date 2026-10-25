# Task 10 — Payslip/email regression review

## Spec Compliance

- ✅ Spec compliant within the Task 10 gate and the root's explicit route-policy scope extension. The only production change permits existing roles through `/payslips`; it adds no administrative grant, finance change, schema change, provider integration, or payroll mutation (`frontend/lib/auth/route-access.ts:40`).
- ✅ Both actual HR/OWNER form paths, PDF downloads, stable reopen identity/bytes, distinct local delivery attempts, actual Mailpit recipients/attachments, and reloaded terminal history are asserted (`frontend/e2e/payslip-delivery.e2e.ts:68`, `:93`, `:103`, `:110`). Exact actor grants prevent an OWNER/HR grant from masking the scoped cases (`:75`, `:133`).
- ✅ Four linked self-service actors use the visible sidebar, read/download their own slips, see no administrative controls, and receive server-side denials for other-person metadata/PDF/history/send and their own generate/send operations; anonymous PDF access must return 401 (`frontend/e2e/payslip-delivery.e2e.ts:127`, `:137`, `:142`, `:145`, `:150`).
- ✅ Fixture facts are inserted before locking, with exact decimal amounts, earned bases differing from contracted salary, and retained adjustment items. The real salary-payable service produces the comparison projection directly; no summary PDF is used to construct a slip (`backend/src/features/payslip/payslip.test-support.ts:33`, `:46`, `:47`, `:48`, `:57`; `frontend/e2e/payslip-delivery.e2e.ts:42`).
- ✅ No payout is required: browser assertions check unprepared payment rows, and retained verification records four locked records/four slips, zero payments, unchanged financial facts, matching stored/download/inbox hashes, and all four PDFs' amounts (`frontend/e2e/payslip-delivery.e2e.ts:120`; `docs/superpowers/reports/payslip-email-evidence/evidence-verification.json:2`).
- ⚠️ Unchanged backend uniqueness, failure/recovery, and immutable delivery implementations are outside this task diff. Retained focused service results cover stable slip identity, cross-employee denial, append-only attempts, and stale-pending recovery; this review accepts that evidence rather than making a new whole-backend correctness claim (`docs/superpowers/reports/payslip-email-evidence/backend-focused.log:12`). Full actor/use-case UAT and external deliverability are explicitly outside this gate (`docs/superpowers/reports/10-payslip-email-regression.md:56`).

## Strengths

- The production repair addresses the demonstrated shared-policy root cause with one line and has a narrow unit regression that also retains unrelated management-route denials (`frontend/lib/auth/route-access.test.ts:80`; `docs/superpowers/reports/payslip-email-evidence/route-policy-RED.log:9`).
- The regression checks delivered PDF bytes against actual browser downloads, matches a persisted attempt to its Mailpit MessageID, and separately records SMTP acceptance and inbox receipt; successful UI text alone is insufficient to pass (`frontend/e2e/payslip-delivery.e2e.ts:48`, `:93`, `:103`, `:114`).
- The test-only fixture is guarded by an explicit disposable-database opt-in and local endpoint allowlist; its writes occur inside a transaction and precede locking (`backend/src/features/payslip/payslip.test-support.ts:13`, `:16`, `:24`, `:48`). The retained SMTP target is credential-free local Mailpit (`docs/superpowers/reports/payslip-email-evidence/smtp-target.json:2`).

## Issues

### Critical

- None found.

### Important

- None found.

### Minor

- **P3 — conflicting color environment adds warning noise.** `docs/superpowers/reports/payslip-email-evidence/browser-check.log:5` reports `NO_COLOR` ignored because `FORCE_COLOR` is set. This does not affect the two passing browser cases or product behavior, but leaves the harness output noisy. Use one color setting in the final verification harness. This is the already-recorded, deferred harness cleanup; it does not block Task 10.

## Checks and Review Limits

- Reviewed the supplied frozen package, backend base `1cf39ab` / frontend base `8840416` to working tree, and the brief/report. The first combined output truncated the package's beginning, so only that missing section was read again. No git recrawl, source edits, index/HEAD edits, or test reruns were performed.
- Named risk: widening the shared route policy could expose management UI to supervisor/manager. Focused unchanged-page inspection confirms only HR/OWNER select admin mode; every other role loads `mine` (`frontend/app/(dashboard)/payslips/page.tsx:61`, `:63`, `:97`). The real browser negative API checks address privilege escalation at the server boundary (`frontend/e2e/payslip-delivery.e2e.ts:142`). A guessed sidebar-file path did not exist; no conclusion depends on that failed lookup. Actual sidebar navigation is exercised by the new browser case (`:134`).
- Named risk: fixture loading at browser-test discovery could diverge from existing verification conventions. Focused inspection of `frontend/playwright.config.ts:5` and neighboring fixture-backed cases found the same isolated-stack, single-worker, explicit-fixture pattern (`frontend/e2e/payable-reports.e2e.ts:3`; `frontend/e2e/payroll-payment-lifecycle.e2e.ts:3`). The documented fresh-fixture command and explicit override make the focused Task 10 case repeatable; no full-browser-suite claim is accepted (`docs/superpowers/reports/10-payslip-email-regression.md:54`).
- Inspected retained final logs: actual browser **2 passed / 22.0s** (`browser-check.log:10`); frontend **51 pass / 0 fail / 172 assertions** (`frontend-unit.log`, final summary); backend focused **10 pass / 0 fail / 32 assertions** (`backend-focused.log`, final summary). Type/lint logs and the durable report record successful required checks. No backend runtime source changed, so repeating the prior full guarded DB suite was not required by this brief.
- Did not independently rerun SMTP, database, browser, PDF rendering, or hash verification. Retained `evidence-verification.json`, local target metadata, test logs, and the controller's direct visual inspection provide that gate evidence. No external mail, transfer, or production action was performed by this review.

## Assessment

**Spec verdict:** ✅ Compliant.

**Task quality:** Approved.

**Reasoning:** The minimal route fix is consistent with the existing self-read mode and backed by actual navigation plus server denial checks for all four linked actors. The new regression verifies financial identity, PDF identity, attempt persistence, and local mail attachment identity without changing locked payroll or administrative permissions. Only non-blocking harness warning cleanup remains.
