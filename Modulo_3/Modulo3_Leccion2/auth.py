# Blueprint para manejar autenticación
from flask import Blueprint, request, redirect, url_for
from flask_login import LoginManager, login_user
from flask_principal import identity_changed, Identity
from models import User

# Crear blueprint de autenticación
auth_blueprint = Blueprint('auth', __name__)

# Inicializar LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Vista a redirigir si no está logueado

# Cargar usuario desde la base de datos usando su ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ruta para iniciar sesión (GET para mostrar formulario, POST para enviar datos)
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form.get('username')
        password = request.form.get('password')

        # Buscar usuario por nombre
        user = User.query.filter_by(username=username).first()

        # Validar contraseña (no se usa hash aquí por simplicidad)
        if user and user.password == password:
            login_user(user)  # Inicia sesión
            # Asociar identidad del usuario con Flask-Principal
            identity_changed.send(request._get_current_object(), identity=Identity(user.id))
            return redirect(url_for('index'))

        return 'Credenciales incorrectas.'

    # Mostrar formulario simple
    return '''
        <form method="POST">
            Usuario: <input type="text" name="username"><br>
            Contraseña: <input type="password" name="password"><br>
            <input type="submit" value="Iniciar sesión">
        </form>
    '''
