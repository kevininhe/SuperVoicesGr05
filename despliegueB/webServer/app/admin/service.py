import requests

URL_ENTRY_FILE="http://172.28.208.1:5003/entry/%s/%s"
URL_CONVERTED_FILE="http://172.28.208.1:5003/converted/%s/%s"

def deleteAudioAPI(name,format):
    todelete=URL_ENTRY_FILE % (name,format)
    requests.delete(todelete)
    todelete=URL_CONVERTED_FILE % (name,format)
    requests.delete(todelete)