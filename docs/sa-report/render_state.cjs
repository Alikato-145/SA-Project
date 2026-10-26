// Use the workspace dependency runtime and set NODE_PATH to its package directory.
const fs = require('node:fs');
const path = require('node:path');
const { instance } = require('@viz-js/viz');
const sharp = require('sharp');
(async () => {
  const viz = await instance();
  const specs = JSON.parse(fs.readFileSync(path.join(__dirname, 'evidence/senior-template-diagrams.json'), 'utf8'));
  for (const spec of specs) {
    const svg = viz.renderString(spec.dot, { format: 'svg' });
    await sharp(Buffer.from(svg), { density: 200 }).png().toFile(path.join(__dirname, 'figures', path.basename(spec.out)));
  }
  process.stdout.write(`Rendered ${specs.length} state diagrams\n`);
})().catch(error => { process.stderr.write(`${error}\n`); process.exitCode = 1; });
