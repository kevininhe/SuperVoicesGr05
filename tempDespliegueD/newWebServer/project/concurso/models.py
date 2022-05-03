from project import db
import datetime
from project.usuario.models import Usuario
from bson import ObjectId
import json

class Concurso(db.DynamicDocument):
    meta = {'collection': 'Concurso'} 

    nombre=db.StringField(required=True)
    imagen=db.StringField(required=True)
    url=db.StringField(required=True)
    valor=db.FloatField(required=True)
    fechaInicio=db.DateTimeField(default=datetime.datetime.now(),required=True)
    fechaFin=db.DateTimeField(default=datetime.datetime.now(),required=True) 
    guion=db.StringField(required=True)
    recomendaciones=db.StringField(required=True)
    usuario=db.ReferenceField(Usuario,required=True,reverse_delete_rule=2)
    usuario_id=db.StringField(required=True)
    fechaCreacion=db.DateTimeField(default=datetime.datetime.now(),required=True) 

    def __repr__(self): 
        return "<Concurso '{}'>".format(self.nombre)

    @staticmethod
    def deleteAllDocuments():
        Concurso.objects.delete()
    @staticmethod
    def findByUsuario(_id):
        return Concurso.objects(usuario_id=_id)
    @staticmethod
    def get_all():
        return Concurso.objects()
    @staticmethod
    def get_by_id(id):
        return Concurso.objects(id=ObjectId(id)).first()
    @staticmethod
    def get_by_url(url):
        return Concurso.objects(url=url).first()