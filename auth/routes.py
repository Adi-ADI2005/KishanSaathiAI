from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import users_collection

auth_bp = Blueprint("auth", __name__)


# ==========================
# SIGNUP
# ==========================
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name=request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validation
        if not all([first_name, email, password, confirm_password]):
            flash("All fields required", "error")
            return redirect(url_for("auth.signup"))

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("auth.signup"))

        # Check existing user
        if users_collection.find_one({"email": email}):
            flash("Email already exists", "error")
            return redirect(url_for("auth.signup"))
        # Save user
        users_collection.insert_one({
            "first_name": first_name,
            "last_name":last_name,
            "email": email,
            "password": password,
            "role": "farmer"
        })

        flash("Signup successful! Login now.", "success")
        return redirect(url_for("auth.signin"))

    return render_template("signup.html")


# ==========================
# SIGNIN
# ==========================

@auth_bp.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users_collection.find_one({"email": email})

        if user and user["password"] == password:
            session["user"] = user["email"]
            session["role"] = user.get("role", "farmer")

            # ✅ ADD THIS (IMPORTANT)
            session["first_name"] = user.get("first_name", "User")

            flash("Login successful!", "success")

            # 🔥 Role-based redirect
            if session["role"] == "admin":
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("home"))

        flash("Invalid email or password", "error")

    return render_template("signin.html")

# ==========================
# LOGOUT
# ==========================
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.signin"))