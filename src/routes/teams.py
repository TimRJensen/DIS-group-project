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
    team_list = []
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
        for team in teams:
            team_data = {
                "id": team.id,
                "name": team.name,
                "code": team.code,
                "logo": team.logo,
                "rank": team.rank,
                "points": team.points,
                "wins": team.wins,
                "loses": team.loses,
                "group_id": team.group_id
            }
            team_list.append(team_data)

    return render_template("teams.html", teams=team_list)
