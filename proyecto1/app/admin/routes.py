from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime


from app.models import Concurso
from . import admin_bp
from .forms import ConcursoForm

@admin_bp.route("/admin/concurso/", methods=['GET', 'POST'], defaults={'concurso_id': None})
@admin_bp.route("/admin/concurso/<int:concurso_id>/", methods=['GET', 'POST','PUT'])
@login_required
def concurso_form(concurso_id): 
    form = ConcursoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        imagen = form.imagen.data
        url = form.url.data
        valor = form.valor.data
        fechaInicio = form.fechaInicio.data
        fechaFin = form.fechaFin.data
        guion = form.guion.data
        recomendaciones = form.recomendaciones.data
        fechaCreacion = datetime.now()
        concurso = Concurso(user_id=current_user.id
                        ,nombre=nombre
                        ,imagen=imagen
                        ,url=url
                        ,valor=valor
                        ,fechaInicio=fechaInicio
                        ,fechaFin=fechaFin
                        ,guion=guion
                        ,recomendaciones=recomendaciones
                        ,fechaCreacion=fechaCreacion)
        concurso.save()
        return redirect(url_for('public.index'))
    return render_template("concurso_form.html", form=form)

@admin_bp.route("/concursoDelete/<int:concurso_id>/", methods=['GET', 'POST'])   
def  concurso_delete(concurso_id):
    concurso = Concurso.get_by_id(concurso_id)
    concurso.delete()
    return redirect(url_for('public.index'))

@admin_bp.route("/concursoupdate/<int:concurso_id>/", methods=['GET', 'POST'])   
def concurso_update(concurso_id):
    concurso = Concurso.get_by_id(concurso_id)
    if concurso:
        form = ConcursoForm(formdata=request.form, obj=concurso)
        if request.method == 'POST' and form.validate():
            concurso.nombre = form.nombre.data
            concurso.imagen = form.imagen.data
            concurso.url = form.url.data
            concurso.valor = form.valor.data
            concurso.fechaInicio = form.fechaInicio.data
            concurso.fechaFin = form.fechaFin.data
            concurso.guion = form.guion.data
            concurso.recomendaciones = form.recomendaciones.data
            concurso.update()

            return redirect(url_for('public.index')) 
        return render_template('concurso_form.html', form=form)



from app.models import Participante
#from . import admin_bp
from .forms import ParticipanteForm

@admin_bp.route("/admin/participante/", methods=['GET', 'POST'], defaults={'participante_id': None})
@admin_bp.route("/admin/participante/<int:participante_id>/", methods=['GET', 'POST','PUT'])
#@login_required
def participante_form(participante_id): 
    form = ParticipanteForm()
    if form.validate_on_submit():
        concurso_id = form.concurso_id.data
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

@admin_bp.route("/participanteDelete/<int:participante_id>/", methods=['GET', 'POST'])   
def  participante_delete(participante_id):
    participante = Participante.get_by_id(participante_id)
    participante.delete()
    return redirect(url_for('public.index'))

@admin_bp.route("/participanteupdate/<int:participante_id>/", methods=['GET', 'POST'])   
def participante_update(participante_id):
    participante = Participante.get_by_id(participante_id)
    if participante:
        form = ParticipanteForm(formdata=request.form, obj=participante)
        if request.method == 'POST' and form.validate():
            participante.concurso_id = form.concurso_id.data
            participante.path_audio = form.path_audio.data
            participante.nombres = form.nombres.data
            participante.apellidos = form.apellidos.data
            participante.mail = form.mail.data
            participante.observaciones = form.observaciones.data
            participante.convertido = form.convertido.data
            concurso.update()

            return redirect(url_for('public.index')) 
        return render_template('participante_form.html', form=form)