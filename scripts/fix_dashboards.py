"""
scripts/fix_dashboards.py
Patches all dashboard JSON files:
  1. Adds "instant": true to every Prometheus target (so Pushgateway gauges show up)
  2. Changes time range to now-30m so recent pushes are always visible
  3. Adds "interval": "" and "intervalFactor": 1 for instant queries
"""

import json
import pathlib

DASH_DIR = pathlib.Path("/workspace/config/grafana/dashboards")

def fix_target(target):
    ds = target.get("datasource", {})
    ds_type = ds.get("type", "") if isinstance(ds, dict) else ""
    if ds_type == "prometheus":
        target["instant"] = True
        target["range"] = False
        target.setdefault("interval", "")
        target.setdefault("intervalFactor", 1)
    return target

def fix_dashboard(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    # Fix time range — extend to 2 hours to capture freshly-pushed metrics
    data["time"] = {"from": "now-2h", "to": "now"}
    for panel in data.get("panels", []):
        for t in panel.get("targets", []):
            fix_target(t)
        # Handle collapsed row panels
        for inner in panel.get("panels", []):
            for t in inner.get("targets", []):
                fix_target(t)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Fixed: {path.name}")

for f in sorted(DASH_DIR.glob("*.json")):
    if f.name == "dashboards.yml":
        continue
    fix_dashboard(f)

print("\nAll dashboards patched!")
