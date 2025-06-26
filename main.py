# main.py

# Importamos la base y el motor desde database.py
from database.database import Base, engine

# Importamos el modelo Tarea, que queremos guardar en la base de datos
from database.models import Tarea

if __name__ == '__main__':
    # Creamos todas las tablas definidas en los modelos (en este caso, solo "tareas")
    Base.metadata.create_all(bind=engine)
    print(" Base de datos creada correctamente.")