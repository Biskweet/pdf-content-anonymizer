from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField


# class EmailPasswordForm(FlaskForm):
#     email = StringField("email", validators=[DataRequired(), Email()])
#     password = PasswordField("password", validators=[DataRequired()])


class FileForm(FlaskForm):
    pdf = FileField("pdf")
