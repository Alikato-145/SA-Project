# Current20 — final whole-branch review

## Verdict

**Changes requested — one combined fix wave, followed by one scoped re-review.** No Critical finding and no new application authorization, payroll-history, quota, advance-reason or migration defect was found. One Important test defect and three Important beginner-guide defects remain. The 26 October positive acceptance evidence remains valid; the issue is repeatability outside that date window and completeness of the requested manual.

This is the single broad final review against the fixed initial bases, not `HEAD~1`:

| Repository | Fixed base | Reviewed state |
|---|---|---|
| Root | `0b36631045af2fa6b767865c4e2cfedabc1fa912` | `5ec4c94d8a5f25feb45d3d4a17a708e0e33d7010` plus scoped Task 4/5 documentation, workflow timeout and guide links |
| Backend | `c2a404db6d00df18b0f1a7322e67f15ec9da1d41` | `54f78ea1b3e1e43fe87905f08a89a6db996538a8` |
| Frontend | `e6d6fb65b64096840d563e49df29ece981e355af` | tested source initially at `c066ede0677443fb9c789b3299712f900fa7a763` plus Task 4 E2E, subsequently committed as `c46fd51` with the same source bytes |

Read root/frontend instructions, binding current20 design and plan, cumulative source diffs and relevant surrounding services/controllers/auth/transactions/UI, reports 16–20, Task 1–3 review reports, Task 4 review and Task 5 review. Respected the preserved-academic-baseline boundary and checked the curated publication manifest; unrelated user material is not attributed as newly authored work. This review does not claim a line-by-line reconstruction of the preexisting academic draft. No application edits, database/browser/test/render jobs, commit, push, or delegation were performed. Review mutations are only this report and its SDD copy.

## Critical (must fix)

None.

## Important (fix before integration)

1. **P2 — The new unfiltered UC12 browser tests fail every month on days 1–19.** `frontend/e2e/advance-reasons.e2e.ts:11` unconditionally asserts that the actual Bangkok day is at least 20 before either actor scenario runs. `.github/workflows/verify.yaml` runs `scripts/verify.sh`, whose default path invokes the complete suite through `scripts/full-uat.sh`; there is no eligible-date scheduling restriction. A correct application therefore makes both new cases fail on most calendar days, blocking ordinary CI and future changes. Keep the real clock and business rule: on days 1–19 exercise the UI/API valid-reason submission, assert `ADVANCE_INELIGIBLE_DATE`/422 and no persisted request, and honestly identify that day's negative-date coverage; on eligible dates retain the complete positive reason/rejection/approval persistence journeys. Do not solve this by skipping tests, weakening the application policy or presenting early-date coverage as positive approval acceptance. `employee-self-service.e2e.ts:104` already demonstrates the appropriate real-date branching pattern. Verify the affected positive browser journeys on the actual date and focused branch/assertion logic without changing server time; retain the original full-suite manifest as historical evidence and record changed test hashes separately.

2. **P1 — The beginner guide omits the required leave attachment workflow.** `docs/user-guide/README.md:125` moves directly from submission to pending status; UC09 at line 134 asks the approver to inspect evidence without explaining how it gets attached. A type configured with **ต้องแนบเอกสารก่อนอนุมัติ** cannot complete approval without request evidence (`backend/src/features/leave/leave.service.ts:104`). The implemented request card uses **เอกสารประกอบ → ไฟล์เอกสาร → แนบเอกสาร**, accepts PDF/PNG/JPEG up to 5 MB and displays the saved file (`frontend/components/attachment-panel.tsx:27`). Add a UC08 step to attach to the specific request, reload and verify/download that file, plus UC09 recovery when evidence is missing. An employee's general document tab is a different attachment target. This independently confirms Task 5 review finding 1.

3. **P2 — The first-demo checklist requires a self grant before the employee exists.** `docs/user-guide/README.md:298` instructs linking the employee account and self grant, while line 299 creates that employee. The self-grant form explicitly disables submission without the linked employee (`frontend/features/identity-hr/accounts/account-live.tsx:615`, `:694`). Reorder employee creation before employee-account linking/self grant, or distinguish the initial administrator account from the later employee account. Align the initial recommended order as necessary so a novice can follow it linearly. This independently confirms Task 5 review finding 2.

4. **P2 — UC06 omits the leave wage-deduction control.** `docs/user-guide/README.md:106` lists leave-type inputs and policy switches but omits **หักค่าจ้าง**, which the actual UI exposes (`frontend/components/leave-administration.tsx:59`). A novice following the manual can save the default non-deductible type when their approved policy requires otherwise, changing later payroll treatment. Name the checkbox and explain setting it according to the approved leave policy, keeping ordinary approved paid leave and unpaid excess distinct. This independently confirms Task 5 review finding 3.

## Minor (non-blocking)

- **P3 — Academic UC08 prerequisite overstates quota requirements.** `docs/sa-report/README.md:726` requires employee entitlement for every leave type, while line 731 correctly exempts `quota_type=none`. Retain Task 4 review's non-blocking assessment: clarify this prerequisite when the academic report is next regenerated; no immediate 298-page rebuild is required. Executable behavior and the alternative flow are correct.
- Previously documented color/deprecation warnings do not establish a product defect and do not warrant a refactor or another broad test run.

## Cumulative implementation assessment

- **UC07:** permission fallback is confined to the attendance runtime service, checks a valid active EMPLOYEE/self grant and trusted employee identity, and leaves shared `manage` authorization unchanged. Historical branch, schedule-derived lateness/deduction, protected OLD row provenance/status, meaningful fresh correction reason and locked inputs are checked server-side. The existing serialized transaction and audit persist actor/old/new facts. Staff scope continues through existing authorization.
- **UC08:** both submit and pending edit invoke the per-year quota guard after the existing employee lock and before request/day/action writes. Missing/frozen quota fails even with `allow_exceed`; no-quota types return before quota lookup. Submission does not reserve or consume entitlement; approval still rechecks and consumes atomically. Integer hundredths are safe for the declared nonnegative numeric(8,2) values.
- **UC12:** required trimmed nonblank reason and rejection note are bounded at service, transport and UI boundaries. Response mapping selects public fields and retains existing ID/snake-case conversion. Legacy NULL remains honest. Approval eligibility, money arithmetic and immutable payroll behavior are unchanged.
- **Schema:** independently compared parsed 0005 and 0006 snapshots. Apart from snapshot `id`/`prevId`, the only delta is `public.advance_requests.columns.reason = nullable text`; SQL contains only `ALTER TABLE ... ADD COLUMN reason text`. No other table/index/check/FK delta was found. Schema-owner and pre/post historical-fingerprint evidence is recorded in report 18; this review did not reapply the migration or query a database.
- **Current20 coverage:** refined UC04/17/18/19 scopes preserve staff-only finance and own-only payslips. Payment confirmation remains manual and append-only; QR generation does not claim settlement. Tests use actual named actors and distinguish API fixture setup from UI acceptance. No application source changed in Task 4.

## Evidence and publication checks

Independently read and compared the final browser JSON and manifests rather than assuming the report totals: **69 expected, zero skipped/unexpected/flaky**, duration 1,267,412 ms, run `20261026T052214Z-27083`. All **73 actor/action rows** resolve to exact result titles and cover **20 distinct UC IDs**. All **578 current application/test/script file hashes** match the frozen manifest at review time. DOCX and PDF bytes match their published hashes. Backend 598-pass and frontend 55-pass results, lint/types/build success and independent 12-PDF/4-CSV/2-Mailpit/2-QR checks are supported by retained evidence and the independent Task 4 review; they were not rerun here.

The curated Task 4 manifest has **190 existing paths** and excludes raw fixture/traces/mail/bank-export files. Targeted text scanning of those sources found no credential/JWT/private-key disclosure. This is not a forensic audit of every binary/image pixel. Academic QA records 298 pages reviewed, 284 exact-PNG-hash reused inspections plus 14 direct final inspections and 484 exact page references. This reviewer checked manifest consistency, not all 298 rendered pages anew. User-owned unrelated PPTX/PRODUCT/temporary files remain outside publication.

The workflow timeout increase from 25 to 45 minutes has a concrete local-runtime rationale but is not proof of a hosted CI result. Report 20 correctly leaves integration and remote CI pending. Final report/plan/progress updates, exact commit/remote SHAs and nonforce develop integration remain root-owned completion steps after the bounded fixes. This review does not certify real bank settlement, external SMTP, production deployment, human UAT or another browser engine.

## Bounded follow-up

Combine the one test repair and three manual repairs into one fix wave. Scope the sole re-review to these findings, changed test assertions/evidence, manual/source consistency and publication metadata. The academic P3 is explicitly deferred and is not a blocker. Preserve the original 69-case acceptance and document any post-review test-only delta; do not silently replace the tested-tree evidence. No second broad review is requested.
