# Current20 Use Case Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Match the current20UC report with working role-scoped web journeys, synchronized academic artifacts, real disposable-system evidence and develop integration.
**Architecture:** Minimal vertical extensions in existing attendance/leave/advance services and UI; schema-owner-reviewed nullable reason migration for legacy preservation; synchronize existing20-ID report rather than discard workflows. One writer per task and independent review gates.
**Tech Stack:** Bun/Elysia/Drizzle/PostgreSQL16, Next16/React19, existing Bun/Playwright/Mailpit/report tooling.
**Spec:** docs/superpowers/specs/2026-10-26-use-case-20-alignment-design.md

## Global Constraints

- EMPLOYEE own only, supervisor department, manager branch, HR/OWNER all; no global manage grant relaxation. Accounting HR. Immutable locked facts, append-only history/audit, exact money and effective branch snapshot.
- Current20UC is canonical; retain16→20 mapping. Manual own attendance is requested UC07, no biometric/OCR/new approval subsystem. Quota precheck respects explicitallow_exceed; consumption remains approval-only.
- New advance reason and rejection note required; legacyNULLreason preserved. Root schema-owner coordinates migration0006/logical refs before disposable application; never realDB.
- Real browser UI action+reload+persistence+negative scope per namedactor; no OWNER substitution forHR. Synthetic Mailpit only, no bank API/realcash/productiondeploy.
- Preserve userdirtyacademic material (backup first) and unrelatedfiles; only related finalsource/report artifacts published. No rawtraces/fixtures inGit.
- Authorized push/merge develop after tests/report/reviews; nonforce, testedtreeidentity/remoteSHAs. ExistingautomationPAUSED. Log eachtask honestly, no quota-resetclaims.

## Review Focus

- Employee cannot forge employee/branch, approvedleave or nonmanual source; cannot modify locked/others rows; schedule-derived lateness/deduction still enforced. Test realAPI andUI.
- Quota allaffectedyears/missing/frozen/exhausted and pendingtype/date edit; no quota consumption onsubmit; allowanceexception and approvalrace recheck.
- Advance whitespace/missing/overlong reason/note rejected before writes; valid reason survives reload; legacy NULL not fabricated; migration no historicpayroll mutations.
- New20actor matrix proves HR/OWNER organization/accounts/config/schedules/debt/audit UI, own staff/time and leave/OT decisions; keepfinance limited despite addingattendance route.
- Same20names acrossBP/catalog/diagram/CRUD/sequence/DOCX/model; all current39tables and actualFKcounts, manualpayment flow included. RenderQA not just successfuldocumentbuild.

### Task 1: UC07 employee own manual attendance

Files: owning attendance runtime/service/DTO/controller/routes/repository/tests as necessary; frontend attendance page and route policy, existing sharedemployeecontext; focused E2E + evidence report16.

- [ ] Read nearestAGENTS and relevantNext16docs. Inspect currentstaffattendance UI/API/audit/lockedguards and rolecontext; reproduce employee denied with focusedRED.
- [ ] Permit validselfgrant own manual create/correct with meaningful reason and datedbranchvalidation at backendowninglayer; forbid leave/provenance/otherperson/lockedrows. Reusecurrentstaffworkflow; do not loosen sharedmanage acrossfeatures.
- [ ] Expose employee owncontext UI, hide arbitrarypicker/branchadministration; assert actualsubmit/correct/reload/audit and negative directAPI cases in disposableDB/browser.
- [ ] Run covering tests+types; write reports/16-uc07-self-attendance.md and taskreport with exactRED/GREEN/evidence. Freeze for independent spec+qualityreview before checkpointcommit.

### Task 2: UC08 quota precheck

Files: leave.service.ts/repository contract only if needed, focusedservice/realDBtests and E2E; report17.

- [ ] RED tests for insufficient/missing/frozen/peryear quota during submit/edit with zero persistedrequest/day/action; include nonequota and explicitallowExceed behavior.
- [ ] Implement read/validate under existing employee lock+transaction; do not reserve/consumequota atsubmit; retainapprovalrecheck+consumption and typecorrection rules. Use exactday arithmetic and coherenterrors.
- [ ] RealemployeeUI rejection+validsubmission/reload plus unchangedapprovalboundary; test crossyear/editrollback and concurrentappropriateguards.
- [ ] Focusedchecks/types/report17-uc08-quota-precheck.md, freeze/taskreview/checkpoint.

### Task 3: UC12 advance reason and rejection note

Files: advance schema/DTO/service/runtime/repository/controller/routes/UI/tests; migration0006/meta; DBML/ORM/design root refs; report18.

- [ ] RED nonblankbounded reason/note service+API+UI persistence tests. Existing loan behavior preserved.
- [ ] Generate nullablelegacy advance_requests.reason migration only; notifyrootowner. Root reviews SQL/meta/logicalparity and existinghistorypreservation before applyingonlyverifyDB. Do not drop/reseedhistory.
- [ ] Require new reasons and rejectionnotes atservice/requestboundary andform; showlegacylabel forNULL; reason survives employee/HRreload; rejectedadvance has saveddecisionnote. Update existingfixtures/callers/tests to realrequiredcontract, not fabricatehistoricdata.
- [ ] Realbrowser employee request→HR/OWNERdecision with eligibleactualdate and directdenials; rollback/duplicate/money/thresholdguards. Focusedchecks/types/report18-uc12-advance-reasons.md, freeze/taskreview/checkpoint.

### Task 4: Canonical20 documentation and fullactor UAT

Files: currentdocs/sa-report README/catalog/CRUD/query/ERD/sequence/collaboration/generator/DOCX/PDF onlyasneeded; userbackupsource preserved; newcanonical20actor matrix/crosswalk; focusedmissingE2E; report19.

- [ ] Reconcile all20goal/actor/action/alternative withactualcode; UC04managerownbranchsubset, UC08allowExceedexception, UC12newreasons, UC17generation-vsownread, UC18paymentlifecycle+reports, UC19scopedread-vsfinancialexports. Retain20IDs, no arbitraryrenumbering.
- [ ] Add actualactorUI gaps in tests: HRandOWNER administration (org/accounts/config/leaveadmin/schedules/debt/audit), employeemanualtime/leave/OT/finance, supervisor/managerworkscope+approvals, payroll/reports/payslips/payment, allroleworkspace. Seedfreshguardedfixtures beforemoduleload; paceauth; retainnegativechecks.
- [ ] Update fullschema/model to39tables/currentactualFKenumcounts and advance reason, CRUD/query references; regenerate affecteddiagrams andreportusingdocuments/PDFskills. Renderandinspectpages/tables/figures, no placeholders replacinguserdata. Publishonlyrelatedartifacts, preserveunrelatedPPTX.
- [ ] Runbackendtypes+fullmigrateddisposabletests; frontendunit/lint/types/build; oneentireunfilteredbrowser1worker0retries withallfixturepaths. Freezeapplication/scripts untilcommandexit; preservefailedlogs without selectivepassrollups. VerifylocalSMTPattachments/QR/PDFCSV/own-scope asbefore.
- [ ] Writecanonical20actorcoverage/report19 plusfinalsummaryreport20, independenttaskreview thenwholebranchreview against fixedinitialbases. Oneboundedfinalfixwave/scopedrereview perSDD. Commitreviewedchanges, FFmergedevelop/pushall3repos andverifyremoteSHAs. Reportlimitations/remotestatushonestly. KeepautomationPAUSED.
