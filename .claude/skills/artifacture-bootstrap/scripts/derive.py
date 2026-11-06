#!/usr/bin/env python3
"""
derive.py — deterministic derivation: answers -> ADRs + skeleton stories.

No AI involved. This is the Phase-2 gate artifact: given the same catalog,
mapping and answer set, the output is byte-identical every time.

Usage:
  python3 derive.py --answers answers.json --out ./out [--bundle-dir ..]
  python3 derive.py --validate                  # catalog/mapping sanity only
  python3 derive.py --plan --answers a.json     # print visible nodes + resolved answers

answers.json format:
  { "mode": "fasttrack" | "advanced",
    "answers": { "<node_key>": "<option_value>", ... } }

  "default" is accepted as a legacy alias for "fasttrack".
  "nightmare" is NOT a derivation mode — that level means "no derivation
  at all" and is handled conversationally by the skill, never here.

Resolution rules:
  - Only VISIBLE nodes (all visible_if conditions met, AND semantics) are
    considered. Answers for invisible nodes are rejected (fail loud — an
    answer nobody asked for is a smell, not a convenience).
  - mode=fasttrack: advanced nodes are auto-filled with their default and
    must not appear in the answer set.
  - Missing visible nodes fall back to their default option.
  - Visibility is resolved in topological order; a cycle in the catalog
    aborts derivation (release gate).
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml --break-system-packages")


# ---------- loading ----------

def load_bundle(bundle_dir: Path):
    catalog = yaml.safe_load((bundle_dir / "data" / "catalog.yaml").read_text())
    mapping = yaml.safe_load((bundle_dir / "data" / "mapping.yaml").read_text())
    if mapping.get("catalog_version") != catalog.get("version"):
        sys.exit(
            f"Version mismatch: catalog {catalog.get('version')} "
            f"vs mapping.catalog_version {mapping.get('catalog_version')}"
        )
    return catalog, mapping


# ---------- validation ----------

def toposort(nodes):
    """Kahn's algorithm over visible_if edges. Returns ordered keys or aborts on cycle."""
    keys = [n["key"] for n in nodes]
    if len(keys) != len(set(keys)):
        sys.exit("Duplicate node keys in catalog.")
    by_key = {n["key"]: n for n in nodes}
    indeg = {k: 0 for k in keys}
    children = {k: [] for k in keys}
    for n in nodes:
        for cond in n.get("visible_if", []) or []:
            parent = cond["node"]
            if parent not in by_key:
                sys.exit(f"Node '{n['key']}' references unknown parent '{parent}'.")
            indeg[n["key"]] += 1
            children[parent].append(n["key"])
    # deterministic: preserve catalog file order among ready nodes
    order, ready = [], [k for k in keys if indeg[k] == 0]
    while ready:
        k = ready.pop(0)
        order.append(k)
        for c in children[k]:
            indeg[c] -= 1
            if indeg[c] == 0:
                ready.append(c)
        ready.sort(key=keys.index)
    if len(order) != len(keys):
        cyclic = [k for k in keys if k not in order]
        sys.exit(f"CYCLE in catalog DAG involving: {cyclic} — release refused.")
    return order


def validate_catalog(catalog, mapping, bundle_dir: Path):
    problems = []
    nodes = catalog["nodes"]
    order = toposort(nodes)  # aborts on cycle
    for n in nodes:
        defaults = [o for o in n["options"] if o.get("default")]
        if len(defaults) != 1:
            problems.append(f"Node '{n['key']}' must have exactly one default option.")
        vals = [o["value"] for o in n["options"]]
        if len(vals) != len(set(vals)):
            problems.append(f"Node '{n['key']}' has duplicate option values.")
        for cond in n.get("visible_if", []) or []:
            parent = next(p for p in nodes if p["key"] == cond["node"])
            pvals = {o["value"] for o in parent["options"]}
            unknown = set(map(str, cond["in"])) - {str(v) for v in pvals}
            if unknown:
                problems.append(f"Node '{n['key']}' condition references unknown values {unknown} of '{cond['node']}'.")
        tpl = bundle_dir / "templates" / "adr" / n["adr_template"]
        if not tpl.exists():
            problems.append(f"Missing ADR template: {tpl.name}")
    node_keys = {n["key"] for n in nodes}
    for m in catalog.get("mandatory_adrs", []) or []:
        if m["key"] in node_keys:
            problems.append(f"'{m['key']}' is both a node and a mandatory ADR — pick one.")
        tpl = bundle_dir / "templates" / "adr" / m["adr_template"]
        if not tpl.exists():
            problems.append(f"Missing ADR template: {tpl.name}")
        for cond in m.get("visible_if", []) or []:
            if cond["node"] not in node_keys:
                problems.append(f"Mandatory ADR '{m['key']}' references unknown node '{cond['node']}'.")
    for r in mapping["rules"]:
        tpl = bundle_dir / "templates" / "stories" / r["story_template"]
        if not tpl.exists():
            problems.append(f"Missing story template: {tpl.name}")
        for cond in r.get("conditions", []) or []:
            if cond["node"] not in node_keys:
                problems.append(f"Mapping rule '{r['story_template']}' references unknown node '{cond['node']}'.")
    if problems:
        sys.exit("Catalog/mapping invalid:\n  - " + "\n  - ".join(problems))
    return order


# ---------- resolution ----------

DERIVATION_MODES = ("fasttrack", "advanced")


def normalize_mode(mode: str) -> str:
    """fasttrack | advanced, with 'default' as legacy alias.

    'nightmare' is a real level in the skill, but it means 'derive nothing'.
    Reaching this function with it is a bug in the caller, not a user error.
    """
    m = str(mode or "fasttrack").strip().lower()
    if m == "default":
        return "fasttrack"
    if m == "nightmare":
        sys.exit(
            "mode=nightmare derives nothing — the skill handles that level "
            "conversationally. derive.py must not be called for it."
        )
    if m not in DERIVATION_MODES:
        sys.exit(f"Unknown mode '{mode}'. Legal: {list(DERIVATION_MODES)} (or 'default').")
    return m


def resolve(catalog, user_answers: dict, mode: str, order):
    """Walk DAG in topo order, compute visibility, apply defaults. Returns
    (resolved_answers, visible_keys, deviations)."""
    by_key = {n["key"]: n for n in catalog["nodes"]}
    resolved, visible = {}, []
    deviations = []

    def default_of(n):
        return next(o["value"] for o in n["options"] if o.get("default"))

    for key in order:
        n = by_key[key]
        conds = n.get("visible_if", []) or []
        is_visible = all(
            str(resolved.get(c["node"])) in {str(v) for v in c["in"]} for c in conds
        )
        if not is_visible:
            if key in user_answers:
                sys.exit(f"Answer given for invisible node '{key}' — refusing (answers must match the DAG).")
            continue
        visible.append(key)
        if n.get("advanced") and mode == "fasttrack":
            if key in user_answers:
                sys.exit(f"Advanced node '{key}' answered in fasttrack mode — use mode=advanced.")
            resolved[key] = default_of(n)
            continue
        if key in user_answers:
            val = str(user_answers[key])
            legal = {str(o["value"]) for o in n["options"]}
            if val not in legal:
                sys.exit(f"Illegal value '{val}' for node '{key}'. Legal: {sorted(legal)}")
            resolved[key] = val
            if val != str(default_of(n)):
                deviations.append(key)
        else:
            resolved[key] = default_of(n)

    extra = set(user_answers) - set(visible)
    if extra:
        sys.exit(f"Answers for unknown/invisible nodes: {sorted(extra)}")
    return resolved, visible, deviations


# ---------- generation ----------

def fill(template: str, params: dict) -> str:
    def sub(m):
        key = m.group(1)
        if key not in params:
            sys.exit(f"Template placeholder '{{{key}}}' has no value. Params: {sorted(params)}")
        return str(params[key])
    return re.sub(r"\{([a-z_.]+)\}", sub, template)


def resolve_param(value: str, resolved: dict):
    m = re.fullmatch(r"\{answers\.([a-z_]+)\}", str(value))
    if not m:
        return value
    return resolved.get(m.group(1), "n/a")


def generate(catalog, mapping, resolved, visible, deviations, bundle_dir: Path, out: Path,
             mode: str = "fasttrack"):
    today = date.today().isoformat()
    by_key = {n["key"]: n for n in catalog["nodes"]}

    # Root-level ADR/ per init-artifacture-umbrella convention (NOT docs/adr).
    adr_dir = out / "ADR"
    adr_dir.mkdir(parents=True, exist_ok=True)
    adr_index = []
    for i, key in enumerate(visible, start=1):
        n = by_key[key]
        opt = next(o for o in n["options"] if str(o["value"]) == str(resolved[key]))
        tpl = (bundle_dir / "templates" / "adr" / n["adr_template"]).read_text()
        body = fill(tpl, {
            "n": f"{i:03d}",
            "date": today,
            "answer_value": opt["value"],
            "answer_label": opt["label"],
            "default_note": "(bewusste Abweichung vom Default)" if key in deviations
                            else "(Haus-Default, unverändert übernommen)",
        })
        fname = f"{i:03d}-{key.replace('_', '-')}.md"
        (adr_dir / fname).write_text(body)
        adr_index.append({"file": fname, "node": key, "value": resolved[key],
                          "deviation": key in deviations})

    # Mandatory ADRs: house rules, no enum, no deviation. Numbered after the
    # node ADRs so answer-driven numbering stays stable.
    for m in catalog.get("mandatory_adrs", []) or []:
        conds = m.get("visible_if", []) or []
        if not all(str(resolved.get(c["node"])) in {str(v) for v in c["in"]} for c in conds):
            continue
        i = len(adr_index) + 1
        tpl = (bundle_dir / "templates" / "adr" / m["adr_template"]).read_text()
        body = fill(tpl, {"n": f"{i:03d}", "date": today})
        fname = f"{i:03d}-{m['key'].replace('_', '-')}.md"
        (adr_dir / fname).write_text(body)
        adr_index.append({"file": fname, "node": m["key"], "value": "mandatory",
                          "deviation": False})

    stories = []
    for rule in sorted(mapping["rules"], key=lambda r: r["sort_order"]):
        conds = rule.get("conditions", []) or []
        if not all(str(resolved.get(c["node"])) in {str(v) for v in c["in"]} for c in conds):
            continue
        tpl = (bundle_dir / "templates" / "stories" / rule["story_template"]).read_text()
        params = {k: resolve_param(v, resolved) for k, v in (rule.get("params") or {}).items()}
        params.setdefault("catalog_version", catalog["version"])
        body = fill(tpl, params)
        title = re.search(r'^title:\s*"(.+)"', body, re.M).group(1)
        stories.append({"sort_order": rule["sort_order"],
                        "template": rule["story_template"],
                        "title": title, "spec": body})

    slots = [s["sort_order"] for s in stories]
    assert len(slots) == len(set(slots)), f"Mapping produced two stories in one slot: {slots}"

    (out / "stories.json").write_text(json.dumps(stories, indent=2, ensure_ascii=False))
    manifest = {
        "catalog_version": catalog["version"],
        "derived_at": today,
        "mode": mode,
        "answers": resolved,
        "deviations_from_default": deviations,
        "adrs": adr_index,
        "story_count": len(stories),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    return manifest, stories


# ---------- cli ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", type=Path)
    ap.add_argument("--out", type=Path, default=Path("./out"))
    ap.add_argument("--bundle-dir", type=Path,
                    default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--plan", action="store_true")
    args = ap.parse_args()

    catalog, mapping = load_bundle(args.bundle_dir)
    order = validate_catalog(catalog, mapping, args.bundle_dir)
    if args.validate:
        print(f"OK — catalog {catalog['version']} valid, {len(order)} nodes, topo order: {order}")
        return

    if not args.answers:
        sys.exit("--answers required (or use --validate)")
    payload = json.loads(args.answers.read_text())
    mode = normalize_mode(payload.get("mode", "fasttrack"))
    resolved, visible, deviations = resolve(catalog, payload.get("answers", {}), mode, order)

    if args.plan:
        advanced_keys = [n["key"] for n in catalog["nodes"]
                         if n.get("advanced") and n["key"] in visible]
        print(json.dumps({"mode": mode, "visible": visible,
                          "asked": [k for k in visible
                                    if not (mode == "fasttrack" and k in advanced_keys)],
                          "resolved": resolved, "deviations": deviations}, indent=2))
        return

    manifest, stories = generate(catalog, mapping, resolved, visible, deviations,
                                 args.bundle_dir, args.out, mode)
    print(f"Derived {len(manifest['adrs'])} ADRs and {len(stories)} stories "
          f"-> {args.out}/ (catalog {manifest['catalog_version']})")
    for s in stories:
        print(f"  [{s['sort_order']:>3}] {s['title']}")


if __name__ == "__main__":
    main()
