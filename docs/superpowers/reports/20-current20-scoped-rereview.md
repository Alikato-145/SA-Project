# Current20 — sole scoped re-review

## Verdict

**Approved.** All four Important findings from `20-current20-final-review.md` are **ADDRESSED**. No new blocking issue was found in the bounded fixes. **Task 5 SPEC: PASS; QUALITY: Approved** after the three manual corrections. The original broad review and report 21 remain intact as historical findings; this report records their closure.

This is the one scoped re-review after the one combined fix wave, not a second broad review. Scope: the frontend E2E diff from `c46fd51`, the three changed guide areas and related ordering text, the fix report, focused evidence and post-review metadata. No tests, database/browser/render jobs, application changes or subagents were used. Only this report and `.superpowers/sdd/2026-10-26-use-case-20-alignment/final-scoped-review.md` were written.

## Finding closure

| Original finding | Status | Review result |
|---|---|---|
| P2: UC12 E2E fails on actual days 1–19 | **ADDRESSED** | Removed the unconditional date assertion. Invalid-reason UI/API checks execute on both calendar branches. Before day 20, a valid-reason UI submission must return 422/`ADVANCE_INELIGIBLE_DATE`, followed by reload and an empty employee-scoped request list. The branch reports `positiveAdvance:false`; it does not skip or alter server time. Eligible dates retain reason persistence, direct scope denials and HR rejection/OWNER approval journeys. The `finally` still closes the browser context after an early return. |
| P1: Missing required leave attachment workflow | **ADDRESSED** | UC08 now names the specific request's **เอกสารประกอบ → ไฟล์เอกสาร → แนบเอกสาร**, permitted PDF/PNG/JPEG and 5 MB limit, success text and filename persistence after reload. UC09 checks that same request's attachment and supplies missing-document recovery, including a type changed during approval. These labels and ownership match `AttachmentPanel` and the request-specific `/leave-requests/${row.id}/attachments` path. |
| P2: Self grant before employee creation | **ADDRESSED** | Both the recommended startup order and first-demo checklist use an installer-supplied HR/OWNER account, create the employee and assignment in UC04, and only then link the employee account and grant self access in UC03. This agrees with the disabled self-grant form when no employee is linked. |
| P2: Missing wage-deduction checkbox | **ADDRESSED** | UC06 now explicitly names **หักค่าจ้าง**, instructs following approved policy, and distinguishes paid approved leave, unpaid leave types and separately configured unpaid excess. This matches the existing `is_deductible` checkbox; no application policy was changed. |

Task 5's previously checked 20-case coverage remains intact. The author's post-fix document check records exact 20 unique catalog headings and resolved internal anchors. This scoped review inspected the changed instructions against the source; it did not repeat every unrelated manual workflow or broaden the review.

## Evidence and metadata consistency

- Frontend diff from `c46fd51` changes only `e2e/advance-reasons.e2e.ts` (11 insertions, 3 deletions). No runtime, schema or migration delta belongs to this fix.
- Independently compared the current files with the historical full-run manifest: **577 unchanged, exactly one changed E2E**. The actual old/new hashes equal `current20-post-review-test-delta.json` and the acceptance manifest's `postReviewDelta`:
  - Historical full-run test hash: `43cfe35735fd3b6c338a03ad5f190475077df188f558888c93208b5069f1a48b`.
  - Current test hash: `2c3211a8609b42e1ab58263a7d3407a260d69268a4068d5d938beb7dd103dff5`.
- Current guide hash independently matches the delta manifest: `6c8316d208da67da8be532ef6238bacf8a5e07ed386a972346e11f3df1724fc0`.
- Read the retained focused browser log: **2 passed in 40.9 seconds**, one worker/zero retries, run `20261026T122137Z-38962`, actual business date **26 October 2026**. It observes both the HR rejection and OWNER approval persistence journeys with the revised test. This run did not supply the legacy NULL fixture and does not re-establish that historical case.
- Read the backend boundary log: **29 pass, 0 fail**, including the existing injected-date service test that rejects day 19 and permits day 20. That test checks business policy; it is not an early-month browser execution. The actual early-month browser branch has **not** been observed, and the fix report/delta/summary state this explicitly. Static review confirms the branch's real response and zero-write assertions; no server clock bypass or skip was introduced.
- Lint and TypeScript exit 0 are recorded in the fix handoff; retained log files contain no diagnostics. This reviewer did not rerun those commands.
- Reports 19 and 20 preserve the historical **69-case full-suite** result and explicitly distinguish the later test-only delta and two-case focused result. They no longer claim the changed E2E bytes were the ones run in the original full suite. The original frozen source hashes remain unchanged inside that historical evidence.

The pending re-review wording in the delta and delivery metadata was accurate when written; root may now close it by linking this approval. Integration SHAs and remote CI are still pending normal final publication and must be recorded only after observed results. This is not an unresolved code finding.

## Remaining limits

The academic UC08 precondition P3 remains the explicitly accepted non-blocking deferral; the adjacent alternative correctly documents `quota_type=none`. No report regeneration or second broad review is requested. Prior limitations about disposable automated acceptance, external email, bank settlement, human UAT and production deployment remain unchanged. Root can proceed with the already-authorized integration and publication steps.
