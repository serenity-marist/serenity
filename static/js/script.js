

$(function() {

  $(".cont-btn").click(function(){
    $(".main-inside").hide();
    $(".log-seg").show();

  });
    $('#submitBtn').click(function() {

      $(".log-seg").hide();
      loaderShow();
      var submissionData = $('#creds').serialize()
        $.ajax({
            url: '/webScraperTool',
            data: submissionData,
            type: 'POST',
            success: function(body){
              var studInfo  = body[0];
              var totalCredComplete = body[1];
              var concentrationCredComplete = body[2]
              var pathwayCred = body[3]
              for(var i=0; i<totalCredComplete; i++){
                var  {title, completedCredits, totalCredits}  = totalCredComplete[i]
                // append totalCredits to the proper placement
              }
              for(var i=0; i<concentrationCredComplete; i++){
                var  {currCourseNum, currCourseTitle, currCreditValue}  = concentrationCredComplete[i]
              }
              for(var i=0; i<pathwayCred; i++){
                var  {pathwayNum, pathwayTitle, pathwayGrade}  = pathwayCred[i]
              }
              var {College, Major, Level, Student,ID,Classification} = studInfo;
                $(".main-content").empty();
                $(".main-content").append("<h1> Success </h1>")
                $(".main-content").append(`<p> ${Student}: ${ID}</p>`)
                $(".main-content").append(`${College} ${Major}: ${Level}`);
                window.location.href="/dashboard"



              //localStorage["college"] = body[0]["College"]
              // var {College, Major, Level, Student,ID,Classification} = body
              //   $(".main-content").empty();
              //   $(".main-content").append("<h1> Success </h1>")
              //   $(".main-content").append(`<p> ${Student}: ${ID}</p>`)
              //   $(".main-content").append(`${College} ${Major}: ${Level}`)
              //

            },
            error: function(body){
              $(".main-content").prepend(`<h1> There was an error logging you in! Please try again</h1>`);




            },
            complete: function(body){
              loaderDelete();


            }
        });
    });


function loaderShow(){
  $(".loader").show();

}

function loaderDelete(){
  $(".loader").hide();
}


});
