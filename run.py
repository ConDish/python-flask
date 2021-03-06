from flask import Flask, request, render_template, redirect, url_for, session
import json
import os
import forms
from models import db
from models import Users




app = Flask(__name__)
db.init_app(app)
app.secret_key = 'hacking'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://arjhprbqdjuxfz:2fedab1c6840c4c07e20622d13b973f67d469170f6dddbaee24919dd14700e4b@ec2-54-235-160-57.compute-1.amazonaws.com:5432/d7ipmac3li50cn"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



@app.route("/", methods=['GET', 'POST'])
def hello():

    search = forms.search(request.form)

    if 'username' in session:
        return render_template("index.html", searched = search, username = session["username"])
    else:
        return render_template("index.html", searched = search)


@app.route("/registro", methods=['GET', 'POST'])
def registrar():
    register = forms.registro(request.form)
    search = forms.search(request.form)

    msg = 0

    if request.method == 'POST':
        try:
            name = request.form['name']
            lastname = request.form['lastname']
            user = request.form['username']
            password = request.form['password']

            register = Users(name=name, lastname=lastname, user=user, password=password)

            db.session.add(register)
            db.session.commit()

            session['username'] = user
            msg = 1
        except:
            con.rollback()
            msg = 0
        finally:
            if msg == 1:

                return redirect(url_for('ir'))

            else:
                return redirect(url_for('registrar'))


    return render_template("registro.html", searched = search, registre = register)


@app.route("/logeado", methods=['GET', 'POST'])
def ir():
    search = forms.search(request.form)


    rows = Users.query.order_by().all()

    if 'username' in session:
        return render_template("logeado.html", searched = search, rows = rows, username = session["username"])
    else:
        return redirect(url_for('registrar'))


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('hello'))

@app.route("/login", methods=['GET', 'POST'])
def login():

    login = forms.login(request.form)
    search = forms.search(request.form)

    if request.method == 'POST':

        user = login.username.data
        password = login.password.data


        usuario = Users.query.filter_by(user=user,password=password).first()

        if usuario is None:
            return redirect(url_for("login"))
        else:
            session['username'] = user
            return redirect(url_for("ir"))



    return render_template("login.html", form = login , searched = search)


@app.route("/foro", methods=['GET', 'POST'])
def foro():
    search = forms.search(request.form)

    if 'username' in session:

        return render_template("foro.html", searched = search, username = session['username'])
    else:
        return render_template("foro.html", searched = search)




if __name__ == "__main__":

    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
