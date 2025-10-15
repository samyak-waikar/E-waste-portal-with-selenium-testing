from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)

    requests = db.relationship("PickupRequest", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

class PickupRequest(db.Model):
    __tablename__ = "pickup_requests"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_type = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    location = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    request_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PickupRequest {self.id} - {self.item_type} - {self.status}>"
