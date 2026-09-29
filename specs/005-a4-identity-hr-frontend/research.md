# A4 Research and Design Decisions

## 1. Shared-shell dependency

**Decision**: Implement feature-owned presentation, view models, form state, fixtures, route pages, and navigation metadata now. Do not implement a network client or query provider.

**Rationale**: The frontend is still a starter and Person C owns the shared API client, auth behavior, dashboard layout, navigation, and QueryClient provider. A duplicate client would create inconsistent cookies, errors, cache, and request IDs.

**Alternatives considered**: Direct `fetch` inside A4 or a feature query provider. Rejected because both create parallel infrastructure that must later be removed.

## 2. Next.js 16 boundaries

**Decision**: Keep pages as Server Components by default; use Client Components only for interactive forms, filters, tabs, and transient state. Dynamic route params are awaited.

**Rationale**: This follows the installed Next.js 16 local documentation, reduces shipped JavaScript, and keeps integration seams explicit.

## 3. Visual direction

**Decision**: Use a restaurant-operations ledger aesthetic: rice-paper surfaces, deep kitchen-green structure, turmeric action accents, and vermilion warnings. Dense operational tables adapt to labeled mobile records. Typography favors highly legible Thai-capable system faces.

**Palette**: Charcoal `#17201D`, kitchen green `#1F6B52`, turmeric `#D7A443`, rice `#F7F3E8`, vermilion `#C94B3C`, slate `#66736D`.

**Rationale**: The product manages real restaurant staff and payroll history. The direction feels operational and trustworthy without becoming a generic blue SaaS dashboard.

**Alternatives considered**: Dark fintech dashboard, cream editorial layout, generic rounded-card dashboard. Rejected as mismatched or overly templated.

## 4. Security and transient secrets

**Decision**: Password and bank-number inputs remain local to their forms, are cleared on completion/cancel, never enter fixtures, URL state, navigation metadata, or cached view models. One-time credentials use a dismissible result panel.

**Rationale**: A4 must preserve A1/A3 safe-response and audit assumptions.

## 5. Authorization presentation

**Decision**: Present capability-based actions only where useful, but label preview data and document that the backend is authoritative. Forbidden and hidden-resource states remain explicit presenters.

**Rationale**: Hiding controls improves usability but cannot enforce permission.

## 6. Testing before shared integration

**Decision**: Validate view-model/reducer behavior, page compilation, lint, production build, keyboard semantics, responsive structure, and secret scanning. Defer live cookie/API and end-to-end integration tests.

**Rationale**: These are independently valuable and do not fabricate a working backend connection.
