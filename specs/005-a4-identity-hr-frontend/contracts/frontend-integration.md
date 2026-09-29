# A4 Frontend Integration Contract

## Ownership boundary

A4 exports presentation routes, typed safe view models, navigation metadata, and an interface describing required operations. Person C owns the implementation that binds this interface to the shared API client, cookie behavior, error envelope, request ID display, global providers, and dashboard navigation.

A4 does not call `fetch` directly and does not create a QueryClient provider.

## Required operation groups

- Authentication: login, logout, current actor
- Accounts: list, detail, create, reset password, change status, list roles, grant role, revoke grant
- Organization: list/detail/create/update/deactivate for shops, branches, departments, positions
- Employees: list, detail, create/update/status, atomic onboarding
- Assignments: list and create effective-dated assignment
- Bank accounts: masked list, add, update, make primary, deactivate
- Weekly holidays: list, add/replace, end

All IDs and money cross the boundary as strings. Error results expose a stable public code, safe message, optional field errors, and request ID.

## Navigation manifest

A4 exports route metadata with label, href, required presentation capability, and grouping. Person C chooses final placement and must not use the metadata as an authorization boundary.

## Deferred integration acceptance

Integration is complete only when:

1. Shared client sends cookies and origin/content-type requirements correctly.
2. Login maps locked, disabled, invalid credential, and validation errors.
3. Protected pages derive capabilities from current actor data.
4. Query invalidation refreshes affected list/detail/history screens.
5. Full bank numbers and temporary passwords never enter long-lived cache.
6. Root navigation consumes the manifest.
