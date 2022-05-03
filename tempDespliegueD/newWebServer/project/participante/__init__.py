from flask import Blueprint
participantes_blueprint = Blueprint('participantes', __name__, template_folder='templates')

from . import routes