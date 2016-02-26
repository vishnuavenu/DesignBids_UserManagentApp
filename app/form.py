from wtforms import StringField, SubmitField, Form, SelectField, PasswordField
from wtforms.validators import DataRequired


class UserForm(Form):
    username = StringField('Fullname', validators=[DataRequired()])
    home = StringField('Home directory', validators=[DataRequired()])
    shell = SelectField("Shell type", choices=[("/bin/zsh", "ZSH" ), ("/bin/bash","BASH"), ("/bin/sh", "SH")], default=("/bin/bash","BASH"))
    password = PasswordField('Password ', validators=[DataRequired()])
    submit = SubmitField("Add")

