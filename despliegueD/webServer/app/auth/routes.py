from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User
from app import store
import pickle

@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
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
            user = User.get_by_email(email)
            if user is not None:
                flash(f'El email {email} ya se encuentra registrado')
            else:
                user = User(email=email, nombres=nombres, apellidos=apellidos)
                user.set_password(password)
                user.save()
                login_user(user, remember=True)
                next_page = request.args.get('next', None)
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('public.index')
                    return redirect(next_page)
        else:
            flash('La contraseña no coincide')
    return render_template("signup_form.html", form=form, error=error)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.principal')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

    
@auth_bp.route('/logout')
def logout():
    # Delete key from Elasticache
    if current_user.is_authenticated:
        userk = 'user_{}'.format(current_user.id)
        if store.get(userk):
            store.delete(userk)
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    # Crear la llave
    userk = 'user_{}'.format(user_id)
    # Intenta cargar el usuario desde la cache
    user_obj = pickle.loads(store.get(userk)) if store.get(userk) else None
    if user_obj is None:
        user_obj = User.get_by_id(int(user_id))
        # Usa picke para poder serializar el objeto y guardarlo en la cache
        user_pkl = pickle.dumps(user_obj)
        # Conserva el usuario en la cache por 10 minutos
        store.set(userk,user_pkl,ex=600)
    return user_obj
