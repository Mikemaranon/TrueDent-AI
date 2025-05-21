function subirImagen() {
    const input = document.getElementById('inputImagen');
    const file = input.files[0];
    const resultadoDiv = document.getElementById('resultado');

    if (!file) {
        resultadoDiv.innerHTML = "Por favor selecciona una imagen.";
        return;
    }

    const formData = new FormData();
    formData.append('imagen', file);

    fetch('/detectar', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultadoDiv.innerHTML = `<span style="color:red;">${data.error}</span>`;
        } else {
            resultadoDiv.innerHTML = `<strong>Resultado:</strong> ${data.resultado}`;
        }
    })
    .catch(error => {
        resultadoDiv.innerHTML = `<span style="color:red;">Error al procesar: ${error}</span>`;
    });
}
