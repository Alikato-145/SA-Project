# UC12 advance reasons and required rejection notes — 26 October 2026

Task3 scope: `.superpowers/sdd/2026-10-26-use-case-20-alignment/task-3-brief.md` and the global/UC12 sections of `docs/superpowers/specs/2026-10-26-use-case-20-alignment-design.md`. Implementation and focused verification are complete and frozen for independent review. No commits, push, merge, automation changes, production database access, external email or real payment were performed by this writer. Existing UC07/UC08 behavior was preserved.

## Root cause and minimal change

Advance submissions previously accepted only employee/amount, so there was no persisted request reason. Rejection accepted an optional note and the finance page rejected with `{}`. The database already had `decision_note`; only the request reason needed a new column.

New submission now requires `reason` through the existing route, controller, runtime transaction and service. New rejection requires the existing API field `note` through those same boundaries. Both fields must be strings, contain at least one non-whitespace character after `trim()`, and have at most 1000 input characters. The service trims before persistence and returns the established `VALIDATION_ERROR`/HTTP422 for invalid text. Route schemas additionally reject missing/null/empty/overlong input. This follows the existing loan convention without changing loan policy or introducing shared abstractions/dependencies.

The repository insert contract now requires a reason. The advance response DTO/mapper includes nullable `reason`, and the controller invokes that mapper for both one-record and list responses. Existing public IDs remain decimal strings through the shared response envelope; internal actor/time metadata stays excluded.

The existing finance page has a required reason textarea and a required rejection-note form beside each pending advance. Native `required`/`maxLength=1000` and a small advance-only submit guard reject blank, whitespace-only and overlong text before sending. Requester and finance history display saved reason and decision note after reload. A NULL reason displays **รายการเดิม: ไม่ได้บันทึกเหตุผลที่ขอ**; no historic reason is invented. Existing loan forms and actions remain unchanged. Long text wraps without changing the established page design.

Eligibility, date20/work20/half-base/non-negative net checks, exact money calculations, own/finance authorization, pending-only decisions, payroll-input locks, runtime transactions and successful-change audit plumbing were retained. No reason-edit endpoint was added.

## Schema-owner coordination and historic preservation

Generated files: `backend/drizzle/0006_advance_reason.sql`, `backend/drizzle/meta/0006_snapshot.json`, and an appended idx6 entry in `_journal.json`. SQL is exactly:

```sql
ALTER TABLE "advance_requests" ADD COLUMN "reason" text;
```

There is no default, NOT NULL constraint, UPDATE/backfill, new table, deleted constraint or destructive statement. Nullable storage preserves pre-contract rows; new application writes require reason. Migration SQL SHA256 is `c6c3434b39218d751d62b105641965ce278263f587b0a004ae3c37ea895dc9ce`.

The writer notified root and did not apply the migration. Root independently reviewed SQL, snapshot predecessor/journal and logical-reference parity, captured before fingerprints, approved, and applied only to the existing **haris-payroll-verify** disposable database. Root confirmed 39 tables / 25 enums / 91 FKs, a seven-migration chain, and `reason text` nullable. All 48 existing advance reasons were NULL after apply.

Root's before/after migration fingerprints matched:

| Existing facts | Rows | MD5 of ordered historic values |
|---|---:|---|
| Advances, excluding the newly added reason column | 48 | `30190754f70336a28a96bdf2db486fa3` |
| Locked payroll records | 1015 | `7d82a7ed9c6a00bf2828400311144305` |
| Locked payroll items | 11927 | `82e8e8f3aaf9e83e47a23c602d9a236d` |

Independent final read after all focused tests also found those same 48 pre-migration advances with the same fingerprint and all 48 reasons still NULL. The additive test fixtures are retained only in the disposable database. The explicit synthetic legacy fixture omits reason to represent the old contract; ordinary new-write fixtures/callers now provide actual fixture reasons. No original facts were reset, reseeded, deleted or rewritten. Root owns logical DBML/ORM/design/shared-guide updates and final schema review.

## RED evidence and preserved failures

- Service RED, before production changes: **6 pass / 12 fail**. Missing/null/blank/whitespace/1001-character reason and rejection note were accepted; saved text was not trimmed. The existing six eligibility tests remained green.
- Route/service RED, before production changes: **6 pass / 5 fail**. Missing reason and missing/blank/whitespace rejection notes reached writes; the positive reason round trip was unavailable. Some invalid reason payloads already failed the old additional-properties schema; those passing negative cases were not claimed as newly broken behavior.
- Actual UI RED, before UI changes: **1 fail**, because the required advance-reason field did not exist. Screenshot, error context, trace, HTML report and raw log are preserved under `browser-red-*`.
- First supplemental realDB run: **6 pass / 1 fail**. The test helper's default parameter replaced an explicitly passed undefined reason with a valid fixture reason; the resulting HTTP200 was correct for the sent payload. Corrected the invalid-input test to construct an actually missing `reason` field; no product change resulted. `database-first.log` is retained.
- First full migratedDB run: **597 pass / 0 skip / 1 fail**. The canonical catalog test still expected six migrations while the approved schema had seven. Updated that existing assertion to seven; the failing log remains `backend-full-database-first-catalog-failure.log`.
- An initial sandboxed browser preflight could not reach localhost (`fetch failed`) and executed no scenarios. The authorized same command ran with the necessary local verification access; it did not change the target or its security settings. Tool transcript retains that preflight result.

## Verification and commands

All database/browser jobs were sequential and used **haris-payroll-verify** only: HTTP18083, PostgreSQL55440, Mailpit18025. No migration application preceded root's approval. Local host Bun was1.4.2; verification backend Bun was1.3.11. Existing production login limiter was unchanged and browser logins used the existing shared pacing helper.

| Check | Command/package | Result |
|---|---|---|
| Service + route GREEN | backend: `bun test src/features/advance/advance.test.ts src/features/advance/advance.routes.test.ts` |29 pass /0 fail,73 assertions |
| Focused real app/PostgreSQL | verification backend: `TEST_DATABASE_URL="$DATABASE_URL" RELEASE_DISPOSABLE_DB=1 bun test src/features/advance/advance.integration.test.ts` |7 pass /0 fail,68 assertions |
| Final backend types + entire sequential migratedDB suite | `docker exec haris-payroll-verify-backend-1 sh -ec 'bun run typecheck; export TEST_DATABASE_URL="$DATABASE_URL" RELEASE_DISPOSABLE_DB=1; bun run test:db'` |types exit0;598 pass /0 skip /0 fail,123 files |
| Frontend unit | frontend: `bun test` |55 pass /0 fail,177 assertions,19 files |
| Frontend lint | frontend: `bun run lint` |exit0 |
| Frontend types | frontend: `bun run node_modules/typescript/bin/tsc --noEmit` |exit0, including final browser assertion |
| Frontend production build | frontend: `bun run build` |exit0;22 static pages generated |
| Final changed-browser lint | frontend: `bun run node_modules/eslint/bin/eslint.js e2e/advance-reasons.e2e.ts` |exit0 |
| Whitespace | `git -C backend diff --check`; `git -C frontend diff --check` |exit0 |
| UI mechanical detector | `impeccable detect --json` on finance page |empty findings array |

The existing payroll projection emits a pg parallel-query `DeprecationWarning` during focused realDB approval. It is retained in raw logs, predates this text-field change, and was not suppressed or expanded into an unrelated query refactor.

Main browser invocation from frontend, with application and scripts frozen throughout, `NO_COLOR`/`FORCE_COLOR` cleared, fresh scoped fixtures, workers1/retries0:

```sh
env -u NO_COLOR -u FORCE_COLOR UC12_LEGACY_FIXTURE_FILE=/Users/manus/University/SA-Project/docs/superpowers/reports/18-uc12-advance-reasons-evidence/legacy-fixture.json E2E_BASE_URL=http://localhost:18083 E2E_EVIDENCE_DIR=/Users/manus/University/SA-Project/docs/superpowers/reports/18-uc12-advance-reasons-evidence PLAYWRIGHT_HTML_OUTPUT_DIR=/Users/manus/University/SA-Project/docs/superpowers/reports/18-uc12-advance-reasons-evidence/browser-green-html bun run test:e2e e2e/advance-reasons.e2e.ts e2e/employee-self-service.e2e.ts e2e/loan-requests.e2e.ts --workers=1 --retries=0 --output=/Users/manus/University/SA-Project/docs/superpowers/reports/18-uc12-advance-reasons-evidence/browser-green-artifacts
```

Result: **7 pass /0 fail in1.7m**: new HR reject and OWNER approve (2); existing employee leave/eligible advance/HR decision (1); existing loan pending, HR approval, OWNER rejection and scope denials (4).

One final test-only refinement added explicit rejection-note overlong input after removing native maxlength, asserting zero POSTs. The application did not change. Only `e2e/advance-reasons.e2e.ts` was rerun, same environment/worker/retry/freeze rules, `browser-final-*` output paths: **2 pass /0 fail in37.2s**. The broader seven tests and fullDB suite were not repeated after this assertion-only change. Separate seven-run and final-two-run source manifests prevent claiming the seven-run contained the later assertion.

## Observed browser/database facts

Actual Bangkok business date was **2026-10-26**, with26 attended days and a30000.00 base; no clock bypass. New UC12 requests were100.01. Fresh accounts had only EMPLOYEE grants. Missing/whitespace/1001-character request reasons and rejection notes were denied by service/API; UI rejected missing/whitespace/overlong input without POSTs. A valid reason survived employee reload, finance selection/reload and decision, then employee reload. Direct forged employee and employee decision attempts returned403.

| Browser run | Employee/account | Advance | Observed decision |
|---|---|---|---|
| Main seven, HR |1566 /893 |143 |Rejected by HR account2; trimmed reason and note persisted |
| Main seven, OWNER |1567 /894 |144 |Approved by OWNER account1; reason persisted |
| Existing self-service regression |1568 /895 |145 |Approved by HR account2; own request reason persisted |
| Final two, HR |1569 /896 |146 |Rejected by HR account2; includes explicit note overlong client guard |
| Final two, OWNER |1570 /897 |147 |Approved by OWNER account1 |
| Synthetic legacy fixture |1418 /823 |109 |Reason remains NULL; existing documented rejection note displayed to HR |

Independent read-only PostgreSQL queries confirmed saved values and exactly one request per employee/month. Audit shows successful submit then decision with the correct employee/HR/OWNER actors, preserved old/new reasons, saved rejection note and no successful invalid writes. Final records and raw evidence are in `browser-persistence-final.log`; the earlier main-run check is retained as `browser-persistence-confirmed.log`.

RealDB supplemental tests additionally cover zero request/audit rows on invalid submit; byte-for-byte unchanged request/audit snapshots on invalid reject; pending-only conflict; own-only read/write; a serialized concurrent duplicate with one200/one409 and original reason retained; maximum1000-character reason/note; true NULL legacy reads/decision;19 versus20 worked-day boundary;15000.00 half-base versus15000.01; independently derived payroll projection at exactly0.00 versus-0.01. Existing fullDB suite covers locked inputs/history protections and the broader payroll/loan rules.

Screenshots of HR rejection and NULL legacy history were visually inspected: saved text and status are readable and the established layout remains intact. Passing screenshot files under the evidence root reflect the latest final-two run; logs/manifests retain both runs. This is desktop1280×900 workflow/copy QA, not a new mobile-design certification.

## Evidence, source freeze and handoff

Ignored evidence directory: `docs/superpowers/reports/18-uc12-advance-reasons-evidence/`. Contains RED/failure/GREEN/type/lint/build logs, root schema-owner before/after/migrate evidence, browser reports/screenshots/traces, read-only persistence queries and source manifests. Synthetic credentials may appear in local traces; those artifacts remain ignored/local.

Tested bases: backend `a551e05f1b116180e6579360905e2850f7fd9d16`; frontend `103f0bb85731eae382f7a182582c6d0efdf34080`. `tested-source-browser-seven-sha256.json` records the seven-run, `tested-source-browser-final-two-sha256.json` records the final two-run, and `tested-source-sha256.json` is the final source manifest (20 changed source/schema/test files plus unchanged test dependencies). `source-freeze-confirmed.json` confirms no changed-file hash mismatch and no application/script changes during either invocation.

Changed backend scope: advance DTO/mapper/controller/routes/service/runtime/repository/schema; advance unit/route/realDB tests; migration0006+metadata; B5 new-write fixture/callers; catalog migration-count assertion. Changed frontend scope: finance page; advance browser scenarios; existing self-service reason input/forged request contract; operations-client fixture body. Existing loan implementation and browser scenarios were exercised without edits. Task1 attendance and Task2 leave code were not changed.

**DONE — implementation/focused acceptance frozen, no commits.** Root should dispatch independent spec and code-quality reviews against the exact brief and binding global/UC12 design. No known UC12 implementation defect remains. Existing pg warning and actual eligible-date requirement for the positive integration/browser scenarios are recorded limits. The optional legacy UI block takes the disposable realDB fixture via `UC12_LEGACY_FIXTURE_FILE`; normal full browser runs still execute both fresh positive UC12 scenarios without a legacy fixture or skips.

Root owns logical-reference/shared-guide/ledger updates, independent review and checkpoint, whole20-use-case actor UAT, final broad review and integration. This focused report does not certify the complete20-case catalog, real bank settlement or external email delivery.
