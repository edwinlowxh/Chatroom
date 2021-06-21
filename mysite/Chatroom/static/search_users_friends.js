$(document).ready(()=> {
  var pathname = window.location.pathname;
  if (pathname == "/Chatroom/friends"){
    document.title = "Friends";
    $(".user-details").append('<span id="email"></span><label>Email </label>');
    $("#send-message-add-friend").append('<div id="send-message"><span class="material-icons" id="send-message-icon">chat</span><span>Send Message</span></div>');
  }
  else{
    document.title = "Users";
    $("#send-message-add-friend").append('<div id="add-friend"><span class="material-icons" id="person-add-icon">person_add</span><span>Add Friend</span></div>');
  }

  $(".list-group-item").click(e=> {
    if ($(e.currentTarget).attr("type") == "requests"){
      $("#profile-pic").empty();
      $("#name").empty();
      $("#username").empty();
      $("#email").empty();
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
      body: JSON.stringify({"user_id": user_id}),
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
    })
    .catch(error => {
      alert(error.message);
    });
  });

  //Add friend
})
