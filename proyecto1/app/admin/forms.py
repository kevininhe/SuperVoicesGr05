from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,TextAreaField, BooleanField,DateField,IntegerField
from wtforms.validators import DataRequired, Email, Length

class ConcursoForm(FlaskForm):
    id = IntegerField('id')
    nombre =  StringField('Nombre', validators=[Length(max=128)])
    imagen =  StringField('Imagen', validators=[Length(max=128)])
    url = StringField('Url', validators=[Length(max=128)])
    valor =  StringField('Valor', validators=[Length(max=128)])
    fechaInicio = DateField('Fecha Inicio')
    fechaFin = DateField('Fecha Finalizacióm')
    guion =  TextAreaField('Guion', validators=[Length(max=128)])
    recomendaciones =  TextAreaField('recomendaciones', validators=[Length(max=128)])
    submit = SubmitField('Enviar')

class ParticipanteForm(FlaskForm):
    id = IntegerField('id')
    concurso_id =  StringField('concurso_id', validators=[Length(max=128)])
    path_audio =  StringField('path_audio', validators=[Length(max=128)])
    nombres = StringField('nombres', validators=[Length(max=128)])
    apellidos =  StringField('apellidos', validators=[Length(max=128)])
    mail = StringField('mail', validators=[Length(max=128)])
    observaciones =  TextAreaField('observaciones', validators=[Length(max=128)])
    convertido = StringField('convertido', validators=[Length(max=128)])
    submit = SubmitField('Enviar')