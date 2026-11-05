---
name: aurora-validate
description: "Use before delivering any Aurora page: run the repo auditor and measure the render instead of trusting the markup."
version: 1.0.0
license: MIT
tags: [design-system, css, qa, audit, aurora]
---

# Aurora — validate before you deliver

The lint catches vocabulary and rules. The browser catches what the lint cannot see. A page is
done when **both** are green — never when it "looks fine".

## 0. First, the tool that ships with the plugin

```
aurora_validate(path="page.html")     # or html="<html>…"
```

It answers offline, in milliseconds, straight from the bundled census: invented classes,
packs used but not linked, gradients, `backdrop-filter`, `!important`, hand-written colours,
emojis in UI, duplicate `<h1>`, missing attribution. You get `ok`, `failures` (must fix) and
`warnings` (read them). It is a subset of the repository auditor — narrower, but it runs
anywhere, including machines without a clone of the design system.

Loop until `ok: true`, then continue below for the checks a linter cannot do. The repository
auditor stays the final judge when the clone is available.

## 1. The judge: `auditar-uso.py`

With a clone of the repo (`~/Projects/Aurora` or wherever it lives):

```bash
python3 scripts/auditar-uso.py mi-pagina.html
```

It checks: invented classes, packs that are needed but not linked, gradients,
`backdrop-filter`, `!important`, hand-written colours, desktop-first CSS, duplicate `<h1>`,
emojis in UI, and the attribution footer. It prints in Spanish — read the last line:

```
→ 0 fallos · 2 avisos
```

**Zero `fallos` (failures) is the bar.** `avisos` (warnings) do not block, but each one is a question you answer in
your head: a saturated-colour budget overrun, a brand moment with no accent. The canonical
examples ship with one or two warnings, so seeing a warning is not automatically a bug — seeing
a failure always is.

It is also the reference implementation: if you build your own checker (another language, a
generated page), pass the *same* file through both and compare verdicts. Then sabotage a copy
(one invented class + a gradient + `backdrop-filter` + `!important` + two `<h1>` + one emoji)
and confirm your checker reports all six.

## 2. Never trust classes in the DOM

`nz-*` classes appear in the markup even when the CDN 404s and no CSS loaded. Prove the render:

```js
document.styleSheets.length                     // the sheets that actually loaded
getComputedStyle(document.querySelector('.nz-navbar')).display   // "flex", not "block"
```

If the CSS comes from the CDN, 1–2 s is not enough: measured, at 1.2 s the navbar reported
36 px / weight 400 (no sheet) and at 5 s 61 px / `display:flex`. Wait, re-measure, then judge.

## 3. Measure mobile for real

```js
await page.setViewportSize({width: 320, height: 760});   // BEFORE navigating
const ok = await page.evaluate(() =>
  document.scrollingElement.scrollWidth === document.scrollingElement.clientWidth);
```

Three traps that produce fake results:

- **Apply the device metrics before navigating.** Overriding a page that is already laid out
  measures the previous viewport: you get phantom overflows (container at 374 px with
  `clientWidth` 320).
- **Confirm the width took.** If `innerWidth` still says 1264 after asking for 360, the test
  did not run. Repeat in a clean session; never interpret that measurement.
- `window.open` does not help on `file://` (null origin blocks access to the child document).

Also check the primary action at 320/360/390: `getBoundingClientRect()` of the control against
`innerHeight`. If it falls below the fold, it is not delivered.

## 4. Check the furniture nobody checks

- **Links and anchors**: no `#` placeholders in a product, no broken relative paths. Moving a
  folder means rewriting relative paths — a real incident served every page without CSS because
  paths stayed one level up, and the HTML was still valid.
- **Images and icons**: count referenced assets against present ones. A helper that returns an
  empty string when an asset is missing hides the failure: the lint passes, nothing overflows,
  the icon is just... not there.
- **Print**, if the deliverable is a report.

## 5. Report

Deliver with the evidence, not the adjective:

```
auditar-uso.py ....... 0 findings
sheets loaded ........ 7
mobile 320/360/390 ... scrollWidth == clientWidth ✔
primary action ....... 412 px < 760 (visible) ✔
computed .nz-navbar .. display:flex ✔
```

If a check fails, reproduce the command by hand before concluding the page is broken: the
failure may be in your test, not the deliverable. Say which one it was.
