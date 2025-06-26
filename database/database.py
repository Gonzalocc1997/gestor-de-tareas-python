from sqlalchemy import create_engine  # Importamos para conectar con la base de datos
from sqlalchemy.ext.declarative import declarative_base  # Base para los modelos
from sqlalchemy.orm import sessionmaker  # Para crear sesiones y hacer consultas
import os  # Para manejar rutas y archivos

# Obtenemos la ruta absoluta donde está este archivo (database.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construimos la ruta completa donde estará la base de datos (archivo database.db)
DB_PATH = os.path.join(BASE_DIR, 'database.db')

# Dirección completa para conectarnos a la base de datos SQLite con la ruta anterior
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Creamos el motor que conecta con SQLite usando la URL de la base de datos
# connect_args={'check_same_thread': False} es necesario para evitar problemas de concurrencia con SQLite y Flask
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

# Creamos una "fábrica" de sesiones que usaremos para interactuar con la base de datos
# autocommit=False para controlar cuando hacemos commit, autoflush=False para no refrescar automáticamente los datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creamos la base que van a usar los modelos para que SQLAlchemy entienda que son tablas
Base = declarative_base()
