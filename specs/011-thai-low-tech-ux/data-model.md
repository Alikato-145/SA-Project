# Presentation Model: Thai Low-Tech UX Across the Application

No persistence model changes are required. These view-level concepts are derived from existing authenticated and feature data.

## Page Context

| Field | Meaning | Rule |
|---|---|---|
| Page title | The user-facing Thai name of the current workspace | Present on every route. |
| Purpose | One short Thai sentence explaining why the page exists | Uses plain language, not implementation or role codes. |
| Role context | Safe current account and permitted work context | Never expands server-side scope. |
| Primary action | The next safe action a user can take | Hidden when not permitted or not meaningful in the current state. |

## Feedback State

| State | Required user information |
|---|---|
| Loading | What is loading and that no result is ready yet. |
| Empty | Whether no data exists and the next available action. |
| No result | The active filter produced no match and how to change it. |
| Success | What was saved or completed and the next sensible action. |
| Warning | What may affect the result before the user proceeds. |
| Denied | That the account cannot access the area, with a route back to available work. |
| Error | The cause when safely known and how to recover. |
| Final | That a record is approved, rejected, locked, or otherwise immutable and the permitted correction path. |

## Status Display

Every stateful record uses a Thai label plus text context. Raw identifier or code remains secondary information only when a support or administrative task genuinely needs it.
