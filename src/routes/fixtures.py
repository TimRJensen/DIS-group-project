from collections import defaultdict
from datetime import datetime
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

Fixtures = Blueprint("fixtures", __name__, url_prefix="/fixtures")

@Fixtures.get("/")
def fixtures():
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
            date_str = fixture.date.strftime("%Y-%m-%d")
            fixtures_by_date[date_str].append(fixture_data)

    return render_template("fixtures.html", fixtures_by_date=fixtures_by_date)
