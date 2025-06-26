from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

# Creamos la base para los modelos, es la clase que heredan todas las tablas
Base = declarative_base()

# Modelo para la tabla 'persona'
class Persona(Base):
    __tablename__ = 'persona'  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)  # ID único y clave primaria
    name = Column(String, nullable=False)  # Campo obligatorio para el nombre
    edad = Column(Integer, nullable=False)  # Campo obligatorio para la edad

    def __str__(self):
        # Método para mostrar la persona como texto de forma sencilla
        return "Nombre: {}, Edad: {}".format(self.name, self.edad)


# Modelo para la tabla 'tarea'
class Tarea(Base):
    __tablename__ = 'tarea'  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)  # ID único y clave primaria
    contenido = Column(String, nullable=False)  # Texto de la tarea, obligatorio
    categoria = Column(String, nullable=True)  # Categoría, campo opcional
    fecha_limite = Column(DateTime, nullable=True)  # Fecha límite para completar la tarea, opcional
    persona_id = Column(Integer, ForeignKey('persona.id'))  # Relación con la tabla persona (ID)
    completada = Column(Boolean, default=False)  # Indica si la tarea está completada o no, por defecto False
    fecha_creacion = Column(DateTime, default=datetime.utcnow)  # Fecha de creación, se asigna automáticamente la fecha y hora actual

    def __str__(self):
        # Muestra el contenido de la tarea con su estado (completada o pendiente)
        estado = "[OK]" if self.completada else "[Pendiente]"
        return f"{self.contenido} {estado}"
