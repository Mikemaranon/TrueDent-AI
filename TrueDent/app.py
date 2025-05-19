from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detectar', methods=['POST'])
def detectar():
    if 'imagen' not in request.files:
        return jsonify({'error': 'No se subió ninguna imagen'})

    file = request.files['imagen']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Aquí iría tu modelo de IA
    resultado = detectar_caries(filepath)

    return jsonify({'resultado': resultado})

def detectar_caries(ruta_imagen):
    # Simulamos una predicción
    return "Se detectaron caries en el lado izquierdo inferior."

if __name__ == '__main__':
    print("Iniciando Flask...")
    app.run(debug=True)
