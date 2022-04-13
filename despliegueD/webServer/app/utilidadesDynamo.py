import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

# Constantes
dynamodb = boto3.resource('dynamodb')
TABLE = dynamodb.Table('ConcursoYParticipante')

# Seccion de concurso
def traerUUIDConcurso(urlConcurso):
    response = TABLE.scan(
        FilterExpression=Attr('url_concurso').eq(urlConcurso)
    )
    items = response['Items']
    if len(items) > 0:
        return items[0]["PK"].replace("CON#","")

def traerInfoConcurso(urlConcurso):
    uid = traerUUIDConcurso(urlConcurso)
    pk = 'CON#{}'.format(uid)
    sk = 'METADATA#{}'.format(uid)
    response = TABLE.query(
        KeyConditionExpression=Key('PK').eq(pk) & Key('SK').eq(sk)
    )
    items = response['Items']
    if len(items) > 0:
        return items[0]

def traerConcursosUsuario(idUser):
    response = TABLE.scan(
        FilterExpression=Attr('user_id').eq(idUser)
    )
    items = response['Items']
    return items

def insertarConcurso(user_id,nombre,imagen,url,valor,fechaInicio,fechaFin,guion,recomendaciones,fechaCreacion):
    uid = str(uuid.uuid4())
    return actualizarConcurso(uid,user_id,nombre,imagen,url,valor,fechaInicio,fechaFin,guion,recomendaciones,fechaCreacion)

# Retorna un diccionario con dos keys: Attributes y ResponseMetadata. Attributes trae el objeto despues de ser actualizado
def actualizarConcurso(uid,user_id,nombre,imagen,url,valor,fechaInicio,fechaFin,guion,recomendaciones,fechaCreacion):
    pk = 'CON#{}'.format(uid)
    sk = 'METADATA#{}'.format(uid)

    updatedElement = TABLE.update_item(
    Key={
        'PK': pk,
        'SK': sk
    },
    UpdateExpression='SET user_id = :user_id,nombre = :nombre,imagen = :imagen,url_concurso = :url_concurso,valor = :valor,fechaInicio = :fechaInicio,fechaFin = :fechaFin,guion = :guion,recomendaciones = :recomendaciones,fechaCreacion = :fechaCreacion',
    ExpressionAttributeValues={
        ':user_id':user_id,
        ':nombre':nombre,
        ':imagen':imagen,
        ':url_concurso':url,
        ':valor':valor,
        ':fechaInicio':fechaInicio,
        ':fechaFin':fechaFin,
        ':guion':guion,
        ':recomendaciones':recomendaciones,
        ':fechaCreacion':fechaCreacion
    },
    ReturnValues="ALL_NEW"
    )
    return updatedElement

# Retorna un diccionario con dos keys: Attributes y ResponseMetadata. Attributes trae el objeto despues de ser actualizado
def actualizarConcursoForm(uid,nombre,imagen,url,valor,fechaInicio,fechaFin,guion,recomendaciones):
    pk = 'CON#{}'.format(uid)
    sk = 'METADATA#{}'.format(uid)

    updatedElement = TABLE.update_item(
    Key={
        'PK': pk,
        'SK': sk
    },
    UpdateExpression='SET nombre = :nombre,imagen = :imagen,url_concurso = :url_concurso,valor = :valor,fechaInicio = :fechaInicio,fechaFin = :fechaFin,guion = :guion,recomendaciones = :recomendaciones',
    ExpressionAttributeValues={
        ':nombre':nombre,
        ':imagen':imagen,
        ':url_concurso':url,
        ':valor':valor,
        ':fechaInicio':fechaInicio,
        ':fechaFin':fechaFin,
        ':guion':guion,
        ':recomendaciones':recomendaciones
    },
    ReturnValues="ALL_NEW"
    )
    return updatedElement

def actualizarConcursoFormNoImg(uid,nombre,url,valor,fechaInicio,fechaFin,guion,recomendaciones):
    pk = 'CON#{}'.format(uid)
    sk = 'METADATA#{}'.format(uid)

    updatedElement = TABLE.update_item(
    Key={
        'PK': pk,
        'SK': sk
    },
    UpdateExpression='SET nombre = :nombre,url_concurso = :url_concurso,valor = :valor,fechaInicio = :fechaInicio,fechaFin = :fechaFin,guion = :guion,recomendaciones = :recomendaciones',
    ExpressionAttributeValues={
        ':nombre':nombre,
        ':url_concurso':url,
        ':valor':valor,
        ':fechaInicio':fechaInicio,
        ':fechaFin':fechaFin,
        ':guion':guion,
        ':recomendaciones':recomendaciones
    },
    ReturnValues="ALL_NEW"
    )
    return updatedElement

# Retorna un diccionario con dos keys: Attributes y ResponseMetadata. Si no elimina nada, no viene Attributes
def eliminarConcurso(uid):
    pk = 'CON#{}'.format(uid)
    sk = 'METADATA#{}'.format(uid)
    response = TABLE.delete_item(
        Key={
        'PK': pk,
        'SK': sk
        },
        ReturnValues="ALL_OLD"
    )
    return response

# Seccion de participantes

def traerParticipantesConcurso(uidConcurso,traerSoloProcesados=False):
    pk = uidConcurso
    sk = 'VOZ#'
    response = None
    if traerSoloProcesados:
        response = TABLE.query(
            KeyConditionExpression=Key('PK').eq(pk) & Key('SK').begins_with(sk),
            FilterExpression=Attr('procesado').eq(True)
        )
    else:
        response = TABLE.query(
            KeyConditionExpression=Key('PK').eq(pk) & Key('SK').begins_with(sk)
        )
    if response:
        items = response['Items']
        itemsSorted = sorted(items, key = lambda diction : datetime.strptime(diction["fechaCreacion"],"%Y-%m-%d-%H:%M:%S"), reverse=True)
        return items
    else:
        return []

def insertarParticipante(concurso_id,path_audio,path_audio_origin,nombres,apellidos,mail,observaciones,convertido,fechaCreacion):
    uid = str(uuid.uuid4())
    return actualizarParticipante(uid,concurso_id,path_audio,path_audio_origin,nombres,apellidos,mail,observaciones,convertido,fechaCreacion)

# Retorna un diccionario con dos keys: Attributes y ResponseMetadata. Attributes trae el objeto despues de ser actualizado
def actualizarParticipante(uid,concurso_id,path_audio,path_audio_origin,nombres,apellidos,mail,observaciones,convertido,fechaCreacion):
    pk = 'CON#{}'.format(concurso_id)
    sk = 'VOZ#{}'.format(uid)

    updatedElement = TABLE.update_item(
    Key={
        'PK': pk,
        'SK': sk
    },
    UpdateExpression='SET path_audio = :path_audio,path_audio_origin = :path_audio_origin,nombres = :nombres,apellidos = :apellidos,mail = :mail,observaciones = :observaciones,convertido = :convertido,fechaCreacion = :fechaCreacion',
    ExpressionAttributeValues={
        ':path_audio': path_audio,
        ':path_audio_origin': path_audio_origin,
        ':nombres': nombres,
        ':apellidos': apellidos,
        ':mail': mail,
        ':observaciones': observaciones,
        ':convertido': convertido,
        ':fechaCreacion': fechaCreacion
    },
    ReturnValues="ALL_NEW"
    )
    return updatedElement

def traerInfoParticipante(urlConcurso,participante_id):
    uid = traerUUIDConcurso(urlConcurso)
    pk = 'CON#{}'.format(uid)
    sk = participante_id
    response = TABLE.query(
        KeyConditionExpression=Key('PK').eq(pk) & Key('SK').eq(sk)
    )
    items = response['Items']
    if len(items) > 0:
        return items[0]

# Retorna un diccionario con dos keys: Attributes y ResponseMetadata. Si no elimina nada, no viene Attributes
def eliminarParticipante(urlConcurso,participante_id):
    uid = traerUUIDConcurso(urlConcurso)
    pk = 'CON#{}'.format(uid)
    sk = participante_id
    response = TABLE.delete_item(
        Key={
        'PK': pk,
        'SK': sk
        },
        ReturnValues="ALL_OLD"
    )
    return response