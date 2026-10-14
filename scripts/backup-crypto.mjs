import { createCipheriv, createDecipheriv, randomBytes } from "node:crypto";
import { createReadStream, createWriteStream } from "node:fs";
import { open, readFile, rename, stat, unlink } from "node:fs/promises";
import { pipeline } from "node:stream/promises";
import { pathToFileURL } from "node:url";

const magic = Buffer.from("HARISBK1");
const headerSize = magic.length + 12;

export async function protectBackup(mode, input, output, keyPath) {
  if (!["encrypt", "decrypt"].includes(mode)) throw new Error("Use encrypt or decrypt.");
  const keyInfo = await stat(keyPath);
  if (!keyInfo.isFile() || (keyInfo.mode & 0o077) || keyInfo.size > 128) throw new Error("Key must be a private regular file (mode 600).");
  const encoded = (await readFile(keyPath, "utf8")).trim();
  if (!/^[0-9a-f]{64}$/i.test(encoded)) throw new Error("Key must contain 32 random bytes as hex.");
  const key = Buffer.from(encoded, "hex");
  const source = await open(input, "r");
  // Authenticate into a private temporary file; publish plaintext only after verification.
  const temporary = `${output}.${randomBytes(8).toString("hex")}.partial`;
  let destination;
  try {
    destination = await open(temporary, "wx", 0o600);
    if (mode === "encrypt") {
      const header = Buffer.concat([magic, randomBytes(12)]);
      const cipher = createCipheriv("aes-256-gcm", key, header.subarray(magic.length));
      cipher.setAAD(header);
      await destination.write(header);
      await pipeline(createReadStream(input), cipher, createWriteStream(temporary, { flags: "r+", start: headerSize }));
      await destination.write(cipher.getAuthTag(), 0, 16, (await destination.stat()).size);
    } else {
      const size = (await source.stat()).size;
      if (size < headerSize + 16) throw new Error("Invalid encrypted backup.");
      const header = Buffer.alloc(headerSize), tag = Buffer.alloc(16);
      await source.read(header, 0, headerSize, 0);
      await source.read(tag, 0, 16, size - 16);
      if (!header.subarray(0, magic.length).equals(magic)) throw new Error("Unsupported backup format.");
      const decipher = createDecipheriv("aes-256-gcm", key, header.subarray(magic.length));
      decipher.setAAD(header); decipher.setAuthTag(tag);
      await pipeline(createReadStream(input, { start: headerSize, end: size - 17 }), decipher, createWriteStream(temporary, { flags: "r+" }));
    }
    await destination.close(); destination = undefined;
    // Reserve the destination to prevent replacing an existing backup.
    const reserved = await open(output, "wx", 0o600); await reserved.close();
    try { await rename(temporary, output); } catch (error) { await unlink(output); throw error; }
  } finally {
    key.fill(0); await source.close(); await destination?.close();
    await unlink(temporary).catch(error => { if (error.code !== "ENOENT") throw error; });
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [mode, input, output, keyPath] = process.argv.slice(2);
  if (!mode || !input || !output || !keyPath) throw new Error("Usage: bun scripts/backup-crypto.mjs encrypt|decrypt input output private-key-file");
  await protectBackup(mode, input, output, keyPath);
}
