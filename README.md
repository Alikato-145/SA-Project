# Haris Payroll

## Development with Hot Reload

The default `compose.yaml` runs the frontend and backend in watch mode. Source
directories are bind-mounted, while dependencies and the Next.js cache use
Docker volumes so they are not mixed with host files.

```bash
cp .env.example .env
docker compose up --build
```

Changes under `frontend/` and `backend/src/` reload automatically. Polling is
enabled for Next.js so file changes are detected through Docker Desktop bind
mounts on Windows and macOS as well as Linux.

After all health checks pass:

- Frontend: <http://localhost>
- Backend: <http://localhost/api>
- Gateway health check: <http://localhost/healthz>

Only the gateway is publicly exposed. PostgreSQL is additionally bound to
`127.0.0.1:5432` for local database tools and is not reachable from other
machines. The frontend and backend communicate over the private
`haris_payroll_network` Docker network.

The backend applies pending Drizzle migrations automatically before starting.

```bash
docker compose down       # stop containers, preserve database data
docker compose down -v    # stop containers and remove database data
```

Dependencies are synchronized into their Docker volumes when containers start.
Rebuild the development images after changing a `Dockerfile.dev`:

```bash
docker compose up --build
```

## Production

Production uses optimized images: the frontend runs as a Next.js standalone
server and the backend runs without watch mode. It has a separate network and
database volume from development.

Stop the development stack before starting production because both bind the
same HTTP port.

```bash
docker compose -f compose.production.yaml up --build -d
docker compose -f compose.production.yaml down
```
