# Spec: Login and Logout

## Overview
Implement session-based authentication so registered users can sign in and out of Spendly. This step upgrades the existing stub `GET /login` route into a fully functional form that accepts a POST, verifies credentials against the `users` table, and establishes a session. It also replaces the `/logout` placeholder with real session-clearing logic. `base.html` already branches its nav on `session.user_id` and links to `url_for('logout')`, `url_for('profile')`, and `url_for('analytics')` — this step makes `session.user_id` real and makes `/logout` work, unblocking those nav links (the `profile` and `analytics` routes themselves remain out of scope and are covered by later steps).

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`, `get_user_by_email()`)
- Step 02 — Registration (users must be able to register before they can log in)

## Routes
- `GET /login` — render login form — public (already exists as stub, upgrade it)
- `POST /login` — verify credentials, establish session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/login` — logged-in (currently a placeholder string, replace it)

## Database changes
No new tables or columns. The existing `users` table and `get_user_by_email()` helper in `database/db.py` cover all requirements. No new DB helpers needed.

## Templates
- **Modify:** `templates/login.html`
  - Form already posts to `url_for('login')` with `method="POST"` and has `name` attributes on `email`/`password` — no structural changes needed
  - Add a block to display a flashed error message (e.g. "Invalid email or password"), matching the flash pattern used in `register.html`

## Files to change
- `app.py`:
  - Upgrade `login()` to accept `methods=["GET", "POST"]`
  - On `POST`: look up the user via `get_user_by_email()`, verify the password with `werkzeug.security.check_password_hash`, and on success set `session["user_id"]` (and optionally `session["user_name"]`) then `redirect(url_for('profile'))`
  - On failure (no such email, or wrong password): `flash` a generic "Invalid email or password" error and re-render `login.html` — do not reveal whether the email exists
  - Replace the `logout()` placeholder: clear the session (`session.clear()` or `session.pop("user_id", None)`) and `redirect(url_for('login'))`
  - Import `session` and `check_password_hash` where needed
- `templates/login.html` — add flash message display block

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security.check_password_hash` (already installed via `werkzeug`) and Flask's built-in `session` / `flash` / `redirect` / `url_for`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL (reuse `get_user_by_email()`, no new raw SQL needed)
- Passwords hashed with werkzeug — verify with `check_password_hash`, never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode URLs
- On invalid login, show one generic error message — do not distinguish "email not found" from "wrong password"
- `session.clear()` (or removing `user_id`) must fully log the user out — no residual session data
- Use `abort(405)` if an unsupported HTTP method reaches `/login`
- Do not implement `/profile` or `analytics` route logic in this step — only enough for `/login` to redirect somewhere reasonable and for `/logout` to be reachable from the nav once `session.user_id` is set

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting valid demo credentials (`demo@spendly.com` / `demo123`) sets `session.user_id` and redirects toward `/profile`
- [ ] Submitting an unknown email re-renders the form with a generic "Invalid email or password" error, no session set
- [ ] Submitting a known email with the wrong password re-renders the form with the same generic error, no session set
- [ ] After a successful login, `base.html`'s nav shows "Analytics" / "Dashboard" / "Sign out" instead of "Sign in" / "Get started"
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/login`, and the nav reverts to the logged-out state
- [ ] No plaintext password comparison anywhere in the code
