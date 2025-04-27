from flask import Flask, session, request, redirect, url_for
from .routes import account_routes, settings_routes, refresh_routes, index_routes, login_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev"

    # Register blueprints
    app.register_blueprint(account_routes.bp)
    app.register_blueprint(index_routes.bp)
    app.register_blueprint(settings_routes.bp)
    app.register_blueprint(refresh_routes.bp)
    app.register_blueprint(login_routes.bp)

    @app.before_request
    def require_login():
        if request.endpoint not in ('login_routes.login', 'static') and not session.get('logged_in'):
            return redirect(url_for('login_routes.login'))


    return app
app = create_app()