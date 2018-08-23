from flask import Flask, request, render_template, redirect, url_for, session
import json
import os
import forms


app = Flask(__name__)
app.secret_key = 'hacking'
# host = os.environ.get('IP', 'https://python-flask-condish.c9users.io')
# port = int(os.environ.get('PORT', 8080))




@app.route("/", methods=['GET', 'POST'])
def hello():
    formulario = forms.comment(request.form)
    otro = forms.search(request.form)
    
    if request.method == 'POST':
        user = formulario.username.data
        
        dato = json.dumps({"user":user})
        
        
    
    return render_template("index.html", form = formulario, prueba = otro)

@app.route("/prueba", methods=['GET', 'POST'])
def prueba():
    
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        data = {"usuario" : user, "password" : password}
    
    return render_template("prueba.html", title=user)
    

@app.route("/hola", methods=['GET', 'POST'])
def ir():
    
    # user = request.form['username']
    # password = request.form['password']
    busqueda = request.form['searched']
    session['busqueda'] = request.form['searched']
    
    # eliminar session = session.clear()
    
    # print (user, password)
    
    return render_template("prueba.html", search = session['busqueda'])
    
    




if __name__ == "__main__":
    app.run(debug=False, port=5000)