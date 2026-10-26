// Read-only catalog/sample verification for the isolated academic report.
import { getTableConfig, PgTable } from "/app/node_modules/drizzle-orm/pg-core/index.js";
import { is } from "/app/node_modules/drizzle-orm/index.js";
import * as schema from "/app/src/db/schema";
import { pool, closeDatabase } from "/app/src/core/db/client";

const url = new URL(process.env.DATABASE_URL ?? "http://missing");
if (process.env.RELEASE_DISPOSABLE_DB !== "1" || url.hostname !== "postgres") throw new Error("Disposable verification stack required");
const tables = [];
try {
  for (const table of Object.values(schema)) {
    if (!is(table, PgTable)) continue;
    const cfg = getTableConfig(table);
    const columns = cfg.columns.map(c => ({ name: c.name, type: c.getSQLType(), notNull: c.notNull, pk: c.primary, unique: c.isUnique, enumValues: c.enumValues ?? null }));
    const constraints = (await pool.query("select conname as name, contype as kind, pg_get_constraintdef(oid) as definition from pg_constraint where conrelid=$1::regclass order by conname", [cfg.name])).rows;
    const actual = (await pool.query("select a.attname as name,format_type(a.atttypid,a.atttypmod) as type,a.attnotnull as not_null from pg_attribute a where a.attrelid=$1::regclass and a.attnum>0 and not a.attisdropped order by a.attnum", [cfg.name])).rows;
    if (actual.length !== columns.length || columns.some(c => !actual.some(a => a.name === c.name && a.not_null === c.notNull))) throw new Error(`Drizzle/catalog mismatch: ${cfg.name}`);
    const indexes = (await pool.query("select indexname as name,indexdef as definition from pg_indexes where schemaname='public' and tablename=$1 order by indexname", [cfg.name])).rows;
    const count = Number((await pool.query(`select count(*) as count from "${cfg.name}"`)).rows[0].count);
    tables.push({ name: cfg.name, columns, constraints, indexes, actual, count });
  }
  const enums = (await pool.query("select t.typname as name,array_agg(e.enumlabel order by e.enumsortorder) as values from pg_type t join pg_enum e on e.enumtypid=t.oid join pg_namespace n on n.oid=t.typnamespace where n.nspname='public' group by t.typname order by t.typname")).rows;
  for (const entry of enums) if (typeof entry.values === "string") entry.values = entry.values.slice(1, -1).split(",");
  const migrations = Number((await pool.query('select count(*) as count from drizzle.__drizzle_migrations')).rows[0].count);
  const queries = [
    { id: "Q020", uc: ["UC12"], name: "อ่านคำขอเงินกู้โดยไม่เปิดเผยข้อมูลรับรอง", tables: ["loan_requests"], sql: 'select id,employee_id,principal_amount,installment_count,status,loan_id from loan_requests order by id limit $1', params: [5] },
    { id: "Q021", uc: ["UC18"], name: "อ่านสถานะและยอด snapshot การจ่าย", tables: ["payroll_payments"], sql: 'select id,payroll_record_id,branch_id_snapshot,payment_method,amount,status from payroll_payments order by id limit $1', params: [5] },
    { id: "Q022", uc: ["UC01"], name: "นับประวัติเพิกถอน session โดยไม่เปิดเผย token หรือ hash", tables: ["revoked_session_tokens"], sql: 'select count(*) as revoked_count from revoked_session_tokens where expires_at > $1::timestamptz', params: [new Date().toISOString()] },
    { id: "Q023", uc: ["UC12"], name: "ตรวจเหตุผลใหม่และ legacy โดยไม่แสดงข้อความส่วนบุคคล", tables: ["advance_requests"], sql: 'select (reason is null) as legacy_reason,count(*) as count from advance_requests group by (reason is null) order by legacy_reason', params: [] },
    { id: "Q024", uc: ["UC15", "UC18"], name: "อ่าน earned-base และสมาชิก snapshot ที่ล็อกแล้ว", tables: ["payroll_records"], sql: 'select id,is_social_security_member_snapshot,social_security_base_snapshot,net_pay from payroll_records where status=$1 order by id limit $2', params: ["locked", 5] },
  ];
  const entries = [];
  for (const q of queries) {
    const result = await pool.query(q.sql, q.params);
    entries.push({ ...q, source: "Read-only catalog acceptance query; not a service authorization test", verified: true, resultCount: result.rows.length, rows: result.rows });
  }
  const foreignKeys = tables.reduce((n, t) => n + t.constraints.filter(c => c.kind === "f").length, 0);
  if (tables.length !== 39 || foreignKeys !== 91 || enums.length !== 25 || migrations !== 7) throw new Error("Unexpected current model counts");
  await Bun.write("/tmp/current20-model.json", JSON.stringify({ verifiedAt: new Date().toISOString(), database: "haris-payroll-verify / PostgreSQL 16", policy: "Read only; protected session data has aggregate evidence only; no fabricated sample rows", tables, enums, migrations, foreignKeys, entries }, null, 2));
  console.log(JSON.stringify({ tables: tables.length, foreignKeys, enums: enums.length, migrations, queries: entries.length }));
} finally { await closeDatabase(); }
