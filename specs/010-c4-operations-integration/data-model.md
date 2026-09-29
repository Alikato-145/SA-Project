# Data Model: C4 Operations Integration and Usability

No schema or migration change is part of this feature.

## Existing entities consumed

| Entity | Integration use | Historical rule |
|---|---|---|
| Authenticated actor | Supplies account, linked employee, and active role grants | Session claims are reloaded; scope is never browser-supplied |
| Employment assignment | Resolves employee branch and department on a business date | Effective-dated history is read, never rewritten |
| Work-day record | Supports attendance list/create/correction | Branch is a historical snapshot and locked records remain protected |
| Leave request and approval action | Supports self-service and decisions | Decisions and actions remain append-only |
| Overtime record and approval action | Supports request and decision workflows | Only explicitly approved records are payable |
| Advance, loan, and debt records | Supports employee finance workflows | Loan installments and debt history remain immutable/append-only as defined by existing services |

## Integration-only data

The adapter accepts only the server-authenticated actor and resolves targets from
existing records or effective assignments. It persists no new entity and never
accepts role scope, employee identity, branch, or department as authorization
proof from the browser.
