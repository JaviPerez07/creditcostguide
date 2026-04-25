# CreditCostGuide Redirect Cleanup Report

Date: 2026-04-25

## URLs antiguas detectadas

- Detectadas en superficies de redirección válidas:
  - `/index.html`
  - `/contact.html`
  - `/pages/*.html`
  - `http://creditcostguide.com/*`
  - `http://www.creditcostguide.com/*`
  - `https://www.creditcostguide.com/*`
- Detectadas en documentación interna del repo, no en superficies SEO públicas:
  - `search_console_redirect_fix.md`
  - `search_console_expansion_audit.md`
  - `cleanup-report-creditcostguide.md`
- No se detectaron URLs antiguas en:
  - `sitemap.xml`
  - `robots.txt`
  - canonicals HTML
  - `og:url`
  - `twitter:url`
  - JSON-LD en HTML
  - breadcrumbs renderizados
  - navegación y footer renderizados

## Archivos corregidos

- `scripts/build_site.py`
  - `data-page-path` ahora usa la ruta pública limpia en lugar de la ruta física con `.html`.
  - El verificador generado ahora resuelve enlaces absolutos limpios contra archivos físicos `.html`.
  - La comprobación de sitemap generada ahora valida URLs públicas limpias.
- `scripts/verify_site.py`
  - Alineado con URLs limpias para evitar interpretar `/about` o `/pages/foo` como enlaces rotos.
- `main.js`
  - La reescritura para `file://` ahora convierte URLs absolutas limpias a archivos `.html` locales correctamente.
- HTML regenerado desde el generador base
  - Actualizado `data-page-path` renderizado en las páginas regeneradas.

## Redirects comprobados

- `_redirects` mantiene reglas útiles para:
  - `/index.html -> /`
  - `/contact.html -> /contact`
  - `/pages/*.html -> /pages/*`
  - `http -> https`
  - `www -> non-www` en la intención declarada del archivo

## Curl output resumido

- `http://creditcostguide.com/`
  - Resultado: `301 -> https://creditcostguide.com/ -> 200`
  - Estado: OK

- `http://www.creditcostguide.com/`
  - Resultado: `301 -> https://www.creditcostguide.com/ -> 200`
  - Estado: pendiente
  - Nota: no termina en non-www, así que no cumple el objetivo final esperado.

- `https://www.creditcostguide.com/`
  - Resultado: `200`
  - Estado: pendiente
  - Nota: debería redirigir a `https://creditcostguide.com/` si se quiere consolidación total non-www.

- `https://creditcostguide.com/index.html`
  - Resultado: `308 -> / -> 200`
  - Estado: OK

- `https://creditcostguide.com/contact.html`
  - Resultado: `308 -> /contact -> 200`
  - Estado: OK

- `https://creditcostguide.com/pages/credit-cards-guide.html`
  - Resultado: `308 -> /pages/credit-cards-guide -> 200`
  - Estado: OK

- `https://creditcostguide.com/pages/mortgage-guide.html`
  - Resultado: `308 -> /pages/mortgage-guide -> 200`
  - Estado: OK

- URLs limpias verificadas previamente durante la auditoría:
  - `https://creditcostguide.com/ -> 200`
  - `https://creditcostguide.com/contact -> 200`
  - `https://creditcostguide.com/about -> 200`
  - `https://creditcostguide.com/privacy-policy -> 200`
  - `https://creditcostguide.com/pages/personal-loans-guide -> 200`
  - `https://creditcostguide.com/pages/credit-cards-guide -> 200`
  - `https://creditcostguide.com/pages/mortgage-guide -> 200`
  - `https://creditcostguide.com/pages/credit-score-guide -> 200`

## Casos pendientes

- `www` sigue resolviendo en vivo sin consolidarse a non-www:
  - `https://www.creditcostguide.com/` devuelve `200`
  - `http://www.creditcostguide.com/` redirige a `https://www.creditcostguide.com/`, no a `https://creditcostguide.com/`
- Este punto parece de configuración de dominio/edge y no de enlaces internos del repo.

## Resumen final

- El repo ya no expone `.html`, `http`, ni `www` como fuente interna en superficies SEO públicas.
- `sitemap.xml` solo contiene URLs limpias, `https`, sin `.html`, sin `www`.
- Canonicals, `og:url`, `twitter:url`, JSON-LD y breadcrumbs renderizados usan URLs limpias.
- Las redirecciones legacy útiles se mantienen.
- El único caso real pendiente está en la resolución live del host `www`.
