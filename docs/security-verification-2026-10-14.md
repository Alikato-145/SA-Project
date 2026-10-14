# Security verification — 14 October 2026

Checks ran against synthetic localhost stacks. No production user data, real SMTP
credentials, or real bank details were used. Schema and migrations were unchanged.

## Dependency changes and evidence

The registry audit reported vulnerable dependency versions. Updated:

| Package | Before | Locked after |
|---|---|---|
| Next.js / eslint-config-next | 16.3.4 | 16.3.8 |
| Drizzle ORM | 0.44.7 | 0.45.4 |
| Sharp | 0.35.4 | 0.35.5 |
| source-map-js | 1.2.1 | 1.2.2 |
| brace-expansion | 1.1.18 / 5.0.9 | 1.1.21 / 5.0.12 |

Primary advisories: [Next.js ImageResponse](https://github.com/advisories/GHSA-vcvr-r3jv-pc5j),
[Drizzle identifier escaping](https://github.com/advisories/GHSA-gpj5-g38j-94v9),
[Sharp librsvg](https://github.com/advisories/GHSA-wq5f-xc86-pv6w).
The Next.js advisory describes a particular attacker-controlled SVG use case;
the app does not have an ImageResponse route. Updating still removes the affected
version and the other registry-reported Next.js advisories.

`shadcn` is a generation CLI and has no application imports; it now belongs in
devDependencies. No new library or dependency override was introduced.

Production-only graphs were resolved in private temporary directories from copies
of each package's manifest/lockfile, with devDependencies removed and install
scripts disabled. `bun audit --json` returned `{}` with exit code 0 for both.
This is an npm dependency check, not an OS/image scan or a guarantee against all
vulnerabilities. The actual upgraded stacks passed 472 database-gated backend
checks, 45 frontend checks, and 20 browser cases; production image startup and TLS
login are checked separately.

## Remaining development-tool advisories

The full workspace graph still reports:

- `braces@3.0.3`: high severity; audit reports no published fixed version. It is
  reached through development file/glob tooling (nodemon/chokidar and frontend
  tooling). Do not process untrusted glob patterns through these tools.
- `esbuild@0.18.20`: moderate severity through drizzle-kit's esbuild-kit dependency,
  whose range blocks the safe version. The application does not run its development
  HTTP server. Keep it as development migration tooling; do not expose that server.

These were not hidden with an audit ignore or forced incompatible override.
Maintainer follow-up remains required when upstream versions become available.

## Authorized image scans and fixes

The user authorized only SBOM/image/package metadata for CVE scanning, with no
image push. After Docker Desktop login, local image scans completed. No image was
pushed to a registry. Counts below are unique High/Critical CVE IDs, not SARIF
result rows (one advisory may produce multiple package/version matches).

| Production image | Before | After | Change |
|---|---:|---:|---|
| Backend | 71 | 0 | Production-only dependencies; existing SQL applied by ORM migrator instead of shipping Drizzle Kit/esbuild/nodemon; Alpine patch upgrade |
| Frontend | 11 | 0 | Remove unused npm/corepack from Node runtime; Alpine patch upgrade |
| Gateway | 35 | 3 | Nginx stable 1.30.5 instead of 1.27; Alpine patch upgrade |
| PostgreSQL | 35 | 34 | Retain supported major 16; Alpine patch upgrade |

These are scan results on 14 October, not a guarantee against unknown flaws.
Final backend/frontend scans did not hide findings with package/base-image ignores.
Scanner metadata and report locations are recorded in release-verification-2026-10-14.md.

### Unresolved vendor-image findings

- Gateway: `libxml2@2.13.9-r2` (CVE-2026-86140, no fix reported) and
  `expat@2.8.5-r0` (CVE-2026-102633/CVE-2026-77214, scanner lists 2.9.0-r0;
  the current Alpine repository upgrade only supplied 2.8.5-r0).
- PostgreSQL: the same unfixed libxml2 advisory plus 33 Go stdlib advisories for
  embedded Go 1.24.6. The official PostgreSQL 16 image pull was already current.
  Presence in a binary does not establish reachability, and no applicability
  exception has been claimed. Preserve the inventory for upstream/vendor review.

The infrastructure owner must select a reviewed vendor patch/image or document
risk acceptance before real production use. Authorization to share scan metadata
is not acceptance of these CVEs. We did not change PostgreSQL major, rewrite the
vendor entrypoint or silently suppress its findings.

The production migrator uses the [official Drizzle runtime migration API](https://orm.drizzle.team/docs/migrations).
An empty disposable database and a second invocation both passed: 36 public tables,
one migration journal row. The existing migration SQL/schema files were not changed.

## Other checks

- Local production TLS: Secure/HttpOnly/SameSite=Lax session, CSRF rejection,
  health headers and organization persistence; restart rehearsal passed.
- Login throttle: 30 synthetic invalid requests from a separate container IP
  returned 21 HTTP 401 and 9 HTTP 429 with RATE_LIMITED.
- Database outage on the restore stack: live=200, ready=503, recovered ready=200.
- Encrypted latest checkpoint: 45 document hashes and 66 bank decryptions verified;
  every checked historical table count matched source. Restored PDF download
  retained its hash and locked net; unauthenticated download was rejected.
- Restore explicitly clears SMTP credentials. Example env values are mock
  placeholders at the user's request; external inbox delivery is unverified.
