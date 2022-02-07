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