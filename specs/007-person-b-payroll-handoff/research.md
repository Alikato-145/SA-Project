# B5 Research

- `LeaveService.approveLeave` already passes `session.transaction` into `LeaveAttendanceEffect.applyApprovedLeave`; its transaction wraps quota, daily leave rows, attendance effect, decision, and approval action.
- `AttendanceService.findForPayrollRange` is bounded but does not count worked days. `AdvanceService` asks an injected eligibility provider to return that count and effective base salary.
- `OvertimeRepository.findApproved`, `LeaveRepository.findApprovedDays`, and `AdvanceRepository.findApprovedForMonth` filter approved status. `LoanRepository.findDue` filters scheduled installments. Debt candidate filtering is read-only because the append-only trigger blocks settlement-field updates.
- No Person A auth/assignment service or Person C payroll service/app composition exists yet in this checkout. B5 can provide concrete B-owned adapters and a handoff, not an end-to-end payroll demo.
