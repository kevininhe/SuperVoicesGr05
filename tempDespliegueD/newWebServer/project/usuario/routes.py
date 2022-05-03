from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
import pickle

from project import login_manager
from . import users_blueprint
from .forms import SignupForm, LoginForm
from project.usuario.models import Usuario

@users_blueprint.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('participantes.index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        nombres = form.nombres.data
        apellidos = form.apellidos.data
        password = form.password.data
        confirmar_password = form.password2.data
        if password == confirmar_password:
            error = 'La contraseña de verificación no coincide.'
            user = Usuario.get_by_email(email)
            if user is not None:
                flash(f'El email {email} ya se encuentra registrado')
            else:
                user = Usuario(email=email, nombres=nombres, apellidos=apellidos)
                user.set_password(password)
                user.save()
                print(user)
                login_user(user, remember=True)
                next_page = request.args.get('next', None)
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('participantes.index')
                    return redirect(next_page)
        else:
            flash('La contraseña no coincide')
    return render_template("signup_form.html", form=form, error=error)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('participantes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('participantes.principal')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

    
@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('participantes.index'))


@login_manager.user_loader
def load_user(user_id):
    user_obj = Usuario.get_by_id(user_id)
    return user_obj