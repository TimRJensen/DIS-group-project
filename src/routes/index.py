from flask import Blueprint, render_template, request
from src import con

Index = Blueprint("index", __name__)

@Index.get("/")
@Index.get("/index")
def index():
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM version()")
        return render_template("index.html", 
            name=request.args.get("greet"), 
            psql_v=cursor.fetchone()[0])
