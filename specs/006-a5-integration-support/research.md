# A5 Research Decisions

- Reuse createEmployeeOperationContextService as the B/C dated-context boundary; attendance runtime already calls it.
- Reuse payroll's dated assignment lookup and decimal calculator. Do not refactor Person C's repository without a demonstrated failure and owner coordination.
- Use isolated Bun tests for role/date boundaries. Database-gated checks require a dedicated TEST_DATABASE_URL.
- Preserve A1–A3 audit registries and observer pattern; test coverage/redaction rather than add another mechanism.
- A4 is already wired to shared shell/API on develop; A5 is verification and bug fixes, not a new UI feature.

## Coverage inventory

- A1: auth/authorization tests cover fixed role scopes, inactive grants, and owner role administration; A1 audit registry covers 13 public actions.
- A2: organization scope/route tests cover branch and department grants; A2 audit registry covers 20 actions.
- A3: employee, assignment, onboarding, bank, and holiday tests cover effective-date history and redaction; A3 audit registry covers 16 actions.
- Attendance runtime uses EmployeeOperationContextService for dated authorization and branch snapshots. A5 adds transfer-date visibility regression.
- Payroll dated projection already tests gaps and the calculator already tests per-day salary/welfare/configuration changes. A5 retains that coverage and adds a live login→history route journey.
- A4 frontend tests exercise authenticated API adapters, route access, pagination, and onboarding; frontend lint/build verify route composition.
