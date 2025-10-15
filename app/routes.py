from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from . import db
from .models import User, PickupRequest
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("main.login"))
        hashed = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=hashed, role="user")
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("main.admin_dashboard"))
        else:
            return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid credentials.", "danger")
            return render_template("login.html")
        login_user(user)
        flash("Logged in successfully.", "success")
        if user.role == "admin":
            return redirect(url_for("main.admin_dashboard"))
        else:
            return redirect(url_for("main.dashboard"))
    return render_template("login.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))

@main.route("/dashboard")
@login_required
def dashboard():
    my_requests = PickupRequest.query.filter_by(user_id=current_user.id).order_by(PickupRequest.request_date.desc()).all()
    return render_template("dashboard.html", requests=my_requests)

@main.route("/request-pickup", methods=["GET", "POST"])
@login_required
def request_pickup():
    if request.method == "POST":
        item_type = request.form.get("item_type", "").strip()
        quantity = request.form.get("quantity", "1")
        location = request.form.get("location", "").strip()
        if not item_type or not location:
            flash("Item type and location are required.", "danger")
            return render_template("request_pickup.html")
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            flash("Quantity must be a positive integer.", "danger")
            return render_template("request_pickup.html")
        pr = PickupRequest(user_id=current_user.id, item_type=item_type, quantity=quantity, location=location, status="Pending")
        db.session.add(pr)
        db.session.commit()
        flash("Pickup request submitted successfully.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("request_pickup.html")

def require_admin():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(403)

@main.route("/admin")
@login_required
def admin_dashboard():
    require_admin()
    all_requests = PickupRequest.query.order_by(PickupRequest.request_date.desc()).all()
    return render_template("admin_dashboard.html", requests=all_requests)

@main.route("/admin/update-status/<int:request_id>", methods=["POST"])
@login_required
def update_status(request_id):
    require_admin()
    new_status = request.form.get("status")
    pr = PickupRequest.query.get_or_404(request_id)
    if new_status not in ("Pending", "Scheduled", "Completed", "Cancelled"):
        flash("Invalid status.", "danger")
        return redirect(url_for("main.admin_dashboard"))
    pr.status = new_status
    db.session.commit()
    flash(f"Request #{pr.id} status updated to {new_status}.", "success")
    return redirect(url_for("main.admin_dashboard"))

@main.route("/cancel-request/<int:request_id>", methods=["POST"])
@login_required
def cancel_request(request_id):
    pr = PickupRequest.query.get_or_404(request_id)
    if pr.user_id != current_user.id:
        flash("You are not authorized to cancel this request.", "danger")
        return redirect(url_for("main.dashboard"))
    if pr.status in ("Completed", "Cancelled"):
        flash("Request already closed.", "warning")
        return redirect(url_for("main.dashboard"))

    pr.status = "Cancelled"
    db.session.commit()
    flash(f"Request #{pr.id} has been cancelled.", "success")
    return redirect(url_for("main.dashboard"))
    
