$(document).ready(()=> {
  //Get the chatroom name
  var groupname = $("#interface-container .nav-link").html();
  var group_id = $("#interface-container .nav-link").attr("id");
  var user_id = $("#user_id").html();
  var first_name = $("#first_name").html().slice(1, -1); //Slice to remove inverted commas

  $("#interface-container .nav-link").on("click", e=>{
    groupname = $(e.currentTarget).html();
    group_id = $(e.currentTarget).attr("id");
  })

  //Create socket
  const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/Chatroom/'
    + group_id
    + '/'
  );

  //Receiving messages
  chatSocket.onmessage = e=>{
    const data = JSON.parse(e.data);

    //Return if receiving one's sent message
    if (data.user_id == user_id){
      return;
    }

    //Append message to chat container
    $("#message-box").append('<div class="d-flex justify-content-start mb-4 message-container">\
                                <div class="circle" id="profile-pic">\
                                  <span class="profile-pic-initial">' + data.first_name.slice(0, 1).toUpperCase() + '</span>\
                                </div>\
                                <div class="ml-3 message-container-message">' + data.message +
                                  '<div class="d-flex justify-content-end message-information">\
                                    <span id=>' + data.time + ', Today</span>\
                                    <span class="material-icons" id="delete-icon">delete</span>\
                                  </div>\
                                </div>\
                              </div>');
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

      //Get current date and time
      var currentdate = new Date();

      if (currentdate.getHours() >= 12){
        var meridiem = "PM";
      }
      else{
        var meridiem = "AM";
      }

      var hour = currentdate.getHours() % 12;
      var minutes = currentdate.getMinutes();

      //Send message
      const message = $("#message-input").val();
      chatSocket.send(JSON.stringify({
        'message': message,
        'user_id': user_id,
        'first_name': first_name,
        'time': hour.toString() + ':' + minutes.toString() + ' ' + meridiem
      }));
      $("#message-input").val("");

      //Append message to chat container
      $("#message-box").append('<div class="d-flex justify-content-end mb-4 message-container">\
                                <div class="mr-3 message-container-message">' + message +
                                  '<div class="d-flex justify-content-start message-information">\
                                    <span id=>' + hour + ':' + minutes + ' ' + meridiem + ', Today' + '</span>\
                                    <span class="material-icons" id="delete-icon">delete</span>\
                                  </div>\
                                </div>\
                                <div class="circle" id="profile-pic">\
                                  <span class="profile-pic-initial">' + first_name.slice(0, 1).toUpperCase() + '</span>\
                                </div>\
                              </div>');

      //Send request to store message in database
      fetch(window.location.pathname, {
        method: "POST",
        headers:{
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': $("input[name=csrfmiddlewaretoken]").val(),
        },
        body: JSON.stringify({"user_id": user_id, "function": "message", "group_id": group_id, "message": message}),
      })
      .then((response) => {
        if (response.status == 200){
          return response.json();
        }
        else{
          //Throw error message
          throw Error("Message failed to sent");
        }
      })
      // .then(response => {
      //
      // })
      .catch(error => {
        alert(error.message);
      });

      a.stopImmediatePropagation();
    })
  })
});
