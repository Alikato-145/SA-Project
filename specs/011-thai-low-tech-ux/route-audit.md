# Route and UX Audit

## Baseline: 2026-09-29

| Route group | Permitted roles | Server boundary | Baseline UX gap |
|---|---|---|---|
| `/login` | unauthenticated | Auth service creates the session | Responsive shell existed, but recovery and form language were not shared with the workspace. |
| `/dashboard` | all authenticated roles | Route guard and feature APIs | Still described old mock/C1 work instead of helping users start their permitted task. |
| `/employees`, nested employee pages | HR, Owner | Employee feature enforces master-data access | Preview views mix real-looking controls with illustrative data and technical preview wording. |
| `/accounts`, `/organization`, `/settings` | HR/Owner; settings Owner | Identity/organization routes enforce roles and scope | Setup sequence needs plain-language purpose, consequences, and consistent result feedback. |
| `/attendance` | Supervisor, Branch Manager, HR, Owner | Operations route checks role scope and record lock state | Uses raw status codes, a raw correction ID, and a dense table without a clear selected-record flow. |
| `/leave` | all | Operations service checks the employee and pending/final state | Employee context was corrected to self-only; remaining work is shared labels, management explanation, and responsive consistency. |
| `/overtime` | all | Operations service checks the employee and approval scope | Employee picker is still exposed to employees; raw OT/state text remains. |
| `/finance` | HR, Owner | Finance operations route owns all-scope policy and ledger state | Financial actions need explicit outcome/final-state language and named context. |
| `/payroll` | Branch Manager, HR, Owner | Payroll feature owns calculation, lock, and adjustment constraints | Dense multi-step workspace needs a clearer next action and immutable-period explanation. |
| `/payslips` | Employee, HR, Owner | Payslip API enforces own-only access and lifecycle | Employee list exposes technical payroll record terminology; administrator flow relies on raw IDs. |
| `/reports` | HR, Owner | Reports API only exports locked periods | Export form asks for a raw period ID and has mixed English labels. |
| denied/loading/error states | depends on route | Route guard remains final | Feedback is inconsistent and some pages lack a clear return path. |

## Global visual and interaction baseline

- Retain the existing green `--accent`, ink, paper, surface, and line tokens; do not introduce a competing visual system.
- Use native controls with visible labels, a 44px practical target height, clear disabled state, and the existing visible keyboard focus ring.
- Show status in Thai text as well as colour. Use `role="status"` for non-urgent feedback and `role="alert"` for failure requiring attention.
- Keep dashboard density with bordered sections and responsive columns; use contained table overflow only where the data cannot be sensibly stacked.
- Use Thai as the task language. Identifiers are secondary support information, not the starting point for ordinary selection.

## Validation record

Validated on 2026-09-30 for the mounted Audit workflow and current merged
application baseline:

- Backend `bun run typecheck` and the database-independent suite passed: 417
  tests passed, 27 database-gated tests skipped, 0 failed.
- A disposable PostgreSQL 16 stack passed the full suite with 426 passed, 18
  explicitly gated tests skipped, and 0 failed. The process-isolated Person A
  runner passed all 9 files (53 tests), and the seeded Person B attendance,
  leave, and overtime database constraints passed 12 tests with 0 failures.
- Frontend passed 33 tests, ESLint, and the production build; the build emitted
  21 routes including `/audit`.
- Development and production Compose files both passed `docker compose config
  --quiet`; production now receives the required auth and bank-encryption
  environment variables explicitly.
- Web Interface Guidelines review covered every frontend file changed for the
  Audit workflow. Non-auth filter autocomplete/spellcheck and identifier
  translation handling were remediated; no unresolved finding remains in this
  change set.
- Impeccable detector returned no findings. Browser checks at desktop and
  360px confirmed the real authenticated Audit page, contained table overflow,
  readable filters/states, and no page-level horizontal overflow (360/360).

The complete credential-free cross-route and all-role walkthrough remains
pending under T029; this record does not claim that broader manual pass.
