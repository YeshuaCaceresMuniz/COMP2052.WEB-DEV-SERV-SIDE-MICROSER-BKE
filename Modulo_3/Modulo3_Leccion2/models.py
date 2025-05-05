# Importar la extensión de base de datos y el mixin de usuario
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Inicializar SQLAlchemy (se activa en app.py)
db = SQLAlchemy()

# Modelo de tabla de roles
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID del rol
    name = db.Column(db.String(50), unique=True)  # Nombre único del rol (ej: "admin", "editor")

# Modelo de tabla de usuarios
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # ID del usuario
    username = db.Column(db.String(50), unique=True, nullable=False)  # Nombre de usuario
    password = db.Column(db.String(50), nullable=False)  # Contraseña simple (idealmente usar hash)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # Clave foránea al rol
    role = db.relationship('Role')  # Relación ORM para acceder al objeto Role directamente
