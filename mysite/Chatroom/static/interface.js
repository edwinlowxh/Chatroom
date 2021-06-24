$(document).ready(()=> {
  $("#message-input").on("keyup", e=>{
    $("#send-button").on("click", a=>{
      if ($("#message-input").val().length == 0){
        alert("Please enter a message");
      }

      fetch(window.location.pathname, {
        method: "POST",
        headers:{
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': $("input[name=csrfmiddlewaretoken]").val(),
        },
        body: JSON.stringify({"function": "send message", "message": $("#message-input").val()}),
      })
      a.stopImmediatePropagation();
    })
  })
})
