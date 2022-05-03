from project import db
import datetime
from project.concurso.models import Concurso
from bson import ObjectId

class Participante(db.DynamicDocument):
    meta = {'collection': 'Participante'} 
    concurso=db.ReferenceField(Concurso,required=True,reverse_delete_rule=2)
    concurso_id=db.StringField(required=True)
    path_audio=db.StringField(required=True)
    nombres=db.StringField(required=True)
    apellidos=db.StringField(required=True)
    mail=db.EmailField(required=True)
    observaciones=db.StringField(required=True)
    convertido=db.BooleanField(default=False,required=True)
    fechaCreacion=db.DateTimeField(default=datetime.datetime.now(),required=True)

    def __repr__(self): 
        return "<Participantes '{}'>".format(self.mail)

    @staticmethod
    def deleteAllDocuments():
        Participante.objects.delete()
    @staticmethod
    def findByConcurso(_id):
        return Participante.objects(concurso_id=str(_id))
    def get_by_id(id):
        return Participante.objects(id=ObjectId(id)).first()
