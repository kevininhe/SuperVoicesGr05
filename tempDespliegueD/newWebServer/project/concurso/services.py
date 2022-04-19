from project import s3, S3_NAME
import os

def deleteAudioAPI(original,convertido):
    s3.Object(S3_NAME, f'convertidos/{convertido}').delete()
    s3.Object(S3_NAME, f'originales/{original}').delete()

def uploadImage(name,path):
    s3.Object(S3_NAME, 'imagenes/'+name).upload_file(Filename=path)
    os.remove(path)

def deleteImage(name):
    s3.Object(S3_NAME, f'imagenes/{name}').delete()