from flask import render_template, redirect, url_for, request
from datetime import datetime

from app.models import Concurso, Participante
from . import public_bp
from .forms import ParticipanteForm


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
    participantes = Participante.get_by_Concurso_id(concurso.id)
    if concurso is None:
        abort(404)
    return render_template("concurso_view.html", concurso=concurso, participantes=participantes)

@public_bp.route("/participantes/<int:participante_id>/")
def show_participante(participante_id):
    participante = Participante.get_by_id(participante_id)
    if participante is None:
        abort(404)
    return render_template("participante_view.html", participante=participante)

@public_bp.route("/public/participante/", methods=['GET', 'POST'], defaults={'participante_id': None})
@public_bp.route("/public/participante/<int:participante_id>/", methods=['GET', 'POST','PUT'])
def participante_form(participante_id): 
    form = ParticipanteForm()
    if form.validate_on_submit():
        concurso_id = concurso_id
        path_audio = form.path_audio.data
        nombres = form.nombres.data
        apellidos = form.apellidos.data
        mail = form.mail.data
        observaciones = form.observaciones.data
        convertido = form.convertido.data
        fechaCreacion = datetime.now()
        participante = Participante(concurso_id=concurso_id
                        ,path_audio=path_audio
                        ,nombres=nombres
                        ,apellidos=apellidos
                        ,mail=mail
                        ,observaciones=observaciones
                        ,convertido=convertido
                        ,fechaCreacion=fechaCreacion)
        participante.save()
        return redirect(url_for('public.index'))
    return render_template("participante_form.html", form=form)

