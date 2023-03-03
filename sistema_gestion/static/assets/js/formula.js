var wage = document.getElementById("txt_cuota");
wage.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {  //checks whether the pressed key is "Enter"
        validate(e);
    }
});

function suma(a,b,c){
    var suma = a - (-b);
    var resultado = suma/c
    return resultado;
}
function validate(e) {
    var monto = document.getElementById("txt_monto").value;
    var tasa =  document.getElementById("txt_tasa").value;
    var num_cuota =  document.getElementById("txt_cuota").value;
    var monto_interes = (monto*(tasa/100)*num_cuota);
    var num_suma = suma(monto,monto_interes,num_cuota);
    var cuota = num_suma ;
    document.getElementById("txt_valor_cuota").value = cuota.toFixed(2);

}