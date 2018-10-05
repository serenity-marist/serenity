



$(document).ready(function(){

  function callServer(){

    var data = {
      "email": "test123@marist.edu",
      "password":"master97"
      }

    $.ajax({
      url: "/test",
      type: "POST",
      data:"data",
      success: function(body){
        alert(body);

      },
      error: function(body){
        alert(false);
      }

    });
  }


  $(".circle-btn").click(function(){
    var name = $(".name-val").val();
    var pass = $(".pass-val").val();
    var data = {"email": name, "password": pass}

    $.ajax({
      url: "/webScraperTool",
      type: "POST",
      data: data,
      success: function(body){
        console.log(body);

      },
      error: function(body){
        alert(false)
      }
    });




  });

});
