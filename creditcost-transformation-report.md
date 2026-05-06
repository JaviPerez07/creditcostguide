# CreditCostGuide — Forbes-Level E-E-A-T Transformation Report

**Date:** 2026-05-06
**Editor:** Javi Pérez (Almería, Spain)
**Mode:** Auto / autonomous. **No commit performed** (awaiting OK).

---

## 1. Site structure

- **Generators:** two Python scripts.
  - `scripts/build_site.py` (3 470 → 3 770 lines after edits) — canonical generator. Produces 42 of 60 HTML files plus `styles.css`, `main.js`, `robots.txt`, `sitemap.xml`, `_redirects`, `_headers`, `assets/icons/*.svg`, `assets/images/social-preview.svg`, and the verification script.
  - `scripts/build_search_console_expansion.py` (legacy, 68 KB) — was used once to expand the site with 18 supporting articles. Those pages are committed as static HTML and **not** regenerated each build.
- **One-time orphan patcher (new):** `scripts/patch_orphan_pages.py` applies the new schema framework + Javi byline + year fixes to the 18 legacy pages plus `pages/smartcredit-review.html`.
- **Total HTML pages:** 60 (1 home + 6 root + 53 in `pages/` including a 404). All 59 content pages now share the same E-E-A-T head pattern; `404.html` is intentionally noindex/no-AdSense.

## 2. Fictional authors / red-flag phrases — eliminated (audit only)

| Search | Result |
|---|---|
| Fictional names (Sarah Davies, Rachel Morgan, Maya Coleman, Michael Torres, James Carter, Patricia Wells, Alex Turner, David Chen, James R. Mitchell, Maya Ellison) | **0 matches** |
| Fictional credentials (EA, CPA, CFP, JD, Esq., "personally reviewed", IRS Specialist, Tax Specialist, Financial Advisor) | **0 matches** |
| Banned phrases (`AdSense-ready`, `Built to scale`, `Search Console ready`, `Cloudflare-ready`, `Editorially reviewed`, `focuslocalai`, `focuslocalaiagency`) | **0 matches** |
| Fictional phones (`555-01...`) | **0 matches** |
| Broken anchors (`href="#"`, `>undefined<`) | **0 matches** |

The site arrived clean on this dimension — no purge needed.

## 3. E-E-A-T implementation

### 3.1 Editor identity (single human, no fake credentials)

Added centrally in `scripts/build_site.py` so every render reuses one source of truth:

```python
EDITOR_NAME = "Javi Pérez"
EDITOR_ROLE = "Editor, CreditCostGuide"
EDITOR_LINKEDIN = "https://www.linkedin.com/in/javi-perez-guides"
EDITOR_LOCATION = "Almería, Spain"
EDITOR_PHOTO = f"{DOMAIN}/assets/images/javi-perez-guides.jpg"
EDITOR_PHOTO_FALLBACK = f"{DOMAIN}/assets/images/social-preview.svg"
LAST_REVIEWED = "May 2026"
LAST_REVIEWED_ISO = "2026-05-06"
SITEMAP_LASTMOD = "2026-05-06"
CONTACT_EMAIL = "javiperezguides@gmail.com"
```

### 3.2 Editorial byline on every content page

`author_box()` in `build_site.py` was rewritten to render Javi's byline with photo, role, LinkedIn, "Last reviewed: May 2026", and a non-advice disclaimer. The block uses `class="ccg-author-box editorial-byline"` and includes an `onerror` fallback to the existing `social-preview.svg` so the page never shows a broken image while the photo is being uploaded.

**Rendered count:** 59 of 60 pages (404 deliberately excluded).

### 3.3 Homepage trust block

New `editorial_trust_block()` is inserted into `home_body()` immediately above the pillar grid. Headline: *"Built by Javi Pérez with public data you can verify."* Includes circular photo, sourcing summary (CFPB, Federal Reserve, FDIC, BLS), and a CTA link to `/about`.

### 3.4 `/about` rewrite

`about.html` now uses a dedicated `about_body()` with five hand-written sections:

1. **Who runs this site** — Javi's role, location (Almería, Spain), explicit "not a licensed financial advisor / CPA / CFP / loan officer" disclaimer, LinkedIn link.
2. **What this site covers** — 8 pillar guides, 5 calculators.
3. **How we research** — sourcing hierarchy CFPB → Federal Reserve → FDIC → BLS → SEC.
4. **Editorial independence and disclosure** — AdSense + SmartCredit affiliate disclosure with `rel="nofollow sponsored"`.
5. **Contact** — `mailto:javiperezguides@gmail.com`.

Plus 3 FAQ items + Javi byline + related articles. ~900 words of original copy.

### 3.5 `/how-we-research` rewrite

`how-we-research.html` now uses `how_we_research_body()` — a long-form methodology page (~1 100 words) covering:

- **Sourcing hierarchy** (CFPB, Fed, FDIC, BLS, SEC, industry data).
- **Update cycle** (quarterly + monthly Fed-series checks + 5-day regulatory turnaround).
- **Calculator methodology** (formulas listed for loan, card, mortgage, debt, utilization).
- **Correction policy** (5-day SLA, dateModified bumped, no silent rewrites).
- **Editorial independence** (advertisers and affiliates do not influence content).

### 3.6 Hardcoded JSON-LD schemas (rule #5 fixed)

**Before:** `main.js` ran `injectSchema()` on every page, building Organization, WebSite, WebPage, BreadcrumbList, Article/SoftwareApplication, and FAQPage entries from `data-breadcrumbs` / `data-faqs` body attributes. This violates the project rule "NUNCA schemas JSON-LD vía JavaScript".

**After:** new helper `build_jsonld()` in `build_site.py` emits the entire `@graph` directly into `<head>` at build time. `main.js` no longer contains `injectSchema` (function and call removed). Body-level dataset attributes that fed it are gone.

The resulting `@graph` for an article page contains 7 entries:

```
- Organization     ( https://creditcostguide.com/#organization )
- WebSite          ( https://creditcostguide.com/#website )
- Person           ( https://creditcostguide.com/#editor — Javi Pérez, LinkedIn )
- WebPage          ( ${canonical}#page, dateModified 2026-05-06 )
- BreadcrumbList   ( ${canonical}#breadcrumbs )
- Article          ( editor → #editor, publisher → #organization, dateModified 2026-05-06 )
- FAQPage          ( ${canonical}#faq )
```

Calculator pages substitute `SoftwareApplication` for `Article`. The home page uses `WebSite` for the `#page` node and skips the Article entry. `404.html` is the only page that has *no* schema (correctly noindex).

Per project rules, **no `author` Person is asserted** (Javi is not a CPA/CFP). The Person node is the `editor` of every Article — accurate and non-misleading.

### 3.7 Article schema with `editor` on every content page

Confirmed on a full sample of pages: `Article.editor` references `#editor` (Javi Pérez), `Article.publisher` references `#organization`, `Article.dateModified` is `2026-05-06T00:00:00+00:00`, `Article.image` is the social preview SVG, and `Article.inLanguage` is `en-US`.

### 3.8 BreadcrumbList + FAQPage + Organization

- **BreadcrumbList** present on every page where `len(breadcrumbs) > 1` — that's every page except the home (correct).
- **FAQPage** present whenever the page builder produced FAQ items (every guide, calculator, and root content page).
- **Organization** present on every page; includes `email: javiperezguides@gmail.com` and `sameAs: [LinkedIn]`.

## 4. Year update — 2024/2025 → 2026

| Type | Action |
|---|---|
| Forward-looking copy ("options available in 2025", "Best Secured Cards for Rebuilding in 2025") | Updated to **2026** in the build script. |
| `<title>` tags with "2025 to 2026" / "in 2025 and 2026" (`savings-account-interest-rates.html`, `personal-loan-cost-guide.html`) | Patched by `scripts/patch_orphan_pages.py` to drop the dual-year span — titles now reference 2026 only. |
| Editor byline "Last reviewed" | Updated from **April 2026** → **May 2026**. |
| `<title>` containing 2024/2025 anywhere on site | **0** after the run. |
| Historical numeric references citing 2024 Fed data and Experian 2025 release | Left intact (factually correct historical citations) and tagged with `<!-- DATO PENDIENTE VERIFICAR 2026: ... -->` HTML comments at the source so future updates are obvious. **3** such markers in `build_site.py` (lines visible in `pages/credit-score-guide.html`, `pages/debt-payoff-guide.html`, `pages/how-to-lower-credit-card-interest.html` after build). |

## 5. Technical fixes

| Item | Status |
|---|---|
| `ads.txt` | Already correct (`google.com, pub-3733223915347669, DIRECT, f08c47fec0942fa0`). |
| `robots.txt` | **Updated**: now includes `Disallow: /*?q=*` and `Disallow: /*?s=*`. |
| `_redirects` | **Rewritten** by build script. Removed the 3 www-related rules (per project rule, www handled in Cloudflare dashboard). All `.html` → clean URL rules retained as `301!`. **No 200 rules.** |
| `_headers` (new) | Created with `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` and `Strict-Transport-Security`. |
| OG / Twitter Card | Already complete; added `og:locale: en_US`. |
| Sitemap | **Updated**: now emits `<lastmod>2026-05-06</lastmod>` for every URL. No `www.`, no `.html`. |
| Canonicals | Already clean (no `www.`, no `.html`). 0 bad ones detected post-build. |
| Cookie banner | Switched from `hidden` attribute to `style="display:none"`. JS now toggles `style.display`. |
| Email | `javiperezguides@gmail.com` now present on all root pages, in every Organization schema, in `/about` and `/how-we-research` body, and on the contact page. |
| `404.html` | **noindex,nofollow**, no AdSense, no JSON-LD. Same shell/layout for consistency. |
| Schema injection in `main.js` | Removed (was at lines 218–302 of the live file). |
| Editor photo | Referenced at `/assets/images/javi-perez-guides.jpg` (file confirmed present on disk) with `onerror` fallback to `social-preview.svg`. |

## 6. Pending data / human action required

| # | Item | Where | What to do |
|---|---|---|---|
| 1 | Editor photo file | `assets/images/javi-perez-guides.jpg` — present on disk (confirmed 2026-05-06). Code references the same filename. | None. The byline now shows the real photo. |
| 2 | Average household credit-card debt + average APR | `pages/debt-payoff-guide.html` (sourced from 2024 Federal Reserve data) | Tagged with `<!-- DATO PENDIENTE VERIFICAR 2026 -->` in `build_site.py:861`. Refresh when the Fed publishes the 2026 figures. |
| 3 | Average credit-card APR (24.59%) | `pages/how-to-lower-credit-card-interest.html` | Tagged at `build_site.py:1262`. Same refresh cadence. |
| 4 | Average U.S. FICO score (715) | `pages/credit-score-guide.html` | Tagged at `build_site.py:208` (Experian 2025 release). Refresh when Experian publishes 2026 numbers. |
| 5 | LinkedIn URL | Schema + byline | Currently set to `https://www.linkedin.com/in/javi-perez-guides`. Verify this is the correct slug; change `EDITOR_LINKEDIN` in `build_site.py` if needed and rerun the build. |

## 7. Final verification (post-rebuild + post-patch)

```
Total HTMLs:                 60
Pages with editorial-byline: 59 (404 excluded — correct)
Pages with hardcoded ld+json: 59 (404 has noindex — correct)
Pages with AdSense:           59 (404 has no AdSense — correct)
Pages mentioning Javi Pérez: 59
Bad canonicals (.html or www): 0
Forward-looking 2025 in copy: 0
2024/2025 in <title>:         0
404 robots:                  noindex,nofollow
DATO PENDIENTE markers:       3 (all in body content, intentional)
Fictional names / credentials: 0
focuslocalai / 555-01 / banned phrases: 0
www rules in _redirects:      0
Schema injection in main.js:  0 (removed)
```

## 8. Thin content

Threshold: `<800` words after stripping HTML. **0 pages** below the threshold (every guide is well over 1 000 words and every legal page exceeds 1 000 by design via `simple_page_body`).

## 9. Other bugs / observations

- The previous `_redirects` had 3 rules for `www.creditcostguide.com` and `http://creditcostguide.com` — removed because Cloudflare dashboard handles those redirects. If, after deploy, www variants stop redirecting, re-enable them in the Cloudflare dashboard, **not** in `_redirects`.
- The two long-form pages `pages/savings-account-interest-rates.html` and `pages/personal-loan-cost-guide.html` (orphans of `build_search_console_expansion.py`) had legacy "2025 to 2026" titles — the patcher cleaned them.
- `main.js` size dropped from 322 → ~230 lines after removing `injectSchema`.
- Three new functions added to `build_site.py`: `build_jsonld`, `editorial_trust_block`, `about_body`, `how_we_research_body`, `redirects_txt`, `headers_txt`. Plus a flag `is_404` on `html_doc` to suppress AdSense/schemas and switch robots to `noindex,nofollow`.
- The `pages/smartcredit-review.html` is also an orphan; the patcher updated it the same way (added Javi byline + hardcoded schema). Editorial content of that review was not touched.
- A working git worktree mismatch was detected during the run: the shell was attached to a worktree of the **insurancecostguide** repo, not creditcostguide. All edits were made via absolute paths, so no commits crossed repos. **No git operations were performed.** When you commit, do it from `/Users/javiperezz7/Documents/creditcostguide` directly.

---

**Diff scope:**
- `scripts/build_site.py` — substantial: new constants, `build_jsonld`, `editorial_trust_block`, `about_body`, `how_we_research_body`, `redirects_txt`, `headers_txt`, refactored `html_doc`, refactored `author_box`, refactored `main_js` (no `injectSchema`), refactored `robots_txt`, refactored `sitemap_xml`, new write calls for `_redirects` / `_headers`, `is_404` plumbing.
- `scripts/patch_orphan_pages.py` — new (one-time orphan patcher).
- All 60 HTML files — regenerated or patched.
- `styles.css`, `main.js`, `robots.txt`, `sitemap.xml`, `_redirects`, `_headers` — regenerated.

**Awaiting your OK before any `git add` / `git commit` / `git push`.**
