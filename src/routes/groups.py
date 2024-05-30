from flask import Blueprint, render_template, request
from dataclasses import dataclass
from psycopg.rows import class_row
from src.app import con

@dataclass
class Group:
    id: int
    teams: list[int]
    logoes: list[str]
    goals_for: list[int]
    goals_against: list[int]
    points: list[int]

Groups = Blueprint("groups", __name__)

@Groups.get("/groups")
def groups():
    with con.cursor(row_factory=class_row(Group)) as cursor:
        cursor.execute(
"""SELECT 
	groups.id as id, 
	ARRAY_AGG(teams.id ORDER BY teams.rank) as teams, 
	ARRAY_AGG(teams.logo ORDER BY teams.rank) as logoes,
	ARRAY_AGG(teams.points ORDER BY teams.rank) as points,
	ARRAY_AGG(teams.goals_for ORDER BY teams.rank) as goals_for,
	ARRAY_AGG(teams.goals_against ORDER BY teams.rank) as goals_against
FROM groups
JOIN teams ON group_id = groups.id
GROUP BY groups.id
ORDER BY groups.id;""")
        return render_template("groups.html", data=cursor.fetchall())
        
