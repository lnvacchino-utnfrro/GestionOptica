const od_add = document.getElementById("od_add");
const oi_add = document.getElementById("oi_add");

od_add.addEventListener("change", (event) => {
    // (od_lejos_esf,od_lejos_cil,od_lejos_eje) => {
    const od_lejos_esf = document.getElementById("od_lejos_esf");
    const od_lejos_cil = document.getElementById("od_lejos_cil");
    const od_lejos_eje = document.getElementById("od_lejos_eje");
    const add = event.target.value

    document.getElementById("od_cerca_esf").value = parseFloat(od_lejos_esf.value) + parseFloat(add)
    document.getElementById("od_cerca_cil").value = parseFloat(od_lejos_cil.value)
    document.getElementById("od_cerca_eje").value = parseInt(od_lejos_eje.value)
});

oi_add.addEventListener("change", (event) => {
    const oi_lejos_esf = document.getElementById("oi_lejos_esf");
    const oi_lejos_cil = document.getElementById("oi_lejos_cil");
    const oi_lejos_eje = document.getElementById("oi_lejos_eje");
    const add = event.target.value

    document.getElementById("oi_cerca_esf").value = parseFloat(oi_lejos_esf.value) + parseFloat(add)
    document.getElementById("oi_cerca_cil").value = parseFloat(oi_lejos_cil.value)
    document.getElementById("oi_cerca_eje").value = parseInt(oi_lejos_eje.value)
});
