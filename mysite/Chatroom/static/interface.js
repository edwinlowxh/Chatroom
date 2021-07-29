$(document).ready(()=> {
  //Get the chatroom name
  var groupname = $("#interface-container .nav-link").html();
  var group_id = $("#interface-container .nav-link").attr("group_id");
  const user_id = $("#user_id").html();
  var first_name = $("#first_name").html().slice(1, -1); //Slice to remove inverted commas

  //Create socket
  var chatSocket = createChatSocket(group_id);


  //Send request to receive message history
  if (group_id != undefined){
    receiveMessageHistory(group_id, user_id);
  }


  $("#interface-container .nav-link").on("click", e=>{
    //Close current socket;
    chatSocket.close();

    groupname = $(e.currentTarget).html();
    group_id = $(e.currentTarget).attr("group_id");

    //Create socket
    chatSocket = createChatSocket(group_id);

    // Clear message box
    $("#message-box").html("");

    //Send request to receive message history
    receiveMessageHistory(group_id, user_id);
  })

  //Receiving messages
  chatSocket.onmessage = e=>{
    const data = JSON.parse(e.data);

    //Return if receiving one's sent message
    if (data.user_id == user_id){
      return;
    }

    //Append message to chat container
    appendOtherMessage(data.first_name, data.time, data.message)
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
      var time = formatTime(new Date());

      //Send message
      const message = $("#message-input").val();
      chatSocket.send(JSON.stringify({
        'message': message,
        'user_id': user_id,
        'first_name': first_name,
        'time': time
      }));
      $("#message-input").val("");

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
      .then(response => {
        //Append message to chat container
        appendSelfMessage(first_name, time, message);
      })
      .catch(error => {
        alert(error.message);
      });

      a.stopImmediatePropagation();
    })
  })
});

///////////////////////////////////////////////Functions//////////////////////////////////

//Create chatSocket
function createChatSocket(group_id){
  var chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/Chatroom/'
    + group_id
    + '/'
  );

  return chatSocket;
}

// Receive messages
function receiveMessageHistory(group_id, user_id){
  fetch(window.location.pathname, {
    method: "POST",
    headers:{
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': $("input[name=csrfmiddlewaretoken]").val(),
    },
    body: JSON.stringify({"user_id": user_id, "function": "messageHistory", "group_id": group_id}),
  })
  .then((response) => {
    if (response.status == 200){
      return response.json();
    }
    else{
      //Throw error message
      throw Error("Could not load message history.");
    }
  })
  .then(response => {
    //Append message to chat container
    messages = response.messages

    for (i in messages){
      var oldDate;
      var time = formatTime(new Date(messages[i].time));
      if (time.slice(10) != oldDate){
        oldDate = time.slice(10);
        $("#message-box").append('<div class="new-date">' + oldDate + '</div>')
      }
      var message = messages[i].message;
      var sender_id = messages[i].sender__id;
      var sender_first_name = messages[i].sender__first_name;

      if (sender_id != user_id){
        appendOtherMessage(sender_first_name, time, message);
      }
      else{
        appendSelfMessage(sender_first_name, time, message);
      }
    }
  })
  .catch(error => {
    alert(error.message);
  });
}

// Append message(other)
function appendOtherMessage(first_name, time, message){
  $("#message-box").append('<div class="d-flex justify-content-start mb-4 message-container">\
                              <div class="circle" id="profile-pic">\
                                <span class="profile-pic-initial">' + first_name.slice(0, 1).toUpperCase() + '</span>\
                              </div>\
                              <div class="ml-3 message-container-message">' + message +
                                '<div class="d-flex justify-content-end message-information">\
                                  <span id=>' + time + '</span>\
                                  <span class="material-icons" id="delete-icon">delete</span>\
                                </div>\
                              </div>\
                            </div>');
  // Push scrollbar
  updateScroll();
}

// Append message(self)
function appendSelfMessage(first_name, time, message){
  //Append message to chat container
  $("#message-box").append('<div class="d-flex justify-content-end mb-4 message-container">\
                            <div class="mr-3 message-container-message">' + message +
                              '<div class="d-flex justify-content-start message-information">\
                                <span id=>' + time + '</span>\
                                <span class="material-icons" id="delete-icon">delete</span>\
                              </div>\
                            </div>\
                            <div class="circle" id="profile-pic">\
                              <span class="profile-pic-initial">' + first_name.slice(0, 1).toUpperCase() + '</span>\
                            </div>\
                          </div>');
  // Push scrollbar
  updateScroll();
}

//Format Time to string
function formatTime(date){
  if (date.getHours() >= 12){
    var meridiem = "PM";
  }
  else{
    var meridiem = "AM";
  }

  var hour = date.getHours() % 12;
  var minutes = date.getMinutes();
  var year = date.getFullYear();
  var _date = date.getDate();
  var month = date.getMonth();
  var today = new Date();

  if (_date === today.getDate() && month === today.getMonth() && year === today.getFullYear()){
    day = "Today";
  }
  else{
    day = String(_date).padStart(2, '0') + '/' + String(month).padStart(2, '0') + '/' + String(year).padStart(2, '0')
  }

  return String(hour).padStart(2, '0') + ':' + String(minutes).padStart(2, '0') + ' ' + meridiem + ", " + day;
}

//scrollbar to bottom
function updateScroll(){
    $("#message-box").scrollTop($("#message-box")[0].scrollHeight);
}
