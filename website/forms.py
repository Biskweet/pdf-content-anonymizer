from flask_wtf import FlaskForm
from wtforms import FileField


class FileForm(FlaskForm):
    pdf = FileField("pdf")
