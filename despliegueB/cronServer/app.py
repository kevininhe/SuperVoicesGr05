from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@172.28.208.1:49153/app_cloud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'

db = SQLAlchemy()
scheduler = APScheduler()

db.init_app(app)
#El encargado de hacer jobs perodicamente
scheduler.init_app(app)
scheduler.start()    

from .cronJob import jobAudios
@scheduler.task('interval', id='job_process', seconds=20, misfire_grace_time=120)
def cronTask():
    with scheduler.app.app_context():
        jobAudios()

if __name__=="__main__":
    app.run(port=5000,host="0.0.0.0") 