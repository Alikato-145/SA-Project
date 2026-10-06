# B4 Research

- `frontend/AGENTS.md` requires the installed Next 16 docs. The local `page.md`, `layout.md`, and forms guide were read. Route `page.tsx` files can be client components when they need state.
- The frontend is a Next scaffold with no dashboard shell or API client yet. Person C owns those paths, so B4 stays in its four route folders and calls same-origin `/api` endpoints.
- B1 route inputs use camelCase commands; B2/B3 request bodies use snake_case. Each page follows its current backend route contract. C should unify API serialization only as a coordinated contract change.
- Backend role scope is authoritative; the pages present server errors and never infer approval rights from local state.
