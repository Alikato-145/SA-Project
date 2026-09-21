# Team Task Specification Guideline

Use one folder per independently reviewable task:

```text
specs/<feature>/<task-id>-<short-name>/
└── spec.md
```

Do not assign two people tasks that edit the same file. If that is unavoidable,
make the second task depend on the first.

## `spec.md` template

```md
# <Task ID>: <Short title>

## Goal
One outcome that can be reviewed independently.

## Scope
- In: exact behavior and files this task may change.
- Out: explicitly excluded behavior/files.

## Context
Links to the parent feature spec, plan, domain references, and prior task outputs.

## Dependencies
- Must be completed first: <task IDs>
- May run in parallel with: <task IDs>

## Implementation Notes
- Preserve: domain rules, API contracts, migrations, or historical data affected.
- Approach: smallest acceptable change; reuse existing patterns/dependencies.

## Acceptance Criteria
- [ ] Observable outcome is met.
- [ ] Focused command/test passes: `<command>`.
- [ ] No unrelated files changed.
- [ ] Docs/config/migration are updated when the task changes them.

## Handoff
- Changed files:
- Commands run and results:
- Known limitations or follow-up task:
```

## Recommended task sizes

- One owner, one coherent deliverable, normally 1–4 hours.
- Split by file ownership first: schema, runtime config, tests, UI, docs.
- Keep migrations serial: one owner generates/reviews a migration after schema tasks finish.
- Give every task a runnable verification command before assigning it.

## Example task breakdown

For a new Leave feature:

1. `leave-001-schema` — tables, migration, schema tests.
2. `leave-002-service` — validation, authorization, transaction boundaries.
3. `leave-003-api` — route/controller/DTO/mapper only; depends on service.
4. `leave-004-ui` — frontend screen; depends on API contract.
5. `leave-005-integration` — end-to-end boundary tests and docs.

Each task must link back to the parent feature's `spec.md`; do not duplicate the
whole feature specification in every child task.
