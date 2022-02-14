from email.mime import audio
from flask_mail import Message
from .models import Participante
import os

HEADER_EXITO='Tu audio ya se convirtio!'
HEADER_FALLA='Problemas con tu audio'
MENSAJE_EXITO="Hola, %s \n Es de nuestro gusto informarte que tu archivo de audio se convirtio exitosamente"
MENSAJE_FALLA="Hola, %s \n Actualmente presentamos problemas con tu audio \n por favor comunicate con ayuda"
PATH_AUDIOS_NEW = "static/AudioFilesDestiny/audio_%s.mp3"
PATH_AUDIOS_ORIGIN= "static/AudioFilesOrigin/%s"
MAIN_PATH=os.path.dirname(__file__)

def generateMailParticipante(nombre,recipient,mensaje,header,mail):
    msg = Message(header, sender = 'proyectoCloud2022@gmail.com', recipients = [recipient])
    msg.body = mensaje % nombre
    mail.send(msg)
def procesarAudio(path,audio_id):
    path=PATH_AUDIOS_ORIGIN % path
    path = os.path.join(MAIN_PATH, path)
    newPath=PATH_AUDIOS_NEW % audio_id
    newPath = os.path.join(MAIN_PATH, newPath)
    cmd=f'ffmpeg -loglevel quiet -y -i {path} {newPath}'
    os.system(cmd)
    return newPath

def jobAudios(mail):
        print("Job Audios")
        participantes=Participante.get_no_procesados()
        print(f'Participantes sin procesar {len(participantes)}')
        for participante in participantes:
            print(participante)
            audio=participante.path_audio
            mailParticipante=participante.mail
            nombre=participante.nombres
            id=participante.id
            try:
                newPath=procesarAudio(audio,id)
                generateMailParticipante(nombre,mailParticipante,MENSAJE_EXITO,HEADER_EXITO,mail)
                participante.path_audio=newPath
                participante.convertido=True
                participante.update()
            except:
                generateMailParticipante(nombre,mailParticipante,MENSAJE_FALLA,HEADER_FALLA,mail)