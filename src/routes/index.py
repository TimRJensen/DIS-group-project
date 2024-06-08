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
        
@Index.route('/teams')
def teams():
    config = {
        "locale": {
            "navbar": {
                "0": "Teams",
                "1": "Groups",
                "2": "Fixtures"
            },
            "counter": {
                "0": "Days",
                "1": "Hours",
                "2": "Minutes",
                "3": "Seconds"
            },
            "name": "EN"
        },
        "locales": ["EN", "DK"]
    }

    teams_list = []
    with con.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM Teams
        """)
        teams = cursor.fetchall()
        for team in teams:
            teams_list.append({
                "id": team[0],
                "name": team[1],
                "code": team[2],
                "logo": team[3]
            })

    return render_template("teams.html", config=config, teams=teams_list)