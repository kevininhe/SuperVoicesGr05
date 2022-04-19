from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
import boto3
import redis

#TODO create logs
S3_NAME='cloud-temp-s3'
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/850281717368/cola-cloud'
REGION_NAME='us-east-1'
CLOUD_FRONT_URL='https://d3fojgopwmunq.cloudfront.net'


s3 = boto3.resource('s3')
sqs = boto3.client('sqs')
logs=boto3.client('logs')
cache=redis.Redis(host='172.25.240.1',db=0)
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
    

def registerBlueprints(app):
    from .usuario import users_blueprint
    app.register_blueprint(users_blueprint)

    from .participante import participantes_blueprint
    app.register_blueprint(participantes_blueprint)

    from .concurso import concurso_blueprint
    app.register_blueprint(concurso_blueprint)