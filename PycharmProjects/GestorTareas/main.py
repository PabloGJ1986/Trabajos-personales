from flask import Flask, render_template, request, redirect, url_for
from models import Tarea

import db

app = Flask(__name__)
db.Base.metadata.create_all(db.engine)

@app.route('/')
def home():
    todas_las_tareas = db.session.query(Tarea).all()
    return render_template("index.html", lista_de_tareas=todas_las_tareas)

@app.route('/crear-tarea', methods=['POST'])
def crear():
    if request.method == 'POST':
        tarea = Tarea(contenido=request.form['contenido_tarea'], hecha=False)
        db.session.add(tarea)
        db.session.commit()
        return redirect(url_for('home', mensaje="Tarea creada"))
    else:
        return "Error: Esta ruta solo acepta solicitudes POST"

@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/tarea-hecha/<id>')
def hecha(id):
 tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
 tarea.hecha = not(tarea.hecha)
 db.session.commit()
 return redirect(url_for('home'))



    # Iniciar la aplicación
app.run(debug=True)

