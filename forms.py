from wtforms import Form, TextField, StringField, PasswordField


class registro(Form):
    name = StringField('Name')
    lastname = StringField('Last Name')
    username = StringField('Username')
    password = PasswordField('Password')

class login(Form):
    username = StringField('Username')
    password = PasswordField('Password')

class search(Form):
    searched = StringField('Searched')    

