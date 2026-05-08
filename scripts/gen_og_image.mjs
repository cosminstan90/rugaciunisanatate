/**
 * Generate OG image PNG (1200×630) from the existing SVG.
 *
 * Usage:
 *   node scripts/gen_og_image.mjs
 *
 * Requirements:
 *   npm install --save-dev sharp
 *
 * Output: public/og-default.png  (Facebook, LinkedIn, Twitter require PNG/JPEG)
 *
 * After running, commit: git add public/og-default.png && git commit -m "Add OG image PNG"
 */

import { readFileSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

async function main() {
  let sharp;
  try {
    const mod = await import("sharp");
    sharp = mod.default;
  } catch {
    console.error("❌ sharp not installed. Run: npm install --save-dev sharp");
    process.exit(1);
  }

  const svgPath = join(root, "public", "og-default.svg");
  const pngPath = join(root, "public", "og-default.png");

  console.log("Reading SVG...");
  const svgBuffer = readFileSync(svgPath);

  console.log("Converting to PNG 1200×630...");
  await sharp(svgBuffer)
    .resize(1200, 630)
    .png({ quality: 90, compressionLevel: 8 })
    .toFile(pngPath);

  const size = readFileSync(pngPath).length;
  console.log(`✅ Saved: public/og-default.png (${(size / 1024).toFixed(1)} KB)`);
  console.log("");
  console.log("Next steps:");
  console.log("  1. Update SeoHead.astro: defaultOgImage → /og-default.png");
  console.log("  2. git add public/og-default.png && git commit -m 'Add OG image PNG'");
  console.log("  3. git push && server: git pull && npm run build && pm2 restart rugaciunisanatate");
}

main().catch(console.error);
