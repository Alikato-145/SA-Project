# A4 Live Integration Validation

## Automated checks

Run from `frontend/`:

```sh
bun run lint
bunx tsc --noEmit
bun test
bun run build
```

Inspect these routes with a running backend and suitable A1 accounts:

- `/login`
- `/accounts`, `/accounts/new`, `/accounts/1`
- `/organization`
- `/employees`, `/employees/new`, `/employees/1`
- `/employees/1/employment`
- `/employees/1/bank`
- `/employees/1/weekly-holidays`
- `/employees/1/documents`

Use Employee, Supervisor, Branch Manager, HR, and Owner accounts to confirm each server scope. Validate at 360, 768, and 1280 pixel widths with keyboard navigation and reduced-motion mode.

## Required scenarios

1. Login creates an HttpOnly-cookie session and dashboard navigation uses the current account.
2. Account and organization lists, details, create, role changes, status changes, and deactivation use the mounted API and show server errors.
3. Employee search uses server pagination and scope; protected profile fields appear only when present in the response.
4. Onboarding submits one atomic request, preserves decimal strings, clears bank plaintext, and displays a one-time password only after success.
5. Assignment and weekly-holiday changes preserve previous effective-dated history.
6. Bank reads show masked account numbers; updates and deactivation are audited by the backend.
7. Documents state that uploads are deferred and contain no fake upload action.

## Remaining environment checks

Run browser end-to-end smoke tests against a seeded backend for each role and for successful/failed writes. The current workspace has no supplied live test credentials, so this has not been claimed as verified. Attachment upload remains deferred until its backend route is mounted.

## Verification record (2026-09-27)

- `bun run lint`: passed.
- `bun run build`: passed; all A4 preview routes were generated successfully.
- `git diff --check`: passed in the frontend submodule.
- Sensitive-boundary scan: no direct `fetch`, feature-owned `QueryClient`, password hash, encrypted bank-account field, bearer token, or token literal found in A4 route/component sources.
- Browser QA: `/login`, `/employees`, `/employees/new`, and `/employees/101` rendered successfully; mobile viewport at 390 × 844 remained usable, profile tabs were horizontally scrollable, and the browser console contained no warnings or errors.

## Integration record (2026-09-29)

- A4 account, organization, employee, onboarding, and history screens now use the shared API client and mounted backend routes.
- The shell shows the authenticated username and links A4 navigation. Employee reads are available to all scoped roles; employee onboarding stays HR/Owner only.
- `apiRequestPage` preserves backend `page`, `page_size`, and `total` for scoped lists.
- `bun test`: 20 passed; `bun run lint`, `bunx tsc --noEmit`, and `git diff --check`: passed.
- `bun run build --webpack` via package script: passed when run in an environment that permits the Next.js TypeScript subprocess.
- Live browser end-to-end checks are still required with seeded accounts and backend services.
