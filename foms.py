from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired
from wtforms import StringField,SubmitField,IntegerField,BooleanField,FloatField
from wtforms.validators import DataRequired, Regexp
from wtforms.widgets import TextArea
from werkzeug.security import generate_password_hash,check_password_hash

class Nombre(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Entrar')