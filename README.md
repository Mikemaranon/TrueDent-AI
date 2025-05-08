# TrueDent AI: Detección de patologías con un solo click

**TrueDent AI** es una plataforma de análisis inteligente para `radiografías panorámicas dentales`. Su misión es `asistir` a odontólogos y profesionales de la salud dental mediante un sistema automatizado capaz de:

- Detectar y etiquetar estructuras dentales y óseas clave.
- Identificar patologías comunes como caries, pérdida ósea y dientes impactados.
- Generar reportes clínicos automáticos y visualizaciones explicativas.
- (Opcional) Ofrecer reconstrucciones 3D parciales a partir de imágenes panorámicas.

La solución busca mejorar la precisión diagnóstica, optimizar tiempos de análisis y facilitar la comunicación con los pacientes, todo bajo estándares de privacidad y calidad médica.

## 1. Objetivos

- `Detección y Segmentación`: Automatizar la identificación de dientes, mandíbula, senos maxilares y otras estructuras relevantes.
- `Análisis de Patologías`: Implementar detección avanzada de anomalías dentales mediante IA.
- `Generación de Reportes`: Producir descripciones clínicas automáticas y claras para cada imagen analizada.
- `Visualización Avanzada (opcional)`: Explorar la creación de reconstrucciones 3D parciales para un entendimiento más profundo.

## 2. Herramientas utilizadas

El desarrollo de `TrueDent AI` se basa en un stack robusto y probado para aplicaciones de visión por computadora e inteligencia artificial generativa.

| **Función**                  | **Herramientas sugeridas**               |
| ---------------------------- | ---------------------------------------- |
| Preprocesamiento de imágenes | OpenCV, PIL, Pydicom                     |
| Detección y segmentación     | YOLOv8, Detectron2, U-Net, MMDetection   |
| IA generativa visual         | GANs, Stable Diffusion, Segment Anything |
| IA generativa textual        | GPT-4, BLIP2, LLaVA                      |
| Plataforma de desarrollo     | Python, PyTorch/TensorFlow, Hugging Face |
| Dataset panorámico dental    | OpenDSA, Dental X-ray sets en Kaggle     |


### 2.1 Flujo de trabajo

Para poder llevar a cabo el proyecto, necesitamos dividir las tareas y tecnologías para cada labor, en orden cronológico por las distintas fases del proyecto

#### `2.1.1 Recopilacion de datos`
- Uso de datasets públicos y colaboración con clínicas u odontólogos.
- Cumplimiento estricto de normativas de privacidad (GDPR, HIPAA si aplica).

#### `2.1.2 Preprocesamiento`
- Normalización de contraste.
- Remoción de artefactos.
- Recorte de márgenes irrelevantes.

#### `2.1.3 Detección y Fragmentación`
Entrenamiento con modelos como YOLOv8 o U-Net para identificar estructuras dentales (dientes, mandíbula, senos maxilares, etc.).

#### `2.1.4 Clasificación y detección de patologías`
Implementación de modelos para identificar caries, dientes impactados, pérdida ósea y otras anomalías.

#### `2.1.5 Generación de Reportes Automáticos`
Uso de modelos generativos de lenguaje (ej. BLIP2, GPT-4V) para producir descripciones clínicas precisas.

#### `2.1.6 (Opcional) Reconstrucción 3D`
Experimentación con GANs y/o técnicas como NeRF para generar vistas tridimensionales parciales.

## 3. División de Tareas y Roadmap

El desarrollo de `TrueDent AI` está dividido en fases para garantizar un `avance ordenado y medible` a lo largo del proyecto.

### Fase 1: *Recopilación y Preprocesamiento (Semana 1-2)*
- `Recolección` de Datasets
    - Identificar y descargar datasets públicos.
    - Explorar acuerdos con clínicas dentales para ampliar la base de datos.
- `Preprocesamiento`
    - Conversión y manejo de formatos (DICOM, PNG, etc.).
    - Normalización de contraste y remoción de artefactos.
    - Implementación de scripts para recorte y limpieza de imágenes.

### Fase 2: *Detección y Segmentación (Semana 2-4)*
- `Modelado`
    - Entrenamiento de un modelo de detección (YOLOv8 o U-Net)
    - Validación y ajuste fino sobre las estructuras dentales clave
- `Evaluación`
    - Métricas: precisión, recall, F1-score sobre imágenes de prueba
    - Análisis de errores y optimización de hiperparámetros

### Fase 3: *Patologías y Clasificación (Semana 4-5)*
-  `Identificación de Anomalías`
    - Definición de clases (caries, dientes impactados, etc.).
    - Entrenamiento y validación del modelo de patologías.
- `Validación Clínica`
    - Revisión de resultados con apoyo de profesionales

### Fase 4: *Generación de Reportes (Semana 5-6)*
- `Automatización de Informes`
    - Integración con BLIP2 / GPT-4V para generación de textos automáticos.
    - Validación de la claridad y precisión clínica de los reportes

### Fase Opcional: *Reconstrucción Visual (Semana 6+)*
- `Reconstrucción 3D`
    - Pruebas iniciales con GANs o NeRF para reconstrucción parcial.
    - Evaluación de la viabilidad y calidad de las visualizaciones.

### Cronograma estimado

| Semana | Tarea                                                  |
| ------ | ------------------------------------------------------ |
| 1      | Recopilación de datos, preprocesamiento inicial        |
| 2      | Prototipo de detección y segmentación                  |
| 3      | Optimización y validación de segmentación              |
| 4      | Implementación de patología y clasificación            |
| 5      | Generación automática de reportes + pruebas integradas |
| 6      | Ajustes finales, tests de robustez, documentación      |
| Extra  | Visualización 3D (si hay tiempo y recursos)            |


## 4. Instalación

Para correr TrueDent AI, asegurate de tener Python ≥ 3.9 y un entorno compatible con GPU (CUDA recomendado para aceleración).
### Para trabajar en las ramas
```bash
# para mike
git checkout mike

# para javi
git checkout javi
```

### Antes de empezar a trabajar (o cada tanto), muy importante para evitar conflictos después
```bash
# para mike
git checkout mike
git fetch origin
git merge origin/main

# para javi
git checkout javi
git fetch origin
git merge origin/main
```

### para subir el contenido **(MUY IMPORTANTE ESTAR EN NUESTRA RAMA)**
```bash
# como siempre
git add .
git commit -m "feat: [lo que hiciste, ej. mejora de detección]"

# para mike
git push origin mike

# para javi
git push origin javi
```

### Cuando termines tu parte y quieras subirla a `main`
```bash
# para mike
gh pr create --base main --head mike --title "Merge mike into main" --body "Descripción"

# para javi
gh pr create --base main --head javi --title "Merge javi into main" --body "Descripción"
```

### Después que se aprueba el PR
```bash
# para mike
gh pr merge --merge

# para javi
gh pr merge --merge
```

### Para mantener la rama actualizada
```bash
# para mike
git checkout mike
git fetch origin
git merge origin/main

# para javi
git checkout javi
git fetch origin
git merge origin/main
```
