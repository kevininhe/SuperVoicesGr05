from project import sqs, s3, S3_NAME,QUEUE_URL
import os

def postAudioAPI(path,name):
    s3.Object(S3_NAME, 'originales/'+name).upload_file(Filename=path)
    os.remove(path)

def sendMessageSQS(_id,name,mail,nombres):
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        DelaySeconds=10,
        MessageAttributes={
            'id': {
                'DataType': 'String',
                'StringValue': _id
            },
            'path_audio': {
                'DataType': 'String',
                'StringValue': name
            },
            'mail':{
                'DataType':'String',
                'StringValue':mail
            },
            'nombres':{
                'DataType':'String',
                'StringValue':nombres
            }
        },
        MessageBody=(
            'New audio'
        )
    )
    print(response['MessageId'])