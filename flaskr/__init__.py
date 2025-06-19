from flask import Flask, session, request, redirect, url_for
from .routes import account_routes, settings_routes, refresh_routes, index_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev"

    # Register blueprints
    app.register_blueprint(account_routes.bp)
    app.register_blueprint(index_routes.bp)
    app.register_blueprint(settings_routes.bp)
    app.register_blueprint(refresh_routes.bp)



    return app
app = create_app()