// Run with the bundled Node runtime and its NODE_PATH.
const fs = require('node:fs');
const path = require('node:path');
const { instance } = require('@viz-js/viz');
const sharp = require('sharp');
(async () => {
  const viz = await instance();
  const specs = JSON.parse(fs.readFileSync(path.join(__dirname, 'evidence/current20-model-diagrams.json'), 'utf8'));
  for (const spec of specs) {
    const svg = viz.renderString(spec.dot, { format: 'svg' });
    await sharp(Buffer.from(svg), { density: 200 }).resize({ width: 3200, withoutEnlargement: true }).png().toFile(path.join(__dirname, spec.out));
  }
  process.stdout.write(`Rendered ${specs.length} current model diagrams\n`);
})().catch(error => { process.stderr.write(`${error}\n`); process.exitCode = 1; });
