from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
import boto3
import redis
from flask_session import Session

from botocore import UNSIGNED
from botocore.client import Config
import os
from boto3.s3.transfer import TransferConfig

# Set the desired multipart threshold value (50 MBs)
MB = 1024 ** 2
CONFIGTR_S3 = TransferConfig(multipart_threshold=50*MB)

#TODO create logs
S3_NAME = os.environ.get('S3_NAME')
QUEUE_URL = os.environ.get('QUEUE_URL')
REGION_NAME='us-east-1'
CLOUD_FRONT_URL='https://d3fojgopwmunq.cloudfront.net'


#s3 = boto3.resource('s3')
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED),region_name=REGION_NAME)
sqs = boto3.client('sqs', config=Config(signature_version=UNSIGNED),region_name=REGION_NAME)
login_manager = LoginManager()
db = MongoEngine()

def create_app(config_file):
    app= Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile(config_file)
    initializeExtensions(app)
    registerBlueprints(app)
    return app

def initializeExtensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    server_session = Session(app)
    

def registerBlueprints(app):
    from .usuario import users_blueprint
    app.register_blueprint(users_blueprint)

    from .participante import participantes_blueprint
    app.register_blueprint(participantes_blueprint)

    from .concurso import concurso_blueprint
    app.register_blueprint(concurso_blueprint)