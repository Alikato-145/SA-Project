# Implementation Plan: Operations and Finance Screens

**Branch**: `main` | **Date**: 2026-09-22 | **Spec**: [spec.md](spec.md)

**Input**: B4 frontend flows for attendance, leave, OT, advances, loans, and debt.

## Summary

Create four independent client pages under Person B's dashboard route folders. Each page calls the feature's relative `/api` route, validates its own form inputs, renders records and decisions, and refreshes after writes. Person C mounts the backend routes and supplies the shared shell and session.

## Technical Context

**Language/Version**: TypeScript, React 19, Next.js 16
**Primary Dependencies**: Existing Next.js, React, Tailwind CSS; native form controls and fetch
**Storage**: Backend APIs only
**Testing**: Frontend lint and production build; manual route/API smoke after integration
**Target Platform**: Responsive browser
**Project Type**: Web app
**Performance Goals**: Show useful loading/empty states while requests run; no new client data library
**Constraints**: Only `frontend/app/(dashboard)/{attendance,leave,overtime,finance}/`; do not edit Person C layout, navigation, or shared API client
**Scale/Scope**: Four routes, six workflows

## Constitution Check

- History and authorization remain server-owned; UI never directly edits approved historical data.
- No schema, migration, shared backend, or shared frontend changes.
- Each mutating form includes labelled required controls and surfaces public server errors.
- C must mount the feature routes and supply session-aware `/api` access before end-to-end demo.

## Project Structure

```text
specs/006-operations-finance-ui/{spec.md,plan.md,research.md,data-model.md,contracts/,quickstart.md,tasks.md}
frontend/app/(dashboard)/attendance/page.tsx
frontend/app/(dashboard)/leave/page.tsx
frontend/app/(dashboard)/overtime/page.tsx
frontend/app/(dashboard)/finance/page.tsx
```

## Phase 0: Research

Use the existing B1–B3 route contracts. Next 16's local page and client-component docs permit client pages with `use client`. Native fetch with same-origin cookies and native form controls is sufficient until C's client exists. No separate state library is needed for four small screens.

## Phase 1: Design

Each page owns its employee selection, list request, pending state, success and error message, and mutation form. For response shape, preserve current feature DTOs. Approval controls remain visible to scoped managers but a server rejection is displayed directly. Finance groups advances, loans, and debt in one route, with independent forms and lists. Avoid a fake eligibility calculation in the browser.

## Phase 2: Implementation

Implement attendance first, then leave and OT, then finance. Validate lint and build. Capture the route registration and navigation work required from C in the contract and quickstart.
