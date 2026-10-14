# Publication verification — 14 October 2026

Scope: locked payroll, tracked adjustments, PDF payslips and CSV exports. No
payment/reconciliation lifecycle and no schema/migration changes. SMTP placeholders
are deliberate; Mailpit proves local delivery only. All verification data is synthetic.

## Published source revisions

- Backend `develop`: `4feea540537fcddb5a75b129533a5fbc64cd3072`.
- Frontend `person-c`: `03795156d140bf9ac4c9b306df3db1a1e67fcdfc`.
- Root publication branch: `person-c`; read its exact revision with `git rev-parse HEAD`.
  Its gitlinks must match the two SHAs above. Submodules are published first.

## Checks

| Check | Result |
|---|---|
| Root `sh scripts/verify.sh` | Passed; disposable project haris-payroll-verify |
| Backend gated database checks | 477 pass, 0 skip, 0 fail; 103 files |
| Frontend unit checks | 45 pass; lint and TypeScript passed |
| Chromium browser suite | 21 pass |
| WebKit payroll/mobile/organization lifecycle | 3 pass |
| Final production HTTPS browser rehearsal | 1 pass; secure session, CSRF, organization persistence |
| Production Compose build/start | All four services healthy after runtime/OS hardening |
| Runtime migration on an empty disposable database, then repeated | 36 tables, one migration journal row |
| Encrypted checkpoint restore | 45 document hashes, 66 bank decryptions, historical counts match checkpoint |
| Restored baseline/role browser checks | 11 pass |
| Restored immutable PDF check | 1 pass; same SHA256/net and unauthorized download denied |
| Root/submodule diff whitespace checks | Passed |

Recent additions check parent archival dependencies, organization duplicate codes
and pagination, legacy PDF upgrades/conflicts and voided/cross-employee reads.
The complete UI/API golden September flow yields net 2752.91; October yields
2901.66 with daily base earnings 2700, SS 135 and an approved once-only adjustment.

Logs on the verification host (not committed):
`/private/tmp/haris-root-verify-final-20261014.log`,
`/private/tmp/haris-production-final-20261014.log`,
`/private/tmp/haris-restore-latest-20261014.log`.
Browser artifacts use separate Chromium, WebKit and production report directories.

## Exact scanned production images

| Image suffix under haris-payroll-production-rehearsal | Image ID | Remaining High/Critical CVE IDs |
|---|---|---:|
| backend | sha256:390a7584b1c65675d4f93c1592ef68093a9e3ef8f6b88d9112d922845bfd560a | 0 |
| frontend | sha256:664d6f864f61b382729acf2117b32e99f9bb822bc4eea23e8d068b7324da2345 | 0 |
| gateway | sha256:deba113f7e6370d5d9b3f41a4e99df907d2160eefffa2f4ed4a584d7d0a2782a | 3 |
| postgres | sha256:ae27a531071f501861161b7e816ed10891ff203ef4811566ad1ce3f050536ac9 | 34 |

Scanner: Docker Scout 1.24.0, local image resolution, severity High/Critical;
metadata sharing explicitly approved by the user. No image push. Reports are
`/private/tmp/haris-{backend,frontend}-image-security-fixed-20261014.sarif` and
`/private/tmp/haris-{gateway,postgres}-image-security-final-20261014.sarif`.
Details and unresolved vendor findings: security-verification-2026-10-14.md.

## External acceptance gates

Remote CI and published clean-checkout results are recorded after publication.
Real provider TLS/monitoring/off-host retention and RPO/RTO, external SMTP recipient
verification, and signed five-role UAT remain operator/human responsibilities.
See uat-checklist.md. This publication does not claim 100% production acceptance
or blanket CVE risk acceptance.
