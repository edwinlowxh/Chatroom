$(document).ready(()=> {
  var pathname = window.location.pathname;
  if (pathname == "/Chatroom/friends"){
    document.title = "Friends";
    $(".user-details").append('<span id="email"></span><label>Email </label>');
  }
  else{
    document.title = "Users";
  }

  $(".list-group-item").on('click', e=> {
    if ($(e.currentTarget).attr("type") == "requests"){
      $("#profile-pic").empty();
      $("#name").empty();
      $("#username").empty();
      $("#email").empty();
      $("#send-message-add-friend").empty();
      return;
    }
    //alert($(e.currentTarget).attr("value"));
    var user_id = $(e.currentTarget).attr("value");

    //Send request to get user details
    fetch(window.location.pathname,{
      method: "POST",
      headers:{
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': $("input[name=csrfmiddlewaretoken]").val(),
      },
      body: JSON.stringify({"user_id": user_id, "function": "user info"}),
    })
    .then((response) => {
      if (response.status == 200){
        return response.json()
      }
      else{
        throw Error("Error retrieving user details.")
      }
    })
    .then(user => {
      $("#profile-pic").html(user.username.slice(0,1))
      $("#name").html(user.first_name + " " + user.last_name);
      $("#username").html(user.username);
      $("#email").html(user.email);
      if (pathname == "/Chatroom/search_users"){
        $("#send-message-add-friend").html('<div id="add-friend"><span class="material-icons" id="person-add-icon" onclick=>person_add</span><span>Add Friend</span></div>');
        $("#send-message-add-friend").attr("user_id", user.id);
      }
    })
    .catch(error => {
      alert(error.message);
    });
  });

  $("#send-message-add-friend").on('click', "#add-friend span", e=> {
    //User-id of target
    user_id = $(e.currentTarget).parent().parent().attr("user_id");

    //Send POST request to add friend
    fetch(window.location.pathname, {
      method: "POST",
      headers:{
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': $("input[name=csrfmiddlewaretoken]").val(),
      },
      body: JSON.stringify({"user_id": user_id, "function": "add friend"}),
    })
    .then((response) => {
      if (response.status == 200){
        return response.json();
      }
      else{
        //Throw error message
        throw Error("Error adding friend");
      }
    })
    .then(response => {
      if (response.success == "True"){
        alert(response.message);
      }
      else{
        throw Error(response.error);
      }
    })
    .catch(error => {
      alert(error.message);
    });
  });

  //Accept or reject friend request
  $(".list-group.friend-request").on("click", ".material-icons", e => {
    user_id = $(e.currentTarget).parent().attr("value");

    fetch(window.location.pathname, {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': $("input[name=csrfmiddlewaretoken]").val(),
      },
      body: JSON.stringify({"user_id": user_id, "choice": $(e.currentTarget).attr("id"), "function": "accept/reject"}),
    })
    .then(response => {
      if (response.status == 200){
        return response.json();
      }
      else{
        //Throw error message
        throw Error("Error accepting/rejecting friend request");
      }
    })
    .then(response => {
      $(e.currentTarget).parent().remove();
    })
    .catch(error => {
      alert(error);
    })
  });

})
