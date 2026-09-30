# B5 Validation and Handoff

## Baseline — 2026-09-29

Backend develop began at `34a31ba`, frontend develop at `5e043b2`; both submodule working trees were clean. Root already had untracked PRODUCT.md and this feature specification; those unrelated changes are preserved. No branch switch or root submodule pointer update.

Locked package install succeeded. Initial backend typecheck failed because the newly pulled JWT dependencies were not installed; after locked install, typecheck passed. Baseline database-independent suite: 383 passed, 21 skipped, 0 failed with explicit disposable auth/bank test configuration. Missing local auth/bank env was identified before retry; no real credentials were printed.

Created only `haris-b5-check` PostgreSQL test project at port 55433, separate volume/network; applied existing migrations successfully. Schema/migrations remain frozen.

## Specification analysis

Planning/task consistency review was read-only. All 14 functional requirements and 6 buildable acceptance outcomes have task coverage; 17 tasks, 0 critical/high/medium findings, 0 unmapped tasks. Spec checklist: 16 total, 16 complete, 0 unchecked.

Coverage: FR-001 T006–T016; FR-002/003 T002/T004/T006/T016; FR-004 T004/T005/T008/T011/T014; FR-005 T006/T007; FR-006 T009–T011; FR-007 T009–T011; FR-008 T003/T012/T013; FR-009 T013/T014/T016; FR-010 T012/T015/T016; FR-011 T003/T012/T015/T016; FR-012 T003/T007/T015/T016; FR-013 T004/T007/T010/T013/T016; FR-014 T016/T017. SC-001–006 T016/T017.

## Final results

Completed 2026-09-29: all 17 implementation tasks checked. No schema/migration change, new dependency, commit, push or root submodule pointer update. No extensions.yml exists, so after_plan, after_tasks, after_analyze and after_implement hooks were skipped.

| Check | Observed result |
|---|---|
| Backend `bun run typecheck` | Passed |
| Backend full `bun test`, explicit TEST_DATABASE_URL + B1/B2 fixtures | 403 passed, 18 opt-in skips, 0 failed; 1722 assertions, 89 files |
| PostgreSQL catalog file, DATABASE_INTEGRATION=1 | 7 passed (3 catalog checks + 4 URL checks) |
| Audit integration file, DATABASE_INTEGRATION=1 | 3 passed |
| Shop write integration, A2_DATABASE_INTEGRATION=1 | 3 passed |
| Department repository integration, A2_DATABASE_INTEGRATION=1 | 1 passed |
| Organization history, A2_DATABASE_INTEGRATION=1 | 1 passed |
| Branch write, A2_DATABASE_INTEGRATION=1 | 12 passed (includes 1 DB case) |
| Position read, A2_DATABASE_INTEGRATION=1 | 8 passed (includes 2 DB cases) |
| Position write, A2_DATABASE_INTEGRATION=1 | 12 passed (includes 1 DB case) |
| Department write, A2_DATABASE_INTEGRATION=1 | 12 passed (includes 1 DB case) |
| Payroll real-DB projection/lock regression file | 6 passed; also included in full run |
| Authenticated two-branch operations journey | Passed; also included in full run |
| Frontend `bun test` | 17 passed, 0 failed, 58 assertions |
| Frontend `bun run lint` / `bun run build` | Both passed after final changes |
| Root/backend/frontend diff whitespace and frozen schema check | Passed; no schema or migration diff |

The 18 skips in the broad run are opt-in catalog/A2/audit cases plus two hooks. All 16 actual skipped test cases were subsequently run and passed in their separately configured files; hook entries are not test cases. Separate processes avoid an older test file's global pool shutdown affecting another file.

## Runtime evidence

The journey creates unique disposable accounts and two shops, transfers one employee from branch A to B on day 16, and authenticates actual HTTP handlers using database grants. It checks unsigned/expired sessions, cross-employee and branch denial, unsafe public IDs, invalid calendar dates, forged actor fields and rejected mutation origin. It records all work days with dated branch snapshots; approves three-day leave with quota use and append-only history; denies supervisor four-day approval; approves hourly, rest-day and public-holiday OT; creates a loan, charge/reversal and an eligible advance; rejects pending-input lock; reconciles exact preview amounts; locks, then denies correction/reversal/relock. Pending approvals in another shop do not block this shop. Locked payroll items retain attendance/approved leave source evidence and derive debt settlement.

Payroll DB regressions additionally prove conservative advance projection, missing prior attendance rejection, final completeness checks, rollback when audit fails, successful item-before-record locking, immutable snapshots, second-period exclusion of consumed sources and two-connection serialization. Configured eligibility thresholds, Bangkok clock/date boundaries, department-only attendance visibility and OT revalidation have focused checks.

Browser walkthrough used the isolated database and fixture accounts at localhost:3000: all four operations links were available; historical attendance showed branches A/B; dated schedule and shop holiday loaded; an October successor closed the September row and reloaded both; manual October attendance saved and read back. Leave displayed 3.00/10.00 quota and submitted/approved history; OT displayed all three approved types and history; finance displayed deducted advance, current/future installments and retained reversal history. After UI fixes, approved leave showed `No (approved leave)` and settled debt showed outstanding `0.00`, ledger total `25.00` and locked payroll record/time evidence. The shell displayed the actual account. Role/session rejection was verified through actual API handlers; browser walkthrough concentrated on authorized UI save/read-back.

## Handoff and limits

Changes mount eight protected operations features and four existing screens, introduce historical authorization and service-owned transactional adapters, and repair payroll integration/locking. See [quickstart](quickstart.md) for reproducibility and [schema owner handoff](schema-owner-handoff.md) for the frozen debt metadata mismatch. Settlement is derived from immutable locked payroll items; raw debt history remains unchanged. Other consumers reading raw settlement columns must adopt the same evidence or await a confirmed schema-owner decision.

The advance path in the current-month journey runs only on/after day 26, when its fixture can meet 20 worked days; it ran on September 29. Earlier dates still execute the remaining journey and rely on focused configurable eligibility/cutoff regressions. The journey is date-aware and repeats on unique disposable data. The existing pg8 client emits a deprecation notice for concurrent queued reads within transactions; all correctness checks pass, with no dependency change.

Test fixtures are retained exclusively in the isolated project because their histories are append-only. Temporary account details remain in `/private/tmp/haris-b5-demo.json` for local walkthrough only. Validation servers and the isolated database are stopped after verification; test volume is retained. Normal development data is untouched.
