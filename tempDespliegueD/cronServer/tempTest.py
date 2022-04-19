import requests

r=requests.get('http://d3fojgopwmunq.cloudfront.net/convertidos/audio_625d83fb2cd2d272c64653b7.mp3')
print(r.status_code)
print(r.json())