# UI Behavior Contract

## Shared route contract

Every user-facing route provides:

1. A Thai title and a short purpose statement.
2. A role-appropriate primary action or an explanation of why no action is available.
3. A loading, empty/no-result, success, warning, denied, and error treatment whenever that state is applicable.
4. A visible keyboard focus indicator and controls with native semantics.
5. A responsive arrangement that avoids page-level horizontal scrolling.

## Role context contract

| User type | Context shown in self-service | Context shown in management work |
|---|---|---|
| Employee | Own linked employee; no employee picker | Not available unless another active permitted role applies. |
| Supervisor | Own context plus only department-scoped operations | Department-scoped record selection. |
| Branch Manager | Own context plus branch-scoped operations | Branch-scoped record selection. |
| HR / Owner | Safe account context | Authorized broad record selection. |

The frontend may hide unavailable controls. The backend must continue to deny out-of-scope, invalid-state, and unsafe direct requests.

## Feedback copy contract

- Success names the completed action.
- Error names the safe known cause and the next correction or retry.
- Immutable state names the state and permitted alternative, such as a tracked adjustment rather than edit.
- Loading and empty states use Thai plain language and never expose internal errors, SQL, role codes, or secret data.
