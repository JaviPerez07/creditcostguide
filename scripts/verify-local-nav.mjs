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

function toPosix(value) {
  return value.split(path.sep).join("/");
}

function htmlFiles() {
  return walk(ROOT).filter((file) => file.endsWith(".html")).sort();
}

function fileExistsFrom(fromFile, relPath) {
  const clean = relPath.split("#")[0].split("?")[0];
  const target = path.resolve(path.dirname(fromFile), clean);
  return fs.existsSync(target) ? target : null;
}

function collect(pattern, text) {
  return [...text.matchAll(pattern)].map((match) => match[1]);
}

const failures = [];
let broken = 0;
let cssChecks = 0;
let jsChecks = 0;
let assetChecks = 0;
let linkChecks = 0;
let calculatorPages = 0;
let menuPages = 0;

for (const file of htmlFiles()) {
  const html = fs.readFileSync(file, "utf8");
  const relFile = toPosix(path.relative(ROOT, file));
  const pageFailures = [];

  const stylesheetMatches = collect(/<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"/g, html);
  const scriptMatches = collect(/<script[^>]+src="([^"]+)"/g, html);
  const imageMatches = collect(/<(?:img|source)[^>]+src="([^"]+)"/g, html)
    .concat(collect(/<link[^>]+rel="icon"[^>]+href="([^"]+)"/g, html));
  const anchorMatches = collect(/<a[^>]+href="([^"]+)"/g, html);

  const assetRefs = [
    ...stylesheetMatches.map((value) => ["CSS", value]),
    ...scriptMatches.map((value) => ["JS", value]),
    ...imageMatches.map((value) => ["Asset", value]),
  ];

  for (const [label, ref] of assetRefs) {
    if (/^(https?:)?\/\//.test(ref)) {
      if (!ref.startsWith(DOMAIN)) continue;
      pageFailures.push(`- ${label}: absolute site asset left in local HTML -> ${ref}`);
      broken += 1;
      continue;
    }
    const resolved = fileExistsFrom(file, ref);
    if (!resolved) {
      pageFailures.push(`- ${label}: missing ${ref}`);
      broken += 1;
    }
    if (label === "CSS") cssChecks += 1;
    if (label === "JS") jsChecks += 1;
    if (label === "Asset") assetChecks += 1;
  }

  for (const ref of anchorMatches) {
    if (!ref || ref.startsWith("#") || ref.startsWith("mailto:") || ref.startsWith("tel:")) continue;
    if (/^(https?:)?\/\//.test(ref)) {
      if (ref.startsWith(DOMAIN)) {
        pageFailures.push(`- Link: absolute site URL left in local HTML -> ${ref}`);
        broken += 1;
      }
      continue;
    }
    const resolved = fileExistsFrom(file, ref);
    if (!resolved) {
      pageFailures.push(`- Link: missing ${ref}`);
      broken += 1;
    }
    linkChecks += 1;
  }

  if (html.includes('class="ccg-menu-toggle"') && html.includes('class="ccg-mobile-nav"') && /src="(\.\/|\.\.\/)main\.js"/.test(html)) {
    menuPages += 1;
  } else {
    pageFailures.push("- Navigation: mobile menu markup or local main.js reference missing");
    broken += 1;
  }

  if (html.includes('data-calculator=')) {
    calculatorPages += 1;
    if (!/src="(\.\/|\.\.\/)main\.js"/.test(html)) {
      pageFailures.push("- Calculator: page is missing a local main.js reference");
      broken += 1;
    }
  }

  if (pageFailures.length) {
    failures.push(`## ${relFile}\n${pageFailures.join("\n")}\n`);
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
  "- Calculator pages still point to local main.js, which preserves calculator behavior and mobile navigation in preview mode.",
  "",
  broken === 0
    ? "## Result\n- All checked local CSS, JS, icon/image assets, and internal page links resolve successfully."
    : "## Failures",
  ...(broken === 0 ? [] : failures)
].join("\n");

const reportPath = path.join(ROOT, "local-preview-report.md");
fs.writeFileSync(reportPath, summary + "\n", "utf8");

if (broken > 0) {
  console.error(summary);
  process.exit(1);
}

console.log(summary);
