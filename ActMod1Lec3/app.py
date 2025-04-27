from flask import Flask, jsonify, request

# Crear la aplicación Flask
app = Flask(__name__)

# Lista para almacenar usuarios
usuarios = []

# Ruta GET /info - Devuelve información básica del sistema
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "nombre_sistema": "Gestion de Usuarios",
        "version": "1.0",
        "desarrollador": "Yeshua R00625131",
        "mensaje": "Para crear un usuario ve a /crear_usuario (POST)"
    })

# Ruta POST /crear_usuario - Crea un nuevo usuario con nombre y correo
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    data = request.json
    nombre = data.get("nombre")
    correo = data.get("correo")

    # Validar que nombre y correo estén presentes
    if not nombre or not correo:
        return jsonify({"error": "Faltan datos: 'nombre' y 'correo' son requeridos"}), 400

    nuevo_usuario = {
        "id": len(usuarios) + 1,
        "nombre": nombre,
        "correo": correo
    }
    usuarios.append(nuevo_usuario)
    return jsonify({"mensaje": "Usuario creado exitosamente", "usuario": nuevo_usuario})

# Ruta GET /usuarios - Devuelve la lista de usuarios registrados
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    return jsonify(usuarios)

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
