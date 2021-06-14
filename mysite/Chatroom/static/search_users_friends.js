$(document).ready(()=> {
  var pathname = window.location.pathname;
  if (pathname == "/Chatroom/friends"){
    document.title = "Friends";
  }
  else{
    document.title = "Users";
  }

  $(".list-group-item").click(e=> {
    alert($(e.currentTarget).attr("value"));
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
    .then(response =>{
      alert(response.json())
    });

  });
})
