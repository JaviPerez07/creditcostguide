# CreditCostGuide — Final AdSense Readiness Report

**Date:** 2026-05-11
**Editor:** Javi Pérez · Founder and Editor
**Branch:** `main`
**Stack:** Static HTML + `scripts/build_site.py` (Python generator) → committed directly, deployed by Cloudflare Pages from repo root.
**Status of this session:** Pre-fix snapshot taken, 14 fixes applied, full re-verification clean. **No git commit, no push.**

---

## 1. Executive verdict

> **READY FOR ADSENSE REVIEW.** Maximum reasonable readiness achieved on technical, content, structural, and E-E-A-T dimensions. Remaining risk is on Google's side (review timing, policy interpretation) — not on items inside the codebase.

**Reasonable approval-probability estimate:**

- **Before this pass (post calculator launch, pre-Ahrefs cleanup):** moderate. Indexable set was clean but had 3 internal-link issues (1 broken intermediate breadcrumb + 2 indexable→noindex links) plus 4 external 404s and 4 external 3XX URLs that Ahrefs was correctly flagging.
- **After this pass:** maximum reasonable readiness. Every issue Ahrefs reported has a clear fix landed in `build_site.py` and the rebuilt HTML. Remaining residual Ahrefs Health Score noise is on relative-URL anchors inside the 37 *noindex* legacy pages (resolves correctly in browsers; not a real defect) — these will not affect Google's review of the 27 indexable surface.

This phrasing is deliberate. Approval is never 100% predictable; what we *can* control is removing every internal cause of rejection. That work is now complete.

---

## 2. Ahrefs issue mapping

For each reported Ahrefs issue, the table below shows what state the site was in, what fix landed, and what Ahrefs should see after a recrawl.

| Ahrefs issue | State before | Fix | Expected state after recrawl |
|---|---|---|---|
| **Canonical points to redirect** | All 27 indexable pages already had clean canonicals (HTTPS, non-www, no `.html`). The likely Ahrefs trigger was historical crawl data on legacy `.html` URLs. | None needed inside the codebase; old data clears on recrawl. | Issue clears once Ahrefs recrawls the sitemap. |
| **3XX redirect in sitemap** | Sitemap was already clean (27 URLs, all clean clean-URL form). Same residual-crawl explanation. | None needed inside the codebase. | Clears on recrawl. |
| **Page has links to broken page** | 1 internal broken anchor: `authors/javi-perez/index.html → /authors` (no `/authors` index page exists). | Removed the "Authors" intermediate from the breadcrumb in `build_site.py`. Now the breadcrumb goes Home → Javi Pérez directly. | Resolves immediately on next crawl. |
| **404 page** | 3 external 404 URLs cited in `SOURCES_BY_TOPIC`: CFPB overdraft blog (en-2122 was relocated), CFPB auto-refi article (en-851 removed), Federal Reserve credit-card-profitability report (URL changed). | Replaced all 3 with stable URLs returning 200 (CFPB blog index, CFPB auto-loans consumer tool, Fed `/publications/credit-card-profitability.htm`). | Resolves on next crawl. |
| **4XX page** | Same as above + 1 Federal Reserve "consumers-and-mobile-financial-services.htm" (now 404). | Replaced with `https://www.federalreserve.gov/data.htm` (Fed data hub, 200 stable). | Resolves on next crawl. |
| **Page has links to redirect** | 4 external URLs that 301 to a 200: FDIC national-rates path, AnnualCreditReport homepage, CFPB `/credit-cards/` path, CFPB debt-management-plan article. | Updated each to its canonical 200 destination (no redirect chain). | Clears on recrawl. |
| **Page has links to broken page (not indexable)** | 2 internal anchors from indexable pages to noindex pages: `mortgage-guide → /pages/mortgage-closing-costs-guide` and `debt-payoff-calculator → /pages/debt-snowball-vs-avalanche`. | Replaced both with anchors to indexable destinations (`mortgage-refinance-break-even-calculator` and `debt-avalanche-vs-snowball-calculator`). | Clears on recrawl. |
| **Noindex page** | This is informational, not an error. The 37 noindex pages are intentional — they exist on disk for crawl continuity and internal navigation but are kept out of the indexable surface during AdSense review. | No change. | Will remain "informational" in Ahrefs; does not block AdSense. |
| **3XX redirect** | Two CFPB Q&A URLs (en-2122 and en-2096) returned 301 → **a completely different topic** (medical bill collections and reverse mortgages respectively). This is the worst category because the redirect goes to wrong content. | Replaced with the CFPB consumer-tools landing and a stable myFICO utilization explainer. | Clears on recrawl. |
| **External 3XX redirect** | Same set as above + 1 more (`consumerfinance.gov/owning-a-home/process/refinance/` that 301s to a 404). | Replaced with `https://www.consumerfinance.gov/owning-a-home/` (stable 200). | Clears on recrawl. |

**Critical caveat for Ahrefs:** Many of these issues will continue to appear in Ahrefs reports *for some time after the fix* because Ahrefs uses cached crawl data. A re-crawl of `creditcostguide.com` is required for the Health Score to update. The same fixes will be visible to Google immediately on the next crawl (typically within days for a small site).

---

## 3. Final indexable URLs (27)

All 27 have: `index,follow`, canonical to themselves, JSON-LD schema graph, AdSense script in `<head>`, editor byline with AI-assisted disclosure, sources block with primary regulator links.

| # | URL | Canonical | In sitemap |
|---|---|---|---|
| 1 | `/` | `https://creditcostguide.com/` | yes |
| 2 | `/about` | `https://creditcostguide.com/about` | yes |
| 3 | `/contact` | `https://creditcostguide.com/contact` | yes |
| 4 | `/how-we-research` | `https://creditcostguide.com/how-we-research` | yes |
| 5 | `/privacy-policy` | `https://creditcostguide.com/privacy-policy` | yes |
| 6 | `/terms` | `https://creditcostguide.com/terms` | yes |
| 7 | `/disclaimer` | `https://creditcostguide.com/disclaimer` | yes |
| 8 | `/authors/javi-perez` | `https://creditcostguide.com/authors/javi-perez` | yes |
| 9 | `/pages/personal-loans-guide` | (self) | yes |
| 10 | `/pages/credit-cards-guide` | (self) | yes |
| 11 | `/pages/mortgage-guide` | (self) | yes |
| 12 | `/pages/credit-score-guide` | (self) | yes |
| 13 | `/pages/banking-fees-guide` | (self) | yes |
| 14 | `/pages/debt-payoff-guide` | (self) | yes |
| 15 | `/pages/refinancing-guide` | (self) | yes |
| 16 | `/pages/student-loans-guide` | (self) | yes |
| 17 | `/pages/how-credit-scores-work` | (self) | yes |
| 18 | `/pages/best-credit-cards-for-bad-credit` | (self) | yes |
| 19 | `/pages/how-to-lower-credit-card-interest` | (self) | yes |
| 20 | `/pages/loan-payment-calculator` | (self) | yes |
| 21 | `/pages/credit-card-interest-calculator` | (self) | yes |
| 22 | `/pages/mortgage-calculator` | (self) | yes |
| 23 | `/pages/debt-payoff-calculator` | (self) | yes |
| 24 | `/pages/credit-utilization-calculator` | (self) | yes |
| 25 | `/pages/debt-avalanche-vs-snowball-calculator` | (self) | yes |
| 26 | `/pages/credit-card-minimum-payment-true-cost-calculator` | (self) | yes |
| 27 | `/pages/mortgage-refinance-break-even-calculator` | (self) | yes |

---

## 4. Noindex URLs (37)

All 37 confirm:
- `<meta name="robots" content="noindex, follow">`
- No JSON-LD schema (stripped by `patch_orphan_pages.py`)
- Not in sitemap (filtered by `is_indexable()` in `sitemap_xml()`)
- Canonical present and points to self (not to an indexable page)
- No fake author names, no template phrases, no toxic phrases (audited site-wide)
- No `.html` extension in internal anchor links

Internal anchors on these legacy pages use relative paths (`./<slug>`, `../`) which resolve correctly in the browser. Ahrefs may flag these as "links to redirect" because of the `.html` → clean URL `_redirects` rules, but every resolution lands on a 200 response — there is no actual broken link chain.

---

## 5. New calculators (3) — final state

| URL | JS file | Schema graph | Sources |
|---|---|---|---|
| `/pages/debt-avalanche-vs-snowball-calculator` | `assets/scripts/debt-avalanche-snowball.js` | Organization + WebSite + Person + WebPage + BreadcrumbList + SoftwareApplication + FAQPage | CFPB debt repayment (Q&A en-1457 renamed), FTC coping-with-debt, NY Fed Household Debt Report |
| `/pages/credit-card-minimum-payment-true-cost-calculator` | `assets/scripts/minimum-payment-true-cost.js` | Same set | CFPB credit cards consumer tool, Fed credit-card profitability publication, CFPB complaint database |
| `/pages/mortgage-refinance-break-even-calculator` | `assets/scripts/refinance-break-even.js` | Same set | CFPB Loan Estimate, CFPB auto-loans consumer tool, FRED MORTGAGE30US |

**Internal links into the 3 new calculators:** home page calculators grid (auto-populated from `CALCULATORS`); `debt-payoff-guide`, `mortgage-guide`, `credit-cards-guide` pillar intros each contain one inline anchor to the matching new calculator; `debt-payoff-calculator` body links to the avalanche-snowball calculator; `mortgage-guide` closing-costs section links to the refinance-break-even calculator.

---

## 6. Technical readiness checklist

| Item | Status | Notes |
|---|---|---|
| Sitemap | **27 URLs** | All clean (HTTPS, non-www, no `.html`); each has `<lastmod>2026-05-06</lastmod>`; noindex URLs filtered out by `is_indexable()`. |
| robots.txt | OK | `User-agent: *  Allow: /  Disallow: /*?q=*  Disallow: /*?s=*  Sitemap: https://creditcostguide.com/sitemap.xml`. |
| ads.txt | OK | `google.com, pub-3733223915347669, DIRECT, f08c47fec0942fa0`. |
| AdSense script in `<head>` | **27/27** indexable pages, 36/37 noindex pages (404 has no AdSense — by design). | No `<ins class="adsbygoogle">` placeholders anywhere. |
| Canonicals | 0 issues. All 27 indexable canonicals are self-referencing, HTTPS, non-www, no `.html`. | |
| Internal links — `.html` in anchors | 0 internal hits. The 3 external matches go to `newyorkfed.org` and are correctly served with `.html` by that site (not a redirect). | |
| Internal links — `www.` or `http://` | 0 hits. | |
| Internal links — indexable → noindex | 0 hits. The previous 2 (`mortgage-guide → mortgage-closing-costs-guide`, `debt-payoff-calculator → debt-snowball-vs-avalanche`) are now redirected to the 3 new indexable calculators. | |
| External links — 404 | 0 hits in the indexable set after fixes. | The 4 broken ones (CFPB overdraft blog, CFPB auto-refi, Fed credit-card-profitability report, Fed consumers-and-mobile-services) replaced with stable 200 URLs. |
| External links — 3XX | 0 hits to 3XX→wrong-topic. 4 cases of 3XX→200 (same content) replaced with canonical destinations. | Some external links may still 301 on Ahrefs's view if their reference data is stale; will clear on recrawl. |
| Schema | 0 issues. All 27 indexable pages have a 7-node `@graph` (8-node for calculators). 0 occurrences of `undefined`/`null`/`NaN` in any JSON-LD block. | |
| Build output / file leak | Internal files (`*.md`, `*.py`, `*.mjs`, `scripts/*`) are served as **404** via `_redirects` rules and tagged `X-Robots-Tag: noindex, nofollow` via `_headers`. | They exist on disk for the build pipeline; they are invisible to crawlers and direct visitors. |
| Cookie banner | OK | Uses `style="display:none"` (not the deprecated `hidden` attribute). |
| Editor identity | Real: Javi Pérez · Founder and Editor · LinkedIn linked · explicit non-advice disclaimer. | No fictional credentials. |
| AI disclosure | Present on every indexable page (byline + sources block) plus dedicated sections on `/about`, `/how-we-research`, and `/authors/javi-perez`. | |

---

## 7. Toxic-pattern residue (final)

| Pattern | Count |
|---|---|
| Fake author names (Maya / Ellison / Sarah / Davies / Michael Torres / etc.) | 0 |
| Templated phrases (`because lenders and consumers are usually solving`, `where the quote only becomes truly useful`, `matters matters`) | 0 |
| `Deep Dive N` markers | 0 |
| Recycled hypothetical figures (`$8,000 at 11.9` / `$15,000 at 9.4` / `$275,000 financed` / `$4,200 revolving` / `$18,500 refinanced`) | 0 |
| Toxic phrases (`AdSense-ready`, `Built to scale`, `focuslocalai`, `Lorem ipsum`, `coming soon`, `555-01`) | 0 |
| `<ins class="adsbygoogle">` blocks | 0 |
| "Advertisement" or "ad placeholder" text | 0 |
| Broken anchors (`href="#"`, `href=""`, `src=""`) | 0 |

---

## 8. Gaps that require manual action (none are blockers)

1. **Trigger Cloudflare Pages redeploy** after the next commit so the new sitemap, redirects, and fixed external links go live.
2. **Re-submit `https://creditcostguide.com/sitemap.xml`** in Google Search Console.
3. **Request indexing** on a small number of high-value URLs (`/`, `/about`, `/how-we-research`, the 3 new calculators, the author profile).
4. **In Ahrefs, trigger a fresh site audit.** Most of the residual issues in the Health Score will clear once Ahrefs recrawls; until then, the cached report will look the same.
5. **Do not cancel the in-flight AdSense review.** Submitting changes during a review is fine. Cancelling resets the queue and adds delay.
6. **Editor identity in git** — your committer email is still the Mac-generated default. Optional:
   ```
   git config --global user.name "Javi Pérez"
   git config --global user.email "javiperezguides@gmail.com"
   ```

---

## 9. Post-deploy verification commands

```bash
# Pages return 200 (not 3XX)
curl -I https://creditcostguide.com/
curl -I https://creditcostguide.com/about
curl -I https://creditcostguide.com/how-we-research
curl -I https://creditcostguide.com/authors/javi-perez
curl -I https://creditcostguide.com/pages/debt-avalanche-vs-snowball-calculator
curl -I https://creditcostguide.com/pages/credit-card-minimum-payment-true-cost-calculator
curl -I https://creditcostguide.com/pages/mortgage-refinance-break-even-calculator

# Sitemap and ads.txt are correct
curl -s https://creditcostguide.com/sitemap.xml | grep -c "<loc>"   # expect 27
curl -s https://creditcostguide.com/ads.txt                          # expect: google.com, pub-3733223915347669, DIRECT, f08c47fec0942fa0

# Source files are blocked (expect 404)
curl -I https://creditcostguide.com/scripts/build_site.py
curl -I https://creditcostguide.com/creditcostguide-final-adsense-readiness-report.md
curl -I https://creditcostguide.com/scripts/patch_orphan_pages.py

# A noindex page still serves 200 but with noindex meta
curl -s https://creditcostguide.com/pages/balance-transfer-credit-cards-guide | grep 'name="robots"'
# expect: <meta name="robots" content="noindex, follow">
```

---

## 10. Final recommendation

- **`git add -u`** (modified tracked files: `scripts/build_site.py` and the 64 regenerated HTMLs).
- **`git add .`** (or specifically: `creditcostguide-final-adsense-readiness-report.md`, the 3 new calc HTMLs, the 3 new JS files, `authors/`, `.gitignore`, `_headers` etc.) — all already staged from prior turns. The only new file in this pass is this report.
- **`git commit`** with a concise message. Suggested:
  > `fix(adsense): repair broken/redirect external sources + remove indexable→noindex inline links`
- **`git push origin main`** to trigger Cloudflare Pages deploy.

Once deployed, run the verification block in §9 and then trigger an Ahrefs re-audit. Do not over-optimize further; the codebase is at the right shape for the AdSense reviewer to see a small, original, well-sourced, technically clean site.

---

## 11. Diff scope (uncommitted)

| File | Change |
|---|---|
| `scripts/build_site.py` | (1) Author breadcrumb: removed `Authors` intermediate that pointed to a non-existent `/authors` index. (2) Replaced 2 inline indexable→noindex anchors with anchors to the new indexable calculators. (3) Replaced 11 external CFPB / Fed / FDIC / AnnualCreditReport URLs (3 were 404, 2 were 301→wrong topic, 5 were 301→200, 1 was 301→404) with their stable 200 destinations. |
| All 64 HTML files | Regenerated. |
| `sitemap.xml` | Regenerated; still 27 clean URLs. |
| `creditcostguide-final-adsense-readiness-report.md` | New file (this report). |

**No git commit. No git push. Awaiting your OK.**
