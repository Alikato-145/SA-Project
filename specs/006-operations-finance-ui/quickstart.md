# B4 Validation

From `frontend/`, run `bun run lint` and `bun run build`. With Person C's `/api` integration running, open `/attendance`, `/leave`, `/overtime`, and `/finance`; select an authorized employee; submit and decide each applicable workflow; verify list refreshes and business errors.

Validation on 2026-09-22: `bun run lint` and `bunx tsc --noEmit` passed.
`bun run build` failed before app compilation because Turbopack could not bind
its CSS worker to a local port (`Operation not permitted`), including on the
escalated attempt. `bunx next build --webpack` reached font loading but failed
to resolve `fonts.googleapis.com` from the existing Person C-owned root layout.
The UI's live API smoke test awaits Person C's route mounting and proxy.
With Next's temporary `NEXT_FONT_GOOGLE_MOCKED_RESPONSES` fixture and
`next build --webpack`, production compilation and static route generation
passed for `/attendance`, `/leave`, `/overtime`, and `/finance`. This verifies
the B4 pages without editing Person C's root layout.
