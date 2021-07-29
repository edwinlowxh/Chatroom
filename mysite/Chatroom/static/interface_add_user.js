$(document).ready(() =>{
  var group_id;
  // Modal
  $(".more-icon.material-icons").on("click", e=>{
    $("#groupSettings")[0].style.display = "block";
    group_id = $(e.currentTarget).attr("group_id");

    //Send request to Load users that are not in group yet
    fetch(window.location.pathname, {
      method: "POST",
      headers:{
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': $("input[name=csrfmiddlewaretoken]").val(),
      },
      body: JSON.stringify({"function": "users_not_added", "group_id": group_id}),
    })
    .then((response) => {
      if (response.status == 200){
        return response.json();
      }
      else{
        //Throw error message
        throw Error("Unable to retrieve users");
      }
    })
    .then(response => {
      //Append users to select container
      var new_users = response["new_users"]
      for (let i = 0;i < new_users.length; i++){
        $("#users_to_add").append("<option value=" + new_users[i].id  + ">" + new_users[i].username +"</option>")
      }
    })
    .catch(error => {
      alert(error.message);
    });
  })

  //Add users
  $(".modal #add").on("click", e=>{
    var users = ($("#users_to_add").val() || []);

    if (users.length === 0){
      alert("No user selected");
      $("#groupSettings .close").click();
    }
    else{
      //Send request to add selected users
      fetch(window.location.pathname, {
        method: "POST",
        headers:{
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': $("input[name=csrfmiddlewaretoken]").val(),
        },
        body: JSON.stringify({"function": "add_users", "group_id": group_id, "users": users}),
      })
      .then((response) => {
        if (response.status == 200){
          return response.json();
        }
        else{
          //Throw error message
          throw Error("Unable to add users");
        }
      })
      .then(response => {
        $("#groupSettings .close").click();
      })
      .catch(error => {
        alert(error.message);
      });
    }
  });

  // Close modal
  $("#groupSettings .close").on("click", e=>{
    $("#groupSettings")[0].style.display ="none";

    // Clear select container
    $("#users_to_add").html("");
  })
});
