"""Database models for the Notes App.

This file defines the SQLAlchemy models used by the application:
- `User`: represents an account with an email, password, and name
- `Note`: represents a short text note tied to a user

Beginners: models are plain Python classes that inherit from
`db.Model`. Columns define the table fields and types.
"""

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    """A note created by a user.

    Fields:
    - `id`: primary key (unique identifier)
    - `data`: the text content of the note
    - `date`: creation timestamp (defaults to now)
    - `user_id`: foreign key linking to the User who owns the note
    """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    """A user account model.

    Inherits `UserMixin` from Flask-Login which provides default
    implementations for common user methods (is_authenticated, etc.).
    Fields:
    - `id`, `email`, `password`, `name`, and a relationship `notes`.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    # `notes` will be a list of Note objects associated with this user
    notes = db.relationship('Note')
