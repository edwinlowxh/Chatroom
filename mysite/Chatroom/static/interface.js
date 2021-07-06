$(document).ready(()=> {
  //Get the chatroom name
  var groupname;
  var user_id = $("#user_id").html();
  var first_name = $("#first_name").html().slice(1, -1); //Slice to remove inverted commas

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
    if (data.user_id != user_id){
      $("#message-box").append(data.message);
    }
  }

  //Close socket
  chatSocket.onclose = e=>{
    console.error("Chat socket closed unexpectedly");
  };

  //Listen for enter key press
  $("#message-input").on("keydown", e=>{
    if (e.keyCode === 13){
      e.preventDefault();
      $("#send-button").trigger("click");
    }
  })

  $("#message-input").on("keyup", e=>{
    $("#send-button").on("click", a=>{
      if ($("#message-input").val().length == 0){
        alert("Please enter a message");
        return;
      }

      //Send message
      const message = $("#message-input").val();
      chatSocket.send(JSON.stringify({
        'message': message,
        'user_id': user_id,
        'first_name': first_name
      }));
      $("#message-input").val("");

      //Append message to chat container
      $("#message-box").append('<div class="d-flex justify-content-start mb-4 message-container">\
                                  <div class="circle" id="profile-pic">\
                                    <span class="profile-pic-initial">A</span>\
                                  </div>\
                                  <div class="ml-3 message-container-message">' + message +
                                    '<div class="d-flex justify-content-end message-information">\
                                      <span id=>9:12 AM, Today</span>\
                                      <span class="material-icons" id="delete-icon">delete</span>\
                                    </div>\
                                  </div>\
                                </div>');
      a.stopImmediatePropagation();
    })
  })
})
