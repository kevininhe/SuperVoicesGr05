from pickle import TRUE
from flask import render_template, redirect, url_for, request,send_file
from flask_login import login_required, current_user
from datetime import datetime
from project.usuario.models import Usuario
from werkzeug.utils import secure_filename
import os
from project.concurso.models import Concurso
from project.participante.models import Participante
from . import concurso_blueprint
from .forms import ConcursoForm
from .services import deleteAudioAPI, deleteImage, uploadImage
import json
from collections import namedtuple



@concurso_blueprint.route("/admin/concurso/", methods=['GET', 'POST'], defaults={'concurso_id': None})
@concurso_blueprint.route("/admin/concurso/<string:concurso_id>/", methods=['GET', 'POST','PUT'])
@login_required
def concurso_form(concurso_id): 
    form = ConcursoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        path_imagen = secure_filename(form.imagen.data.filename)
        form.imagen.data.save("project/static/images_concurso/" + path_imagen)
        url = form.url.data
        valor = form.valor.data
        fechaInicio = form.fechaInicio.data
        fechaFin = form.fechaFin.data
        guion = form.guion.data
        recomendaciones = form.recomendaciones.data
        fechaCreacion = datetime.now()
        concurso = Concurso(usuario=Usuario.get_by_id(current_user.id)
                        ,usuario_id=str(current_user.id)
                        ,nombre=nombre
                        ,imagen=path_imagen
                        ,url=url
                        ,valor=valor
                        ,fechaInicio=fechaInicio
                        ,fechaFin=fechaFin
                        ,guion=guion
                        ,recomendaciones=recomendaciones
                        ,fechaCreacion=fechaCreacion)
        concurso.save(cascade=True)
        uploadImage(path_imagen,"project/static/images_concurso/" + path_imagen)
        return redirect(url_for('participantes.index'))
    return render_template("concurso_form.html", form=form)

@concurso_blueprint.route("/concursoDelete/<string:concurso_id>/", methods=['GET', 'POST'])   
@login_required
def  concurso_delete(concurso_id):
    concurso = Concurso.get_by_id(concurso_id) 
    participantes = Participante.findByConcurso(concurso_id)
   	    
    for k in participantes:
        print(k.path_audio)
        deleteAudioAPI(k.path_audio,k.path_audio_origin)
        k.delete()

    #os.remove("app/static/images_concurso/{}".format(concurso.imagen))
    deleteImage(concurso.imagen)
    concurso.delete()
    return redirect(url_for('participantes.index'))

@concurso_blueprint.route("/concursoupdate/<string:concurso_id>/", methods=['GET', 'POST'])  
@login_required  
def concurso_update(concurso_id):
    concurso = Concurso.get_by_id(concurso_id)
    if concurso:
        form = ConcursoForm(obj=concurso)
        #if request.method == 'POST' and form.validate():
        if request.method == 'POST':
            try:
                concurso.update(nombre = form.nombre.data)
                path_imagen = secure_filename(form.imagen.data.filename)
                form.imagen.data.save("project/static/images_concurso/" + path_imagen)
                pre_imagen=concurso.imagen
                concurso.update(imagen = path_imagen)
                concurso.update(url = form.url.data)
                concurso.update(valor = form.valor.data)
                concurso.update(fechaInicio = form.fechaInicio.data)
                concurso.update(fechaFin = form.fechaFin.data)
                concurso.update(guion = form.guion.data)
                concurso.update(recomendaciones = form.recomendaciones.data)
                concurso.save(cascade=TRUE)
                deleteImage(pre_imagen)
                uploadImage(path_imagen,"project/static/images_concurso/" + path_imagen)
            except:
                concurso.update(nombre = form.nombre.data)
                concurso.update(url = form.url.data)
                concurso.update(valor = form.valor.data)
                concurso.update(fechaInicio = form.fechaInicio.data)
                concurso.update(fechaFin = form.fechaFin.data)
                concurso.update(guion = form.guion.data)
                concurso.update(recomendaciones = form.recomendaciones.data)
                concurso.save(cascade=TRUE)
            return redirect(url_for('participantes.index')) 
        
        return render_template('concurso_form.html', form=form)

@concurso_blueprint.route("/participanteDelete/<string:participante_id>/", methods=['GET', 'POST'])   
@login_required
def  participante_delete(participante_id):
    participante = Participante.get_by_id(participante_id)
    deleteAudioAPI(participante.path_audio,participante.path_audio_origin)
    participante.delete()
    return redirect(url_for('participantes.index'))