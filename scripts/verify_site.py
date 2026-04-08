from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://creditcostguide.com"

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_desc = None
        self.canonical = None
        self.og_url = None
        self.in_title = False
        self.schemas = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('name') == 'description':
            self.meta_desc = attrs.get('content')
        if tag == 'meta' and attrs.get('property') == 'og:url':
            self.og_url = attrs.get('content')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        if tag == 'title':
            self.in_title = True
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.schemas += 1
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title += data

def public_url(rel_path: str) -> str:
    return f"{DOMAIN}/" if rel_path == 'index.html' else f"{DOMAIN}/{rel_path.removesuffix('.html')}"

def run():
    problems = []
    html_files = sorted([p for p in ROOT.rglob('*.html') if '.git' not in p.parts])
    expected_urls = []
    for file in html_files:
        parser = LinkParser()
        text = file.read_text(encoding='utf-8')
        parser.feed(text)
        rel = file.relative_to(ROOT).as_posix()
        expected = public_url(rel)
        expected_urls.append(expected)
        if parser.canonical != expected:
            problems.append(f'Canonical mismatch: {rel}')
        if parser.og_url != expected:
            problems.append(f'OG URL mismatch: {rel}')
        if parser.schemas != 0:
            problems.append(f'Static schema found: {rel}')
        if re.search(r'https://creditcostguide\.com[^" ]*\.html', text):
            problems.append(f'.html URL leaked in HTML: {rel}')
        if 'http://' in text:
            problems.append(f'http URL leaked in HTML: {rel}')
        if 'www.creditcostguide.com' in text:
            problems.append(f'www URL leaked in HTML: {rel}')
    sitemap = ET.parse(ROOT / 'sitemap.xml').getroot()
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [loc.text for loc in sitemap.findall('sm:url/sm:loc', ns)]
    if sorted(urls) != sorted(expected_urls):
        problems.append('sitemap.xml does not exactly match clean canonical URLs')
    if problems:
        print('Verification failed:')
        for item in problems:
            print(f'- {item}')
        sys.exit(1)
    print('Verification passed.')

if __name__ == '__main__':
    run()
