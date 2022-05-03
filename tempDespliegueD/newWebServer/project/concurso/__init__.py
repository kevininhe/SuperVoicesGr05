from flask import Blueprint
concurso_blueprint = Blueprint('concurso', __name__, template_folder='templates')

from . import routes