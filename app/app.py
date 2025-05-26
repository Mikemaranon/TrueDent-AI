from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegura que exista el directorio de uploads
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Carga el modelo entrenado (ajusta el nombre si es distinto)
modelo = tf.keras.models.load_model('modelo_caries.h5')

# Configura el tamaño de entrada según tu modelo
IMG_SIZE = (224, 224)

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

    # Procesar imagen con el modelo
    resultado = detectar_caries(filepath)

    return jsonify({'resultado': resultado})

def detectar_caries(ruta_imagen):
    try:
        img = image.load_img(ruta_imagen, target_size=IMG_SIZE)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalización si fue entrenado así

        prediccion = modelo.predict(img_array)[0]

        # Asumimos modelo binario con una salida (0=no caries, 1=caries)
        if prediccion > 0.5:
            return "🦷 Se detectaron caries en la imagen."
        else:
            return "✅ No se detectaron caries."
    except Exception as e:
        return f"❌ Error al procesar la imagen: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
