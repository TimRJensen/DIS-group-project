import os, json
from re import match
from flask import Flask, redirect, request
from psycopg import Connection
from psycopg.rows import dict_row
from dotenv import load_dotenv

locale = None
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

    from src.routes.index import Index
    from src.routes.error import Error
    app.register_blueprint(Index)
    app.register_blueprint(Error)

    locales = []
    app.config["locales"] = []
    app.config["locale"] = {}

    with con.cursor(row_factory=dict_row) as cursor:
        locales = cursor.execute("SELECT * FROM locales;").fetchall()
        for key in list(locales[0].keys())[1:]:
            app.config["locales"].append((key, match(r"^[a-z]{2}_([a-z]{2})", key)[1].upper()))
    
    @app.get("/locale/<iso>")
    def set_locale(iso: str):
        app.config["locale"]["name"] = match(r"^[a-z]{2}_([a-z]{2})", iso)[1].upper()

        for row in locales:
            stack = row["id"].split(":")
            next = stack.pop(0)
            locale = app.config["locale"]
            while (len(stack)):
                if not next in locale:
                    locale[next] = {}
                locale = locale[next]
                next = stack.pop(0)
            if next.isdigit():
                locale[int(next)] = row[iso]
            else:
                locale[next] = row[iso]

        if request:
            return redirect(request.referrer)

    set_locale("en_en")
    print(app.config["locale"])

    
    return app
