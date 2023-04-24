function enviarDatos() {
    var fecha = document.getElementById("datepicker_fecha").value;
    var id_prestamo = document.getElementById("txt_prestamo").value;
    var url = "/cobros/registrar/{{"+ id_prestamo +"}}/ {{ "+ fecha + " }}";
    window.location = url;
}

$(document).ready(function() {
  const dateInput = $('#datepicker_fecha');
  const id = $('#txt_prestamos');
  const input1 = $('#txt_mora');
  const input2 = $('#txt_monto_total');
  const input3 = $('#txt_monto_capital');
  const input4 = $('#txt_monto_interes');
  const input5 =  $('#txt_total_pagado')

  dateInput.on('change', function() {
    const selectedDate = dateInput.val();
    const id_prestamo = id.val()
    $.ajax({
      url: '/cobros/registrar/actualizar/',
      data: {
        'fecha': selectedDate,
        'id'   : id_prestamo
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
  });
});