$(document).ready(function(){
    const tipo = document.getElementById('txt_tipo').value

    if (tipo == 'Vehiculo'){
        document.getElementById("Vehiculo").style.display = 'block'
        document.getElementById("Garantia").style.display = 'block'
    }else if(tipo == 'Inmobiliario'){
         document.getElementById("Inmobiliario").style.display = 'block'
         document.getElementById("Garantia").style.display = 'block'
    }else{
        document.getElementById("Garante").style.display = 'block'
    }
});