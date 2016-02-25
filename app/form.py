from wtforms import StringField, SubmitField, Form, SelectField
from wtforms.validators import DataRequired


class UserForm(Form):
    username = StringField('Enter the Fullname', validators=[DataRequired()])
    home = StringField("Enter the Folder's Name", validators=[DataRequired()])
    shell = SelectField("Choose your Shell type", choices=[("/bin/zsh", "ZSH" ), ("/bin/bash","BASH"), ("/bin/sh", "SH")], default=("/bin/bash","BASH"))
    password = StringField('Enter the Password ', validators=[DataRequired()])
    submit = SubmitField("Add User")

