

$(function() {


  $(".cont-btn").click(function(){
    $(".main-inside").hide();
    $(".log-seg").show();

  });

  $("#submitBtn").click(function(){
   $(".log-seg").hide();
     loaderShow("Validating credentials...");
     var submissionData = $('#creds').serialize();
     $.ajax({
       url: '/login',
       data:submissionData,
       type: 'POST',
       success: function(body){
         loaderDelete();
          scrapeData();
       },
       error: function(body){
         loaderDelete();
         $(".log-seg").show();
         $(".main-content").prepend(`<h1> Please provide your correct Marist login credentials.</h1>`);


       },
       complete: function(){


       }
     })

  })





function loaderShow(text){
  $(".load-p").text(text)
  $(".loader").show();

}

function loaderDelete(){
  $(".loader").hide();
}


function scrapeData(){

  $(".log-seg").hide();
  loaderShow("Loading dashboard...");
    $.ajax({
        url: '/webScraperTool',
        type: 'POST',
        success: function(body){

          console.log(body);
          $(".main-content-wrapper").hide();
          $(".dashboard").show();
        //  $(".main-content").empty();

          var studInfo  = body[0];
          var totalCredComplete = body[1];
          var concentrationCredComplete = body[2]
          var pathwayCred = body[3]
          totalCredComplete.forEach(function(val){
            var {completedCredits, title, totalNeeded } = val;
            console.log(completedCredits);
            console.log(title);
            console.log(totalNeeded);
            $(".main-content").append(`<p> Completed Credits: in ${title}: ${completedCredits} </p> `)
            $(".main-content").append(`<p> Total Credits Needed: ${totalNeeded} </p>`)

          });
          for(var i=0; i<totalCredComplete; i++){
            console.log("test");
            // var  {title, completedCredits, totalCredits}  = totalCredComplete[i]
            // console.log(title);

            // append totalCredits to the proper placement
          }
          // for(var i=0; i<concentrationCredComplete; i++){
          //   var  {currCourseNum, currCourseTitle, currCreditValue}  = concentrationCredComplete[i]
          // }
          concentrationCredComplete.forEach(function(val){
            var {currCourseNum, currCourseTitle, currCreditValue} = val
            console.log(currCourseNum);
            console.log(currCourseTitle);
            console.log(currCreditValue);
            $(".main-content").append(`<p> Course Name: ${currCourseTitle} </p>`)
            $(".main-content").append(`<p> Course Value: ${currCreditValue}  </p>`)
          });
          for(var i=0; i<pathwayCred; i++){
            var  {pathwayNum, pathwayTitle, pathwayGrade}  = pathwayCred[i]
          }
          var {College, Major, Level, Student,ID,Classification} = studInfo;
            $(".main-content").append("<h1> Success </h1>")
            $(".main-content").append(`<p> ${Student}: ${ID}</p>`)
            $(".main-content").append(`${College} ${Major}: ${Level}`)

        },
        error: function(body){
          $(".main-content").prepend(`<h1> There was an error scraping your data, please log in`);
        },
        complete: function(body){
          loaderDelete();


        }
    });
}

});
