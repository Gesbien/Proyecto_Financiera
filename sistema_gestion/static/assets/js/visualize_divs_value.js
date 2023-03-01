$(document).ready(function(){
    const tipo = document.getElementById('txt_tipo').value

    if (tipo == 'Vehiculo'){
        document.getElementById("Vehiculo").style.display = 'block'
    }else{
        document.getElementById("Inmobiliario").style.display = 'block'
    }
});