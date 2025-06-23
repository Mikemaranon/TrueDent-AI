const formulario = document.getElementById('formulario');
const resultadoDiv = document.getElementById('resultado');
const analyzeTeeth = document.getElementById('analyze-teeth');

formulario.addEventListener('submit', async function (e) {
    e.preventDefault();

    const resultadoDiv = document.getElementById('resultado');
    resultadoDiv.innerHTML = '';
    resultadoDiv.style.display = 'block';

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
        resultadoDiv.innerHTML = "<p class='text-danger'>❌ Error en la detección.</p>";
    }
});

function render_image_from_blob(imageUrl) {
    const resultadoDiv = document.getElementById('resultado');
    resultadoDiv.innerHTML = ''; // Limpiamos contenido anterior

    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = 'Resultado';

    resultadoDiv.appendChild(img);
}

