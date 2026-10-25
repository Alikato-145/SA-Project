# Full Use Case Handover UAT Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Complete reproducible real-browser evidence for Login and UC1–16 by every actor, then align handover documentation with verified behavior.

**Architecture:** Reuse focused E2E scenarios and synthetic verification fixtures, add only missing actor/action coverage and test-login pacing. Preserve production auth protection. Record each actual UI submission, persisted/reloaded result and direct-API denial; final whole-branch review follows all task gates.

**Tech Stack:** Existing Playwright/Bun disposable verification compose, local Mailpit, Markdown and existing project documentation tooling.

**Spec:** docs/superpowers/specs/2026-10-25-use-case-delivery-design.md

## Global Constraints

- Accounting uses HR grant, no ACCOUNTING role.
- Full UC1–16 and Login, each named actor, UI submission + persisted result + negative authorization checks.
- Manual actual cash/bank/QR transfers only; no bank API integration or external email sends. Mailpit only for email tests.
- Never edit locked payroll values; use a tracked payroll adjustment instead.
- Root retains pre-existing unrelated document edits. Do not reset them or update submodule pointers.
- No real database/payment/external email/push/merge/deploy. No quota-reset claims. Disable heartbeat only after all tasks and final review genuinely complete.

## Review Focus

- An OWNER account must not substitute for HR or scoped manager in actor evidence.
- Rapid full-suite logins hit production nginx10r/m burst20; fix harness pacing, preserve actual401/403/429 expectations and production configuration.
- UI buttons alone are insufficient: confirm backend persisted effect and same state after reload.
- Individual passing reruns must not be described as one clean complete run.
- Documentation must distinguish manual bank payout from app confirmation, prepared from paid, and salary creditor summary from employee debt.

---

### Task 1: Reproducible full actor matrix and handover evidence

**Files:**
- Modify focused frontend/e2e files and narrowly shared test support/global-setup as needed; inspect existing files before adding duplicates.
- Create docs/superpowers/reports/11-full-use-case-uat.md and a readable UC actor evidence matrix.
- Update docs/use-case-delivery-audit-2026-10-25.md with final verified status, preserve baseline history.
- Update approved BP/ERD/manual source documentation within delivery scope; coordinate with existing docs/sa-report dirty files instead of overwriting report work. Any generated report document requires relevant document skill and render QA.

**Coverage contract:**
- Login: EMPLOYEE, SUPERVISOR, BRANCH_MANAGER, HR, OWNER each single-role account actual UI; reload/session/logout/replay, independent session, disabled/locked/no-grant boundaries from AUTH tests.
- UC1 create employee, UC2 edit employee, UC3 deactivate employee: HR/OWNER all branches and manager own branch; manager other branch denied and no role/bank escalation. Preserve employment/history and separate account status.
- UC4 create payroll period, UC5 current adjustment, UC6 close/lock period: HR and OWNER each actual UI, correct pending approval/attendance readiness and immutable locked values.
- UC7 record payout, UC8 select channel, UC9 branch cash group, UC10 branch transfer group, UC11 social-security group: HR and OWNER each UI. Frozen recipient/amount, exclusive groups, no-zero outstanding, independent QR decode and correct manual confirmation/history/totals.
- UC12 generate payslip, UC13 email payslip, UC14 salary/creditor PDFs: HR and OWNER each UI, correct downloads and local SMTP evidence; individual amounts reconcile locked data.
- UC15 submit leave and UC16 submit loan/advance: EMPLOYEE own UI, valid eligibility/approval/loan installment path, other-person denial. Supervisor/manager approval boundaries remain tested where workflows require them, including leave3vs4days.
- Additional self-read payslip/PDF own-only and department/branch scope regressions remain required even if omitted from displayed use-case diagram.

- [x] Reconcile task reports02–10 and actual E2E tests into matrix with actor, UI action, persistence assertion, denial case, evidence path and result. Mark untested rows honestly; do not infer coverage from API tests or other actors.
- [x] Add failing harness regression for genuine Login throttling handling without changing production limiter. Implement shared successful-login setup pacing or response-aware bounded retry only for429; preserve negative Login tests and auth error expectations. Keep workers1 and use safe timeouts. Do not hide failures by broad retrying assertions.
- [x] Add only missing UI actor scenarios/fixtures from matrix. Keep synthetic data unique and full-suite order-independent; no external sends. For any concrete app bug, RED→minimal owning-layer fix→GREEN with fresh task-scoped review before whole-suite continuation.
- [x] Run backend typecheck and full migrated disposable DB suite sequentially, then frontend unit/lint/types/build as applicable. Run one entire browser suite with paced setup. Save exact total passed/failed/skipped and log paths. If failures need repair, rerun affected cases then the full suite after fix; never combine partial runs into a fictitious single-green result.
- [x] Check all downloadable PDFs with relevant visual workflow and representative long/branch-filtered pages; bank/SS CSV values and frozen destinations; real QR image decode; Mailpit attachment bytes; reload/persistence and negative direct URLs.
- [x] Update BP explanation as numbered natural-language steps grouped by roles, no coded process IDs. State web vs manual operations within each step, no separate heading. Include employee leave/loan/advance, manual external payout then app confirmation, proper payroll payable summary. ERD display may focus use-case tables, full logical/executable references must remain consistent.
- [x] Write final UAT report with limitations, synthetic test setup, actor credentials only public fixture values, evidence paths and unresolved findings. Fresh spec+quality review of Task11; then final whole-branch review following superpowers final-review instructions with only one bounded fix wave. No unfinished Critical/Important issues silently dropped.
- [x] After all review gates and checks pass, record local commits and final matrix, mark ledger tasks complete and disable existing automation haris-payroll-30 with automation tool. Do not push/merge/deploy. Deliver concise Thai completion report with report links and remaining real-world manual limits.

Completion26October2026: final49/0fail0skip run20261025T131201Z-66768,backend540/frontend54/build, finalreview12 scopedPASS all5findingsclosed. ExistingheartbeatPAUSED. Later explicit userauthorization supersedes original no-push/no-merge constraint: publish and integrate into develop, without productiondeployment.
