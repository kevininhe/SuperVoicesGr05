from flask import render_template, redirect, url_for, request,send_file
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from app.models import Concurso, Participante
from . import admin_bp
from .forms import ConcursoForm
from .service import deleteAudioAPI
from app.utilidadesDynamo import *
from collections import namedtuple


@admin_bp.route("/admin/concurso/", methods=['GET', 'POST'], defaults={'concurso_id': None})
@admin_bp.route("/admin/concurso/<int:concurso_id>/", methods=['GET', 'POST','PUT'])
@login_required
def concurso_form(concurso_id): 
    form = ConcursoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        path_imagen = secure_filename(form.imagen.data.filename)
        form.imagen.data.save("app/static/images_concurso/" + path_imagen)
        url = form.url.data
        valor = form.valor.data
        fechaInicio = form.fechaInicio.data
        fechaFin = form.fechaFin.data
        guion = form.guion.data
        recomendaciones = form.recomendaciones.data
        fechaCreacion = datetime.now()
        # Inserta el concurso en Dynamo
        concurso = insertarConcurso(user_id=current_user.id
                        ,nombre=nombre
                        ,imagen=path_imagen
                        ,url=url
                        ,valor=valor
                        ,fechaInicio=fechaInicio.strftime('%Y-%m-%d')
                        ,fechaFin=fechaFin.strftime('%Y-%m-%d')
                        ,guion=guion
                        ,recomendaciones=recomendaciones
                        ,fechaCreacion=fechaCreacion.strftime('%Y-%m-%d-%H:%M:%S'))
        return redirect(url_for('public.index'))
    return render_template("concurso_form.html", form=form)
 
@admin_bp.route("/concursoDelete/<string:url_concurso>/", methods=['GET', 'POST'])
def concurso_delete(url_concurso):
    concurso = traerInfoConcurso(url_concurso)
    concurso["PK"] = concurso["PK"].replace("CON#","")
    # TODO : Eliminar voces almacenadas en S3
    """
    participantes = Participante.get_paths_Concurso_id(concurso_id)
   	    
    for k in participantes:
        print(k.path_audio)
        deleteAudioAPI(k.path_audio.split("."))
    """

    os.remove("app/static/images_concurso/{}".format(concurso["imagen"]))
    # Eliminar concurso en Dynamo
    eliminarConcurso(concurso["PK"])
    return redirect(url_for('public.index'))

@admin_bp.route("/concursoupdate/<string:url_concurso>/", methods=['GET', 'POST'])   
def concurso_update(url_concurso):
    concurso = traerInfoConcurso(url_concurso)
    if concurso:
        # Formatear campos para que puedan ser mostrados en el form
        concurso["fechaInicio"] = datetime.strptime(concurso["fechaInicio"],'%Y-%m-%d')
        concurso["fechaFin"] = datetime.strptime(concurso["fechaFin"],'%Y-%m-%d')
        concurso["url"] = concurso["url_concurso"]
        concurso["PK"] = concurso["PK"].replace("CON#","")
        # Crear objeto a partir de diccionario
        concurso_obj = namedtuple('Struct', concurso.keys())(*concurso.values())
        form = ConcursoForm(obj=concurso_obj)

        if request.method == 'POST' and form.validate():
            try:
                path_imagen = secure_filename(form.imagen.data.filename)
                form.imagen.data.save("app/static/images_concurso/" + path_imagen)
                # Actualiza el concurso en Dynamo
                response = actualizarConcursoForm(uid=concurso["PK"]
                                ,nombre=form.nombre.data
                                ,imagen=path_imagen
                                ,url=form.url.data
                                ,valor=form.valor.data
                                ,fechaInicio=form.fechaInicio.data.strftime('%Y-%m-%d')
                                ,fechaFin=form.fechaFin.data.strftime('%Y-%m-%d')
                                ,guion=form.guion.data
                                ,recomendaciones=form.recomendaciones.data)
            except:
                # Actualiza el concurso en Dynamo sin la imagen
                response = actualizarConcursoFormNoImg(uid=concurso["PK"]
                                ,nombre=form.nombre.data
                                ,url=form.url.data
                                ,valor=form.valor.data
                                ,fechaInicio=form.fechaInicio.data.strftime('%Y-%m-%d')
                                ,fechaFin=form.fechaFin.data.strftime('%Y-%m-%d')
                                ,guion=form.guion.data
                                ,recomendaciones=form.recomendaciones.data)
            return redirect(url_for('public.index')) 
        return render_template('concurso_form.html', form=form)

@admin_bp.route("/participanteDelete/<int:participante_id>/", methods=['GET', 'POST'])   
def  participante_delete(participante_id):
    participante = Participante.get_by_id(participante_id)
    os.remove("app/static/AudioFilesDestiny/{}".format(participante.path_audio))
    os.remove("app/static/AudioFilesOrigin/{}".format(participante.path_audio_origin))	
    participante.delete()
    return redirect(url_for('public.index'))


@admin_bp.route('/participante/uploads/<path:filename>', methods=['GET', 'POST'])
def download_participante(filename):
    path = "static/AudioFilesDestiny/{}".format(filename)
    return send_file(path, as_attachment=True)

@admin_bp.route('/participante/uploads_origin/<path:filename>', methods=['GET', 'POST'])
def participante_origin_download(filename):
    path = "static/AudioFilesOrigin/{}".format(filename)
    return send_file(path, as_attachment=True)