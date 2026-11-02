"""Printify catalogue check: every mug blueprint, its print providers (location) and colour variants.
Reads the key from env PRINTIFY_KEY (never printed). Writes reports/printify/mugs.json + mugs.md."""
import json, os, pathlib, time, urllib.request
KEY = os.environ.get("PRINTIFY_KEY", "").strip()
OUT = pathlib.Path("reports/printify"); OUT.mkdir(parents=True, exist_ok=True)
def get(path):
    for i in range(4):
        try:
            r = urllib.request.Request("https://api.printify.com/v1/" + path, headers={"Authorization": "Bearer " + KEY, "User-Agent": "ZANS"})
            return json.load(urllib.request.urlopen(r, timeout=40))
        except Exception as e:
            print(path, "error", getattr(e, "code", e)); time.sleep(3 * (i + 1))
    return None
if not KEY:
    (OUT / "mugs.md").write_text("No Printify key found in secrets.\n"); raise SystemExit(0)
bps = get("catalog/blueprints.json") or []
mugs = [b for b in bps if "mug" in b.get("title", "").lower()]
res = []; md = ["# Printify mugs (catalogue check)\n"]
for b in mugs:
    pps = get(f"catalog/blueprints/{b['id']}/print_providers.json") or []
    for pp in pps:
        det = get(f"catalog/print_providers/{pp['id']}.json") or {}
        loc = det.get("location", {})
        v = get(f"catalog/blueprints/{b['id']}/print_providers/{pp['id']}/variants.json") or {}
        vars_ = v.get("variants", [])
        opts = sorted({json.dumps(x.get("options", {}), sort_keys=True) for x in vars_})
        row = {"blueprint": b["id"], "title": b["title"], "brand": b.get("brand"), "provider": pp["id"], "provider_name": pp.get("title"),
               "country": loc.get("country"), "city": loc.get("city"), "variants": [{"id": x["id"], "title": x.get("title"), "options": x.get("options")} for x in vars_]}
        res.append(row)
        md.append(f"- {b['id']} {b['title']} | {pp.get('title')} ({loc.get('country')}) | {len(vars_)} variants: " + "; ".join(x.get('title','') for x in vars_)[:600])
        time.sleep(0.4)
(OUT / "mugs.json").write_text(json.dumps(res, indent=1))
(OUT / "mugs.md").write_text("\n".join(md) + "\n")
print(len(mugs), "mug blueprints,", len(res), "provider rows")
