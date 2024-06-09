from collections import defaultdict
from datetime import datetime
from dateutil import tz
from flask import Blueprint, render_template
from dataclasses import dataclass
from psycopg.rows import class_row
from src import con

@dataclass
class Fixture:
    id: int
    date: datetime
    venue: str
    home_id: int
    home_name: str
    home_logo: str
    away_id: int
    away_name: str
    away_logo: str

Fixtures = Blueprint("fixtures", __name__, url_prefix="/")

@Fixtures.get("/")
@Fixtures.get("/index")
def fixtures():
    return render_fixtures_page()

@Fixtures.get("/fixtures/<int:id>")
def fixture_id(id: int):
    return render_fixtures_page(scroll_to_id=id)

def render_fixtures_page(scroll_to_id=None):
    fixtures_by_date = defaultdict(list)
    with con.cursor(row_factory=class_row(Fixture)) as cursor:
        cursor.execute("""
            SELECT 
                f.id, 
                f.date, 
                f.venue, 
                ht.id AS home_id,
                ht.name AS home_name, 
                ht.logo AS home_logo, 
                at.id AS away_id,
                at.name AS away_name, 
                at.logo AS away_logo
            FROM Fixtures f
            JOIN Teams ht ON f.home_id = ht.id
            JOIN Teams at ON f.away_id = at.id
            ORDER BY f.date;
        """)
        fixtures = cursor.fetchall()
        from_zone = tz.tzutc()
        to_zone = tz.gettz("CET")
        for fixture in fixtures:
            fixture_data = {
                "id": fixture.id,
                "date": fixture.date,
                "venue": fixture.venue,
                "home_id": fixture.home_id,
                "home_name": fixture.home_name,
                "home_logo": fixture.home_logo,
                "away_id": fixture.away_id,
                "away_name": fixture.away_name,
                "away_logo": fixture.away_logo
            }
            fixture_data["date"] = fixture.date.replace(tzinfo=from_zone)
            fixture_data["date"] = fixture.date.astimezone(to_zone)
            date_str = fixture_data["date"].strftime("%Y-%m-%d")
            fixtures_by_date[date_str].append(fixture_data)

    return render_template("fixtures.html", fixtures_by_date=fixtures_by_date, scroll_to_id=scroll_to_id)
