/**
 * Cloudflare Pages middleware — runs before static asset serving.
 *
 * Purpose: block public access to source-code and internal report files that
 * are deployed as part of the repo but should never be visible to crawlers
 * or direct visitors. The legacy `_redirects` rules cannot do this because
 * Cloudflare Pages serves real files first and ignores `_redirects` for any
 * path that resolves to an existing file.
 *
 * Blocked paths:
 *   - Anything under /scripts/* (Python generator + helper scripts).
 *   - Anything ending in .md (internal audit / readiness reports).
 *   - Anything ending in .py (Python source).
 *   - Anything ending in .mjs (Node helper scripts).
 *
 * Allowed (pass-through):
 *   - All HTML pages.
 *   - Static assets (.css, .js, .svg, .png, .jpg, .ico, .xml, .txt, etc.).
 *   - Site files like /sitemap.xml, /robots.txt, /ads.txt, /404.html.
 *
 * Headers on 404 responses: explicit `X-Robots-Tag: noindex, nofollow` so
 * crawlers that ever land on these paths receive a deny signal beyond the
 * status code.
 *
 * Single source of truth: this file. The matching legacy `_redirects` rules
 * are kept as harmless defense-in-depth but Cloudflare ignores them in
 * practice (they never fire because the underlying files exist).
 */
export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const path = url.pathname;

  // Source code / helper scripts.
  const inScriptsDir = path.startsWith("/scripts/");

  // Internal report files (.md), Python source (.py), Node helpers (.mjs).
  // Match is case-insensitive on the extension.
  const blockedExtension = /\.(md|py|mjs)$/i.test(path);

  if (inScriptsDir || blockedExtension) {
    return new Response("Not Found", {
      status: 404,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "X-Robots-Tag": "noindex, nofollow",
        "Cache-Control": "public, max-age=300",
      },
    });
  }

  return next();
}
