# Employee Context Integration Contract

EmployeeOperationContextService.context(employeeId, date) resolves the effective assignment for a business date, returning employee, branch, department, shop, and base salary. Missing context raises PAYROLL_ASSIGNMENT_MISSING; consumers must not substitute today's assignment.

assertEmployee(actor, employeeId, date, action) checks grants against that dated branch/department. Employee self grants permit own read/submit only. Department grants require both branch and department. Branch grants require branch. HR and owner all-scope grants span branches. Finance remains global-duty-only. An account ID is not an employee ID. Attendance retains the work-day branch snapshot; payroll uses effective compensation and exact decimals. A5 adds no HTTP/persistence contract.
