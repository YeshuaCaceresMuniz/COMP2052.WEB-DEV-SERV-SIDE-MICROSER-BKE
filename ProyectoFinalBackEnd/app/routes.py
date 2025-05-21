from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import ArticuloForm, ChangePasswordForm
from app.models import db, Articulo, User

main = Blueprint('main', __name__)

# Página de inicio
@main.route('/')
def index():
    return render_template('index.html')

# Cambiar contraseña
@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('La contraseña actual es incorrecta.')
            return render_template('cambiar_password.html', form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Contraseña actualizada exitosamente.')
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

# Dashboard de usuario
@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name == 'Admin':
        articulos = Articulo.query.all()
    else:
        articulos = Articulo.query.filter_by(autor_id=current_user.id).all()

    return render_template('dashboard.html', articulos=articulos)

# Crear nuevo artículo
@main.route('/articulos', methods=['GET', 'POST'])
@login_required
def crear_articulo():
    form = ArticuloForm()
    if form.validate_on_submit():
        articulo = Articulo(
            titulo=form.titulo.data,
            contenido=form.contenido.data,
            categoria=form.categoria.data,
            fecha_publicacion=form.fecha_publicacion.data,
            estado=form.estado.data,
            autor_id=current_user.id
        )
        db.session.add(articulo)
        db.session.commit()
        flash("✅ Artículo creado exitosamente.")
        return redirect(url_for('main.dashboard'))

    return render_template('articulo_form.html', form=form)

# Editar artículo
@main.route('/articulos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_articulo(id):
    articulo = Articulo.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Editor'] and articulo.autor_id != current_user.id:
        flash('No tienes permiso para editar este artículo.')
        return redirect(url_for('main.dashboard'))

    form = ArticuloForm(obj=articulo)
    if form.validate_on_submit():
        articulo.titulo = form.titulo.data
        articulo.contenido = form.contenido.data
        articulo.categoria = form.categoria.data
        articulo.fecha_publicacion = form.fecha_publicacion.data
        articulo.estado = form.estado.data
        db.session.commit()
        flash("✅ Artículo actualizado correctamente.")
        return redirect(url_for('main.dashboard'))

    return render_template('articulo_form.html', form=form, editar=True)

# Eliminar artículo
@main.route('/articulos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_articulo(id):
    articulo = Articulo.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Editor'] and articulo.autor_id != current_user.id:
        flash('No tienes permiso para eliminar este artículo.')
        return redirect(url_for('main.dashboard'))

    db.session.delete(articulo)
    db.session.commit()
    flash("✅ Artículo eliminado correctamente.")
    return redirect(url_for('main.dashboard'))

# Listar usuarios (solo admin)
@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("No tienes permiso para ver esta página.")
        return redirect(url_for('main.dashboard'))

    usuarios = User.query.join(User.role).all()
    return render_template('usuarios.html', usuarios=usuarios)
