import { expect, test } from "bun:test";
import { copyFile, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

// Execute the real wrappers; stub only external Docker/Bun commands, never a DB or browser.
const cases = [
  { name: "defaults target the same isolated stack and browser", entry: "full-uat.sh", env: {}, compose: "compose|18083|55440|18025", browser: "browser|http://localhost:18083|18083|55440|18025", exit: 0 },
  { name: "verify overrides reach both stack creation and browser", entry: "verify.sh", env: { VERIFY_HTTP_PORT: "18084", VERIFY_POSTGRES_PORT: "55441", VERIFY_MAIL_PORT: "18026" }, compose: "compose|18084|55441|18026", browser: "browser|http://localhost:18084|18084|55441|18026", exit: 0 },
  { name: "standalone wrapper also honors verify overrides", entry: "full-uat.sh", env: { VERIFY_HTTP_PORT: "18084", VERIFY_POSTGRES_PORT: "55441", VERIFY_MAIL_PORT: "18026" }, compose: "compose|18084|55441|18026", browser: "browser|http://localhost:18084|18084|55441|18026", exit: 0 },
  { name: "inherited stack ports take precedence over verify fallbacks", entry: "full-uat.sh", env: { HTTP_PORT: "18085", POSTGRES_PORT: "55442", VERIFY_HTTP_PORT: "18084", VERIFY_POSTGRES_PORT: "55441", VERIFY_MAIL_PORT: "18027" }, compose: "compose|18085|55442|18027", browser: "browser|http://localhost:18085|18085|55442|18027", exit: 0 },
  { name: "browser failure exit code propagates through verify entrypoint", entry: "verify.sh", env: { STUB_BROWSER_EXIT: "17", VERIFY_MAIL_PORT: "18025" }, compose: "compose|18083|55440|18025", browser: "browser|http://localhost:18083|18083|55440|18025", exit: 17 },
];

for (const scenario of cases) test(scenario.name, async () => {
  const directory = await mkdtemp(join(tmpdir(), "haris-uat-wrapper-"));
  try {
    await Promise.all(["scripts", "frontend", "bin"].map(name => mkdir(join(directory, name))));
    for (const script of ["full-uat.sh", "verify.sh"]) await copyFile(new URL(script, import.meta.url), join(directory, "scripts", script));
    await writeFile(join(directory, "bin/docker"), '#!/bin/sh\nprintf "compose|%s|%s|%s\\n" "$HTTP_PORT" "$POSTGRES_PORT" "$VERIFY_MAIL_PORT" >> "$CALLS_FILE"\n', { mode: 0o755 });
    await writeFile(join(directory, "bin/bun"), '#!/bin/sh\nif [ "$1" = run ] && [ "$2" = test:e2e ]; then\n  printf "browser|%s|%s|%s|%s\\n" "$E2E_BASE_URL" "$HTTP_PORT" "$POSTGRES_PORT" "$VERIFY_MAIL_PORT" >> "$CALLS_FILE"\n  printf "color|%s|%s\\n" "${NO_COLOR:-unset}" "${FORCE_COLOR:-unset}" >> "$CALLS_FILE"\n  exit "${STUB_BROWSER_EXIT:-0}"\nfi\n', { mode: 0o755 });
    const env: Record<string, string | undefined> = { ...process.env };
    for (const name of ["HTTP_PORT", "POSTGRES_PORT", "VERIFY_HTTP_PORT", "VERIFY_POSTGRES_PORT", "VERIFY_MAIL_PORT", "VERIFY_BROWSER", "E2E_BASE_URL", "STUB_BROWSER_EXIT"]) delete env[name];
    Object.assign(env, scenario.env, { PATH: `${join(directory, "bin")}:/usr/bin:/bin`, CALLS_FILE: join(directory, "calls"), NO_COLOR: "1", FORCE_COLOR: "1" });
    const child = Bun.spawn(["/bin/sh", join(directory, "scripts", scenario.entry)], { cwd: directory, env, stdout: "pipe", stderr: "pipe" });
    const [exit, stdout, stderr] = await Promise.all([child.exited, new Response(child.stdout).text(), new Response(child.stderr).text()]);
    expect(exit, stdout + stderr).toBe(scenario.exit);
    const calls = (await readFile(join(directory, "calls"), "utf8")).trim().split("\n");
    expect(calls.filter(line => line.startsWith("browser|"))).toEqual([scenario.browser]);
    expect(calls.filter(line => line.startsWith("color|"))).toEqual(["color|unset|unset"]);
    const compose = calls.filter(line => line.startsWith("compose|"));
    expect(compose.length).toBeGreaterThan(0);
    for (const line of compose) expect(line).toBe(scenario.compose);
  } finally { await rm(directory, { recursive: true, force: true }); }
});
