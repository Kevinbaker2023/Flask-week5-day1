from flask import Blueprint

pokemon = Blueprint('pokemon', __name__)

from . import routes