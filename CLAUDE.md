# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a Flask expense-tracker web app, built as a guided, step-by-step learning exercise. Templates, static assets, and the database layer already exist; `app.py` initializes and seeds the database on startup, but its routes still return plain placeholder strings for `/logout`, `/profile`, and the expense CRUD routes, with no session/auth logic, following a numbered step plan referenced in code comments (Step 1, Step 3, Step 4, Step 7-9, etc.). When asked to "implement the next step," check these comments in `app.py` to find the current step and its expected scope rather than jumping ahead.

**Known gaps** (don't assume these are wired up — verify before relying on them):
- `templates/base.html` links to `url_for('analytics')` and checks `session.user_id`, but `app.py` has no `analytics` route, no session/auth logic, and no `secret_key` configured.
- `templates/register.html` and `templates/login.html` already POST to `url_for('register')` / `url_for('login')`, but those routes in `app.py` only accept GET — submitting either form will 405 until POST handling is added.
- `database/queries.py`'s expense CRUD and analytics helpers aren't called from any route yet — only `init_db()`/`seed_db()` from `database/db.py` are wired up so far.

## Commands

Run all commands from the repository root.

```
pip install -r requirements.txt   # install dependencies
python app.py                     # run dev server on http://localhost:5001 (debug=True)
pytest                            # run tests
pytest path/to/test_file.py::test_name   # run a single test
```

There is no lint/format tooling configured in this repo. There are no tests in the repo yet, despite `pytest` and `pytest-flask` being listed in `requirements.txt` — they're presumably for a later step.

## Architecture

- **`app.py`** — single-file Flask app; all routes are defined directly on the module-level `app` object (no blueprints). At module level (so it runs under `python app.py` and under any WSGI import), it calls `init_db()`/`seed_db()` inside `app.app_context()` to ensure the database exists and is seeded before any request is handled. Templated routes (`/`, `/register`, `/login`, `/terms`, `/privacy`) call `render_template`. Placeholder routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`) currently return plain "coming in Step N" strings and have no real logic yet.
- **`database/db.py`** — `get_db()` opens a `sqlite3` connection to `spendly.db` at the **project root** (`DB_PATH` resolves two directories up from `database/db.py`) with `row_factory = sqlite3.Row` and foreign keys enabled; `init_db()` creates the `users` and `expenses` tables (`CREATE TABLE IF NOT EXISTS`); `seed_db()` inserts one demo user (`demo@spendly.com`) and sample expenses if the `users` table is empty; `create_user()` / `get_user_by_email()` handle auth lookups with `werkzeug.security` password hashing. `spendly.db` is gitignored (bare `spendly.db` pattern, matches at any depth).
- **`database/queries.py`** — expense CRUD (`insert_expense`, `get_expense_by_id`, `update_expense`, `delete_expense_by_id`) and read-side helpers for the profile/analytics views (`get_user_by_id`, `get_recent_transactions`, `get_summary_stats`, `get_category_breakdown`), all scoped by `user_id` and each opening/closing its own connection via `get_db()`. Not yet called from any route in `app.py`.
- **`templates/`** — Jinja2 templates, all extending `base.html`'s `title`/`head`/`content`/`scripts` (and sometimes `flash`) blocks: `landing.html`, `register.html`, `login.html`, `terms.html`, `privacy.html`, `profile.html`, `analytics.html`, `add_expense.html`, `edit_expense.html`. `base.html` defines the shared nav/footer, pulls in the Google Fonts + `static/css/style.css`, and renders flash messages via `get_flashed_messages`.
- **`static/css/`** — `style.css` is the shared base stylesheet; `landing.css`, `profile.css`, `analytics.css`, `add_expense.css` are page-specific overrides loaded from each template's `{% block head %}`.
- **`static/js/main.js`** — minimal, currently near-empty.

When adding a new page, follow the existing pattern: add a route in `app.py` returning `render_template(...)`, create a template under `templates/` extending `base.html`, and link it via `url_for('<endpoint>')` rather than hardcoded paths. When wiring up a route to real data, use `database/db.py` for connections/auth and `database/queries.py` for expense/analytics reads and writes rather than writing raw SQL in `app.py`.
