from wtforms import Form, TextField, StringField, PasswordField


class comment(Form):
    username = StringField('Username')
    password = PasswordField('Password')

class search(Form):
    searched = StringField('Searched')    

