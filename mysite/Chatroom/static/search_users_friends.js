$(document).ready(function() {
  var pathname = window.location.pathname;
  if (pathname == "/Chatroom/friends"){
    document.title = "Friends";
  }
  else{
    document.title = "Users";
  }
})
