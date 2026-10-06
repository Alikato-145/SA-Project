# Research: Leave and Overtime

**Leave decision**: Approve leave by changing state, appending history, locking and
updating quota, and creating/linking attendance in one transaction. This prevents
partial effects and double quota use.

**Authority**: Supervisors may approve up to three days in their department;
branch managers may approve any request in their branch. Retain original leave type,
store final type, and append a type-change action when it differs.

**OT rules**: OT is payable only after explicit approval. Hourly OT requires
positive hours only; rest-day/public-holiday OT require day units over zero and at
most one only. Do not infer OT from clock-out time.

**OT state**: Submit and decide atomically with append-only actions. Only approved
records appear in payroll reads; a second decision is a state conflict.

**Integration**: Inject scope, effective assignment, weekly-holiday/holiday and
attendance-context validation. Person C supplies route composition, error boundary,
transaction helper and payroll lock guard.
