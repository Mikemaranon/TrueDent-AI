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
document.addEventListener('click', function (e) {
    if (e.target.tagName === 'IMG' && !e.target.classList.contains('logo')) {
        const src = e.target.getAttribute('src');
        const modalImage = document.getElementById('modalImage');
        modalImage.src = src;

        const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
        imageModal.show();
    }
});

analyzeTeeth.addEventListener('click', async function () {
    resultado_2.innerHTML = ''; // Limpiamos contenido anterior
    resultado_2.style.display = 'block';

    try {
        const response = await send_API_request('GET', '/api/detect');
        const data = await response.json();

        if (!Array.isArray(data)) {
            throw new Error('Respuesta inesperada del servidor');   
        }

        console.log(data);

        // Filtramos las predicciones con caries
        const cariousTeeth = data.filter(item => item.predicted_class === 0);

        if (cariousTeeth.length === 0) {
            resultado_2.innerHTML = "<p>No se detectaron dientes con caries.</p>";
            return;
        }

        // Mostramos cada imagen con caries
        cariousTeeth.forEach(item => {
            render_teeth(item);
        });

    } catch (err) {
        console.error(err);
        resultado_2.innerHTML = "<p class='text-danger'>❌ Error al analizar los dientes.</p>";
    }
});

function render_image_from_blob(imageUrl) {
    resultado_1.innerHTML = ''; // Limpiamos contenido anterior

    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = 'Resultado';

    resultado_1.appendChild(img);
}

async function render_teeth(item) {

    const body = {
        image_name: item.image_name
    }

    const image = await send_API_request('POST', `/api/get-image`, body);
    const blob = await image.blob();
    const imageUrl = URL.createObjectURL(blob);

    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = `Diente con caries`;
    img.style.maxWidth = "150px";
    img.style.margin = "10px";

    const info = document.createElement('p');

    let confidence = Math.abs(item.confidence - 0.5) / 0.5;
    info.textContent = `Confianza: ${(confidence * 100).toFixed(1)}%`;

    const label = document.createElement('p');
    label.textContent = "🦷 ¡Caries detectada!";
    label.style.color = "red";
    label.style.fontWeight = "bold";

    const container = document.createElement('div');
    container.style.display = "inline-block";
    container.style.textAlign = "center";
    container.style.margin = "10px";
    container.appendChild(img);
    container.appendChild(label);
    container.appendChild(info);

    resultado_2.appendChild(container);
}