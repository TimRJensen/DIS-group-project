import re
from datetime import datetime
from dateutil import tz
from flask import Blueprint, render_template, request
from dataclasses import dataclass
from psycopg.rows import class_row
from src import con

Search = Blueprint("search", __name__)

@dataclass
class SearchResult:
    id: int
    date: datetime
    home_id: int
    away_id: int
    home_logo: str
    away_logo: str

@Search.route("/search", methods=["GET", "POST"])
def search():
    if not request.form.get("query"):
        return render_template("search.html", data=[])

    query = request.form.get("query")
    matches = re.findall(r"(\b\w+\b)+", query)
    data = []
    for match in matches:
        with con.cursor(row_factory=class_row(SearchResult)) as cursor:
            cursor.execute(
"""SELECT DISTINCT
	f.id,
	f.date,
	th.id home_id,
	th.logo home_logo,
	ta.id away_id,
	ta.logo away_logo
FROM locales
JOIN (fixtures f
	JOIN teams th ON th.id = f.home_id 
	JOIN teams ta ON ta.id = f.away_id
) 
	ON LOWER(jsonb_extract_path_text(to_jsonb(locale), 'teams', 'name', th.id::VARCHAR(255))) LIKE LOWER('%{0}%')
	OR LOWER(jsonb_extract_path_text(to_jsonb(locale), 'teams', 'name', ta.id::VARCHAR(255))) LIKE LOWER('%{0}%')
GROUP BY (f.id, th.id, ta.id)
ORDER BY (f.date);
""".format(match))
            data += cursor.fetchall()
    from_zone = tz.tzutc()
    to_zone = tz.gettz("CET")
    for item in data:
        item.date = item.date.replace(tzinfo=from_zone)
        item.date = item.date.astimezone(to_zone)
    return render_template("search.html", data=data)
