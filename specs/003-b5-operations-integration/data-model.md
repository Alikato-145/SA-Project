# Data Model: B5 Integration

No new tables, columns, enums, or migrations. Existing feature schemas remain authoritative.

| Entity | Fields and relationships | Validation and transitions |
|---|---|---|
| Account/grant | account ID, optional employee ID; role and branch/department per grant | Permission and target scope must match the same grant; actor comes from session |
| Assignment | employee, branch, department, base salary/welfare, effective dates | Historical date lookup; no overlapping ranges |
| Branch schedule/override | branch, hours, grace, effective range; override date and closed flag | Real dates/times; successor schedule closes prior day; closed override has no hours |
| Holiday | shop, holiday date/name, active flag | Shop-level master; scoped reads, global administration; preserve locked-period facts |
| Work day | employee, historical branch, work date, status, timestamps, late minutes, deduction flag/source | One employee/date; valid chronological timestamps; approved leave only through approval workflow |
| Leave request/day/quota/action | employee, original/final type, dates, quota use, decision actor/time | Non-overlap; atomic pending→approved/rejected; supervisor approval ≤3 days; append-only decisions |
| Overtime/action | employee, work date, type, hours/day units, optional work day | hourly requires hours; rest/public holiday requires day_units; context validated; explicit pending→approved/rejected |
| Advance | employee, month, amount, request/decision actor/time | configured date/worked days/cap, exact positive amount, non-negative projected net; pending→approved/rejected→deducted |
| Loan/installment | employee, principal/reason, due month, amounts/status | 1–5 installments sum exactly to principal; scheduled→deducted once |
| Debt | employee/type, positive amount, kind/date, original transaction, settlement | charge/adjustment→append-only reversal; reversed originals excluded; settled entries immutable; settlement record/time are derived from locked payroll source evidence because frozen debt rows reject updates |
| Payroll | shop/period; employee record/items/snapshot, adjustments | unique employee/period, blockers resolved, exact calculation; lock immutable; settlement atomic |
| Audit | actor/action/target/old-new/time/request | same transaction as mutation; redact credentials/bank secrets |

Public identifier constraint: `positive decimal string, converted only when safely representable by current persistence mapping`.
Money constraint: `decimal string; never floating-point arithmetic`.
Business date constraint: `real ISO YYYY-MM-DD date`.
Transactions coordinate input mutation and final payroll projection so no late input can silently evade the locked snapshot.
