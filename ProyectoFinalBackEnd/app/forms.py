from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField,
    DateField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

# ----------------------------
# Formulario de Inicio de Sesión
# ----------------------------
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# ----------------------------
# Formulario de Registro de Usuario
# ----------------------------
class RegisterForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirmar Contraseña',
        validators=[DataRequired(), EqualTo('password')]
    )
    role = SelectField(
        'Rol',
        choices=[('Autor', 'Autor'), ('Editor', 'Editor')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Registrarse')

# ----------------------------
# Formulario para cambiar contraseña
# ----------------------------
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Contraseña Actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirmar Nueva Contraseña',
        validators=[DataRequired(), EqualTo('new_password')]
    )
    submit = SubmitField('Actualizar Contraseña')

# ----------------------------
# Formulario para Artículos
# ----------------------------
class ArticuloForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    contenido = TextAreaField('Contenido', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    fecha_publicacion = DateField('Fecha de Publicación', validators=[DataRequired()])
    estado = SelectField(
        'Estado',
        choices=[('Borrador', 'Borrador'), ('Publicado', 'Publicado')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Guardar')
