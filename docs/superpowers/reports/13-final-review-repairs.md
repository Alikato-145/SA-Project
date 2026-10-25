# Final-review repairs — I1–I3 and M1–M2

วันที่ 25 October 2026. Repair wave เดียวหลัง report12; bases backend `dc936bd3f5a93b10f2665be6ac32d51a1004135a`, frontend `b85658846924c6d3699695d44ff945f623fba524`. ไม่มี schema/migration/dependency change และไม่มี commit/push/merge/automation mutation โดย implementer. Root เป็นผู้ทำ scoped re-review และ integration ต่อไป; รายงานนี้ไม่แทน final acceptance.

## Findings และการแก้

| Finding | Root cause → minimal repair | Regression/evidence |
|---|---|---|
| I1 | `getPaymentDestination` ยอมรับ linked employee identity เพียงอย่างเดียว → ต้องมี matching identity พร้อมอย่างน้อยหนึ่ง grant ที่ผ่าน established `parseActiveGrant`; HR/OWNER admin policy เดิม | Real service + Elysia GET regressions: no grant, inactive role, invalid role/scope shape, final grant removal และ other employee ถูก deny ก่อน recipient repository lookup; linked EMPLOYEE/SUPERVISOR/BRANCH_MANAGER และ HR/OWNER ยังอ่านได้. `auth/me` และ intentional no-grant account-state behavior ไม่เปลี่ยน |
| I2 | Phone-first ternary ซ่อน frozen bank tuple → แสดง frozen bank code/holder/masked last4 และ registered phone แยก label; SS member ระบุ bank/noQR | Actual Chromium UI ทดสอบ transfer และ SS-member dual snapshots หลัง live bank/holder/number/phone เปลี่ยน; confirmation ยังแสดง004/old holder/1234 และ0812345678 ไม่แสดง live values/full bank. Desktop/mobile captures; acknowledgement/reference/history/QR warning เดิมยังอยู่ |
| I3 | E2E hardcoded Mailpit18025 → shared mailbox consumer อ่าน inherited `VERIFY_MAIL_PORT` หรือ default18025 | Focused no-network checks เรียก actual messages/message/attachment methods และตรวจ outgoing URLs ทั้ง18026และ18025; full browser ใช้ default local Mailpit ไม่อ้างว่า full run เปลี่ยน port |
| M1 | Own submission และ approval journey ใช้คนละ request → ขยาย existing self-service test ให้ HR UI approve exact employee-created `leave.id`, employee reload เห็น approved + decision history | API persistence ตรวจ employee/status/final type/history ของ id เดิม; UI แสดง remark; actual current-date advance ยังทดสอบตาม eligibility จริง |
| M2 | Inherited NO_COLOR/FORCE_COLOR ชนกับ Playwright worker color injection → launcher clearsทั้งสอง flags แล้วให้ Playwright จัด worker policy | Real shell stub RED/GREEN และ actual browser log ตรวจไม่มี color warning; production auth/rate policy ไม่เปลี่ยน |

ไม่มี I1–I3/M1–M2 ที่ defer. Scope เพิ่มที่ root มอบหมายหลังเริ่ม run: CI upload-artifact ต้องครอบคลุม generated full-UAT evidence path และ root .gitignore ต้องกัน generated `*-evidence/` ออกจาก Git. แก้เฉพาะสอง config lines หลัง browser command จบ; คง WebKit paths/config และไฟล์ local ทั้งหมด. Artifact-path/ignore change ไม่เปลี่ยน app/source/test behavior จึงตรวจ syntax + actual generated path และไม่รัน full suite ซ้ำ.

## TDD และ retained failures

- I1 initial service RED:2pass/1fail; split service+route RED:2pass/2fail (service resolved; GET returned200แทน403). GREEN4pass/0fail,63assertions. Logs `i1-red.log`, `i1-red-boundaries.log`, `i1-green.log`.
- I3 RED1pass/1fail: actual three consumer URLs ยังเป็น18025เมื่อ override18026. GREEN2pass/0fail,2assertions. Logs `i3-red.log`, `i3-green.log`. Only request boundary stubbed; no mailbox/network.
- I2 actual UI RED run `20261025T115932Z-61994`:1fail missing frozen bank label after live edits. Actual UI GREEN in mixed run `20261025T120048Z-62283`:1pass(I2)/1fail(M1 new selector matched two inputs). Failed screenshots/traces preserved. Corrected M1 selector scope to load form; run `20261025T120157Z-62469`:1pass/0fail. Final suite also covers mobile dual destinations and employee-visible decision remark added before final checks.
- M2 first shell policy unset FORCE_COLOR/set NO_COLOR passed5/38 but actual Playwright RED log still warned because worker injected FORCE_COLOR. Retained as an insufficient initial harness attempt, not a claim warning was solved. Final policy clears both inherited flags: explicit RED0pass/5fail → GREEN5pass/0fail,38assertions. Logs `m2-{red,green}.log`, `m2-playwright-policy-{red,green}.log`.
- Initial I1 test split command used a backend-prefixed path with backend cwd, giving FileNotFoundError before any edit; corrected boundary run follows. Initial service RED retained. No production fix before observed RED.

## Verification

**Fresh resumed full run `20261025T131201Z-66768`: EXIT0;49expected/0unexpected/0flaky/0skipped, errors=[]; actualWorkers=1, retries=0,596923.037ms (9.9min).** HTML structured report และ browser.log ตรงกัน; color-warning count0. Positive advance ใช้วันที่ Bangkok2026-10-25,25worked days,base30000,amount100.01; employee1198/leave255/advance82. HR/OWNER แต่ละคน SMTP accepted + local inbox received และ attachment/download SHA256 ตรงกัน (slip period572,earnings19100.65/deductions950/net18150.65). Payment lifecycle ยังคง175.03total/150.03paid/25outstanding และ cancelled history; QR decoded amount123.45 และ9999999999.99.

| Check | Result | Retained path under `docs/superpowers/reports/final-wave-evidence/` |
|---|---|---|
| Backend typecheck + full guarded migrated disposable suite | exit0;540pass/0skip/0fail,119files | `backend-full.log` |
| Frontend unit | exit0;54pass/0fail,19files,175assertions | `frontend-unit.log` |
| Frontend lint/types/build | each exit0; successful Next.js production build | `frontend-lint.log`, `frontend-types.log`, `frontend-build.log` |
| Shell syntax + submodule diff checks | exit0 | commands in `commands.md` |
| Scoped UI mechanical detector | exit0,[] | `ui-detector.json` |
| SMTP read-only config check | local mailpit:1025;secure=false;credentialsUnset=true | `smtp-target.json` |
| Final fresh full browser | exit0;49pass/0fail/0skip/0flaky;9.9min;no color warning | `resumed-full-browser-launch.log`; run-specific `browser.log`, `full-browser-summary.json` |
| Workflow YAML/artifact path + generated evidence ignore | YAML parsed;original4paths+new generated path exact;actual files covered;git check-ignore exit0;files preserved | `integration-artifact-proof.json`, `workflow-yaml-check.log` |

Exact commands/cwds/results are retained in `commands.md`; no selective-rollup full49 claim. Backend/frontend checks precede final browser and source stayed unchanged. Explicit user pause interrupted prior full invocation `20261025T120339Z-62697` at27 completed scenarios (SIGTERM/exit143): **NOT full-suite PASS**. On explicit resume, inspected no orphan wrapper/Playwright jobs and569paths unchanged; reused passing540/54/build checks and created fresh fixtures for the new unfiltered run. Partial logs preserved in original run directory, `full-browser-launch.log`, `interrupted-run.json`.

All application tests target disposable `haris-payroll-verify` (web18083/PG55440/Mailpit18025). No simultaneous DB-mutating/browser suites; no production DB, external mail or actual payment. Wrapper/source/config were frozen during each browser command. Fresh run is one unfiltered invocation, workers1/retries0. Raw traces/screenshots/fixtures/hash manifests remain local or CI artifacts, excluded from Git by the narrow generated-evidence rule; compact top-level reports remain versionable.

## Evidence และ freeze

- Final browser log/HTML/structured summary: `docs/superpowers/reports/full-uat-evidence/20261025T131201Z-66768/browser.log`, `playwright-report/index.html`, `full-browser-summary.json`.
- Actual confirmation screenshots (all4 visually inspected; readable, no clipping): `docs/superpowers/reports/full-uat-evidence/20261025T131201Z-66768/dual-destination-member.png`, `dual-destination-transfer.png`, `dual-destination-member-mobile.png`, `dual-destination-transfer-mobile.png`.
- Same employee-created leave after HR approval and employee reload/visible remark: `docs/superpowers/reports/full-uat-evidence/20261025T131201Z-66768/employee-same-leave-approved.png`.
- Fresh local email/download proof: `docs/superpowers/reports/full-uat-evidence/20261025T131201Z-66768/payslips/delivery-proof.json`; HR/OWNER local receipt and equal PDF hashes.
- Durable proof details: `final-wave-evidence/ui-visual-verification.json`, `integration-artifact-proof.json`, `source-freeze-verification.json` (local/CI-artifact paths under this reports directory).


Before hashes for preexisting files derive from root's captured `final-wave-base.json`; new files have `before:null`. `change-hashes.json` records every changed source/test/harness/config before+after SHA256, including separately captured workflow/.gitignore before values. `source-freeze-before-checks.json`, `source-freeze-before-full.json`, `source-freeze-before-resumed-full.json`, `source-freeze-after-full.json` and `source-freeze-verification.json` establish the broad569path capture and unchanged561 application/test/harness paths during the full browser command. The broad manifest has exactly ONE root-owned documentation delta: `docs/superpowers/reports/delivery-decisions-and-limits.md`; root confirmed updating review exclusions and later push/merge authorization during the run. All other568paths match. Exact coordination-only diff is retained in `root-document-coordination.diff`; this is not an application source change. Initial post-run metadata assertion expecting zero broad-manifest deltas stopped before summary extraction; subsequent artifact proof also stopped on that missing derived summary. Corrected metadata checks record the document delta explicitly and extract actual results; see `metadata-validation-note.md`. No browser-suite failure was hidden. Later workflow/.gitignore-only changes are separately identified; no claim those config lines were exercised by the earlier browser command.


### Changed-file SHA256 (exact before → after)

| Path | Before | After |
|---|---|---|
| `backend/src/features/employee/employee.service.ts` | `10010d0de691ac1a42feab36fa338d8c7161d0561a5fdb1675af23197d397f46` | `7102e5a9bf37b43c90fd0491c6401893e97c5d4583f96c710653e54f24cc5881` |
| `backend/src/features/employee/employee.payment-destination.test.ts` | `bae2414cd051b45970700e7e333f06c89ad9886bd4432e4fbb19b0bc46723ea1` | `d6803dd1c96117076e7c8b70e9df0b034d7a6ed79ec728dc27b6d560344449b3` |
| `frontend/components/payroll-payments.tsx` | `a65637402399defec9d2ca2b5189bb5184bc62bff5d00351bfd2f8011581df47` | `00b37df80f8a84f9a0fc4253f981c51114856eb3b2f4872bcd0c38028b085937` |
| `frontend/e2e/employee-self-service.e2e.ts` | `3453969052ca232498b7e4141139cc81058a3797880b80e8114c797724f50b6e` | `0534cab838c3a2e8968d2612b19c0ae0e0309f7a9dcec07c7c1d83e1487ce3ca` |
| `frontend/e2e/payroll-payments.e2e.ts` | `1e0b13b55a52b6434a85944d8ef1eb903b040eedd4fdb7486421ec88c533f91e` | `695d4b92abb8d7947b6ce1e27b0e45ae1186faa9b14ed16655ac99df6591e6a7` |
| `frontend/e2e/payslip-delivery.e2e.ts` | `98812910eae0c49a9d519a9c15920c7428647824919a00974018260787d358a6` | `0581dbce0308cf0cbd5951f2c7e60e36743c9865444a09022074947fc03674ed` |
| `frontend/e2e/mailbox.ts` | `new` | `0b4c91d687aa40b8408601597aa5af89ec0ff9fbd7993bd1f107c03f07aa83ba` |
| `frontend/e2e/mailbox.test.ts` | `new` | `ff4ed0fa4cd14155d4d0b9d9ca2c4222fa789cfea4497d2c26a8128e6b272693` |
| `scripts/full-uat.sh` | `be0a359b601927e84d457d2bff4a6699cb5e4610d494f4588b43a9e916adeb0b` | `0f8bd30db142874440042988410df9abd6c0280e7639273f4c299fdfbea4e2cd` |
| `scripts/full-uat.test.ts` | `cbeb02b15953330a0ebc3dbe78923feaac506f9edac00217e7680c6db0678c1f` | `5704b32a1a9c58f5288ea6faec481d098bb42c42131de30e281dc18922f84c99` |
| `.github/workflows/verify.yaml` | `5a5b54af704a3f3ce8626f46a5392488f464dd197b820bad421161cc295d0498` | `c2495e2c65be7213b2cf5c163e0fa8d08d6c54b8ea1f1311a1bdd487c7e38c51` |
| `.gitignore` | `f4fb20792829fc2283e81f41faf5cedeceac1ea63e9ca1118d337c415c437606` | `cc706918cc1b60351d59dcd940b9c6e6f4d3499e98c47be4a7683046b5e03843` |

## Limits / handback

I3 override is proven at actual consumer request boundary without network; final full browser uses default18025. CI workflow edit has local YAML/path/ignore verification only; no remote CI run claimed. Existing PDF generation code did not change; fresh browser asserts downloaded documents, frozen data and mail attachment bytes, but this wave does not repeat the prior exhaustive PDF visual audit.

Root's accepted report12 exclusions1–6 remain: real settlement/PromptPay ownership/banking-app limits; external bank/SS certification/legal acceptance; external inbox/provider configuration; production performance/revocation retention/migration rollout/backup; partial payouts/refunds/paid reversals/download revocation; deferred time-clock/OCR. These need separate integration/operational/UAT work and are not claimed tested. Local authorization, frozen confirmation and local Mailpit configuration were repaired inside scope.

Ready for the SAME final reviewer's one scoped re-review; implementer stops editing after this handback. Root owns commits/push/merge develop under the user's later authorization and any automation action; automation remains paused. No whole-project PASS or remote integration success is asserted here.
