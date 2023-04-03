var wage = document.getElementById("txt_mora");
wage.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {  //checks whether the pressed key is "Enter"
        suma(e);
    }
});
function suma(e){
    var monto_interes = document.getElementById("txt_monto_interes").value;
    var monto_capital = document.getElementById("txt_monto_capital").value;
    var monto_mora    = document.getElementById("txt_mora").value;
    var suma = monto_capital - (-monto_interes) - (-monto_mora);
    document.getElementById("txt_monto_total").value = suma.toFixed(2);
}
