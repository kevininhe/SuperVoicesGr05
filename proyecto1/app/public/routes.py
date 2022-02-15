from flask import render_template, redirect, url_for, request
from datetime import datetime
from werkzeug.utils import secure_filename
from app.models import Concurso, Participante
from . import public_bp
from .forms import ParticipanteForm



@public_bp.route("/")
def index():
   # concursos = Concurso.get_all()
   # concursos = Concurso.get_by_user(0)
   # if current_user.is_authenticated:
   #     concursos = Concurso.get_by_user(current_user.id)
    return render_template("principal.html")

@public_bp.route("/concursos")
def principal():
    concursos = Concurso.get_all()
    # concursos = Concurso.get_by_user(0)
    # if current_user.is_authenticated:
    #     concursos = Concurso.get_by_user(current_user.id)
    return render_template("index.html", concursos=concursos)

@public_bp.route("/concursos/<string:url>/")
def show_concurso(url):
    concurso = Concurso.get_by_url(url)
    participantes = Participante.query.filter_by(concurso_id='{}'.format(url)).order_by(Participante.fechaCreacion.desc()).slice(0, 20).all()
    if concurso is None:
        abort(404)
    return render_template("concurso_view.html", concurso=concurso, voz=participantes)

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
    choices_concursos = Concurso.query.with_entities(Concurso.url).all()
    list_concursos = [tup[0] for tup in choices_concursos]
    form.concurso_id.choices = list_concursos
    if form.validate_on_submit():
        concurso_id = form.concurso_id.data
        path_audio = secure_filename(form.path_audio.data.filename)
        form.path_audio.data.save("app/static/AudioFilesOrigin/" + path_audio)
        nombres = form.nombres.data
        apellidos = form.apellidos.data
        mail = form.mail.data
        observaciones = form.observaciones.data
        convertido = False
        fechaCreacion = datetime.now()
        participante = Participante(concurso_id=concurso_id
                        ,path_audio=path_audio
                        ,nombres=nombres
                        ,apellidos=apellidos
                        ,mail=mail
                        ,observaciones=observaciones
                        ,convertido=False
                        ,fechaCreacion=fechaCreacion)
        participante.save()
        return redirect(url_for('public.index'))
    return render_template("participante_form.html", form=form)


@public_bp.route("/concursos/<string:url>/page2", methods=['GET', 'POST'])
def concursopage2(url):
    concurso = Concurso.get_by_url(url)
    participantes = Participante.query.filter_by(concurso_id='{}'.format(url)).order_by(Participante.fechaCreacion.desc()).slice(20, 40).all()
    return render_template('concursopage2.html', voz=participantes, concurso=concurso)

@public_bp.route("/concursos/<string:url>/page3", methods=['GET', 'POST'])
def concursopage3(url):
    concurso = Concurso.get_by_url(url)
    participantes = Participante.query.filter_by(concurso_id='{}'.format(url)).order_by(Participante.fechaCreacion.desc()).slice(40, 60).all()
    return render_template('concursopage3.html', voz=participantes, concurso=concurso)

@public_bp.route("/concursos/<string:url>/page4", methods=['GET', 'POST'])
def concursopage4(url):
    concurso = Concurso.get_by_url(url)
    participantes = Participante.query.filter_by(concurso_id='{}'.format(url)).order_by(Participante.fechaCreacion.desc()).slice(60, 80).all()
    return render_template('concursopage4.html', voz=participantes, concurso=concurso)

@public_bp.route("/concursos/<string:url>/page5", methods=['GET', 'POST'])
def concursopage5(url):
    concurso = Concurso.get_by_url(url)
    participantes = Participante.query.filter_by(concurso_id='{}'.format(url)).order_by(Participante.fechaCreacion.desc()).slice(80, 100).all()
    return render_template('concursopage4.html', voz=participantes, concurso=concurso)
