document.addEventListener('DOMContentLoaded', function() {
    const radioButtons = document.querySelectorAll('input[name="tipo_trabajo"]');
    
    // Ejecutar al cargar la página
    actualizarVistaTrabajo();
    
    // Agregar event listener a cada radio button
    radioButtons.forEach(radio => {
        radio.addEventListener('change', actualizarVistaTrabajo);
    });

    document.querySelectorAll(".input-grad").forEach(input => {
      input.addEventListener("focus", () => input.select());
    });
});

function actualizarVistaTrabajo() {
    // Actualiza la vista del trabajo dependiendo del tipo de trabajo seleccionado
    const tipoSeleccionado = document.querySelector('input[name="tipo_trabajo"]:checked').value;
    const grupoMonofocal = document.getElementById('grupo-anteojo-monofocal');
    const grupoUnico = document.getElementById('grupo-anteojo-unico');
    
    if (tipoSeleccionado === 'MONO') {
        // Mostrar grupo monofocal (lejos/cerca) y ocultar grupo único
        grupoMonofocal.style.display = 'block';
        grupoUnico.style.display = 'none';
    } else {
        // Ocultar grupo monofocal (lejos/cerca) y mostrar grupo único
        grupoMonofocal.style.display = 'none';
        grupoUnico.style.display = 'block';
    }
}