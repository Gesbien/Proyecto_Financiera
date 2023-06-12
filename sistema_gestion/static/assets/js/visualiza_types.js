var tips=["Garantia","Garante"];
var dropDown = document.getElementById("roleSel1");

dropDown.onchange = function(){
    for(var x = 0; x <= 4; x++){
            document.getElementById(tips[x]).style.display="none"
            document.getElementById(this.value).style.display = "block";
    }
}