$(document).ready(()=> {
  //Get the chatroom name
  var groupname;
  $("#interface-container .nav-link").on("click", e=>{
    groupname = $(e.currentTarget).html();
  })

  //Create socket
  const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/Chatroom/'
    + groupname
    + '/'
  );

  //Receiving messages
  chatSocket.onmessage = e=>{
    const data = JSON.parse(e.data);
    $("#message-box").append(data.message);
  }

  //Close socket
  chatSocket.onclose = e=>{
    console.error("Chat socket closed unexpectedly");
  };


  $("#message-input").on("keyup", e=>{
    $("#send-button").on("click", a=>{
      if ($("#message-input").val().length == 0){
        alert("Please enter a message");
        return;
      }

      //Send message
      const message = $("#message-input").val();
      chatSocket.send(JSON.stringify({
        'message': message
      }));
      $("#message-input").val("");
      a.stopImmediatePropagation();
    })
  })
})
