from flask import Blueprint, render_template, request
from dataclasses import dataclass
from psycopg.rows import class_row
from src.app import con

@dataclass
class Group:
    id: int
    teams: list[int]
    logoes: list[str]

Groups = Blueprint("groups", __name__)

@Groups.get("/groups")
def groups():
    with con.cursor(row_factory=class_row(Group)) as cursor:
        cursor.execute(
"""SELECT groups.id as id, ARRAY_AGG(teams.id) as teams, ARRAY_AGG(teams.logo) as logoes 
    FROM groups
    JOIN teams ON group_id = groups.id
    GROUP BY groups.id
    ORDER BY groups.id
    """)
        return render_template("groups.html", data=cursor.fetchall())
        
