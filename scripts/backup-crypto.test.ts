import { expect, test } from "bun:test";
import { mkdtemp, readFile, writeFile, readdir, rm } from "node:fs/promises";
import { randomBytes } from "node:crypto";
import { tmpdir } from "node:os";
import { join } from "node:path";
// @ts-expect-error standalone operator script has no generated declaration
import { protectBackup } from "./backup-crypto.mjs";

test("backup encryption restores exact bytes and rejects tampering, wrong keys and overwrites", async () => {
  const dir = await mkdtemp(join(tmpdir(), "haris-backup-crypto-"));
  try {
    const input = join(dir, "input"), encrypted = join(dir, "encrypted"), restored = join(dir, "restored"), key = join(dir, "key"), wrongKey = join(dir, "wrong-key");
    const content = randomBytes(1024 * 1024 + 3);
    await writeFile(input, content, { mode: 0o600 });
    await writeFile(key, randomBytes(32).toString("hex"), { mode: 0o600 });
    await writeFile(wrongKey, randomBytes(32).toString("hex"), { mode: 0o600 });
    await protectBackup("encrypt", input, encrypted, key);
    await protectBackup("decrypt", encrypted, restored, key);
    expect((await readFile(restored)).equals(content)).toBe(true);
    await expect(protectBackup("decrypt", encrypted, restored, key)).rejects.toThrow();
    expect((await readFile(restored)).equals(content)).toBe(true);
    await expect(protectBackup("decrypt", encrypted, join(dir, "wrong-result"), wrongKey)).rejects.toThrow();
    const damaged = await readFile(encrypted); damaged[30] ^= 1;
    await writeFile(encrypted, damaged);
    await expect(protectBackup("decrypt", encrypted, join(dir, "damaged-result"), key)).rejects.toThrow();
    expect(await readdir(dir)).not.toContain("damaged-result");
    expect((await readdir(dir)).some(file => file.endsWith(".partial"))).toBe(false);
  } finally { await rm(dir, { recursive: true, force: true }); }
});
