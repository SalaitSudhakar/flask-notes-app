"""Entry point for the Notes App.

This file creates and runs the Flask application instance returned
by `website.create_app()`. When you run this file directly (for
example `python main.py`), Flask's built-in development server will
start and serve the application on `localhost`.

Beginners: keep this file minimal — it simply wires the app factory
to the command-line run behavior.
"""

from website import create_app

# Create the Flask application using the application factory.
# The `create_app` function (in `website/__init__.py`) configures
# extensions, registers blueprints, and prepares the app for use.
app = create_app()


if __name__ == "__main__":
    # Run the app in debug mode (auto-reloads on changes and shows
    # debugging information). Do not use debug mode in production.
    app.run(debug=True)
