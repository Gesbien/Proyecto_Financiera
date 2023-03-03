var ids=["Inmobiliario","Garante","Vehiculo"];
var dropDown = document.getElementById("roleSel");

dropDown.onchange = function(){
    for(var x = 0; x <= 3; x++){
            document.getElementById(ids[x]).style.display="none"
            document.getElementById(this.value).style.display = "block";
    }
}