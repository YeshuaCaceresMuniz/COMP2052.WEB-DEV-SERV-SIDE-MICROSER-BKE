from flask import Blueprint, jsonify, request
from app.models import db, Articulo

# Blueprint para pruebas API
main = Blueprint('main', __name__)

# -------------------------------
# GET /articulos → Obtener todos
# -------------------------------
@main.route('/articulos', methods=['GET'])
def get_articulos():
    articulos = Articulo.query.all()
    return jsonify([
        {
            'id': a.id,
            'titulo': a.titulo,
            'contenido': a.contenido,
            'categoria': a.categoria,
            'fecha_publicacion': str(a.fecha_publicacion),
            'estado': a.estado
        } for a in articulos
    ])

# -------------------------------------
# GET /articulos/<id> → Obtener uno
# -------------------------------------
@main.route('/articulos/<int:id>', methods=['GET'])
def get_articulo(id):
    articulo = Articulo.query.get_or_404(id)
    return jsonify({
        'id': articulo.id,
        'titulo': articulo.titulo,
        'contenido': articulo.contenido,
        'categoria': articulo.categoria,
        'fecha_publicacion': str(articulo.fecha_publicacion),
        'estado': articulo.estado
    })

# ------------------------------------------
# POST /articulos → Crear nuevo artículo
# ------------------------------------------
@main.route('/articulos', methods=['POST'])
def crear_articulo():
    data = request.get_json()
    nuevo = Articulo(
        titulo=data['titulo'],
        contenido=data['contenido'],
        categoria=data['categoria'],
        fecha_publicacion=data['fecha_publicacion'],
        estado=data['estado'],
        autor_id=data['autor_id']
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Artículo creado', 'id': nuevo.id}), 201

# ------------------------------------------
# PUT /articulos/<id> → Actualizar artículo
# ------------------------------------------
@main.route('/articulos/<int:id>', methods=['PUT'])
def actualizar_articulo(id):
    data = request.get_json()
    articulo = Articulo.query.get_or_404(id)
    articulo.titulo = data['titulo']
    articulo.contenido = data['contenido']
    articulo.categoria = data['categoria']
    articulo.estado = data['estado']
    db.session.commit()
    return jsonify({'mensaje': 'Artículo actualizado'})

# ------------------------------------------
# DELETE /articulos/<id> → Eliminar artículo
# ------------------------------------------
@main.route('/articulos/<int:id>', methods=['DELETE'])
def eliminar_articulo(id):
    articulo = Articulo.query.get_or_404(id)
    db.session.delete(articulo)
    db.session.commit()
    return jsonify({'mensaje': 'Artículo eliminado'})
