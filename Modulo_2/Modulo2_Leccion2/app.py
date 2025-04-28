# Importamos las librerías necesarias
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# Inicializamos la aplicación Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "clave_segura"  # Clave secreta para proteger los formularios (CSRF)

# Ruta de la página principal
@app.route("/")
def index():
    return "<h1>Bienvenido a la página principal</h1><p><a href='/register'>Ir al registro</a></p>"

# Definimos el formulario de registro usando FlaskForm
class RegistrationForm(FlaskForm):
    name = StringField("Nombre", validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, message="El nombre debe tener al menos 3 caracteres.")
    ])
    email = StringField("Correo", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Formato de correo inválido.")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
    ])
    submit = SubmitField("Registrarse")  # Botón de envío

# Ruta para mostrar y procesar el formulario de registro
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # Si el formulario es válido al enviarlo
        return f"Usuario registrado: {form.name.data}"  # Mostramos mensaje de éxito
    return render_template("register.html", form=form)  # Renderizamos el formulario en caso contrario

# Ejecutamos la aplicación en modo debug
if __name__ == "__main__":
    app.run(debug=True)
