from flask import Blueprint, render_template, request
from src.app import con

Index = Blueprint("index", __name__)

@Index.get("/")
@Index.get("/index")
def index():
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM version()")
        return render_template("index.html", 
            name=request.args.get("greet"), 
            psql_v=cursor.fetchone()[0])
        


@Index.route('/fixtures')
def fixtures():
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
    
    fixtures_list = []
    with con.cursor() as cursor:
        cursor.execute("""
            SELECT f.id, f.date, f.venue, ht.name AS home_id, at.name AS away_id
            FROM Fixtures f
            JOIN Teams ht ON f.home_id = ht.id
            JOIN Teams at ON f.away_id = at.id
        """)
        fixtures = cursor.fetchall()
        for fixture in fixtures:
            fixtures_list.append({
                "id": fixture[0],
                "date": fixture[1],
                "venue": fixture[2],
                "home_id": fixture[3],
                "away_id": fixture[4]
            })
    
    return render_template("fixtures.html", config=config, fixtures=fixtures_list)
