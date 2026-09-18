# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a Flask expense-tracker web app, built as a guided, step-by-step learning exercise. Most of the codebase is a scaffold: some routes and templates are complete, but the database layer and expense CRUD routes are intentionally left as stubs for the "student" to implement, following a numbered step plan (Step 1, Step 3, Step 4, Step 7-9, etc. — see comments in `app.py` and `database/db.py`). When asked to "implement the next step," check these comments to find the current step and its expected scope rather than jumping ahead.

## Commands

Run all commands from this directory (`expense-tracker/expense-tracker`).

```
pip install -r requirements.txt   # install dependencies
python app.py                     # run dev server on http://localhost:5001 (debug=True)
pytest                            # run tests
pytest path/to/test_file.py::test_name   # run a single test
```

There is no lint/format tooling configured in this repo.

## Architecture

- **`app.py`** — single-file Flask app; all routes are defined directly on the module-level `app` object (no blueprints). Templated routes (`/`, `/register`, `/login`, `/terms`, `/privacy`) call `render_template`. Placeholder routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`) currently return plain "coming in Step N" strings and have no real logic yet.
- **`database/db.py`** — intended to hold `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (creates tables with `CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample dev data). Currently empty; the SQLite file is `expense_tracker.db` (gitignored, created at runtime).
- **`templates/`** — Jinja2 templates. `base.html` defines the shared layout (nav, footer, font/CSS links) with `title`/`head`/`content`/`scripts` blocks; page templates extend it. The brand name "Spendly" and footer tagline live in `base.html`.
- **`static/css/style.css`** — all styling in one stylesheet (no CSS framework).
- **`static/js/main.js`** — minimal, currently near-empty.

When adding a new page, follow the existing pattern: add a route in `app.py` returning `render_template(...)`, create a template under `templates/` extending `base.html`, and link it via `url_for('<endpoint>')` rather than hardcoded paths.
