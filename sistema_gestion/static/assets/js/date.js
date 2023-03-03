function addMonths(event) {
  if (event.keyCode === 13) { // check if the Enter key was pressed
    let inputDate = new Date(document.getElementById("datepicker-monthi").value); // get the input date
    let numberOfMonthsToAdd = parseInt(document.getElementById("txt_cuota").value); // set the number of months to add
    let newDate = new Date(inputDate.setMonth(inputDate.getMonth() + numberOfMonthsToAdd)); // add months to the date
    document.getElementById("dateInput").value = newDate.toISOString().slice(0,10); // set the input value to the new date
  }
}