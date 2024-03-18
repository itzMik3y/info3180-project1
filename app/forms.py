from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename

class UploadForm(FlaskForm):
    image= FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg','png'], 'Images only!')
    ])