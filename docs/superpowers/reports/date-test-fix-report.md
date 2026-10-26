# Current20 UC12 date-dependent E2E fix

## Root cause and scope

`frontend/e2e/advance-reasons.e2e.ts` asserted `day >= 20` before either browser case ran. On actual Bangkok dates 1–19, a correct application would fail both tests before testing the expected `ADVANCE_INELIGIBLE_DATE` response. This change touches only that E2E file; no application rule, server clock, fixture clock, or skip flag changed.

## Exact source diff

```diff
- const [year,month,day]=today.split("-").map(Number);expect(day,"Positive eligible advance must use actual day >=20").toBeGreaterThanOrEqual(20);
+ const [year,month,day]=today.split("-").map(Number);
@@ after UI blank/whitespace/overlength checks @@
+  for(const bad of [undefined,null,""," \t\n ","x".repeat(1001)]){const result=await employee.request.post("/api/v1/advance-requests",{headers,data:{employee_id:onboard.employee.id,amount:"100.01",...(bad===undefined?{}:{reason:bad})}});expect(result.status()).toBe(422);expect((await result.json()).error.code).toBe("VALIDATION_ERROR");}
   const reasonText=`Emergency household expenses ${key}`;await reason.fill(`  ${reasonText}  `);
-  const submitted=employee.waitForResponse(r=>new URL(r.url()).pathname==="/api/v1/advance-requests"&&r.request().method()==="POST");await form.getByRole("button",{name:"ส่งคำขอเงินทดรองจ่าย",exact:true}).click();const response=await submitted;expect(response.ok(),await response.text()).toBe(true);const advance=(await response.json()).data;expect(advance.reason).toBe(reasonText);
+  const submitted=employee.waitForResponse(r=>new URL(r.url()).pathname==="/api/v1/advance-requests"&&r.request().method()==="POST");await form.getByRole("button",{name:"ส่งคำขอเงินทดรองจ่าย",exact:true}).click();const response=await submitted;
+  if(day<20){
+   expect(response.status()).toBe(422);expect((await response.json()).error.code).toBe("ADVANCE_INELIGIBLE_DATE");
+   await employee.reload();await employee.getByRole("button",{name:"โหลดข้อมูลการเงิน",exact:true}).click();
+   const ownResponse=await employee.request.get(`/api/v1/advance-requests?employee_id=${onboard.employee.id}`);expect(ownResponse.ok()).toBe(true);expect((await ownResponse.json()).data).toEqual([]);
+   console.log(JSON.stringify({businessDate:today,employee:onboard.employee.id,finance,positiveAdvance:false,reason:"Legitimate before-20 eligibility denial"}));
+   return;
+  }
+  expect(response.ok(),await response.text()).toBe(true);const advance=(await response.json()).data;expect(advance.reason).toBe(reasonText);
@@ after pending employee screenshot @@
-  for(const bad of [undefined,null,""," \t\n ","x".repeat(1001)]){const result=await employee.request.post("/api/v1/advance-requests",{headers,data:{employee_id:onboard.employee.id,amount:"100.01",...(bad===undefined?{}:{reason:bad})}});expect(result.status()).toBe(422);}
```

The invalid-reason API loop now runs on both dates and checks the exact `VALIDATION_ERROR` code. On days 1–19, the valid-reason UI request must return 422 with `ADVANCE_INELIGIBLE_DATE`; after reload, the employee-scoped API list must be empty. On days 20–31, the existing reason persistence and HR rejection / admin approval journeys continue unchanged.

## Verification on 26 October 2026 (Asia/Bangkok)

| Check | Result | Raw evidence |
| --- | --- | --- |
| `bunx eslint e2e/advance-reasons.e2e.ts` | exit 0, no diagnostics | `20-controller-evidence/date-test-fix-lint.log` |
| `bunx tsc --noEmit --incremental false` | exit 0, no diagnostics | `20-controller-evidence/date-test-fix-typecheck.log` |
| `bun test src/features/advance/advance.test.ts src/features/advance/advance.routes.test.ts` | 29 pass, 0 fail; includes day 19 rejection / day 20 acceptance and reason validation | `20-controller-evidence/date-test-fix-backend-boundary.log` |
| `sh scripts/full-uat.sh --grep 'UC12 EMPLOYEE reason survives reload' --workers=1 --retries=0` | 2 pass, 0 fail in 40.9s, fresh disposable fixtures; HR rejection and admin approval persistence observed | `full-uat-evidence/20261026T122137Z-38962/browser.log` |
| `git diff --check` in `frontend/` | exit 0 | command output empty |

Changed E2E SHA-256: `2c3211a8609b42e1ab58263a7d3407a260d69268a4068d5d938beb7dd103dff5`. The historical full-suite manifest remains unchanged. The focused run used no legacy NULL-reason fixture, so it does not retest that UI case.

The actual browser date was 26 October, so the 1–19 browser branch was **not observed in this run**. The existing backend injected-date boundary test verifies the date policy on day 19 and day 20; it is not evidence of an early-month browser run. The branch remains executable under the real clock on the next early-month run without changing server time.
