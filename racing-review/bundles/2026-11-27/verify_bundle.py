"""Recompute every file hash and the combined sha256 for this bundle. Run from the repo root: python racing-review/bundles/2026-11-27/verify_bundle.py"""
import hashlib, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, "..", "..", ".."))
m = json.load(open(os.path.join(here, "MANIFEST.json")))
bad = 0
for f in m["files"]:
    p = os.path.join(root, f["path"])
    if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != f["sha256"]:
        print("MISMATCH", f["path"]); bad += 1
lines = "".join(f'{f["sha256"]}  {f["path"]}\n' for f in sorted(m["files"], key=lambda x: x["path"]))
top = hashlib.sha256(lines.encode()).hexdigest()
print(len(m["files"]), "files,", bad, "mismatches, combined", top, "OK" if top == m["combined_sha256"] and not bad else "FAIL")
sys.exit(1 if bad or top != m["combined_sha256"] else 0)
