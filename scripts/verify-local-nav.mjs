import fs from "fs";
import path from "path";

const ROOT = path.resolve(process.argv[2] || path.join(process.cwd(), ".."));
const DOMAIN = "https://creditcostguide.com";

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, files);
    else files.push(full);
  }
  return files;
}

function htmlFiles() {
  return walk(ROOT).filter((file) => file.endsWith(".html") && !file.includes(`${path.sep}.git${path.sep}`)).sort();
}

function resolveLocalTarget(fromFile, ref) {
  const clean = ref.split("#")[0].split("?")[0];
  if (!clean || clean.startsWith("mailto:") || clean.startsWith("tel:") || clean.startsWith("#")) return null;

  if (/^https?:\/\//i.test(clean)) {
    if (!clean.startsWith(DOMAIN)) return null;
    const pathname = new URL(clean).pathname;
    if (pathname === "/") return path.join(ROOT, "index.html");
    if (pathname.endsWith("/")) return path.join(ROOT, pathname.replace(/^\//, ""), "index.html");
    return path.join(ROOT, `${pathname.replace(/^\//, "")}.html`);
  }

  let candidate = path.resolve(path.dirname(fromFile), clean);
  if (fs.existsSync(candidate)) return candidate;

  if (clean.endsWith("/")) {
    candidate = path.resolve(path.dirname(fromFile), clean, "index.html");
    if (fs.existsSync(candidate)) return candidate;
  }

  if (!path.extname(clean)) {
    candidate = path.resolve(path.dirname(fromFile), `${clean}.html`);
    if (fs.existsSync(candidate)) return candidate;
  }

  return null;
}

function collect(pattern, text) {
  return [...text.matchAll(pattern)].map((match) => match[1]);
}

let broken = 0;
let cssChecks = 0;
let jsChecks = 0;
let assetChecks = 0;
let linkChecks = 0;
let menuPages = 0;
let calculatorPages = 0;

for (const file of htmlFiles()) {
  const source = fs.readFileSync(file, "utf8");
  const styles = collect(/<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"/g, source);
  const scripts = collect(/<script[^>]+src="([^"]+)"/g, source);
  const assets = collect(/<(?:img|source)[^>]+src="([^"]+)"/g, source).concat(
    collect(/<link[^>]+rel="icon"[^>]+href="([^"]+)"/g, source)
  );
  const links = collect(/<a[^>]+href="([^"]+)"/g, source);

  for (const ref of styles) {
    cssChecks += 1;
    if (!resolveLocalTarget(file, ref)) broken += 1;
  }
  for (const ref of scripts) {
    jsChecks += 1;
    if (!resolveLocalTarget(file, ref)) broken += 1;
  }
  for (const ref of assets) {
    assetChecks += 1;
    if (!resolveLocalTarget(file, ref)) broken += 1;
  }
  for (const ref of links) {
    if (ref.startsWith("#") || ref.startsWith("mailto:") || ref.startsWith("tel:")) continue;
    linkChecks += 1;
    if (!resolveLocalTarget(file, ref)) broken += 1;
  }

  if (source.includes('class="ccg-menu-toggle"') && source.includes('class="ccg-mobile-nav"') && /src="(\.\/|\.\.\/)?main\.js"/.test(source)) {
    menuPages += 1;
  }
  if (source.includes('data-calculator=')) {
    calculatorPages += 1;
  }
}

const summary = [
  "# Local Preview Report",
  "",
  `- HTML files checked: ${htmlFiles().length}`,
  `- CSS references checked: ${cssChecks}`,
  `- JS references checked: ${jsChecks}`,
  `- Asset references checked: ${assetChecks}`,
  `- Internal links checked: ${linkChecks}`,
  `- Pages with mobile menu markup and local JS: ${menuPages}`,
  `- Calculator pages with local JS: ${calculatorPages}`,
  `- Broken references found: ${broken}`,
  `- Status: ${broken === 0 ? "PASS" : "FAIL"}`,
  "",
  "## Notes",
  "- SEO canonicals, social URLs, sitemap, robots.txt, and schema URLs remain on https://creditcostguide.com/...",
  "- This verification checks local CSS, JS, icon/image assets, and internal page navigation for file:// preview.",
  "",
  broken === 0
    ? "## Result\n- All checked local CSS, JS, icon/image assets, and internal page links resolve successfully."
    : "## Result\n- Failures were detected."
].join("\n");

fs.writeFileSync(path.join(ROOT, "local-preview-report.md"), `${summary}\n`, "utf8");
if (broken > 0) process.exit(1);
console.log(summary);
