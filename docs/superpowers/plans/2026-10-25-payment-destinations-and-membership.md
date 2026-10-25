# Payment Destinations and Membership Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Store explicit cash/transfer and PromptPay recipient phone, effective-dated social-security membership and correct frozen payroll membership/base snapshots.

**Architecture:** Add a narrowly authorized employee payment-destination operation, extend existing assignment history for membership, and carry membership through daily payroll projection/calculation. Do not read live employee details to reinterpret old payroll. Payment preparation/recipient snapshots and payroll_payments are implemented in Task7 before QR generation; Task8 adds paid/cancel transitions.

**Tech Stack:** Bun/Elysia/Drizzle/PostgreSQL16, Next.js16/React19, exact decimals.

**Spec:** `docs/superpowers/specs/2026-10-25-use-case-delivery-design.md`; follow-up migration concern in `docs/superpowers/plans/delivery-follow-up-notes.md`.

## Global Constraints

- PromptPay recipient phone is separate from contact phone; never copy employees.phone automatically.
- Accounting uses HR; HR/OWNER manage payment destinations, employee reads own, branch manager does not gain bank/account administration.
- Social-security deductions use summed daily base-salary earnings in the period, excluding welfare, OT and adjustments. Do not substitute contracted monthly salary.
- Membership changes use existing effective-dated assignment successor flow. Locked payroll never recalculates from current assignment/member status.
- One schema owner; root reviews/parity/apply only disposable DB. No bank integration or actual transfers.

## Review Focus

- Changing contact phone must not alter the registered payment recipient.
- A mid-period membership change must count only base earnings on covered days while grouping uses last covered assignment snapshot.
- Existing locked data must survive migration and the immutable trigger must remain enforced.
- HR/OWNER destination controls must not appear through manager profile-edit permission.
- Legacy records without the new earned-base snapshot must not silently become0 or contracted salary in reports.

### Task 1: Destination and effective membership vertical slice

**Files:**
- Extend owning employee schema/repository/service/controller/routes/mapper/DTO and focused tests. Add feature-prefixed payment helpers only if needed to keep functions focused.
- Extend employment-assignment schema/DTO/repository/service/history tests; retain existing authorization and lock ordering.
- Extend payroll schema/types/projection/calculator/repository/mapper/tests for daily membership and snapshots.
- Extend frontend employee profile payment controls, onboarding/assignment history inputs and relevant API contracts; add `frontend/e2e/payment-destination.e2e.ts`.
- Generate next serialized additive migration; root updates DBML/references and applies to disposable DB.

**Interfaces and rulings:**
- New shared payment_method enum cash/transfer. employees.payment_method required; default new employees to cash; backfill existing active-primary-bank employees to transfer, others cash. employees.promptpay_phone nullable canonical10-digit Thai mobile recipient.
- Accept canonical0-prefix phone and +66 form after stripping common separators; canonicalize to0-prefix and validate0[689] followed by8digits. Reject malformed values. Cash needs no phone/bank; transfer destination may be registered ahead of preparation. A missing recipient must later produce actionable preparation validation, never automatic contact-phone substitution.
- Dedicated GET/PUT `/api/v1/employees/:employee_id/payment-destination` (or existing employee-route ID parameter convention). GET self or HR/OWNER, PUT HR/OWNER only, server-side. Body payment_method and nullable promptpay_phone. Do not expand generic manager identity-update body to accept finance fields. Audit mutation without full bank details or secrets.
- employment_assignments.is_social_security_member required boolean DEFAULTtrue, preserving old all-member behavior. Include in onboarding/assignment DTOs with defaulttrue for existing clients and UI checkbox. A later change creates a successor effective-dated row; never overwrites historical rows.
- Payroll work-day projection carries membership from that date's assignment. Calculator accumulates qualifying base_salary earnings only on member days; returns socialSecurityBaseSnapshot exact money string. Existing social-security rate/cap rules remain. Do not change absence/leave/rounding policy in this task.
- payroll_records.is_social_security_member_snapshot boolean DEFAULTtrue required; social_security_base_snapshot numeric12,2 nullable for legacy rows, nonnegative when present. New calculations always write both. Snapshot member/branch context uses last covered assignment in the period (last employment day when terminated before month end), never a current assignment read months later.
- Preserve the locked-row trigger: do not disable it or UPDATE old locked records merely to backfill earned base. Existing boolean snapshot defaulttrue reflects prior policy; leave legacy earned-base NULL and document that Task9 reads frozen base_salary items as fallback. Never use0/default monthly salary as legacy earned-base fallback.
- Task7 consumes the authorized destination and locked membership/base snapshots and adds payroll_payments preparation/frozen recipient values. No unused generic snapshot framework or QR code in this task.

- [ ] Read AGENTS/Next docs; write failing phone normalization/separation, payment-role denial and effective-membership payroll tests. Cases: fully nonmember yields0SS; midperiod covered bases only; welfare/OT/adjustments excluded; existing default member calculations preserved. Capture realRED.
- [ ] Generate additive migration with documented backfill/defaults and intact immutable trigger. Send root SQL handoff before apply; no production or independent migration execution.
- [ ] Implement destination endpoint and scoped frontend editor/own read. Reuse existing transaction/audit and mapper boundaries. Verify employee/manager cannot mutate another destination by crafted API calls.
- [ ] Implement assignment history field and daily payroll projection/calculator/snapshots. Test membership successor leaves old range/history intact, new computed snapshot remains unchanged after later assignment edits, legacy locked snapshots stay nullable and old net/items unchanged.
- [ ] Run focused tests/types then real disposable browser: HR registers a recipient, changes contact phone separately and reloads destination unchanged; OWNER changes membership through dated assignment successor; employee ownread allowed and others denied. Prove cash withoutphone accepted and invalid transfer phone rejected.
- [ ] After root migration/parity, run fullDB and frontend unit/lint/typecheck sequentially with browser. Report `docs/superpowers/reports/06-payment-destinations-and-membership.md`, exact commands, evidence and remaining Task7 preparation/QR and Task9 export boundaries. Fresh review before scoped commits; no push/rootgitlink updates.
