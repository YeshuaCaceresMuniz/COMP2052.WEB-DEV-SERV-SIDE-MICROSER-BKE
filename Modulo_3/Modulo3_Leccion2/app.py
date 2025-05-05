# Importar las librerías necesarias de Flask y sus extensiones
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_principal import (
    Principal, Permission, RoleNeed,
    identity_loaded, Identity, identity_changed, AnonymousIdentity
)
from models import db, User, Role
from auth import auth_blueprint, login_manager

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_super_secreta'  # Clave secreta para sesiones
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Base de datos SQLite

# Inicializar extensiones
db.init_app(app)
login_manager.init_app(app)
principal = Principal(app)

# Registrar el blueprint de autenticación
app.register_blueprint(auth_blueprint)

# Definir permisos basados en roles
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))

# Cargar identidad y asociar los roles al usuario actual
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role.name))

# Ruta principal pública
@app.route('/')
def index():
    return 'Bienvenido. <a href="/admin">Ir a Admin</a> | <a href="/logout">Cerrar sesión</a>'

# Ruta protegida: solo accesible por usuarios con rol "admin"
@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin_panel():
    return 'Panel de Administración (solo admins)'

# Ruta protegida: solo accesible por usuarios con rol "editor"
@app.route('/editor')
@editor_permission.require(http_exception=403)
def editor_panel():
    return 'Panel de Edición (solo editores)'

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Finaliza la sesión
    identity_changed.send(app, identity=AnonymousIdentity())  # Resetea la identidad de permisos
    return redirect(url_for('index'))

# Ejecutar la aplicación
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas si no existen

        # Crear roles y usuarios solo si no existen
        if not User.query.first():
            admin_role = Role(name='admin')
            editor_role = Role(name='editor')
            db.session.add_all([admin_role, editor_role])
            db.session.commit()

            admin_user = User(username='admin', password='1234', role_id=admin_role.id)
            editor_user = User(username='editor', password='1234', role_id=editor_role.id)
            db.session.add_all([admin_user, editor_user])
            db.session.commit()

    app.run(debug=True)
