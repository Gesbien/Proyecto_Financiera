function addMonths(event) {
  if (event.keyCode === 13) { // check if the Enter key was pressed
    var fecha = document.getElementById("datepicker-monthi").value;
    var partes = fecha.split("/");
    var fechaJS = new Date(partes[2], partes[1] - 1, partes[0]);
    let mesesAumentar = parseInt(document.getElementById("txt_cuota").value); // set the number of months to add
    fechaJS.setMonth(fechaJS.getMonth() + mesesAumentar);
    var dia = fechaJS.getDate();
    var mes = fechaJS.getMonth() + 1;
    var anio = fechaJS.getFullYear();
    var nuevaFecha = dia + "/" + mes + "/" + anio;
    document.getElementById("dateInput").value = nuevaFecha // set the input value to the new date
  }
}