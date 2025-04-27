from flask import Flask, request, jsonify

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta raíz "/" que devuelve un mensaje de bienvenida
@app.route("/", methods=["GET"])
def home():
    mensaje = """
    Bienvenido a la API REST.

    Para ver la información de la aplicación, escribe /info al final de la barra de direcciones.
    Para enviar un mensaje, realiza una solicitud POST a /mensaje con un mensaje en formato JSON.
    """
    return mensaje, 200

# GET /info - Devuelve información básica de la aplicación
@app.route("/info", methods=["GET"])
def get_info():
    info = {
        "nombre": "Servidor Flask de Ejemplo",
        "version": "1.0",
        "desarrollador": "Yeshua R00625131",
        "mensaje": "Bienvenido a la API REST de ejemplo"
    }
    return jsonify(info), 200  # 200 OK

# POST /mensaje - Recibe un mensaje en JSON y responde confirmándolo
@app.route("/mensaje", methods=["POST"])
def post_mensaje():
    data = request.get_json()  # Recibe los datos en formato JSON

    # Validar que haya una clave llamada "mensaje"
    if not data or "mensaje" not in data:
        return jsonify({"error": "Falta el campo 'mensaje' en el JSON"}), 400  

    mensaje = data["mensaje"]
    respuesta = {
        "respuesta": f"Recibi tu mensaje: '{mensaje}'. Gracias por enviarlo!"
    }
    return jsonify(respuesta), 200

 
if __name__ == "__main__":
    app.run(debug=True)
