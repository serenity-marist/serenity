

$(function() {

  if(isLogged == "True"){
    $(".main-inside").hide();
    logIn();
  //  scrapeData();


  }
  /************* SINGLE PAGE APPLICATION MARKUP **************/
  $(".cont-btn").click(function(){
    $(".main-inside").hide();
    $(".log-seg").show();
  });

  $("#submitBtn").click(function(){

    if($('input[name="email"]').val() == "" || $('input[name="password"]').val() == ""     ){
     //append message here

    } else{
      logIn();
    }
  })


  $(".print-btn").click(function(){
    $(".dash.main.content").printThis();
  })

  function loaderShow(text){
    $(".load-p").text(text)
    $(".loader").show();

  }

  function loaderDelete(){
    $(".loader").hide();
  }

  function logIn(){
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
          $(".main-content").prepend(`<h1> ERROR: Username or Password was incoorect. Please try again..</h1>`);
        },
        complete: function(){
        }
      })

  }
  /************* END SINGLE PAGE MARKUP **************/

  /************* FUNCTION TO PARSE DATA FROM PYTHON SCRAPE INTO HTML ~VISUALS~ **************/
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
        var currClasses = body[2]
        var pathwayCred = body[3]

        /************* POPULATE DEGREE PROGRESS DESCRIPTION **************/
        var {completedCredits, title, totalNeeded } = totalCredComplete[0];
        $("#completedCredits").text(completedCredits);
        $("#creditsLeft").text(totalNeeded - completedCredits);
        /************* END POPULAT DEGREE PROGRESS DESCRIPTION **************/
      //  $(".description").text(`Completed Credits: ${completedCredits} `)
          // totalCredComplete.forEach(function(val){
          //
          //   var {completedCredits, title, totalNeeded } = val;
          //   console.log(val);
          //   $(".main-content").append(`<div class='description'> Completed Credits: in ${title}: ${completedCredits} </p> `)
          //   $(".main-content").append(`<p> Total Credits Needed: ${totalNeeded} </p>`)
          //
          // });
        for(var i=0; i<totalCredComplete; i++){
          // console.log("test");
        }
        /************* POPULATE AND NUMERATE TOTAL CURRENT CLASSES **************/
        currClasses.forEach(function(val){
          var {currCourseNum, currCourseTitle, currCreditValue} = val
          $('#currClassTable').append(`<tr><td>${currCourseNum}</td><td>${currCourseTitle}</td><td>${currCreditValue}</td></tr>`);
        });

        $('.detail.classes').append(currClasses.length);
        /************* END FOR CURRENT CLASSES **************/
        for(var i=0; i<pathwayCred; i++){
          var  {pathwayNum, pathwayTitle, pathwayGrade}  = pathwayCred[i]
        }
        /************* POPULATE STUDENT VIEW TABLE AJAX **************/
        var {College, Concentration, Major, Level, Student, ID, Classification, Advisor, Minor} = studInfo;
        $("#studentName").text(Student);

        var nameArray = Student.split(",");
        $("#fname").text(nameArray[nameArray.length-1].trim());


        $("#id").text(ID);
        $("#year").text(Classification);
        $("#majors").text(Major);
        $("#advisor").text(Advisor);
        $("#minors").text(Minor);
        $("#concentration").text(Concentration);
        $("#gpa").text(studInfo["Overall GPA"]);
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
