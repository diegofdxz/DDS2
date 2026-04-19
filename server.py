from datetime import timedelta

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False
)

app.permanent_session_lifetime = timedelta(days=7)


@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

