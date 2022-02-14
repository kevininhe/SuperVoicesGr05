from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_mail import Mail

login_manager = LoginManager()
db = SQLAlchemy()
scheduler = APScheduler()
mail= Mail()

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB_proyecto1_2.db' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Configuracion del mail
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'proyectoCloud2022@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Cloud2022'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True


    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)
    #el objeto Mail
    mail.init_app(app)
    #El encargado de hacer jobs perodicamente
    scheduler.init_app(app)
    scheduler.start()    

    from .cronJob import jobAudios
    @scheduler.task('interval', id='job_process', seconds=20, misfire_grace_time=120)
    def cronTask():
        with scheduler.app.app_context():
            jobAudios(mail)
            
            

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