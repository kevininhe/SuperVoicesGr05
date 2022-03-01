from crypt import methods
from flask import Flask, Response, request, send_from_directory
import os
from werkzeug.utils import secure_filename


app=Flask(__name__)

convertidos_dir = os.path.join(app.instance_path, 'convertidos')
os.makedirs(convertidos_dir, exists_ok=True)

entrantes_dir = os.path.join(app.instance_path, 'entrantes')
os.makedirs(entrantes_dir, exists_ok=True)

app.secret_key = 'secret'

@app.route('/')
def index():
    return "<h1>Servidor FS</h1><h2>Links</h2><ul><li>/converted</li><li>/entry</li><li>/entry/<string:name></li><li>/converted/<string:name></li></ul>"
@app.route('/converted',methods=["POST"])
def uploadConvertedFile():
    try:
        audio=request.files["audio"]
        audio.save(os.path.join(convertidos_dir, secure_filename(audio.filename)))
        return Response(status=201)
    except Exception:
        return Response(status=400)
@app.route('/entry',methods=["POST"])
def uploadCEntryFile():
    try:
        audio=request.files["audio"]
        audio.save(os.path.join(entrantes_dir, secure_filename(audio.filename)))
        return Response(status=201)
    except Exception:
        return Response(status=400)
@app.route('/entry/<string:name>',methods=["GET","DELETE"])
def entryFile(name):
    path=entrantes_dir+name
    if(os.path.exists(path)):
        if(request.method=="DELETE"):
            try:
                os.remove(path)
                return Response(status=200)
            except Exception:
                return Response(status=500)
        else:
            try:
                return send_from_directory(entrantes_dir,filename=name,as_attachment=True)
            except Exception:
                return Response(status=500)
    else:
        return Response(status=404)
@app.route('/converted/<string:name>',methods=["GET","DELETE"])
def convertidoFile(name):
    path=convertidos_dir+name
    if(os.path.exists(path)):
        if(request.method=="DELETE"):
            try:
                os.remove(path)
                return Response(status=200)
            except Exception:
                return Response(status=500)
        else:
            try:
                return send_from_directory(convertidos_dir,filename=name,as_attachment=True)
            except Exception:
                return Response(status=500)
    else:
        return Response(status=404)

if __name__=="__main__":
    app.run(port=5000,host="0.0.0.0")