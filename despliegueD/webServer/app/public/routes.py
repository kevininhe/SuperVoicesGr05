from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from app.models import Concurso, Participante
from . import public_bp
from .forms import ParticipanteForm
import math
from .service import postAudioAPI
from app.utilidadesDynamo import *


@public_bp.route("/")
def index():
   # concursos = Concurso.get_all()
   # concursos = Concurso.get_by_user(0)
   # if current_user.is_authenticated:
   #     concursos = Concurso.get_by_user(current_user.id)
    return render_template("principal.html")

@public_bp.route("/concursos")
@login_required
def principal():
    concursos = traerConcursosUsuario(current_user.id)
    return render_template("index.html", concursos=concursos)

@public_bp.route("/concursos/<string:url>/", defaults={"page": 1})
@public_bp.route("/concursos/<string:url>/<int:page>")
def show_concurso(page,url):
    concurso = traerInfoConcurso(url)
    participantes = []
    if current_user.is_anonymous:
        participantes = traerParticipantesConcurso(concurso["PK"],True)
    else:
        participantes = traerParticipantesConcurso(concurso["PK"])
    number_pages = 1
    # TODO: Definir si hacemos paginacion
    """
    if number_pages<= 20:
        number_pages=1
    else:
        number_pages= int(math.ceil(number_pages/20)+1)
    """
    return render_template("concurso_view.html", concurso=concurso, voz=participantes, pages=number_pages)

@public_bp.route("/participantes/<string:url_concurso>/<string:participante_id>/")
def show_participante(url_concurso,participante_id):
    concurso = traerInfoConcurso(url_concurso)
    participante = traerInfoParticipante(url_concurso,participante_id)
    if participante is None:
        # TODO: Revisar que se puede usar para este proposito
        abort(404)
    # Guardar el nombre del concurso en el diccionario de participante
    participante["nombre_concurso"] = concurso["nombre"]
    return render_template("participante_view.html", participante=participante)

@public_bp.route("/public/participante/<string:url_concurso>", methods=['GET', 'POST'])
def participante_form(url_concurso):
    concurso = traerInfoConcurso(url_concurso)
    concurso["PK"] = concurso["PK"].replace("CON#","")
    form = ParticipanteForm(concurso["nombre"])
    if form.validate_on_submit():
        concurso_id = concurso["PK"]
        path_audio = secure_filename(form.path_audio.data.filename)
        form.path_audio.data.save("app/static/TempStorage/" + path_audio)
        nombres = form.nombres.data
        apellidos = form.apellidos.data
        mail = form.mail.data
        observaciones = form.observaciones.data
        convertido = False
        fechaCreacion = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        
        # Insertar participante en Dynamo
        response = insertarParticipante(concurso_id=concurso_id
                        ,path_audio=path_audio
			            ,path_audio_origin=path_audio
                        ,nombres=nombres
                        ,apellidos=apellidos
                        ,mail=mail
                        ,observaciones=observaciones
                        ,convertido=False
                        ,fechaCreacion=fechaCreacion)
        # TODO: Guardar la voz en el S3
        #postAudioAPI("app/static/TempStorage/" + path_audio)
        
        flash('Hemos recibido tu voz y la estamos procesando para que sea publicada en la \
                            página del concurso y pueda ser posteriormente revisada por nuestro equipo de trabajo. \
                            Tan pronto la voz quede publicada en la página del concurso te notificaremos por email.')
        return  redirect(url_for('public.participante_form',url_concurso=url_concurso))
    return render_template("participante_form.html", form=form)


