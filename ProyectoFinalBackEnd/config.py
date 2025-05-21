import os

class Config:
    # Clave secreta para proteger sesiones y formularios
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-flask')

    # URL de conexión a tu base de datos MariaDB/MySQL local
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:admin123@localhost/publicacion_articulos'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
