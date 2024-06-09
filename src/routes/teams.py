from flask import Blueprint, render_template
from dataclasses import dataclass
from psycopg.rows import class_row
from src import con

@dataclass
class Team:
    id: int
    name: str
    code: str
    logo: str
    rank: int
    points: int
    wins: int
    loses: int
    draws: int
    group_id: int

Teams = Blueprint("teams", __name__, url_prefix="/teams")

@Teams.get("/")
def teams():
    with con.cursor(row_factory=class_row(Team)) as cursor:
        cursor.execute("""
            SELECT 
                id,
                name,
                code,
                logo,
                rank,
                points,
                wins,
                loses,
                draws,
                group_id
            FROM Teams
            ORDER BY points DESC, rank ASC;
        """)
        teams = cursor.fetchall()

    return render_template("teams.html", teams=teams)


@Teams.get("/<int:id>")
def teams_id(id: int):
    with con.cursor(row_factory=class_row(Team)) as cursor:
        cursor.execute("""
            SELECT 
                id,
                name,
                code,
                logo,
                rank,
                points,
                wins,
                loses,
                draws,
                group_id
            FROM Teams
            ORDER BY points DESC, rank ASC;
        """)
        teams = cursor.fetchall()

    return render_template("teams.html", teams=teams, scroll_to_id=id)
