const od_add = document.getElementById("od_add");
const oi_add = document.getElementById("oi_add");
const all_input_grad = document.getElementsByClassName("input-grad-float");

od_add.addEventListener("change", (event) => {
    // (od_lejos_esf,od_lejos_cil,od_lejos_eje) => {
    const od_lejos_esf = document.getElementById("od_lejos_esf");
    const od_lejos_cil = document.getElementById("od_lejos_cil");
    const od_lejos_eje = document.getElementById("od_lejos_eje");
    const add = event.target.value;

    document.getElementById("od_cerca_esf").value = limitarDecimales((parseFloat(od_lejos_esf.value) + parseFloat(add)).toString());
    document.getElementById("od_cerca_cil").value = limitarDecimales(od_lejos_cil.value);
    document.getElementById("od_cerca_eje").value = od_lejos_eje.value;
})

oi_add.addEventListener("change", (event) => {
    const oi_lejos_esf = document.getElementById("oi_lejos_esf");
    const oi_lejos_cil = document.getElementById("oi_lejos_cil");
    const oi_lejos_eje = document.getElementById("oi_lejos_eje");
    const add = event.target.value

    document.getElementById("oi_cerca_esf").value = limitarDecimales((parseFloat(oi_lejos_esf.value) + parseFloat(add)).toString());
    document.getElementById("oi_cerca_cil").value = limitarDecimales(oi_lejos_cil.value);
    document.getElementById("oi_cerca_eje").value = oi_lejos_eje.value;
})

function limitarDecimales(valor) {
    let partes = valor.split('.');

    if (partes[0] === '') {
        partes[0] = '0'
    }
    
    // Si no hay parte decimal, añadir dos ceros
    if (partes.length === 1) {
        return `${partes[0]}.00`;
    }
    // Si hay una parte decimal, completar con un cero
    else if (partes[1].length === 1) {
        return `${partes[0]}.${partes[1]}0`;
    }
    // Si hay más de dos decimales, truncar a dos decimales
    else if (partes[1].length > 2) {
        return `${partes[0]}.${partes[1].slice(0, 2)}`;
    }
    // Si ya tiene dos decimales, no hacer nada
    return `${partes[0]}.${partes[1]}`;
}
