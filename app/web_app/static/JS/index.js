const formulario = document.getElementById('formulario');
const resultadoDiv = document.getElementById('resultado');

formulario.addEventListener('submit', async function (e) {
    e.preventDefault();

    const resultadoDiv = document.getElementById('resultado');
    resultadoDiv.innerHTML = '';
    resultadoDiv.style.display = 'block';

    const formData = new FormData(this);

    try {
        const response = await send_API_request('POST', '/api/upload-image', formData);
        const data = await response.json();

        console.log(data);

        if (Array.isArray(data.imagenes)) {
            render_images(data);
        } else {
            resultadoDiv.innerHTML = "<p class='text-danger'>⚠️ No se recibio imagen de respuesta.</p>";
        }

    } catch (err) {
        console.error(err);
        resultadoDiv.innerHTML = "<p class='text-danger'>❌ Error en la detección.</p>";
    }
});

function render_images(data) {
    data.imagenes.forEach(imgObj => {
        const colDiv = document.createElement('div');
        colDiv.className = "col-md-4 text-center";

        const img = document.createElement('img');
        img.src = imgObj.image;
        img.alt = imgObj.name || "Imagen detectada";
        img.className = "img-fluid border rounded shadow";
        img.style.maxHeight = "300px";
        img.style.margin = "10px";

        const label = document.createElement('p');
        label.textContent = imgObj.name || "";
        label.className = "text-muted small";

        colDiv.appendChild(img);
        colDiv.appendChild(label);
        resultadoDiv.appendChild(colDiv);
    });
}
