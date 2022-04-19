from email.policy import default
from project import db
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Usuario(db.DynamicDocument,UserMixin):
    meta = {'collection': 'Usuario'} 

    nombres=db.StringField(required=True)
    password=db.StringField(required=True)
    apellidos=db.StringField(required=True)
    email=db.EmailField(required=True)

    def __repr__(self): 
        return "<Usuario '{}'>".format(self.nombres)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    @staticmethod
    def deleteAllDocuments():
        Usuario.objects.delete()

    @staticmethod
    def getByMailPassword(email,password):
        return Usuario.objects(email=email,password=password).first()

    @staticmethod
    def get_by_email(email):
        return Usuario.objects(email=email).first()
    
    @staticmethod
    def get_by_id(id):
        return Usuario.objects(_id=ObjectId(id)).first()
    