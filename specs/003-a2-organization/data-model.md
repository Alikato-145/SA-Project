# Data Model: A2 Organization Management

A2 uses the frozen existing schema and adds no migration.

## Shop

| Field | Contract rule |
|---|---|
| `id` | bigint; decimal string at API boundary |
| `code` | required, trimmed, max 30, globally unique |
| `name` | required, trimmed, max 150 |
| `is_active` | defaults true; false only through deactivate |
| timestamps | database timestamps; ISO strings in responses |

One shop has many branches and positions. Deactivation preserves both.

## Branch

| Field | Contract rule |
|---|---|
| `id` | bigint; decimal string at API boundary |
| `shop_id` | required active shop on create; immutable afterward |
| `code` | required, trimmed, max 30, unique with `shop_id` |
| `name` | required, trimmed, max 150 |
| `address` | optional text; trimmed; empty becomes null |
| `timezone` | valid IANA value, max 50; create default `Asia/Bangkok` |
| `is_active` | defaults true; false only through deactivate |

Effective usability is `branch.is_active AND shop.is_active`.

## Department

| Field | Contract rule |
|---|---|
| `id` | bigint; decimal string at API boundary |
| `branch_id` | required active branch whose shop is active; immutable afterward |
| `code` | required, trimmed, max 30, unique with `branch_id` |
| `name` | required, trimmed, max 100 |
| `is_active` | defaults true; false only through deactivate |

Effective usability is `department.is_active AND branch.is_active AND shop.is_active`.

## Position

| Field | Contract rule |
|---|---|
| `id` | bigint; decimal string at API boundary |
| `shop_id` | required active shop on create; immutable afterward |
| `code` | required, trimmed, max 30, unique with `shop_id` |
| `name` | required, trimmed, max 100 |
| `is_active` | defaults true; false only through deactivate |

Positions never contain compensation. Effective usability is
`position.is_active AND shop.is_active`.

## State transitions

```text
active --authorized deactivate(reason)--> inactive
inactive --ordinary A2 action-----------> no transition
```

A2 exposes no delete, reactivation, or re-parent transition.

## Scope projection

```text
all        → all shops/branches/departments/positions
branch     → granted branch, parent shop, branch departments, parent-shop positions
department → granted department, parent branch/shop, parent-shop positions
self       → empty without explicit A3 assignment context
```

Multiple grants form a union without widening an individual grant.

## Audit allowlists

```text
shop:       id, code, name, is_active
branch:     id, shop_id, code, name, address, timezone, is_active
department: id, branch_id, code, name, is_active
position:   id, shop_id, code, name, is_active
```
