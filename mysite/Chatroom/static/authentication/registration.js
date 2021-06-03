function keyupfunction(){
  if ($("#email").val().length > 0 &&
      $("#username").val().length > 0 &&
      $("#password1").val().length > 0 &&
      $("#password2").val().length > 0){
    $("#register").prop("disabled", false);
  }
  else{
    $("#register").prop("disabled", true);
  }
}

$(document).ready(function() {
  $("#register").prop("disabled", true);
})
