# B2 Data Model

Frozen entities: leave request and dated child days; annual employee/type quota;
append-only leave actions; unique employee/date OT record; append-only OT actions.

Leave transitions are `pending → approved|rejected`; OT transitions are
`pending → approved|rejected`. Approval actions are immutable. Leave approval locks
the quota row and applies quota and attendance changes in the same transaction.

Hourly OT stores positive hours. Rest-day and public-holiday OT store day units in
the range `(0, 1]`. The employee/date uniqueness prevents mixed OT types for a day.
