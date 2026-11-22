"""Extract speed cameras and speed bumps from an OpenStreetMap .pbf extract.

Usage:
    python -I tools/extract_hazards.py egypt-latest.osm.pbf app/src/main/assets/hazards_eg.json

Source data: https://download.geofabrik.de/africa/egypt.html (ODbL, © OpenStreetMap contributors).
"""
import datetime
import json
import re
import sys

import osmium

BUMP_VALUES = {"bump", "hump", "table", "cushion", "yes", "dip", "rumble_strip", "speed_bump"}


def speed(tags):
    m = re.search(r"\d+", tags.get("maxspeed", "") or "")
    if not m:
        return 0
    v = int(m.group())
    return int(v * 1.609) if "mph" in tags.get("maxspeed", "") else v


class Handler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.items = []

    def _kind(self, tags):
        if tags.get("highway") == "speed_camera" or tags.get("enforcement") == "maxspeed":
            return 0
        if tags.get("traffic_calming") in BUMP_VALUES or tags.get("highway") == "speed_bump":
            return 1
        return None

    def node(self, n):
        k = self._kind(n.tags)
        if k is not None:
            self.items.append([k, round(n.location.lat, 6), round(n.location.lon, 6), speed(n.tags), f"n{n.id}"])

    def way(self, w):
        k = self._kind(w.tags)
        if k is None or len(w.nodes) == 0:
            return
        try:
            lats = [nd.location.lat for nd in w.nodes]
            lons = [nd.location.lon for nd in w.nodes]
        except osmium.InvalidLocationError:
            return
        self.items.append([k, round(sum(lats) / len(lats), 6), round(sum(lons) / len(lons), 6),
                           speed(w.tags), f"w{w.id}"])


def main(src, dst):
    h = Handler()
    h.apply_file(src, locations=True)
    out = {"date": datetime.date.today().isoformat(), "source": "© OpenStreetMap contributors (ODbL)",
           "items": h.items}
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, separators=(",", ":"))
    cams = sum(1 for i in h.items if i[0] == 0)
    print(f"cameras={cams} bumps={len(h.items) - cams} -> {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
