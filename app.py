from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from database.database import Base, engine, SessionLocal
from database.models import Tarea



# Inicializamos la aplicación Flask
app = Flask(__name__)
#app = Flask(__name__, template_folder='templates')
print("Ruta absoluta templates:", app.template_folder)
import os
print("Ruta absoluta templates:", os.path.abspath(app.template_folder))



# Esta línea se asegura de crear todas las tablas definidas en los modelos si no existen ya en la base de datos.
Base.metadata.create_all(bind=engine)

@app.route('/')
def index():
    session = SessionLocal()
    tareas = session.query(Tarea).all()
    session.close()
    return render_template('index.html', tareas=tareas)


# Ruta para mostrar el formulario para añadir una tarea nueva
@app.route('/nueva', methods=['GET'])
def nueva_tarea():
    # Simplemente renderizamos la plantilla con el formulario
    return render_template('nueva_tarea.html')

# Ruta que procesa el formulario para crear una tarea nueva
@app.route('/crear', methods=['POST'])
def crear_tarea():
    # Recogemos los datos enviados desde el formulario
    contenido = request.form.get('contenido')
    categoria = request.form.get('categoria')
    fecha_limite_str = request.form.get('fecha_limite')

    # Convertimos la fecha límite del formulario a un objeto date si viene definida
    fecha_limite = None
    if fecha_limite_str:
        try:
            fecha_limite = datetime.strptime(fecha_limite_str, '%Y-%m-%d').date()
        except ValueError:
            fecha_limite = None  # Si el formato es incorrecto, dejamos la fecha como None

    # Solo añadimos la tarea si el contenido no está vacío
    if contenido:
        session = SessionLocal()
        nueva = Tarea(
            contenido=contenido,
            categoria=categoria,
            fecha_limite=fecha_limite,
            completada=False  # Al crearla, la tarea siempre empieza sin completar
        )
        session.add(nueva)  # Añadimos la tarea a la sesión
        session.commit()  # Guardamos los cambios en la base de datos
        session.close()  # Cerramos la sesión

    # Finalmente redirigimos a la página principal para ver la lista actualizada
    return redirect(url_for('index'))

# Ruta para marcar una tarea como completada
@app.route('/completar/<int:tarea_id>')
def completar_tarea(tarea_id):
    session = SessionLocal()
    tarea = session.query(Tarea).get(tarea_id)  # Buscamos la tarea por su ID
    if tarea:
        tarea.completada = True  # Cambiamos el estado a completada
        session.commit()  # Guardamos el cambio
    session.close()
    return redirect(url_for('index'))

# Ruta para eliminar una tarea por su ID
@app.route('/eliminar/<int:tarea_id>')
def eliminar_tarea(tarea_id):
    session = SessionLocal()
    tarea = session.query(Tarea).get(tarea_id)
    if tarea:
        session.delete(tarea)  # Borramos la tarea de la base de datos
        session.commit()
    session.close()
    return redirect(url_for('index'))

# Ruta para mostrar el formulario de edición de una tarea
@app.route('/editar/<int:tarea_id>', methods=['GET'])
def editar_tarea(tarea_id):
    session = SessionLocal()
    tarea = session.query(Tarea).get(tarea_id)  # Obtenemos la tarea a editar
    session.close()
    if not tarea:
        # Si no existe la tarea, redirigimos al índice para evitar errores
        return redirect(url_for('index'))
    # Renderizamos la plantilla con los datos actuales de la tarea para editar
    return render_template('editar_tarea.html', tarea=tarea)

# Ruta que procesa la actualización de una tarea desde el formulario de edición
@app.route('/actualizar/<int:tarea_id>', methods=['POST'])
def actualizar_tarea(tarea_id):
    # Recogemos los nuevos datos del formulario
    contenido = request.form.get('contenido')
    categoria = request.form.get('categoria')
    fecha_limite_str = request.form.get('fecha_limite')
    completada = request.form.get('completada') == 'on'  # Checkbox para marcar completada

    fecha_limite = None
    if fecha_limite_str:
        try:
            fecha_limite = datetime.strptime(fecha_limite_str, '%Y-%m-%d').date()
        except ValueError:
            fecha_limite = None

    session = SessionLocal()
    tarea = session.query(Tarea).get(tarea_id)
    if tarea:
        # Actualizamos los campos con los nuevos valores
        tarea.contenido = contenido
        tarea.categoria = categoria
        tarea.fecha_limite = fecha_limite
        tarea.completada = completada
        session.commit()
    session.close()
    # Redirigimos a la página principal para ver la lista actualizada
    return redirect(url_for('index'))

# Ejecutamos la app en modo debug para desarrollo local
if __name__ == '__main__':
    app.run(debug=True)
