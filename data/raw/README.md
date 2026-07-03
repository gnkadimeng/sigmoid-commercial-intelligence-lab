# data/raw/

**Immutable inputs.** Original data exactly as received, never edited in place.

- Treat everything here as read-only. Transformations produce outputs in `data/processed/`.
- Each drop should be accompanied by a note of its provenance (source, date, method) and any usage
  restrictions.
- Contents are git-ignored by default (see `.gitignore`) — commit only small, shareable, licensed
  inputs, and add a note here describing what lives in this zone.

At v0.1 this zone is empty; the lab runs on synthetic data in `data/sample/`.
