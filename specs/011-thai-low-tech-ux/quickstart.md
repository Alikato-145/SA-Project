# Validation Guide: Thai Low-Tech UX Across the Application

## Prerequisites

- The repository dependencies are installed.
- The local authenticated application and database are running through the existing Compose setup.
- Seeded development accounts exist for Employee, Supervisor, Branch Manager, HR, and Owner. Do not record credentials, cookies, or tokens in validation output.

## Route review

Review login and every current dashboard route: dashboard, accounts and nested account pages, organization, employees and nested employee pages, attendance, leave, overtime, finance, payroll, payslips, reports, settings, and denied states.

For each route, verify:

1. Thai title and purpose are visible.
2. Role-inappropriate actions and employee selectors are absent.
3. A primary action or clear unavailable explanation is present.
4. Loading, empty/no-result, success, denied, and error states are clear when relevant.
5. Status labels are Thai and not colour-only.
6. No page-level horizontal scroll appears at 360px or 1280px.
7. Keyboard focus remains visible and controls can be activated with keyboard.

## Commands

```sh
cd backend && bun run typecheck && bun test
cd frontend && bun run lint && bun run build
docker compose up --build -d
docker compose ps
```

## Expected result

All checks pass, every route remains protected by existing server authorization, and a low-tech Thai user can identify the page purpose and next safe step without entering a raw identifier as their primary workflow.
