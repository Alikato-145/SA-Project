# Haris Payroll

## Run the complete stack

The default values are suitable for local development. To customize database
credentials, copy the environment template first:

```bash
cp .env.example .env
docker compose up --build
```

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
