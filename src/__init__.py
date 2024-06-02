import os, json
from re import match
from flask import Flask, redirect, request, g
from psycopg import Connection, connect
from psycopg.rows import dict_row
from dotenv import load_dotenv

con = None

try:
    load_dotenv(".env")
    con = Connection.connect(
        host = os.getenv("POSTGRES_HOST"),
        port = os.getenv("POSTGRES_PORT"),
        dbname = os.getenv("POSTGRES_DB"),
        user = os.getenv("POSTGRES_USER"),
        password = os.getenv("POSTGRES_PASSWORD")
    )
except Exception as e:
    exit(1)

def create_app():
    app = Flask(__name__)
    locales = None
    locale

    from src.routes.index import Index
    from src.routes.error import Error
    from src.routes.groups import Groups
    app.register_blueprint(Index)
    app.register_blueprint(Error)
    app.register_blueprint(Groups)

    with con.cursor(row_factory=dict_row) as cursor:
        locales = [row["locale"] for row in cursor.execute("SELECT * FROM locales;").fetchall()]

    @app.get("/locale/<iso>")
    def set_locale(iso: str):
        global locale
        for row in locales:
            if row["id"] != iso:
                continue
            locale = row
            break
        if request:
            return redirect(request.referrer)
    @app.context_processor
    def inject_locale():
        return {"locale": locale, "locales": locales}

    set_locale("en_EN")
    return app
