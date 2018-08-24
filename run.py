from flask import Flask, request, render_template, redirect, url_for, session
import json
import os
import forms
import sqlite3 as sql


app = Flask(__name__)
app.secret_key = 'hacking'


# host = os.environ.get('IP', 'https://python-flask-condish.c9users.io')
# port = int(os.environ.get('PORT', 8080))






@app.route("/", methods=['GET', 'POST'])
def hello():
    
    search = forms.search(request.form)
    
    
    return render_template("index.html", searched = search)

@app.route("/registro", methods=['GET', 'POST'])
def registrar():
    register = forms.registro(request.form)
    search = forms.search(request.form)

    if request.method == 'POST':
        try:
            name = request.form['name']
            lastname = request.form['lastname']
            user = request.form['username']
            password = request.form['password']
            with sql.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user VALUES(Null,?,?,?,?)", (name,lastname,user,password))
                con.commit()
                session['username'] = user
                msg = 1
        except:
            con.rollback()
            msg = 0
        finally:
            if msg == 1:

                return redirect(url_for('ir'))
                con.close()
            else:
                return redirect(url_for('registrar'))
    
    
    return render_template("registro.html", searched = search, registre = register)

    
    

@app.route("/logeado", methods=['GET', 'POST'])
def ir():
    search = forms.search(request.form)

    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()

    cur.execute("select * from user")
    rows = cur.fetchall()

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

        con = sql.connect("database.db")
        con.row_factory = sql.Row

        cur = con.cursor()

        cur.execute("select * from user where username = ? and password = ?", (user,password))
        rows = cur.fetchone()

        if rows == None:
            return redirect(url_for("login"))
        else:
            session['username'] = user
            return redirect(url_for("ir"))
        


    return render_template("login.html", form = login , searched = search)



if __name__ == "__main__":

   

    
    app.run(debug=False, port=5000)