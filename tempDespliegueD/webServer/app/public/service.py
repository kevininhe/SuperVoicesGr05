import requests
import os

URL_ENTRY="http://172.28.208.1:5003/entry"
URL_ENTRY_FILE="http://172.28.208.1:5003/entry/%s/%s"
URL_CONVERTED_FILE="http://172.28.208.1:5003/converted/%s/%s"

def postAudioAPI(path):
    requests.post(URL_ENTRY,files={"audio":open(path,"rb")})
    os.remove(path)