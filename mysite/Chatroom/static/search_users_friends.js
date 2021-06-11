$(document).ready(()=> {
  var pathname = window.location.pathname;
  if (pathname == "/Chatroom/friends"){
    document.title = "Friends";
  }
  else{
    document.title = "Users";
  }

  $(".list-group-item").click(()=> {
    $(".user-profile").find("#name").html("{{Users.1.first_name}}")
    $(".user-profile").find("#name").load("search_users_friends.html");
  });
})
