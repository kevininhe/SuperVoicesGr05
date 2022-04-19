from flask import Flask
from flask_apscheduler import APScheduler
from flask_mongoengine import MongoEngine
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import boto3

HEADER_EXITO='Tu audio ya se convirtio!'
HEADER_FALLA='Problemas con tu audio'
MENSAJE_EXITO="Hola, %s \n Es de nuestro gusto informarte que tu archivo de audio se convirtio exitosamente"
MENSAJE_FALLA="Hola, %s \n Actualmente presentamos problemas con tu audio \n por favor comunicate con ayuda"

S3_NAME='cloud-temp-s3'
queue_url = 'https://sqs.us-east-1.amazonaws.com/850281717368/cola-cloud'


s3 = boto3.resource('s3')
sqs = boto3.client('sqs')
sg = sendgrid.SendGridAPIClient(api_key='')

app = Flask(__name__)

app.config['MONGODB_HOST'] = 'mongodb+srv://admin:admin@cluster0.8xlzy.mongodb.net/SuperVoices?retryWrites=true&w=majority'

convertidos_dir = os.path.join(app.instance_path, 'convertidos')
os.makedirs(convertidos_dir, exist_ok=True)

entrantes_dir = os.path.join(app.instance_path, 'entrantes')
os.makedirs(entrantes_dir,exist_ok=True)


app.secret_key = 'secret'

scheduler = APScheduler()
db = MongoEngine()

db.init_app(app)
scheduler.init_app(app)
scheduler.start()

class Participante(db.DynamicDocument):
    meta = {'collection': 'Participante'} 
    path_audio=db.StringField(required=True)
    nombres=db.StringField(required=True)
    apellidos=db.StringField(required=True)
    mail=db.StringField(required=True)
    convertido=db.BooleanField(default=False,required=True)

    def __repr__(self): 
        return "<Participantes '{}'>".format(self.mail)


def generateMailParticipante(nombre,recipient,mensaje,header):
    from_email = Email("proyectoCloud2022@gmail.com") 
    to_email = To(recipient)  # Change to your recipient
    subject = header
    content = Content("text/plain", mensaje % nombre)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    try:
        sg.client.mail.send.post(request_body=mail_json)
    except:
        print("Send mail uwu")

def procesarAudio(name,audio_id):
    path=entrantes_dir+"/"+name
    newPath=convertidos_dir+"/"+"audio_"+str(audio_id)+".mp3"
    cmd=f'ffmpeg -loglevel quiet -y -i {path} {newPath}'
    os.system(cmd)
    return f'audio_{audio_id}.mp3'
def sendAudio(name):
    path=convertidos_dir+"/"+name
    s3.Object(S3_NAME, 'convertidos/'+name).upload_file(Filename=path)
def getAudio(name):
    try:
        s3.Object(S3_NAME, 'originales/'+name).download_file(entrantes_dir+'/'+name)
    except Exception as e:
        print("Failure")
        raise e
def deleteAudioConverted(name):
    path=convertidos_dir+"/"+name
    os.remove(path)
def deleteAudioEntry(name):
    path=entrantes_dir+"/"+name
    os.remove(path)
def updateParticipante(id,newPath):
    participante=Participante.objects(id=id).first()
    participante.update(path_audio=newPath)
    participante.update(convertido=True)
    participante.save(cascade=True)
    
def jobAudios():
        response = sqs.receive_message(QueueUrl=queue_url,AttributeNames=['SentTimestamp'],MaxNumberOfMessages=1,MessageAttributeNames=['All'],VisibilityTimeout=0,WaitTimeSeconds=0)
        if('Messages' in response.keys()):
            message = response['Messages'][0]
            audio=message['MessageAttributes']['path_audio']['StringValue']
            mailParticipante=message['MessageAttributes']['mail']['StringValue']
            nombre=message['MessageAttributes']['nombres']['StringValue']
            id=message['MessageAttributes']['id']['StringValue']
            receipt_handle = message['ReceiptHandle']
            try:
                getAudio(audio)
                newPath=procesarAudio(audio,id)
                sendAudio(newPath)
                deleteAudioEntry(audio)
                deleteAudioConverted(newPath)
                updateParticipante(id,newPath)
                generateMailParticipante(nombre,mailParticipante,MENSAJE_EXITO,HEADER_EXITO)
                sqs.delete_message(QueueUrl=queue_url,ReceiptHandle=receipt_handle)
            except Exception as e:
                print(str(e))
            

@scheduler.task('interval', id='job_process', seconds=60, misfire_grace_time=120)
def cronTask():
    with scheduler.app.app_context():
        jobAudios()

if __name__=="__main__":
    app.run(port=5000,host="0.0.0.0")