# A4 Frontend View Model

A4 introduces no persistence model. These are safe UI-facing view models and transient states.

## Session capability

- Account ID and optional employee ID as decimal strings
- Username
- Active roles and scope labels
- Capability keys for presentation only
- Never contains cookie, token, password hash, or raw authorization internals

## Account summary

- Decimal-string ID
- Username and linked employee ID
- Active, disabled, or locked status
- Safe grant summaries with role and scope
- Never contains password or password hash

## Organization item

- Resource kind: shop, branch, department, position
- Decimal-string ID and parent identifiers
- Code, display name, active flag
- Optional timezone for branches
- Deactivation reason exists only in transient confirmation state

## Employee summary/profile

- Safe response fields as supplied by the role-specific API
- Decimal-string organization identifiers
- Status and optional current organization labels
- Optional masked identity values
- Missing protected fields remain absent, not blank placeholders

## Assignment history item

- IDs and employment type
- Exact decimal strings for base salary and welfare when authorized
- Inclusive effective-from and optional effective-to dates
- History action creates a new period and may close the prior period

## Bank account summary

- Metadata, last four digits, masked display
- Active and primary flags
- No plaintext number or ciphertext

## Weekly holiday item

- Weekday integer 0–6
- Inclusive effective dates
- Historical rows remain visible

## Onboarding draft

- Step: identity or employment options
- Employee identity/contact fields
- Initial assignment with exact decimal strings
- Optional transient bank plaintext
- Zero or more weekly holidays
- Optional account username
- Validation map and submit state

Plaintext bank input and any password are transient and cleared on completion, cancel, or unmount.

## Request state

- idle
- loading
- empty
- validation error
- conflict
- forbidden
- not found
- retryable error
- success
