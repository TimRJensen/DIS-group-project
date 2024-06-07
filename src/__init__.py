import os, json
from re import match
from flask import Flask, redirect, request
from psycopg import Connection
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

    app.config["locales"] = []
    for locale in os.listdir("src/locale"):
        app.config["locales"].append(match(r"^[a-z]{2}_([A-Z]{2}).json$", locale)[1])
    with open("src/locale/en_EN.json", "r") as file:
        app.config["locale"] = json.load(file)

    from src.routes.index import Index
    from src.routes.error import Error
    app.register_blueprint(Index)
    app.register_blueprint(Error)


    @app.get("/locale/<locale>")
    def set_locale(locale:str):
        with open(f"locale/{locale.lower()}_{locale}.json", "r") as file: 
            app.config["locale"] = json.load(file)
        return redirect(request.referrer)
    
    return app
