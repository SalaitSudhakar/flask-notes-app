"""Views (routes) for the Notes App.

This module registers the main application routes:
- `/` : home page (view and add notes)
- `/delete-note` : AJAX endpoint to delete a note
- `/edit-note` : handle edits to existing notes

Routes use Flask-Login to ensure only authenticated users can
access note operations.
"""

from flask import Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    """Render the home page and handle adding new notes.

    - GET: render `home.html` with the user's notes.
    - POST: add a note submitted from the form, then reload the page.
    """
    if request.method == "POST":
        # Grab the note content from the form
        note = request.form.get("note")

        # Simple length check to avoid empty notes
        if len(note) < 1:
            flash("Note is too short!", "error")
        else:
            try:
                # Create a new Note instance and save it
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash("Note Added!", "success")
            except Exception as e:
                db.session.rollback()
                flash("An error occurred adding your note.", "error")
                print("DB ERROR:", e)

    # `new_user` is optionally used to display a welcome message
    return render_template("home.html", new_user=request.args.get("new_user"))


@views.route("/delete-note", methods=["POST"])
def delete_note():
    """Delete a note via AJAX (expects JSON payload with `noteId`).

    This endpoint checks that the note belongs to the current user
    before deleting it to prevent unauthorized access.
    """
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)

    # Verify the note exists and belongs to the logged-in user
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()

    # Return an empty JSON response (client will refresh the page)
    return jsonify({})


@views.route("/edit-note", methods=["POST"])
@login_required
def edit_note():
    """Handle updates to an existing note.

    The form sends `noteId` and `note` (new text). Only the owner
    may update the note.
    """
    note_id = request.form.get("noteId")
    new_data = request.form.get("note")

    note = Note.query.get(note_id)

    if note and note.user_id == current_user.id:
        note.data = new_data
        db.session.commit()
        flash("Note updated successfully!", "success")
    else:
        flash("Error updating note.", "error")

    return redirect("/")
