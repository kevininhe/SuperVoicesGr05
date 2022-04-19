from flask import render_template, redirect, url_for, request, flash
from datetime import datetime
from werkzeug.utils import secure_filename
from project.concurso.models import Concurso
from project.participante.models import Participante
from . import participantes_blueprint
from .forms import ParticipanteForm
import math
from .services import postAudioAPI, sendMessageSQS
from flask_login import login_required, current_user
import json
from bson import ObjectId


@participantes_blueprint.route("/")
def index():
    return render_template("principal.html")

@participantes_blueprint.route("/concursos")
def principal():
    concursos=[]
    if not current_user.is_authenticated:
        concursos = Concurso.get_all()
    else:
        concursos = Concurso.findByUsuario(str(current_user.id))
    return render_template("index.html", concursos=concursos)

@participantes_blueprint.route("/concursos/<string:url>/", defaults={"page": 1})
@participantes_blueprint.route("/concursos/<string:url>/<int:page>")
def show_concurso(page,url):
    concurso = Concurso.get_by_url(url)
    participantes = Participante.objects(concurso=concurso.id).order_by('-fechaCreacion').paginate(page=page, per_page=20).items
    number_pages = Participante.objects(concurso=concurso.id).count()
    if number_pages<= 20:
        number_pages=1
    else:
        number_pages= int(math.ceil(number_pages/20)+1)
    return render_template("concurso_view.html", concurso=concurso, voz=participantes, pages=number_pages)

@participantes_blueprint.route("/participantes/<string:participante_id>/")
@login_required
def show_participante(participante_id):
    participante = Participante.get_by_id(participante_id)
    if participante is None:
        abort(404)
    return render_template("participante_view.html", participante=participante)

@participantes_blueprint.route("/public/participante/<string:concurso_id>", methods=['GET', 'POST'])
def participante_form(concurso_id):
    concurso=Concurso.get_by_url(concurso_id)
    concurso_id=str(concurso.id)
    form = ParticipanteForm(concurso_id)
    if form.validate_on_submit():
        concurso_id =form.concurso_id
        mail = form.mail.data
        path_audio = secure_filename(form.path_audio.data.filename)
        format_file=path_audio.split('.')[-1]
        form.path_audio.data.save("project/static/TempStorage/" + path_audio)
        nombres = form.nombres.data
        apellidos = form.apellidos.data
        observaciones = form.observaciones.data
        convertido = False
        fechaCreacion = datetime.now()
        participante = Participante(concurso=Concurso.get_by_id(concurso_id)
                        ,concurso_id=concurso_id
                        ,path_audio=path_audio
			            ,path_audio_origin=path_audio
                        ,nombres=nombres
                        ,apellidos=apellidos
                        ,mail=mail
                        ,observaciones=observaciones
                        ,convertido=False
                        ,fechaCreacion=fechaCreacion)
        participante.save(cascade=True)
        postAudioAPI("project/static/TempStorage/" + path_audio,str(participante.id)+'.'+format_file)
        participante.update(path_audio=str(participante.id)+'.'+format_file)
        participante.save(cascade=True)
        sendMessageSQS(str(participante.id),str(participante.id)+'.'+format_file,mail,nombres)
        flash('Hemos recibido tu voz y la estamos procesando para que sea publicada en la \
                            página del concurso y pueda ser posteriormente revisada por nuestro equipo de trabajo. \
                            Tan pronto la voz quede publicada en la página del concurso te notificaremos por email.')
        return  redirect(url_for('participantes.participante_form',concurso_id=concurso.url))
    return render_template("participante_form.html", form=form)


