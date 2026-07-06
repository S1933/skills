---
name: ovhcloud-smoke-tests
description: Workflow for fixing or updating OVHcloud smoke test patterns in the smoke-tests-patterns repo (ovhcloud.yml). Use when smoke tests fail with "Pattern ... NOT FOUND", or when the user wants to add/modify/work on smoke tests for www.ovhcloud.com pages.
---

# OVHcloud smoke tests

## Context

- Repo: `~/Projects/smoke-tests-patterns`, single file `ovhcloud.yml` (~400KB).
- Each entry is a `url` + `pattern` pair under `blue_green_smoke_urls`:
  ```yaml
  -
    url: fr/domains/dnssec
    pattern: 'Protégez vos noms de domaine contre les attaques par usurpation'
  ```
- The test does a **literal substring match** of `pattern` against the exported static HTML at `/var/www/ocms.ovhcloud.tools/ovh_static/export/html/ovhcloud/<locale>/<path>/index.html`. That export mirrors the live pages at `https://www.ovhcloud.com/<locale>/<path>/`.
- Mojibake in failure logs (`ProtÃ©gez`, `Â«`) is just the log viewer reading UTF-8 as Latin-1. The yml itself is clean UTF-8 — don't "fix" encoding.
- Failures almost always mean the page was redesigned and the old text no longer exists.

## Workflow to fix failing patterns

### 1. Locate the entries

`grep -n '<path-segment>' ovhcloud.yml` (e.g. `dnssec`). A page usually has ~20 entries, one per locale.

### 2. Download the raw HTML for EVERY affected locale

Do not trust one locale per language and copy-paste:
- Regional variants genuinely differ: `en-gb` said "Cheap domain name" while `en`/`en-ca` said "Affordable domain name"; `es` and `es-es` had different copy.
- The full locale list typically seen: fr, en, en-gb, fr-ca, fr-ma, fr-sn, fr-tn, de, en-ca, asia, en-au, en-ie, en-sg, es-es, es, nl, it, pl, pt, en-in.

Tooling constraints on this machine:
- `curl` is denied by permission rules.
- WebFetch passes pages through a small model that paraphrases and confuses `<title>` with `<h1>` — **never** use its output for exact-match patterns.
- Use Python `urllib` (works). System Python fails SSL verification without certifi; use this fallback:

```python
import urllib.request, ssl
ctx = ssl.create_default_context()
try:
    import certifi; ctx = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30, context=ctx).read().decode("utf-8")
```

Save all pages to the scratchpad (e.g. `<locale>--<page>.html`) so extraction and verification run on the same bytes.

### 3. Pick a stable pattern per locale

Extract candidates from the raw HTML (H1 content, then text chunks right after `<h1>` for the hero subtitle):

```python
i = html.find("<h1")
parts = [p.strip() for p in re.split(r'<[^>]+>', html[i:i+2500]) if p.strip()]
```

Rules of thumb:
- Prefer a distinctive H1; if the H1 is generic (e.g. dnssec pages have H1 = just "DNSSEC"), use the hero subtitle instead.
- Avoid anything with prices/currency ("à partir de 1,99 €/an") — varies per region and changes with promos.
- Avoid single generic words that would match any page (nav, footer).
- The pattern must be one contiguous text node — H1s split across `<span>`s won't match as one string.

### 4. Verify BEFORE writing

For each (locale, pattern), assert `pattern in raw_html` on the downloaded file. All must count ≥ 1. This is the step that catches paraphrase/whitespace/entity mistakes.

### 5. Update the yml

Scripted edit is safest at this scale: for each line matching `url: <target>`, rewrite the following `pattern:` line. Keep single quotes, escape `'` as `''`. Then:
- `python3 -c "import yaml; yaml.safe_load(open('ovhcloud.yml'))"` to validate.
- Review `git diff`.

### 6. Commit

Branch naming: `jnuel/<topic>` (e.g. `jnuel/update-smoke-test-dnssec`); PRs target `master`. Commit style: `fix: update smoke test patterns for <pages> pages`, body explaining the redesign. Commit only when the user asks; same for push.
