

$(function() {
    $('#submitBtn').click(function() {
      var submissionData = $('#creds').serialize()
        $.ajax({
            url: '/webScraperTool',
            data: submissionData,
            type: 'POST',
            success: function(body){
              var parse = JSON.parse(body);
              var {College, Major, Level, Student,ID,Classification} = parse
                $(".main-content").empty();
                $(".main-content").append("<h1> Success </h1>")
                $(".main-content").append(`<p> ${Student}: ${ID}</p>`)
                $(".main-content").append(`${College} ${Major}: ${Level}`)


            },
            error: function(body){
              $(".main-content").prepend(`<h1> There was an error logging you in! Please try again</h1>`);




            }
        });
    });
});
