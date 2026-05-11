# CreditCostGuide — 3 New Calculators Integration Report

**Date:** 2026-05-11
**Editor:** Javi Pérez
**Status:** Built + verified. **No git commit, no push.** Awaiting your OK.

---

## 1. What was built

Three Chart.js-powered calculators integrated through `scripts/build_site.py` (same generator, same `INDEXABLE_PAGES` gate, same `PAGE_CONTENT` framework). No separate static HTML files, no design drift — the new calculators reuse the site's existing header, footer, byline, hero, JSON-LD schema, Sources & Methodology block, and styles.

| URL | Calc type | Page size | Per-page JS |
|---|---|---|---|
| `/pages/debt-avalanche-vs-snowball-calculator` | `avalanche-snowball` | 26.2 KB | `assets/scripts/debt-avalanche-snowball.js` (7.4 KB) |
| `/pages/credit-card-minimum-payment-true-cost-calculator` | `min-payment` | 24.7 KB | `assets/scripts/minimum-payment-true-cost.js` (5.0 KB) |
| `/pages/mortgage-refinance-break-even-calculator` | `refinance` | 24.9 KB | `assets/scripts/refinance-break-even.js` (4.7 KB) |

All three live inside `INDEXABLE_PAGES`, so they automatically appear in:

- `sitemap.xml` (now **27 URLs**, up from 24)
- The homepage calculators grid (auto-populated from the `CALCULATORS` list)
- Internal cross-links from their pillar guides (see §4)

---

## 2. Files created / modified

| Path | Status | Purpose |
|---|---|---|
| `scripts/build_site.py` | Modified | New constants `CHARTED_CALCS`, three new `CALCULATORS` entries, three new entries in `INDEXABLE_PAGES`, three new `PAGE_CONTENT` blocks, three widget renderers (`_calc_module_avalanche_snowball`, `_calc_module_min_payment`, `_calc_module_refinance`), three JS emitters (`calc_js_*`), `html_doc(extra_scripts=...)` parameter, CSS additions for charted widgets, internal cross-links added to existing pillar copy. |
| `pages/debt-avalanche-vs-snowball-calculator.html` | Created | Generated page. |
| `pages/credit-card-minimum-payment-true-cost-calculator.html` | Created | Generated page. |
| `pages/mortgage-refinance-break-even-calculator.html` | Created | Generated page. |
| `assets/scripts/debt-avalanche-snowball.js` | Created | Browser-local JS — no localStorage, no analytics, no input tracking. |
| `assets/scripts/minimum-payment-true-cost.js` | Created | Same. |
| `assets/scripts/refinance-break-even.js` | Created | Same. |
| `styles.css` | Modified | Added `.ccg-calc-card--charted`, `.ccg-calc-row`, `.ccg-debt-input-table`, `.ccg-result-grid--three`, range-slider styling, chart-wrap padding. Reuses existing CSS variables so dark/light theme works out of the box. |
| `sitemap.xml` | Modified | 24 → 27 URLs. |

---

## 3. Formulas implemented

### Debt Avalanche vs Snowball
- **Monthly interest**: `balance × (APR / 12)` per active debt.
- **Avalanche priority**: sort active debts by APR descending (tiebreak: smaller balance first).
- **Snowball priority**: sort active debts by balance ascending (tiebreak: higher APR first).
- **Payment allocation**: full monthly budget cascades down the priority list; cascades to the next debt only when the prior one hits zero.
- **Negative-amortization guard**: if total monthly interest ≥ monthly budget, the warning fires.
- **Hard cap**: 600 months (50 years). If a strategy doesn't amortize within that, the result shows "600+ months".

### Minimum Payment True Cost
- **Monthly interest**: `current × (APR / 12)`.
- **Minimum payment**: `max(current × (minPct / 100), minFloor)`.
- **Two parallel simulations**: minimum-only and minimum + extra.
- **Negative-amortization guard**: if `payment ≤ interest` for any month, return `amortizes: false`.
- **Hard cap**: 720 months (60 years).

### Refinance Break-Even
- **Closed-form fixed-rate amortization**: `P · r / (1 − (1 + r)^−n)` for both current and new loans.
- **Monthly savings**: `oldPmt − newPmt`.
- **Break-even months**: `ceil(closingCosts / monthlySavings)` when savings positive, `Infinity` otherwise.
- **Cumulative-savings chart**: `(monthlySavings × i) − closingCosts` for i = 0…horizon.
- **Planned-sale warning**: fires when `plannedYears × 12 < breakEvenMonths`.
- **Higher-payment warning**: fires when `newPmt ≥ oldPmt` (no payment-based break-even).

---

## 4. Internal linking

Inline cross-links added to existing pillar copy:

| From | To | Anchor |
|---|---|---|
| `/pages/debt-payoff-guide` intro | `/pages/debt-avalanche-vs-snowball-calculator` | "avalanche vs snowball calculator" |
| `/pages/mortgage-guide` intro | `/pages/mortgage-refinance-break-even-calculator` | "refinance break-even calculator" |
| `/pages/credit-cards-guide` intro | `/pages/credit-card-minimum-payment-true-cost-calculator` | "minimum payment true cost calculator" |

Automatic links:
- **Homepage calculators grid** picks up all 3 new entries from `CALCULATORS` (grid now shows 8 cards).
- **Sitemap** includes all 3 (filtered via `is_indexable()`).
- **Related Articles** sections on relevant pages cycle through the related_pool which includes calculators.

---

## 5. Editorial content per page

Each of the 3 new pages has a unique `PAGE_CONTENT` entry rendered by `rich_article_body()`:

- **Intro section** (~150 words) with `intro_h2` + `intro_body` HTML.
- **4 named sections** (~700 words total) with `kicker`, `h2`, `body`. Each section has unique copy explaining a different facet of the calculator's domain.
- **6 unique FAQs** (one is always the non-advice disclaimer).
- **Sources & Methodology block** auto-populated from `SOURCES_BY_TOPIC` (CFPB, Federal Reserve, FRED, etc.) keyed by `sources_topic` in PAGE_CONTENT.
- **Editor byline** with AI-assisted-drafting disclosure (`AI_DISCLOSURE` constant).
- **Related Articles** with 4 contextually relevant links.

Total editorial word count per page: **~950–1,050 words**, all original.

---

## 6. Schema graph per page (validated)

Each of the 3 new pages emits a 7-node `@graph`:

```
Organization → WebSite → Person (editor) → WebPage → BreadcrumbList → SoftwareApplication → FAQPage
```

- `SoftwareApplication.applicationCategory = "FinanceApplication"`.
- `SoftwareApplication.offers = { price: "0", priceCurrency: "USD" }`.
- `Article.editor` → `#editor` (Javi Pérez, with `sameAs` LinkedIn).
- `FAQPage.mainEntity` ↔ visible FAQ section on the page (1:1 match).
- All schemas are **hardcoded in `<head>`**, not injected by JS. No JSON-LD via JavaScript per project rule #5.

---

## 7. AdSense and ad-placement checks

| Check | Status |
|---|---|
| `<script async src="https://pagead2.googlesyndication.com/...">` in `<head>` of all 3 pages | ✅ Present |
| `<ins class="adsbygoogle">` elements | ✅ 0 (none added) |
| "Advertisement" placeholder text | ✅ 0 |
| Visible ad slots / placeholders | ✅ 0 |
| `ads.txt` | ✅ unchanged, still correct |

Note: AdSense automatically places ads on indexable pages once the site is approved. We do not pre-place ad units.

---

## 8. Build verification

```
=== Build run ===
$ python3 scripts/build_site.py    # exit 0, no errors
$ python3 scripts/patch_orphan_pages.py    # 19 orphan pages, all still noindex

=== Index/noindex split ===
Sitemap URLs:        27   (was 24, +3 new calcs)
Indexable HTMLs:     27   (exact match with sitemap)
Noindex HTMLs:       37   (unchanged — legacy + orphans)

=== Per-page sanity (3 new calculators) ===
AdSense script:      1 per page  ✅
JSON-LD schema:      1 per page  ✅
Chart.js CDN:        1 per page  ✅
Per-page JS:         1 per page  ✅
Editor byline:       6 mentions per page (header link + byline section + cross-refs)  ✅
Robots meta:         index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1  ✅

=== Cross-link verification ===
Home → 3 new calcs:                              ✅
debt-payoff-guide → avalanche-snowball:          ✅
mortgage-guide → refinance-break-even:           ✅
credit-cards-guide → min-payment-true-cost:      ✅

=== Toxic-pattern residue (still 0 across the site) ===
Recycled figures (8K/15K/275K/4.2K/18.5K):       0
"Deep Dive N" markers:                            0
Visible ad blocks:                                0
Fake author names:                                0
```

---

## 9. UX notes (browser-local only)

- **No localStorage.** Calculator state lives in the DOM only; refreshing the page resets to defaults.
- **No analytics on calculator inputs.** No fetches fire on input changes.
- **All math runs in the user's browser** via the per-page JS bundle and Chart.js (CDN).
- **Mobile-first input sizing:** all `<input>` elements have `min-height: 44px` (text/number) or 32px (range slider, native size).
- **Dark/light mode:** the new components reuse the site's CSS variables (`--ccg-navy`, `--ccg-blue`, `--ccg-line`, `--ccg-ink`, `--ccg-slate`). No separate `calculators.css` was added; everything is in the existing `styles.css`.
- **Accessibility:** all inputs have visible labels, `<canvas>` has `role="img"` + `aria-label`, the calculator card has an `aria-live="polite"` region in the result grid.
- **Privacy:** no tracking, no third-party requests other than the Chart.js CDN and AdSense (both already site-wide).

---

## 10. Post-deploy verification commands (per your prompt)

After commit + push and Cloudflare Pages redeploy:

```bash
curl -I https://creditcostguide.com/pages/debt-avalanche-vs-snowball-calculator
curl -I https://creditcostguide.com/pages/credit-card-minimum-payment-true-cost-calculator
curl -I https://creditcostguide.com/pages/mortgage-refinance-break-even-calculator
curl -I https://creditcostguide.com/sitemap.xml
curl -I https://creditcostguide.com/ads.txt
curl -I https://creditcostguide.com/scripts/build_site.py   # expect 404
```

Then submit `https://creditcostguide.com/sitemap.xml` again in Search Console and request indexing on the 3 new URLs.

---

## 11. Diff summary (uncommitted)

| File | Lines changed |
|---|---|
| `scripts/build_site.py` | ~1100 lines added (3 PAGE_CONTENT blocks ~600 lines, 3 widget renderers ~120 lines, 3 JS emitters ~280 lines, CSS additions ~110 lines, plumbing changes ~30 lines) |
| `pages/debt-avalanche-vs-snowball-calculator.html` | New |
| `pages/credit-card-minimum-payment-true-cost-calculator.html` | New |
| `pages/mortgage-refinance-break-even-calculator.html` | New |
| `assets/scripts/debt-avalanche-snowball.js` | New |
| `assets/scripts/minimum-payment-true-cost.js` | New |
| `assets/scripts/refinance-break-even.js` | New |
| `pages/debt-payoff-guide.html` | +1 inline link |
| `pages/mortgage-guide.html` | +1 inline link |
| `pages/credit-cards-guide.html` | +1 inline link |
| `sitemap.xml` | 24 → 27 URLs |
| `styles.css` | New `.ccg-calc-card--charted`, `.ccg-debt-input-table`, `.ccg-result-grid--three`, range slider, chart wrap. |

**No git commit. No push. Awaiting your OK.**
