# Maintaining This Skill

This skill documents [django-unfold](https://github.com/unfoldadmin/django-unfold), which releases **frequently** and occasionally changes or removes APIs. This guide is the repeatable process for refreshing the skill against a new Unfold release. It is for maintainers only — it is not loaded into Claude Code at runtime.

> **Iron rule: ground every fact in the upstream source, never in memory.** Unfold's API moves fast and model training data lags. Each claim in the skill should be traceable to either the docs ([unfoldadmin.com/docs](https://unfoldadmin.com/docs/)) or the source ([github.com/unfoldadmin/django-unfold](https://github.com/unfoldadmin/django-unfold)). When the two disagree, the source wins (the docs sometimes lag or contain typos — e.g. the dialog `submit_text` vs `form_submit_text` discrepancy).

## When to refresh

- A new Unfold release adds features, renames/removes APIs, or changes the supported Django/Python range.
- Someone reports the skill produced code that doesn't match current Unfold.

## Procedure

### 1. Establish the target version and the delta

- Latest version + supported runtimes: `https://pypi.org/pypi/django-unfold/json` (read `info.version`, `info.requires_dist`, classifiers).
- What changed: read `CHANGELOG.md` on `main` from the last-documented version forward. Note new `unfold.contrib.*` apps, new `ModelAdmin` attributes, new decorators/params, new components, new settings keys, and any removals.

### 2. Update the compatibility block

If the supported Django/Python range moved, update the **"Version & Compatibility"** table in `SKILL.md` and the one-line "Targets …" notes in `README.md` and `CLAUDE.md`.

### 3. Research per feature cluster (grounded)

Work cluster by cluster; for each, pull **exact identifiers** (class names, import paths, settings keys, signatures, template-tag paths) from docs **and** source:

| Cluster | Primary source files |
|---------|----------------------|
| Integrations | `docs/integrations/*`, `src/unfold/contrib/` (enumerate submodules) |
| Settings / command / sidebar / dashboard | `src/unfold/settings.py` (`CONFIG_DEFAULTS`), `src/unfold/sites.py`, `docs/configuration/*` |
| Components | `src/unfold/templates/unfold/components/`, `src/unfold/templatetags/unfold.py`, `docs/components/*` |
| Filters | `src/unfold/contrib/filters/admin/`, `docs/filters/*` |
| Inlines / sections / datasets | `src/unfold/admin.py`, `sections.py`, `datasets.py`, `paginator.py`, `docs/inlines/*`, `docs/configuration/*` |
| Actions / decorators / widgets / forms | `src/unfold/decorators.py`, `enums.py`, `widgets.py`, `dataclasses.py`, `src/unfold/contrib/forms/widgets.py`, `docs/actions/*`, `docs/decorators/*` |

Parallelising this across one research agent per cluster works well. Have each return verbatim identifiers, minimal snippets, source URLs, and an explicit list of anything it could **not** verify (treat unverified items as "do not document" or document with a clear caveat).

### 4. Apply changes

Update the matching files, keeping them consistent with each other:

- `SKILL.md` — quick-start, the third-party detection table, the "Newer Features" map, the ModelAdmin attributes table, and the reference-routing tables.
- `references/*.md` — the cluster reference files. Add a new reference file when a surface is large (that's how `components.md` and `integrations.md` were added).
- `examples/*` — keep runnable-shaped and idiomatic.
- Structure listings in `README.md` and `CLAUDE.md`.

### 5. Verify

Run a consistency sweep, then a retrieval test:

```bash
# Cross-references resolve
grep -oh "references/[a-z-]*\.md" SKILL.md | sort -u | while read f; do test -f "$f" && echo "OK $f" || echo "MISSING $f"; done

# No stale identifiers left behind (extend per release)
grep -rn "command_search\|UnfoldAdminPasswordInput\|UnfoldRelatedFieldWidgetWrapper" . --include="*.md" --include="*.py"
```

**Retrieval test (the real gate):** dispatch fresh agents, each restricted to the skill files (no internet, no prior Unfold knowledge), each given a realistic task that exercises a corrected or new area. Grade their output against the verified upstream facts. An agent that has to *infer* an answer, or gets it wrong, points at a gap to close. This is how the detail-action dialog-signature gap and a bad example signature were caught during the 0.97.x refresh.

## Notes carried forward (recheck each release)

- **Docs vs source mismatches** seen historically: dialog key is `form_submit_text` (docs say `submit_text`); `SearchResult` takes keyword args (docs show dict-call syntax); the filters package `__all__` has a bug, so import filter classes by name, not `import *`.
- **No `unfold.contrib.djangoql`** app exists — djangoql styling is automatic but the search needs djangoql's own `DjangoQLSearchMixin`. Re-confirm this each release.
- **Settings callables:** branding assets, `STYLES`/`SCRIPTS`, and `LOGIN` images are callables `lambda request: static(...)`, not path strings.
- **MRO order differs per integration** — reproduce each as documented rather than normalizing.
