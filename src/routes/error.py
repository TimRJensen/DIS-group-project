from re import match
from flask import Blueprint, render_template

Error = Blueprint("404", __name__)

@Error.app_errorhandler(404)
def error(e):
    code = match(r"(^\d{3})", str(e))[0]
    return render_template("error.html", code = code), 404
