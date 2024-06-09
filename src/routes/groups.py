from datetime import datetime
from dateutil import tz
from flask import Blueprint, render_template
from dataclasses import dataclass
from psycopg.rows import class_row
from src import con

@dataclass
class Group:
    id: int
    teams: list[int]
    logoes: list[str]
    goals_for: list[int]
    goals_against: list[int]
    points: list[int]

Groups = Blueprint("groups", __name__, url_prefix="/groups")

@Groups.get("/")
def groups():
    with con.cursor(row_factory=class_row(Group)) as cursor:
        cursor.execute(
"""SELECT 
	g.id, 
	ARRAY_AGG(t.id ORDER BY t.rank) teams, 
	ARRAY_AGG(t.logo ORDER BY t.rank) logoes,
	ARRAY_AGG(t.points ORDER BY t.rank) points,
	ARRAY_AGG(t.goals_for ORDER BY t.rank) goals_for,
	ARRAY_AGG(t.goals_against ORDER BY t.rank) goals_against
FROM groups g
JOIN teams t ON group_id = g.id
GROUP BY g.id
ORDER BY g.id;""")
        return render_template("groups.html", data=cursor.fetchall())
        
@dataclass
class GroupWithID:
    id: int
    team_id: int
    logo: str
    wins: int
    draws: int
    loses: int
    points: int
    goals_for: int
    goals_against: int

@dataclass
class GroupWithIDFixtures:
    id: int
    fixture_id: int
    home_id: int
    home_logo: str
    away_id: int
    away_logo: str
    date: datetime
    status: str
    home_goals: int
    away_goals: int

@Groups.get("/<id>")
def group(id: str):
    data = {}
    with con.cursor(row_factory=class_row(GroupWithID)) as cursor:
        cursor.execute(
"""SELECT 
    g.id,
    t.id team_id, 
    logo, 
    wins,
    draws,
    loses,  
    points, 
    goals_for, 
    goals_against
FROM groups g
JOIN teams t ON t.group_id = g.id
WHERE g.id = {0}
ORDER BY t.rank;
""".format(id))
        data["group"] = cursor.fetchall()

    with con.cursor(row_factory=class_row(GroupWithIDFixtures)) as cursor:
        cursor.execute(
"""SELECT 
    g.id, 
    f.id fixture_id, 
    th.id home_id, 
    th.logo home_logo, 
    ta.id away_id, 
    ta.logo away_logo, 
    f.date,
    f.status,
    f.home_goals,
    f.away_goals 
FROM groups as g
JOIN (fixtures f
	JOIN teams th ON f.home_id = th.id 
	JOIN teams ta ON f.away_id = ta.id 
) ON th.group_id = g.id OR ta.group_id = g.id
WHERE g.id = {0}
ORDER BY f.date;
""".format(id))
        from_zone = tz.tzutc()
        to_zone = tz.gettz("CET")
        fixtures = cursor.fetchall()
        for item in fixtures:
            item.date = item.date.replace(tzinfo=from_zone)
            item.date = item.date.astimezone(to_zone)
        data["upcomming"] = [row for row in fixtures if row.status == "NS"]
        data["latest"] = [row for row in fixtures if row.status == "FT"]
    return render_template("groups[id].html", **data)
