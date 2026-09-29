# Implementation Plan: C4 Operations Integration and Usability

**Branch**: `codex/c4-operations-integration` | **Date**: 2026-09-28 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/010-c4-operations-integration/spec.md`

**Note**: This template is filled in by the `$speckit-plan` command; its definition describes the execution workflow.

## Summary

Expose the existing Person B operations features through the composed backend and
existing dashboard. Add one application-owned operations adapter that translates
the authenticated actor into feature commands and enforces scope at the service
boundary; it must use services/repositories only through the existing layered
flow. Release the dashboard routes using the shared API client and refine the
shell and workflow feedback for high-frequency operational use.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: TypeScript; Bun 1.3; Next.js 16 / React 19 frontend; Elysia backend

**Primary Dependencies**: Elysia, Drizzle ORM, PostgreSQL, Next.js, Tailwind CSS

**Storage**: Existing PostgreSQL schema only; no migration or schema changes

**Testing**: `bun test`, backend `bun run typecheck`, frontend `bun run lint` and `bun run build`

**Target Platform**: Browser dashboard behind the existing same-origin gateway

**Project Type**: Web application with separate frontend and backend submodules

**Performance Goals**: Operations list/filter feedback is understandable immediately; released pages have no horizontal page scrolling at 360px or 1280px

**Constraints**: Preserve business rules and historical data; authorization stays server-side; use existing dashboard language and native form controls; no new dependencies

**Scale/Scope**: Eight existing operations domains, four existing frontend workflow pages, one shared shell, and focused composition/access/UI checks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Historical integrity**: PASS. The plan adds no schema or history mutation paths and reuses existing services.
- **Authorization and atomic decisions**: PASS only if all exposed routes authenticate and use a centralized scope adapter; frontend route visibility is advisory only.
- **Layered backend**: PASS. Routes call controllers; controllers call existing services; the composition root wires concrete dependencies.
- **Contract discipline**: PASS. Existing response envelope and error boundary are reused for the operations API surface.
- **Minimal change and verification**: PASS. No dependencies, migrations, or feature rewrites; add focused tests before release.

## Project Structure

### Documentation (this feature)

```text
specs/010-c4-operations-integration/
├── plan.md              # This file ($speckit-plan command output)
├── research.md          # Phase 0 output ($speckit-plan command)
├── data-model.md        # Phase 1 output ($speckit-plan command)
├── quickstart.md        # Phase 1 output ($speckit-plan command)
├── contracts/           # Phase 1 output ($speckit-plan command)
└── tasks.md             # Phase 2 output ($speckit-tasks command - NOT created by $speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend/
├── src/
│   ├── app.ts
│   ├── core/auth/
│   └── features/{attendance,branch-schedule,holiday-calendar,leave,overtime,advance,loan,debt}/
└── src/features/operations-integration/ # application composition and scope adapter only

frontend/
├── app/(dashboard)/{attendance,leave,overtime,finance}/
├── components/{application-shell,dashboard-access-guard}.tsx
└── lib/{api,auth,operations}/
```

**Structure Decision**: Retain the existing feature-first backend and App Router
frontend. A narrow operations-integration feature owns only cross-feature
composition and authorization adapters; it does not move Person B business logic
out of existing features.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | — | — |
