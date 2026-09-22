import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from werkzeug.security import check_password_hash

from database.db import init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "dev-secret-key"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        try:
            create_user(name, email, password)
        except sqlite3.IntegrityError:
            flash("Email already registered.", "error")
            return render_template("register.html")

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("login"))
    else:
        abort(405)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("landing"))
    else:
        abort(405)


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": session.get("user_name", "Demo User"),
        "email": "demo@spendly.com",
        "initials": "".join(w[0].upper() for w in session.get("user_name", "Demo User").split() if w),
        "member_since": "April 2026",
    }

    stats = {
        "total": "142.83",
        "count": 6,
        "top_category": "Food",
    }

    expenses = [
        {"id": 1, "date": "05 Apr 2026", "description": "Groceries from REWE", "category": "Food", "amount": "42.50"},
        {"id": 2, "date": "04 Apr 2026", "description": "Deutschlandticket (Student)", "category": "Transport", "amount": "38.00"},
        {"id": 3, "date": "03 Apr 2026", "description": "Weekly haul from Lidl", "category": "Food", "amount": "24.80"},
        {"id": 4, "date": "02 Apr 2026", "description": "Wi-Fi / Internet bill", "category": "Bills", "amount": "39.99"},
        {"id": 5, "date": "01 Apr 2026", "description": "Cinema night with friends", "category": "Entertainment", "amount": "14.00"},
    ]

    categories = [
        {"name": "Food", "amount": "67.30", "percent": 47},
        {"name": "Transport", "amount": "38.00", "percent": 27},
        {"name": "Bills", "amount": "39.99", "percent": 15},
        {"name": "Entertainment", "amount": "14.00", "percent": 11},
    ]

    presets = {
        "this_month": {"date_from": "2026-04-01", "date_to": "2026-04-30"},
        "last_3": {"date_from": "2026-02-01", "date_to": "2026-04-30"},
        "last_6": {"date_from": "2025-11-01", "date_to": "2026-04-30"},
    }

    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        expenses=expenses,
        categories=categories,
        date_from=date_from,
        date_to=date_to,
        presets=presets,
    )


@app.route("/analytics")
def analytics():
    return "Analytics page — coming in a later step"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
