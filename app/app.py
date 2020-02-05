import os

from flask import Flask, render_template
from . import settings, controllers
import sqlite3 as sql

project_dir = os.path.dirname(os.path.abspath(__file__))

def get_cursor():
    conn = sql.connect("purchase.db")
    cur = conn.cursor()
    return cur, conn

def initialize_db():
    cur, conn = get_cursor()

    cur.execute("DROP TABLE IF EXISTS purchase")
    cur.execute("CREATE TABLE purchase (src TEXT, price INTEGER)")

    conn.commit()

def create_app(config_object=settings):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    register_blueprints(app)
    register_errorhandlers(app)
    initialize_db()

    return app

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(controllers.home.blueprint)
    return None

def register_errorhandlers(app):
    """Register error handlers."""
    @app.errorhandler(401)
    def internal_error(error):
        return render_template('401.html'), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return None
