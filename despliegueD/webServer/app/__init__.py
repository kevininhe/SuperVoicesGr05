from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import url_for

login_manager = LoginManager()
db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.secret_key = 'secret'

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)
            
    @app.context_processor
    def utility_processor():
        def abrirURLConcurso(urlConcurso):
            return url_for('public.show_concurso', url=urlConcurso)
        def concurso_update(urlConcurso):
            return url_for('admin.concurso_update',url_concurso=urlConcurso)
        def concurso_delete(urlConcurso):
            return url_for('admin.concurso_delete',url_concurso=urlConcurso)
        return dict(abrirURLConcurso=abrirURLConcurso,concurso_update=concurso_update,concurso_delete=concurso_delete)

    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    @app.before_first_request
    def createDB():
        db.create_all()

    if __name__ == '__main__':
        app.run(debug=True)

    #if __name__ == '__main__':
        #app.run(host="0.0.0.0", port=8080, debug=False)

    return app