import os
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User

app = create_app()

def create_admin():
    with app.app_context():
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        admin_pass = os.environ.get("ADMIN_PASS", "admin123")
        existing = User.query.filter_by(email=admin_email).first()
        if existing:
            print("Admin already exists:", admin_email)
            return
        u = User(username="admin", email=admin_email,
                 password_hash=generate_password_hash(admin_pass),
                 role="admin")
        db.session.add(u)
        db.session.commit()
        print(f"Admin created: {admin_email} / {admin_pass}")

if __name__ == "__main__":
    create_admin()
