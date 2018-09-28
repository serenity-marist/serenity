

function callServer(){

  var data = {
    "email": "test123@marist.edu",
    "password":"master97"
    }

  $.ajax({
    url: "/webScraperTool",
    success: function(body){
      alert(true);

    },
    error: function(body){
      alert(false);
    }

  });
}
