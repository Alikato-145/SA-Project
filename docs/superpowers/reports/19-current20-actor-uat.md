# Current canonical20 actor UAT

สถานะ: PASS — final unfiltered browser69/69 และ artifactQA298หน้า; independent Task4 PASS/Approved; final bounded fixes ผ่าน scoped reviewแล้ว

การตรวจนี้ยึด current academic catalog 20 IDs และ binding design วันที่ 26 ตุลาคม 2026 แยกจากผล 13 กรณีของรูปเล่มเดิมและ 49 กรณีของ delivery16 การสร้าง fixture ด้วย API ไม่ถูกนับเป็นการกรอก UI ของ actor

## ขอบเขตและหลักฐาน actor

ทะเบียนละเอียด [current20-actor-matrix.json](../../sa-report/evidence/current20-actor-matrix.json) มี 73 actor/action rows พร้อมชื่อ test แบบเจาะจง action และ negative/boundary; รายการด้านล่างสรุป goal ของแต่ละ ID

| ID | Goal | Named actors | Actual UI evidence |
|---|---|---|---|
| UC01 | เข้าสู่ระบบและจัดการรหัสผ่าน | EMPLOYEE, SUPERVISOR, BRANCH_MANAGER, HR, OWNER | auth-session.e2e.ts, current20-password.e2e.ts |
| UC02 | จัดการโครงสร้างองค์กร | HR, OWNER | current20-administration.e2e.ts |
| UC03 | จัดการบัญชีและสิทธิ์ผู้ใช้ | HR, OWNER | current20-administration.e2e.ts |
| UC04 | จัดการข้อมูลและประวัติพนักงาน | BRANCH_MANAGER, HR, OWNER | employee-management.e2e.ts, current20-administration.e2e.ts |
| UC05 | กำหนดตารางทำงานและวันหยุดสาขา | HR, OWNER, BRANCH_MANAGER | current20-administration.e2e.ts, current20-operations.e2e.ts |
| UC06 | กำหนดนโยบายเงินเดือนและการลา | HR, OWNER | current20-administration.e2e.ts |
| UC07 | บันทึกและแก้ไขข้อมูลลงเวลา | EMPLOYEE, SUPERVISOR, BRANCH_MANAGER, HR, OWNER | attendance-self.e2e.ts, current20-operations.e2e.ts |
| UC08 | ยื่นคำขอลา | EMPLOYEE | leave-quota.e2e.ts |
| UC09 | พิจารณาคำขอลา | SUPERVISOR, BRANCH_MANAGER, HR, OWNER | current20-operations.e2e.ts |
| UC10 | ยื่นและแก้ไขคำขอทำงานล่วงเวลา | EMPLOYEE | current20-operations.e2e.ts |
| UC11 | พิจารณาคำขอทำงานล่วงเวลา | SUPERVISOR, BRANCH_MANAGER, HR, OWNER | current20-operations.e2e.ts |
| UC12 | จัดการคำขอเงินทดรองและเงินกู้ | EMPLOYEE, HR, OWNER | advance-reasons.e2e.ts, loan-requests.e2e.ts |
| UC13 | บันทึกหนี้และรายการปรับปรุงเงินเดือน | HR, OWNER | current20-administration.e2e.ts, current-adjustments.e2e.ts |
| UC14 | เปิดงวดเงินเดือน | HR, OWNER | current-adjustments.e2e.ts |
| UC15 | คำนวณและตรวจสอบเงินเดือน | HR, OWNER | current-adjustments.e2e.ts |
| UC16 | ตรวจความพร้อมและล็อกรอบเงินเดือน | HR, OWNER | current-adjustments.e2e.ts |
| UC17 | ออกและส่งสลิปเงินเดือน | HR, OWNER, EMPLOYEE, SUPERVISOR, BRANCH_MANAGER | payslip-delivery.e2e.ts |
| UC18 | เตรียมและบันทึกการจ่ายเงินเดือน พร้อมรายงานและไฟล์จ่าย | HR, OWNER | payroll-payments.e2e.ts, payroll-payment-lifecycle.e2e.ts, payable-reports.e2e.ts |
| UC19 | ดูภาพรวมและรายงานตามสิทธิ์ | EMPLOYEE, SUPERVISOR, BRANCH_MANAGER, HR, OWNER | current20-administration.e2e.ts |
| UC20 | ตรวจสอบประวัติการดำเนินงาน | HR, OWNER | current20-administration.e2e.ts |

## การเปลี่ยนแปลง

- เพิ่ม current20-administration: HR และ OWNER สร้าง/แก้องค์กร กำหนดบัญชีและ scope สร้างประวัติค่าตอบแทนและวันหยุด เพิ่มบัญชีแบบอ่านกลับ masked ตั้ง schedule/config successor กำหนด leave type/quota สร้าง/กลับรายการหนี้ และค้น audit จากฟอร์มจริง; ทั้ง5บทบาทเปิด workspace ตามสิทธิ์
- เพิ่ม current20-operations: พนักงานส่ง/แก้ OT และส่งลา; SUPERVISOR/BRANCH_MANAGER/HR/OWNER บันทึก/แก้ลงเวลาและอนุมัติลา/OT จาก UI, reload/history และ direct negative checks
- เพิ่ม current20-password: บัญชีใหม่บทบาทเดียวทั้ง5roles เปลี่ยนรหัสใน Settings, wrong-current422, identity/scopeคงเดิม, logout/copied-session401, old-password login401/new-passwordสำเร็จ; ไม่เปลี่ยน password ของ fixture กลาง และไม่เพิ่ม forced session revocation policy
- เพิ่ม actual UI preview capture สำหรับ HR/OWNER ใน current-adjustments เดิม ไม่มี production application change ใน Task4
- Sync catalog/BP/CRUD/sequence/collaboration/model/dictionary/query และเพิ่ม UC18 payment lifecycle ภายใต้20 IDs เดิม พร้อม separate delivery16→current20 crosswalk; academic34→20 เดิมเก็บบริบทไว้

## Verification gates

| Check | Result / evidence |
|---|---|
| Backend typecheck + full migrated disposableDB | 598 pass /0 skip /0 fail,123files; backend-full.log |
| Frontend unit |55 pass /0 fail,177assertions,19files |
| Frontend lint/types/build |exit0; final changed-E2E lint +types exit0 |
| Focused administration |7/7 in20261025T192647Z-99901; extended UC04 finalfocused7/7 in20261026T045043Z-23331 |
| Focused operations |4/4 in20261026T044247Z-21763 |
| Focused password |5/5 in20261026T051925Z-26399; lint/types exit0 |
| Pre-refinement full browser |64/64,19.2m,20261026T045606Z-24372;577sourcefiles unchanged; retained separately before concrete UC01 gap was closed |
| Independent exports/QR/localMailpit |PASS12PDF/4CSV/2attachments/2QRpayloads; independent-output-checks.json |
| Model catalog |39 tables /91FK /25enums /7migrations; all Drizzle column names/nullability matched actualcatalog; Q020–24 executed read-only |
| Structural report |20IDs/73actorrows/158image references/23sequence+collaboration/24query mappings;39dictionaries;26current model/class/DFDfigures |
| Final unfiltered browser |PASS69/69,21.1m,0skip/0fail/0flaky;20261026T052214Z-27083,workers1/retries0; exact73matrixrows matched finalJSON |
| Source freeze |578application/test/script files; tested-source-final-before.json = tested-source-final-after.json, all unchanged after exit0 |
| DOCX/PDF finalQA |PASS298pages,484exact cached references; zero missing/mismatched; bank row visible page274 |

Raw logs, fixture files, traces, HTML and JSON are retained under ignored 19-current20-actor-uat-evidence and full-uat-evidence. They are not publishable artifacts.

## Failed runs and corrections

- 20261025T192843Z-345:4operations failures, OVERTIME_CONTEXT_INVALID because test fixture scheduled creation after the employee OT submission. The service correctly rejected missing context; reordered fixture/UI actions.
- 20261025T193015Z-617:4operations failures. Scoped employee search correctly excluded future employment, and HR/OWNER leave pages had a second quota picker. Corrected fixture hire/assignment date to2026 and scoped locator to the workspace filter/list ID; no authorization relaxation.
- Final-output checker first hit sandbox denial on localhost Mailpit; the retained denial log is independent-output-checks-sandbox-denial.log. Authorized read-only escalation succeeded; no messages were sent. A temporary read-only page-reference helper first used an undefined XML namespace; corrected iteration then verified484cached references.
- First283-page bundled LibreOffice PDF rendered Thai body/cell text blank. A one-page diagnostic reproduced the missing-font discovery; task-local FONTCONFIG_FILE +SAL_FONTPATH restored Thai. Bad render and diagnostics retained, never counted as QA passing. Font-correct render291pages is an intermediate; final298-page QA passed.
- An initial artifact marker command used unsupported combinedformat and exited2 before authoring; one successful edit/docx marker preceded first document authoring. One document-edit command ran from frontend directory and failed path lookup before mutation, then corrected from root.

## Final command and environment

Only haris-payroll-verify (HTTP18083, PostgreSQL55440, Mailpit18025). Actual Asia/Bangkok date26October2026 allows the positive advance path without changing the clock. Fresh scope/payment/lifecycle/report/payslip fixtures are created before Playwright module load. Existing legacyNULL evidence is explicitly supplied through UC12_LEGACY_FIXTURE_FILE; it is a preserved historical record, not a fabricated new reason.

```sh
env -u NO_COLOR -u FORCE_COLOR -u PENDING_DELIVERY_FIXTURE_FILE -u RESTORED_PAYSLIP_ID UC12_LEGACY_FIXTURE_FILE=/Users/manus/University/SA-Project/docs/superpowers/reports/18-uc12-advance-reasons-evidence/legacy-fixture.json PLAYWRIGHT_JSON_OUTPUT_NAME=/Users/manus/University/SA-Project/docs/superpowers/reports/19-current20-actor-uat-evidence/final-69-browser.json sh scripts/full-uat.sh --reporter=list,html,json --workers=1 --retries=0
```

## Independent output checks

Read the final run's downloaded bytes with bundled Python/pypdf/csv and read-only Mailpit HTTP. Salary/creditor PDFs for HR and OWNER give31800.00 in all/reload and7600.00 in branch/department filters. The separately downloaded individual slip gives11400.00 from the same locked result. Frozen bank CSV rows total15200.00 and exclude the subsequently edited live destination. Social-security CSV uses earned bases12000.00/4000.00 and deductions600.00/200.00, excluding contracted30000.00. Local HR/OWNER attachments exactly equal original/reloaded downloads (nets11500.37/3800.25); each SMTP attempt remains separate. This certifies local receipt only.

Actual displayed QR images were decoded by independent jsQR in the final browser scenario. A separate Python TLV/CRC check confirmed THB amount123.45 and maximum9999999999.99, registered frozen phone recipient and CRCB5E2/C7B8. The lifecycle fixture gives payable175.03, paid150.03, outstanding25.00, paid_count2/outstanding_count1 and complete=false; cancelled history remains. QR generation/scanning never certifies settlement.

## Artifact QA and publication

Current README remains the editorial source, preserving the prior user's material. Scoped refreshers never reset it through complete_rubric.py. Catalog20, separate delivery16 crosswalk, historical academic34 crosswalk,23sequence/collaboration scenarios,39 dictionaries/allcolumns,91FK,25enum lists and current payment/class/DFD additions are synchronized. Partial unique predicates are documented separately from global UQ/cardinality; record-to-payment history is1:N with atmost1active. Identical transition replay returns the prior result; conflicting transitions reject.

The first bundled headless render showed blank Thai; explicit font discovery restored it without desktop LibreOffice. All final pages are inspected, with prior visual reviews reused only for byte-identical PNGs; changed tables/figures receive detailed views. Final evidence and publishable hashes are in current20-artifact-qa.json/current20-artifact-qa.md and current20-acceptance-manifest.json. Curated file staging must use the Task4 publishable manifest, including every158README image reference. Raw fixture credentials, traces, bank CSVs and mail payloads remain ignored.

## Limitations

Automated browser/database acceptance on a disposable stack does not certify human UAT, real bank settlement, external SMTP delivery, production hosting or other browser engines. QR creation/scanning is not payment success. Salary creditor summary means salary payable by the restaurant, not employee debt. Instructor/member/course fields are preserved for the team to complete with real information; unrelated PPTX/PRODUCT/DSStore are outside this change. Root owns final independent reviews, report20 and integration; no commit/push/merge is performed by Task4.

## Post-review test-only follow-up

The historical full69 frozen tree remains above. Final review found unconditional day>=20 in advance-reasons.e2e.ts would fail legitimate early-month CI. A bounded test-only repair now expects real422/ADVANCE_INELIGIBLE_DATE and zero saved requests before20, preserving eligible-date reason/decision flows. Focused two-case browser passed40.9s on26October; early-month browser was not observed. Runtime and other577 frozen files are unchanged; [post-review delta](../../sa-report/evidence/current20-post-review-test-delta.json) records the separate test hash and evidence.
