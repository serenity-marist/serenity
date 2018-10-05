//
//
// function callServer(){
//
//   var data = {
//     "email": "test123@marist.edu",
//     "password":"master97"
//     }
//
//   $.ajax({
//     url: "/webScraperTool",
//     success: function(body){
//       alert(true);
//
//     },
//     error: function(body){
//       alert(false);
//     }
//
//   });
//
//
//
//   $ajax({
//     type: "POST",
//     url: "/webScraperTool.html",
//     data: formData,
//     success: function(){
//                 var form = $('creds');
//
//
//              },
//     dataType: "json",
//     contentType: "application/json"
//   });
// }
//
//
//
// function showCredentials(){
//   var form = $('#creds');
//   $(form).submit(function(event) {
//     // Stop the browser from submitting the form.
//     event.preventDefault();
//     var formData = $(form).serialize();
//
//
//     alert(formData);
//     // Submit the form using AJAX.
//     $.ajax({
//       type: 'POST',
//       url: $(form).attr('action'),
//       data: formData
//     });
//
//   )};
// }




$(function() {
    $('#submitBtn').click(function() {
        $.ajax({
            url: '/webScraperTool',
            data: $('#creds').serialize(),
            dataType: "text",
            type: 'POST',
            success: function(body){
                var parse = JSON.parse(body);
                console.log(parse);
            }
        });
    });
});







//
// $(function() {
//   var form = $('#creds');
//   $(form).submit(function(event) {
//   // Stop the browser from submitting the form.
//   event.preventDefault();
//   var formData = $(form).serialize();
//
//   alert(formData);
//   // Submit the form using AJAX.
//   $.ajax({
//     type: 'POST',
//     url: $(form).attr('action'),
//     data: formData
//   })
//
// });
