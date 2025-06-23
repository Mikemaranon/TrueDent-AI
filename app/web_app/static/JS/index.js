const formulario = document.getElementById('formulario');
const resultado_1 = document.getElementById('resultado_1');
const resultado_2 = document.getElementById('resultado_2');
const analyzeTeeth = document.getElementById('analyze-teeth');

formulario.addEventListener('submit', async function (e) {
    e.preventDefault();

    resultado_1.innerHTML = '';
    resultado_1.style.display = 'block';

    const formData = new FormData(this);

    try {
        const response = await send_API_request('POST', '/api/upload-image', formData);

        // Si la respuesta es directamente una imagen, usamos blob
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);

        // Renderizamos la imagen directamente
        render_image_from_blob(imageUrl);
        analyzeTeeth.style.display = 'block';

    } catch (err) {
        console.error(err);
        resultado_1.innerHTML = "<p class='text-danger'>❌ Error en la detección.</p>";
    }
});

function render_image_from_blob(imageUrl) {
    const resultado_1 = document.getElementById('resultado_1');
    resultado_1.innerHTML = ''; // Limpiamos contenido anterior

    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = 'Resultado';

    resultado_1.appendChild(img);
}

function render_teeth_analysis(analysis) {
    // renderizamos el análisis de los dientes
}