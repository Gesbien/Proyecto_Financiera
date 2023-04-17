var dropdown = document.getElementById("typeSaldo");

function suma(a,b,c){
    var suma = a - (-b);
    var resultado = suma/c
    return resultado;
}

dropdown.onchange=  function() {
    var monto = document.getElementById("txt_monto").value;
    var tasa =  document.getElementById("txt_tasa").value;
    var num_cuota =  document.getElementById("txt_cuota").value;
    var monto_interes = (monto*(tasa/100)*num_cuota);
    var num_suma = 0;
    var cuota = 0;

    if(this.value === 'Insoluto'){
        var valor = (monto * (tasa/100)) / (1 - (1 + (tasa/100)) ** (-num_cuota))
        cuota = valor
    } else if(this.value === 'Absoluto'){
        num_suma = suma(monto,monto_interes,num_cuota);
        cuota = num_suma ;
    }else{
        cuota = monto_interes/num_cuota;
    }
    document.getElementById("txt_valor_cuota").value = cuota.toFixed(2);
};