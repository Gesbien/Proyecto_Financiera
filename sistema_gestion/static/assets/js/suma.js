var wage = document.getElementById("txt_monto_interes");
var total = document.getElementById("txt_monto_total");
wage.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {  //checks whether the pressed key is "Enter"
        suma(e);
    }
});
total.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {  //checks whether the pressed key is "Enter"
        autollenado();
    }
});

function suma(e){
    var monto_interes = document.getElementById("txt_monto_interes").value;
    var monto_capital = document.getElementById("txt_monto_capital").value;
    var monto_mora    = document.getElementById("txt_mora").value;
    var suma = monto_capital - (-monto_interes) - (-monto_mora);
    document.getElementById("txt_monto_total").value = suma.toFixed(2)
    document.getElementById("txt_total_pagado").value = suma.toFixed(2);
}

function autollenado(){
    var monto_total = document.getElementById("txt_monto_total").value;
    var monto_interes = document.getElementById("txt_monto_interes").value;
    var monto_capital = document.getElementById("txt_monto_capital").value;
    var monto_mora    = document.getElementById("txt_mora").value;

    var suma = monto_capital - (-monto_interes) - (-monto_mora);
    const id = $('#txt_prestamos');
    const input1 = $('#txt_mora');
    const input2 = $('#txt_monto_total');
    const input3 = $('#txt_monto_capital');
    const input4 = $('#txt_monto_interes');
    const input5 =  $('#txt_total_pagado')

    $.ajax({
      url: '/cobros/registrar/sumatoria/',
      data: {
        'id'   : id.val(),
          'total': monto_total,
          'interes': monto_interes,
          'capital': monto_capital,
          'mora': monto_mora,
      },
      dataType: 'json',
      success: function(data) {
        input1.val(data.input1_value);
        input2.val(data.input2_value);
        input3.val(data.input3_value);
        input4.val(data.input4_value);
        input5.val(data.input2_value);
      },
    });

}