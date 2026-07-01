# UI Components Reference

Unfold ships a library of reusable UI components rendered through a custom `{% component %}` template tag. **Prefer these over hand-writing Tailwind** when a component exists — they already match Unfold's styling and dark mode. Verified against django-unfold 0.97.x source (`src/unfold/templates/unfold/components/`, `src/unfold/templatetags/unfold.py`).

For hand-rolled Tailwind (when no component fits), see `references/templates-and-components.md`.

## The `{% component %}` tag

Load the tagset with `{% load unfold %}`, then include a component by its template path. The block body becomes the `children` variable inside the component.

```django
{% load unfold %}

{% component "unfold/components/card.html" with title="Revenue" size="md" %}
    <p class="text-2xl font-semibold">$12,500</p>
{% endcomponent %}
```

- First positional argument is the **template path string** (e.g. `"unfold/components/card.html"`).
- `with k=v …` passes context to the component.
- The rendered block body is injected as `{{ children }}` (only set when non-empty).
- Add the bare flag `include_context` to also merge the surrounding context into the component.

### `{% capture %}` — build content for a component parameter

Some parameters (like a card's `action`) expect rendered HTML. Capture it first:

```django
{% load unfold %}

{% capture as card_action %}
    {% component "unfold/components/button.html" with href="/admin/app/model/add/" icon="add" %}Add{% endcomponent %}
{% endcapture %}

{% component "unfold/components/card.html" with title="Orders" action=card_action %}
    ...
{% endcomponent %}
```

Use `{% capture as var silent %}…{% endcapture %}` to store without emitting.

### Size keywords

Cards and tables use `size="md"` for **compact** padding; **omitting `size` gives the larger default**. There is no `"lg"` keyword for cards. Buttons and trackers have their own scales (below).

---

## Component catalogue

Every path below exists under `unfold/components/`.

### card — `unfold/components/card.html`

| Param | Effect |
|-------|--------|
| `title` | Header bar with the title. |
| `action` | Right-aligned content in the title row (requires `title`; build it with `{% capture %}`). |
| `title_class` | Extra classes on the title bar. |
| `label` | Floating primary label, top-right. |
| `icon` | Large faded background Material Symbol (KPI look); `icon_class` to style it. |
| `footer` | Content in a bottom bordered bar. |
| `href` | Makes the whole card a link (`<a>`) with hover styling. |
| `size` | `"md"` = compact (`p-3`); omitted = large (`p-6`). |
| `disable_border` | Removes the border, adds a subtle shadow (use on coloured backgrounds). |
| `class` | Extra classes on the root. |

```django
{% component "unfold/components/card.html" with title="Revenue" icon="payments" label="NEW" %}
    <p class="text-2xl">$12,500</p>
{% endcomponent %}
```

### button — `unfold/components/button.html`

| Param | Notes |
|-------|-------|
| `variant` | `"default"`, `"ghost"`, `"secondary"`, `"danger"`. Any other / omitted value → **primary** (filled). |
| `size` | `"xs"`, `"sm"`, `"md"`, `"lg"` (omitted → default padding). |
| `href` | Renders `<a>` instead of `<button>`. |
| `submit` | Adds `type="submit"`; `type` sets an explicit type. |
| `form` | Sets the `form="…"` attribute. |
| `name`, `value`, `title` | Standard attributes. |
| `icon` | Leading Material Symbol. |
| `attrs` | Dict of HTML attrs (e.g. `{"disabled": True, "data-x": "y"}`); `attrs.disabled` also toggles disabled styling. |
| `extra_attrs` | Raw string of extra attributes appended verbatim. |
| `class` | Extra classes. |

The button is always `position: relative` and a Tailwind `group`, so absolutely-positioned or `group-hover:` children work without adding `relative` yourself.

```django
{% component "unfold/components/button.html" with variant="danger" size="sm" submit=1 icon="delete" %}
    Delete
{% endcomponent %}
```

### progress — `unfold/components/progress.html`

| Param | Notes |
|-------|-------|
| `title` | Optional heading. Omit title & description for a bare bar. |
| `description` | Right-aligned pill (e.g. a percentage). |
| `value` | Single-bar percentage (0–100). |
| `progress_class` | Extra classes on the bar. |
| `items` | Multiple segments; each `{"value": int, "title": str?, "progress_class": str?}`. |
| `class` | Root classes. |

```django
{% component "unfold/components/progress.html" with title="Storage" description="72%" value=72 %}{% endcomponent %}
```

### tracker — `unfold/components/tracker.html`

A row of cells (uptime/heatmap style) built from `data`.

| Param | Notes |
|-------|-------|
| `data` | List of items; each `{"href": str?, "tooltip": str?, "color": str?, "class": str?}` (`color` is a bg class). |
| `size` | `"md"` → `h-6`, `"sm"` → `h-4`, omitted → `h-8`. |
| `class` | Root classes. |

```django
{% component "unfold/components/tracker.html" with data=days size="sm" %}{% endcomponent %}
```

### table — `unfold/components/table.html`

| Param | Notes |
|-------|-------|
| `table` | `{"headers": [...], "rows": [...]}`. |
| `title` | Optional heading. |
| `striped` | `striped=1` → alternating row backgrounds. |
| `card_included` | `card_included=1` → flush inside a card (pair with `card_size`). |
| `height` | `max-height` in px + sticky header + scroll. |
| `class` | Root classes. |

Rows can be a simple list (`["a", "b"]`) or a dict with `cols`, optional `attrs`, and an optional nested `table` for **collapsible nested tables**:

```python
mytable = {
    "headers": ["Name", "Total"],
    "rows": [
        ["Alpha", "12"],
        {
            "cols": ["Beta", "8"],
            "attrs": {"data-id": "5"},
            "table": {"headers": ["Sub"], "rows": [["x"]], "collapsible": True},
        },
    ],
}
```

```django
{% component "unfold/components/table.html" with table=mytable striped=1 height=400 %}{% endcomponent %}
```

### Charts — `unfold/components/chart/bar.html`, `chart/line.html`, `chart/cohort.html`

Charts render with **Chart.js 4.4** (bundled, self-hosted). `data` and `options` are **JSON strings** — build them with `json.dumps(...)` in Python.

| Param | Notes |
|-------|-------|
| `data` | JSON string in Chart.js shape: `{"labels": [...], "datasets": [{"label", "data", "backgroundColor", "borderColor"}]}`. |
| `options` | JSON string of extra Chart.js options (no JS functions). |
| `width`, `height`, `class` | Canvas sizing / classes. |

Dataset colours given as CSS-var strings like `"var(--color-primary-500)"` are resolved at render time, so charts follow the Unfold palette and adapt to dark mode.

```python
# admin.py / dashboard callback
import json
context["sales_chart"] = json.dumps({
    "labels": ["Jan", "Feb", "Mar"],
    "datasets": [{
        "label": "Sales",
        "data": [120, 190, 140],
        "backgroundColor": "var(--color-primary-500)",
    }],
})
```

```django
{% component "unfold/components/chart/bar.html" with data=sales_chart height=320 %}{% endcomponent %}
```

`chart/cohort.html` is a pure HTML/Tailwind table (not Chart.js); its `data` is `{"headers": [...], "rows": [...]}` with per-cell `value`/`subtitle`/`color`.

### link — `unfold/components/link.html`

| Param | Notes |
|-------|-------|
| `href` | Target. |
| `icon` | Leading Material Symbol. |
| `external` | Adds `target="_blank"` + trailing `open_in_new` icon. |
| `class` | Extra classes. (`children` = link text.) |

### Layout & text helpers

| Component | Params |
|-----------|--------|
| `unfold/components/container.html` | `class`; centres content (`mx-auto`). |
| `unfold/components/flex.html` | `col` (→ column), `class`. |
| `unfold/components/separator.html` | `vertical` (`=1` → vertical divider), `class`. |
| `unfold/components/icon.html` | `class`; `children` = Material Symbol name. |
| `unfold/components/text.html` | `class`; `children` = paragraph text. |
| `unfold/components/title.html` | `class`; `children` = heading text. |
| `unfold/components/navigation.html` | `items` (list of `{link, title, icon, active}`), `class`. |
| `unfold/components/layer.html` | invisible wrapper — body is just `{{ children }}` (grouping/nesting). |

### Helper includes (not `{% component %}`)

- `unfold/helpers/label.html` — the label/badge primitive: `text`, `variant` (`info`/`danger`/`warning`/`success`/`primary`), `size`, `href`, `icon`, `label_title`, `class`.
- `unfold/helpers/attrs.html` — render a dict of attributes: `{% include "unfold/helpers/attrs.html" with attrs=mydict %}` (`True` → bare attribute, `False` → omitted).

---

## Python component classes (advanced)

For components that need computed context, register a class with `@register_component` and pass `component_class="MyComponent"` to the tag.

```python
from unfold.components import BaseComponent, register_component

@register_component
class StatsComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["users"] = User.objects.count()
        return ctx
```

```django
{% component "myapp/components/stats.html" with component_class="StatsComponent" %}{% endcomponent %}
```

---

## Material Symbols

All components use **Material Symbols** (Outlined style) — `<span class="material-symbols-outlined">name</span>`. The font is **self-hosted** by Unfold (not the Google CDN). Browse names at https://fonts.google.com/icons (family = Material Symbols). This is *not* the legacy "Material Icons" font — names differ.
