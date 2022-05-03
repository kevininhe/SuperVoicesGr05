from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from flask_login import UserMixin
import os

HEADER_EXITO='Tu audio ya se convirtio!'
HEADER_FALLA='Problemas con tu audio'
MENSAJE_EXITO="Hola, %s \n Es de nuestro gusto informarte que tu archivo de audio se convirtio exitosamente"
MENSAJE_FALLA="Hola, %s \n Actualmente presentamos problemas con tu audio \n por favor comunicate con ayuda"
URL_GET_FILE="http://172.28.208.1:5003/entry/%s/%s"
URL_FS_SERVER="http://172.28.208.1:5003/converted"



app = Flask(__name__)

convertidos_dir = os.path.join(app.instance_path, 'convertidos')
os.makedirs(convertidos_dir, exist_ok=True)

entrantes_dir = os.path.join(app.instance_path, 'entrantes')
os.makedirs(entrantes_dir,exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@172.28.208.1:49154/app_cloud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'

db = SQLAlchemy()
scheduler = APScheduler()

db.init_app(app)
scheduler.init_app(app)
scheduler.start()

sg = sendgrid.SendGridAPIClient(api_key='')

class User(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombres =  db.Column(db.String(256), nullable=False)
    apellidos =  db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Concurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    nombre = db.Column( db.String(250) )
    imagen = db.Column( db.String(250) )
    url = db.Column( db.String(250) )
    fechaInicio = db.Column( db.DateTime )
    fechaFin = db.Column( db.DateTime )
    valor = db.Column( db.String(250) )
    guion = db.Column( db.String(250) )
    recomendaciones = db.Column( db.String(250) )
    fechaCreacion = db.Column( db.DateTime )

class Participante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concurso_id = db.Column(db.Integer, db.ForeignKey('concurso.id', ondelete='CASCADE'), nullable=False)
    path_audio = db.Column( db.String(250), nullable=False )
    path_audio_origin = db.Column(db.String(250), nullable=False)
    nombres = db.Column( db.String(250), nullable=False )
    apellidos = db.Column( db.String(250) , nullable=False)
    mail = db.Column( db.String(250), nullable=False )
    observaciones = db.Column( db.String(250) )
    convertido = db.Column(db.Boolean())
    fechaCreacion = db.Column( db.DateTime )

    @staticmethod
    def get_no_procesados():
        return Participante.query.filter_by(convertido=False).all()

def generateMailParticipante(nombre,recipient,mensaje,header):
    print("Start mail")
    from_email = Email("proyectoCloud2022@gmail.com") 
    print("FROM")
    to_email = To(recipient)  # Change to your recipient
    print("TO")
    subject = header
    print("HEADER")
    content = Content("text/plain", mensaje % nombre)
    print("Content")
    mail = Mail(from_email, to_email, subject, content)
    print("mail")

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()
    print("JSON")

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print("Start mail")
    print(response.status_code)

def procesarAudio(name,audio_id):
    path=entrantes_dir+"/"+name
    print(path)
    newPath=convertidos_dir+"/"+"audio_"+str(audio_id)+".mp3"
    print(newPath)
    cmd=f'ffmpeg -loglevel quiet -y -i {path} {newPath}'
    os.system(cmd)
    return f'audio_{audio_id}.mp3'
def sendAudio(name):
    path=convertidos_dir+"/"+name
    requests.post(URL_FS_SERVER,files={"audio":open(path,"rb")})

def getAudio(name):
    nameFile,formatFile=name.split(".")
    url=URL_GET_FILE% (nameFile,formatFile)
    try:
        r=requests.get(url)
        with open(entrantes_dir+"/"+name,'wb') as f:
            f.write(r.content)
            print("success")
    except Exception as e:
        print("Failure")
        raise e
def deleteAudioConverted(name):
    path=convertidos_dir+"/"+name
    os.remove(path)
def deleteAudioEntry(name):
    path=entrantes_dir+"/"+name
    os.remove(path)

def jobAudios():
        print("Job Audios")
        participantes=Participante.get_no_procesados()
        print(f'Participantes sin procesar {len(participantes)}')
        for participante in participantes:
            print(participante)
            audio=participante.path_audio
            print(audio)
            mailParticipante=participante.mail
            nombre=participante.nombres
            id=participante.id
            try:
                getAudio(audio)
                newPath=procesarAudio(audio,id)
                sendAudio(newPath)
                deleteAudioEntry(audio)
                deleteAudioConverted(newPath)
                participante.path_audio=newPath
                participante.convertido=True
                db.session.commit()
                generateMailParticipante(nombre,mailParticipante,MENSAJE_EXITO,HEADER_EXITO)
            except Exception as e:
                print(str(e))
                #generateMailParticipante(nombre,mailParticipante,MENSAJE_FALLA,HEADER_FALLA)

@scheduler.task('interval', id='job_process', seconds=20, misfire_grace_time=120)
def cronTask():
    with scheduler.app.app_context():
        jobAudios()

if __name__=="__main__":
    app.run(port=5000,host="0.0.0.0") 