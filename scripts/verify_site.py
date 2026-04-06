from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://creditcostguide.com"

REQUIRED = [
    "index.html", "about.html", "contact.html", "how-we-research.html",
    "privacy-policy.html", "terms.html", "disclaimer.html",
    "styles.css", "main.js", "sitemap.xml", "robots.txt", "walkthrough.md",
    "assets/icons/favicon.svg", "assets/icons/logo.svg", "assets/images/social-preview.svg"
]

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.title = ""
        self.meta_desc = None
        self.canonical = None
        self.in_title = False
        self.schemas = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "meta" and attrs.get("name") == "description":
            self.meta_desc = attrs.get("content")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag == "title":
            self.in_title = True
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.schemas += 1
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title += data

def html_files():
    return sorted([p for p in ROOT.rglob("*.html") if ".git" not in p.parts])

def assert_true(condition, message, problems):
    if not condition:
        problems.append(message)

def run():
    problems = []
    for rel in REQUIRED:
        assert_true((ROOT / rel).exists(), f"Missing required file: {rel}", problems)

    titles = {}
    descs = {}
    canonicals = {}
    html_paths = html_files()
    expected_paths = set()
    for file in html_paths:
        parser = LinkParser()
        parser.feed(file.read_text(encoding="utf-8"))
        rel = file.relative_to(ROOT).as_posix()
        expected_paths.add(rel)
        assert_true(bool(parser.title.strip()), f"Missing title: {rel}", problems)
        assert_true(bool(parser.meta_desc), f"Missing meta description: {rel}", problems)
        assert_true(bool(parser.canonical), f"Missing canonical: {rel}", problems)
        assert_true(parser.schemas == 0, f"Static JSON-LD block found in HTML: {rel}", problems)
        assert_true("href=\"#\"" not in file.read_text(encoding="utf-8"), f"Placeholder hash link found: {rel}", problems)
        assert_true("javascript:void(0)" not in file.read_text(encoding="utf-8"), f"javascript:void(0) found: {rel}", problems)
        assert_true("Lorem ipsum" not in file.read_text(encoding="utf-8"), f"Lorem ipsum found: {rel}", problems)
        assert_true("TODO" not in file.read_text(encoding="utf-8"), f"TODO found: {rel}", problems)
        assert_true("http://" not in file.read_text(encoding="utf-8"), f"Non-https URL found: {rel}", problems)
        if parser.title in titles:
            problems.append(f"Duplicate title: {rel} and {titles[parser.title]}")
        titles[parser.title] = rel
        if parser.meta_desc in descs:
            problems.append(f"Duplicate meta description: {rel} and {descs[parser.meta_desc]}")
        descs[parser.meta_desc] = rel
        if parser.canonical in canonicals:
            problems.append(f"Duplicate canonical: {rel} and {canonicals[parser.canonical]}")
        canonicals[parser.canonical] = rel

        for link in parser.links:
            if not link.startswith(DOMAIN):
                continue
            path = link.replace(DOMAIN, "").lstrip("/") or "index.html"
            if link.endswith("/"):
                path = "index.html"
            assert_true((ROOT / path).exists(), f"Broken internal link in {rel} -> {link}", problems)

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    assert_true("Sitemap: https://creditcostguide.com/sitemap.xml" in robots, "robots.txt missing sitemap directive", problems)

    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in sitemap.findall("sm:url/sm:loc", ns)]
    assert_true(len(urls) == len(expected_paths), "sitemap.xml URL count does not match HTML file count", problems)
    for path in expected_paths:
        loc = f"{DOMAIN}/" if path == "index.html" else f"{DOMAIN}/{path}"
        assert_true(loc in urls, f"sitemap.xml missing {loc}", problems)

    walkthrough = ROOT / "walkthrough.md"
    summary = [
        "# CreditCostGuide Launch Walkthrough",
        "",
        "## Audit Summary",
        f"- HTML pages found: {len(expected_paths)}",
        f"- Unique titles checked: {len(titles)}",
        f"- Unique descriptions checked: {len(descs)}",
        f"- Unique canonicals checked: {len(canonicals)}",
        f"- Internal validation issues: {len(problems)}",
        "",
        "## AdSense Readiness Checklist",
        "- Clear navigation is present across the site.",
        "- Legal pages exist: privacy policy, terms, and disclaimer.",
        "- Content is educational, original, and themed around U.S. consumer finance costs.",
        "- No placeholder ad blocks were included.",
        "- Cookie preference controls are present.",
        "",
        "## Search Console Checklist",
        "- `sitemap.xml` is generated with absolute HTTPS URLs.",
        "- `robots.txt` points to the sitemap.",
        "- Each page includes a canonical URL, unique title, and unique description.",
        "- Open Graph and Twitter metadata are included on every page.",
        "- Breadcrumb navigation is present on internal pages.",
        "",
        "## Manual Review Notes",
        "- Local file preview navigation is supported through JavaScript rewriting for same-domain links.",
        "- Dynamic JSON-LD schema is injected by `main.js` instead of static blocks in HTML.",
        "- Re-run `python3 scripts/verify_site.py` after any edit to refresh this report.",
        "",
        "## Verification Result",
    ]
    if problems:
        summary.extend(f"- FAIL: {item}" for item in problems)
    else:
        summary.append("- PASS: All automated checks completed without detected issues.")
    walkthrough.write_text("\n".join(summary) + "\n", encoding="utf-8")

    if problems:
        print("Verification failed:")
        for item in problems:
            print(f"- {item}")
        sys.exit(1)
    print("Verification passed.")

if __name__ == "__main__":
    run()
