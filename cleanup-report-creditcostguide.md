# Cleanup Report — CreditCostGuide

Date: 2026-04-22

## 1. Autor ficticio eliminado

- Nombre detectado: 1 byline individual ficticia detectada en bloques visibles y en schemas Article. El valor legacy exacto se omite en este archivo para mantener los greps finales en `0`.
- Credenciales inventadas: no se detectaron credenciales tipo Licensed, Certified, Dr., MD, EA, CFP, RN, Esq., JD o PhD.
- Archivos modificados (conteo): 69
- Bloques sustituidos por editorial team (conteo): 58 HTML files now render the standardized editorial block.
- Áreas afectadas antes de la limpieza:
  - Bloques visibles de byline en páginas raíz, legales, hubs, artículos y calculadoras.
  - Propiedad `author` en schemas Article.
  - Fallback dinámico de schema Article en `main.js`, generado desde `scripts/build_site.py`.

## 2. Email legacy de contacto

- Ocurrencias pre-limpieza: 2 ocurrencias renderizadas en salida HTML.
- Archivos modificados:
  - `contact.html`
  - `privacy-policy.html`
  - `scripts/build_site.py`
- Estado página Contact: la página ahora muestra el placeholder `We are updating our contact information. Please check back soon.`
- Grep final source:
  - legacy contact string: 0
  - rendered output dirs (`dist/`, `public/`, `build/`): no existen en este proyecto

## 3. Teléfono ficticio

- Detectado: NO
- Ocurrencias: 0

## 4. Frases señaladoras

- Frases detectadas y eliminadas o neutralizadas:
  - `Standalone pages` eliminada del bloque métrico de la home.
  - `AdSense Readiness Checklist` neutralizada en el generador/verificador heredado.
  - `Search Console Checklist` neutralizada en el generador/verificador heredado.
- Bloques completos eliminados de home:
  - Se eliminó el bloque métrico/trust-style que contenía el contador de páginas.

## 5. Social links

- Cantidad de enlaces rotos eliminados: 0
- Hallazgo: no se detectaron iconos sociales con `href="#"`, `href=""`, ni perfiles sociales visibles sin URL válida.

## 6. Metas plantilla (detección)

- Cantidad con patrón detectable: 3 meta descriptions con el mismo arranque literal.
- Patrón común detectado:
  - `Learn how to`
- Patrones solicitados explícitamente y no detectados:
  - `Get practical guidance on`
  - `compare costs and tradeoffs`
  - `understand the records or timelines`
- Generado desde qué archivo:
  - `scripts/build_search_console_expansion.py`

## 7. Datos desactualizados (muestra)

- `scripts/build_search_console_expansion.py:321` — title contains `2025 to 2026`
- `scripts/build_search_console_expansion.py:322` — description contains `2025 and 2026`
- `scripts/build_search_console_expansion.py:323` — hero contains `2025 to 2026`
- `scripts/build_search_console_expansion.py:545` — title contains `2025 to 2026`
- `scripts/build_search_console_expansion.py:546` — description contains `2025 and 2026`
- `scripts/build_search_console_expansion.py:735` — narrative copy contains `For 2025 to 2026 planning`
- `scripts/build_site.py:255` — hardcoded example `$8,000 at 11.9% APR over 36 months`
- `scripts/build_site.py:256` — hardcoded example `$15,000 at 9.4% APR with a 4% fee`
- `scripts/build_site.py:258` — hardcoded example `$4,200 revolving at 24.99% with only minimum payments`
- `scripts/build_site.py:484` — hardcoded calculator default `6.75`

## 8. Redirect loops (check)

- URLs OK:
  - `https://creditcostguide.com/`
  - `https://creditcostguide.com/contact`
  - `https://creditcostguide.com/about`
  - `https://creditcostguide.com/privacy-policy`
  - `https://creditcostguide.com/pages/personal-loans-guide`
  - `https://creditcostguide.com/pages/credit-cards-guide`
  - `https://creditcostguide.com/pages/mortgage-guide`
  - `https://creditcostguide.com/pages/credit-score-guide`
- URLs con redirects múltiples:
  - none detected in the checked set

## 9. Build status

- Build: OK
- Legacy verification script: FAIL
- Motivo: `scripts/verify_site.py` sigue validando enlaces internos y entradas de sitemap como si el sitio publicara rutas con `.html`, por lo que produce falsos positivos contra la arquitectura actual de URLs limpias/extensiónless. No se corrigió en esta pasada por la regla de no arreglar bugs graves fuera de scope.

## 10. Recomendación de prioridad

1. Decidir el email público definitivo y volver a activar el bloque de contacto real desde el generador.
2. Revisar manualmente las meta descriptions repetitivas comenzando por el patrón `Learn how to`.
3. Auditar y actualizar hardcodes sensibles a fecha/rates en ambos generadores.
4. Programar una pasada separada para alinear `scripts/verify_site.py` con la arquitectura real de URLs limpias.
