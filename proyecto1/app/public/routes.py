from flask import abort, render_template

from app.models import Concurso
from . import public_bp


@public_bp.route("/")
def index():
    concursos = Concurso.get_all()
   # concursos = Concurso.get_by_user(0)
   # if current_user.is_authenticated:
   #     concursos = Concurso.get_by_user(current_user.id)
    return render_template("index.html", concursos=concursos)

@public_bp.route("/concursos/<string:url>/")
def show_concurso(url):
    concurso = Concurso.get_by_url(url)
    if concurso is None:
        abort(404)
    return render_template("concurso_view.html", concurso=concurso)