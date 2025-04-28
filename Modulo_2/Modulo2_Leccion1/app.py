 # Aplicación Flask que muestra páginas de inicio, usuarios y productos

from flask import Flask, render_template

# Crear instancia de Flask
app = Flask(__name__)

# Ruta principal (inicio)
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para mostrar usuarios
@app.route('/users')
def users():
    lista_usuarios = ['Juan', 'Pedro', 'Bryan', 'Marisol']
    return render_template('users.html', usuarios=lista_usuarios)

# Ruta para mostrar productos
@app.route('/products')
def products():
    productos = [
        {"nombre": "Laptop", "precio": 1000, "stock": 5},
        {"nombre": "Mouse", "precio": 25, "stock": 50},
        {"nombre": "Teclado", "precio": 45, "stock": 30},
        {"nombre": "Monitor", "precio": 200, "stock": 10},
    ]
    return render_template('products.html', productos=productos)

# Ejecutar aplicación
if __name__ == '__main__':
    app.run(debug=True)
