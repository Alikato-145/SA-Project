# Implementation Plan: A4 Identity and HR Frontend

**Branch**: `codex/a4-identity-hr` | **Date**: 2026-09-27 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/005-a4-identity-hr-frontend/spec.md`

## Summary

Build A4 presentation under feature-owned components and thin App Router routes. The first pass used safe fixtures while the shared shell was pending. After Person C's shell and API client landed, connect account, organization, employee, onboarding, and history workflows to mounted backend routes and mount the A4 navigation metadata.

## Technical Context

**Language/Version**: TypeScript 5, React 19.2, Next.js 16.3 App Router

**Primary Dependencies**: Next.js, React, Tailwind CSS 4; no new runtime dependency

**Storage**: No new persistence; short-lived local form state only

**Testing**: TypeScript strict build, ESLint, production build, pure Node/Bun tests where framework-free reducers and contracts allow

**Target Platform**: Modern desktop and mobile web browsers, minimum 360-pixel viewport

**Project Type**: Web application frontend submodule consuming existing REST contracts

**Performance Goals**: Immediate local interaction feedback; stable rendering for 1,000-row pagination metadata without rendering all records at once

**Constraints**: Keep shared shell and API edits limited to A4 integration points. Do not use direct feature `fetch` or create a duplicate query provider. Client components only at interactive leaves. Never retain passwords or full bank numbers outside transient form state.

**Scale/Scope**: Login plus live account, organization, employee list/detail, onboarding, assignment, bank, and holiday routes; documents remain a deferred read-only explanation.

## Constitution Check

- **Historical integrity — PASS**: UI language describes effective-dated replacement/end actions and never edits prior facts in place.
- **Server authorization — PASS**: Capability presentation is UX only; no frontend check is treated as authority.
- **Feature-first boundaries — PASS**: A4 code stays under `features/identity-hr`; thin routes contain no domain logic.
- **Contract discipline — PASS**: View models mirror safe A1-A3 DTOs, IDs and money stay strings, protected values are absent.
- **Minimal change — PASS**: Shared shell and API changes are limited to A4 navigation, route access, authenticated account display, and pagination metadata; backend remains unchanged.
- **Verification — PASS**: Reducer/state tests, lint, responsive inspection, and production build are required.

No constitution violation requires an exception.

## Project Structure

### Documentation

```text
specs/005-a4-identity-hr-frontend/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── frontend-integration.md
└── tasks.md
```

### Source Code

```text
frontend/
├── app/
│   ├── login/page.tsx
│   └── (dashboard)/
│       ├── accounts/{page.tsx,new/page.tsx,[accountId]/page.tsx}
│       ├── organization/page.tsx
│       └── employees/
│           ├── page.tsx
│           ├── new/page.tsx
│           └── [employeeId]/{page.tsx,employment/page.tsx,bank/page.tsx,weekly-holidays/page.tsx,documents/page.tsx}
└── features/identity-hr/
    ├── contracts/
    ├── fixtures/
    ├── auth/
    ├── accounts/
    ├── organization/
    ├── employees/
    ├── onboarding/
    ├── ui/
    └── route-metadata.ts
```

**Structure Decision**: App Router files are thin adapters. All A4 presenters, view models, fixtures, form logic, and local visual tokens live in one feature package. No feature-owned dashboard layout or network client is introduced.

## Complexity Tracking

No constitution violations.

## Integration continuation — 2026-09-29

After the shared shell and A1–A3 endpoints landed, A4 pages were connected to the real cookie-authenticated API. The frontend uses `lib/api/client.ts` for requests and top-level pagination metadata, preserves masked response fields, and reads grants from `/v1/auth/me` to present permitted controls. Backend authorization remains authoritative. Account and organization mutations, atomic employee onboarding, and effective-dated employee history actions now use mounted routes. Attachment upload remains deferred because there is no mounted attachment endpoint.
