# Radar Maps data

Speed cameras and speed bumps in Egypt for the Radar Maps app.

- `hazards_eg.json` — extracted from OpenStreetMap every week by `.github/workflows/update.yml`
  (source: Geofabrik Egypt extract, © OpenStreetMap contributors, ODbL).
  Format: `{"date": "YYYY-MM-DD", "items": [[type, lat, lon, maxspeed, osmId], ...]}`,
  type 0 = camera, 1 = bump, maxspeed 0 = unknown.
- `user/edits.json` — your own changes, kept apart from the OSM data so the weekly update never overwrites them:
  `{"added": [[type, lat, lon, maxspeed, id], ...], "removed": ["osm-n123", ...]}`.
  The app shows the added ones after every update, and hides the removed ones if you chose
  "keep removed ones removed" in the app.

Run the update by hand: Actions → "Weekly radar & bump update" → Run workflow.
