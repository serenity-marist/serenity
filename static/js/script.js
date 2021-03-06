/**
  * Gets a value from the server, checking if the user has an active session. If the user is logged in on the application end,
  then we make an AJAX request to place the session credentials back into degree works.
  *
*/
$(function() {
  if(isLogged == "True"){
    $(".main-inside").hide();
    logIn();
  }
  /************* SINGLE PAGE APPLICATION MARKUP **************/


  function loaderShow(text){
    $(".load-p").text(text)
    $(".loader").show();
  }

  function loaderDelete(){
    $(".loader").hide();
  }
  function logIn(){
    $(".msg-sect").empty();
    $(".log-seg").hide();
      loaderShow("Validating credentials...");
        var submissionData =  {
          "password": $("input[name=password]").val(),
          "email": $("input[name=email]").val()
        }
      $.ajax({
        url: '/login',
        data:submissionData,
        type: 'POST',
        success: function(body){
          if(body == false){
            loaderDelete();
            $(".log-seg").show();
            $(".msg-sect").html(`<h1> There was an error logging you in!</h1>`);
          }
          else if(body.length !== 0){
            loaderDelete();
            google.charts.load("current", {packages:["corechart"]});
            $(".main-content-wrapper").hide();
            $(".dashboard").show();
            var studInfo  = body[0];
            var totalCredComplete = body[1];
            var currClasses = body[2]
              //Exception handling for pathway in case does not exist
            var ifPathway = true;
            if(body[3] == undefined) {
              var pathwayArray = [];
            }
            if(ifPathway == true) {
              var pathwayArray = body[3];
            }
            /************* POPULATE DEGREE PROGRESS DESCRIPTION **************/
            var {completedCredits, title, totalNeeded } = totalCredComplete[0];
            $("#completedCredits").text(completedCredits);
            var requiredTotal = totalNeeded - completedCredits;

            if(requiredTotal < 0) {
              requiredTotal = 0;
            }

            //exception for if required is negative
            if(requiredTotal == 0) {
              $("#creditsLeft").text("All done!");
            } else {
              $("#creditsLeft").text(requiredTotal);
            }

            /************* CREATE DEGREE PROGRESS DONUT CHART. **************/
            google.charts.setOnLoadCallback(drawDegreeChart);
            //Must parse completecredits and required because if not it displays out as a percentage of a
            //bigger value, making it 1% of the total graph?
            var ccOverall = parseInt(completedCredits);
            var rOverall = parseInt(requiredTotal);
            function drawDegreeChart() {
              var data = google.visualization.arrayToDataTable([
                ['Class', 'Credits'],
                ['Completed',     ccOverall],
                ['Required',      rOverall]
              ]);
              var options = {
                pieHole: 0.5,
                pieSliceTextStyle: {
                  color: 'black',
                },
                legend: 'none'
              };
              var chart = new google.visualization.PieChart(document.getElementById('donutchart'));
              chart.draw(data, options);
            } /************* END CREATE DEGREE PROGRESS DONUT CHART. **************/

            /************* END POPULAT DEGREE PROGRESS DESCRIPTION **************/

            /************* DATA FOR BOTTOM BUTTON PARSING **************/
            var concentrationData = [];
            var majorData = [];
            var minorData = [];
            var totalPathwayCredits = 0;

            for (var i = 0; i < totalCredComplete.length; i++) { //loop to get all objects that are concentration
              if(totalCredComplete[i].title.split('Concentration ')[1]) {
                concentrationData.push(totalCredComplete[i]);
              }
            }//concentrationData

            for (var i = 0; i < totalCredComplete.length; i++) { //loop to get all objects that are majors
              if(totalCredComplete[i].title.split('Major ')[1]) {
                majorData.push(totalCredComplete[i]);
              }
            }//majorData

            for (var i = 0; i < totalCredComplete.length; i++) { //loop to get all objects that are minors
              if(totalCredComplete[i].title.split('Minor ')[1]) {
                minorData.push(totalCredComplete[i]);
              }
            }//minorData

            pathwayArray.forEach(function(val){ //gets total credits completed for your pathway
              var {pathwayCred, pathwayNum, pathwayTitle, pathwayYear} = val;
              totalPathwayCredits += pathwayCred;
              $('#pathwayClassTable').append(`<tr><td>${pathwayNum}</td><td>${pathwayTitle}</td><td>${pathwayYear}</td></tr>`);
            }); //result: totalPathwayCredits = amount of total creds from pathway completed

            $('.detail.pathway').append(totalPathwayCredits);
            //need to find a way to make max 3
            concentrationData.forEach(function(val){ //gets total credits completed for your pathway
              var {completedCredits, totalNeeded, title} = val;

              google.charts.setOnLoadCallback(drawDegreeChart);
              //Must parse completecredits and required because if not it displays out as a percentage of a
              //bigger value, making it 1% of the total graph?
              var cc = parseInt(completedCredits);
              var t = parseInt(totalNeeded);
              var r = t - cc;

              if(r < 0) {
                r = 0;
              }

              function drawDegreeChart() {
                var data = google.visualization.arrayToDataTable([
                  ['Class', 'Credits'],
                  ['Completed',     cc],
                  ['Required',      r]
                ]);
                var options = {
                  pieHole: 0.5,
                  pieSliceTextStyle: {
                    color: 'black',
                  },
                  legend: 'none',
                  title: 'Progress of: ' + title
                };
                var chart = new google.visualization.PieChart(document.getElementById('majorDiv'));
                chart.draw(data, options);
              }
            });

            majorData.forEach(function(val){ //gets total credits completed for your pathway
              var {completedCredits, totalNeeded, title} = val;

              google.charts.setOnLoadCallback(drawDegreeChart);
              //Must parse completecredits and required because if not it displays out as a percentage of a
              //bigger value, making it 1% of the total graph?
              var cc = parseInt(completedCredits);
              var t = parseInt(totalNeeded);
              var r = t - cc;

              if(r < 0) {
                r = 0;
              }

              function drawDegreeChart() {
                var data = google.visualization.arrayToDataTable([
                  ['Class', 'Credits'],
                  ['Completed',     cc],
                  ['Required',      r]
                ]);
                var options = {
                  pieHole: 0.5,
                  pieSliceTextStyle: {
                    color: 'black',
                  },
                  legend: 'none',
                  title: 'Progress of: ' + title
                };
                var chart = new google.visualization.PieChart(document.getElementById('majorDiv'));
                chart.draw(data, options);
              }
            });

            minorData.forEach(function(val){ //gets total credits completed for your pathway
              var {completedCredits, totalNeeded, title} = val;

              google.charts.setOnLoadCallback(drawDegreeChart);
              var cc = parseInt(completedCredits);
              var t = parseInt(totalNeeded);
              var r = t - cc;

              if(r < 0) {
                r = 0;
              }

              function drawDegreeChart() {
                var data = google.visualization.arrayToDataTable([
                  ['Class', 'Credits'],
                  ['Completed',     cc],
                  ['Required',      r]
                ]);
                var options = {
                  pieHole: 0.5,
                  pieSliceTextStyle: {
                    color: 'black',
                  },
                  legend: 'none',
                  title: 'Progress of: ' + title
                };
                var chart = new google.visualization.PieChart(document.getElementById('minorDiv'));
                chart.draw(data, options);
              }
            });
            /************* END DATA FOR BOTTOM BUTTON PARSING **************/
            /************* POPULATE AND NUMERATE TOTAL CURRENT CLASSES **************/
            currClasses.forEach(function(val){
              var {currCourseNum, currCourseTitle, currCreditValue} = val
              $('#currClassTable').append(`<tr><td>${currCourseNum}</td><td>${currCourseTitle}</td><td>${currCreditValue}</td></tr>`);
            });

            $('.detail.classes').append(currClasses.length);
            /************* END FOR CURRENT CLASSES **************/
            /************* POPULATE STUDENT VIEW TABLE AJAX **************/
            var {College, Concentration, Major, Level, Student, ID, Classification, Advisor, Minor} = studInfo;

            // Before population of student data, we have a function for editing advisors names.

            // This function will take the original string of adviors full names and return
            // them in a readable format by simply listing their last names.

            //This function is first going to iterate through the string of advisors,
            //and extract their last names (which have a comma)
            //as its the only to destinguish within the string the different advisors.
            //It then formats the names in a readable manner, and returns a single string,
            //of advisors as "Professor X & Professor Y" as opposed to
            //"LastName, FirstName MiddleInitial LastName, FirstName MiddleInitial"
            function getSeparateNames(advisorsNames){
              var myAdvisors = advisorsNames;

              //Regex matches the name with the comma after it (the last name)
              var regex1 = /[a-zA-Z-]+\,/g;

              var match;
              var lastNames = [];

              while( (match = regex1.exec(myAdvisors)) != null){
              	lastNames.push(match[0]);
              }

              //Iterate through lastNames and take out the comma
              for(var i = 0; i < lastNames.length; i++){
                var commaIndex = lastNames[i].indexOf(',');
                lastNames[i] = lastNames[i].slice(0, commaIndex);
              }

              var editedNames = '';

              for(var i = 0; i < lastNames.length; i++){
                editedNames = editedNames + 'Professor ' + lastNames[i];

                if(i != lastNames.length-1){
                  editedNames = editedNames + ' & '
                }
              }
              return editedNames;
            }
            $("#studentName").text(Student);

            var nameArray = Student.split(",");
            $("#fname").text(nameArray[nameArray.length-1].trim());


            $("#id").text(ID);
            $("#year").text(Classification);
            $("#majors").text(Major);
            $("#advisor").text(getSeparateNames(Advisor));
            $("#minors").text(Minor);
            $("#concentration").text(Concentration);
            $("#gpa").text(studInfo["Overall GPA"]);
            /************* END OF POPULATE STUDENT VIEW TABLE AJAX **************/
            /************* CREATE DEGREE PROGRESS DONUT CHART. **************/
          }

        },
        error: function(body){
          loaderDelete();
          $(".log-seg").show();
          $(".msg-sect").html(`<h1> There was an error logging you in!</h1>`);
        },
        complete: function(){
        }
      })

  }

  function allHide() {
    $('#pathwayDiv').hide();
    $('#majorDiv').hide();
    $('#minorDiv').hide();
  }


  /** Serenity application event listeners
    * Each of the methods below are all event listeners for user actions in the application.
    *
  **/

  $('#pathwayBtn').click(function() {
    allHide();
    $('#pathwayDiv').show();
  });

  $('#majorBtn').click(function() {
    allHide();
    $('#majorDiv').show();
  });

  $('#minorBtn').click(function() {
    allHide();
    $('#minorDiv').show();
  });

  $('#dpMenu').on('click', function() {
    $(window).scrollTop($('.degreeProgress').offset().top);
    $(this).css('color', '#ffd800');
    $('#siMenu').css('color', "#373737");
    $('#pMenu').css('color', "#373737");
    $('#mmMenu').css('color', "#373737");
    $('#ccMenu').css('color', "#373737");
  });

  $('#siMenu').on('click', function() {
    $(window).scrollTop($('.dash.student.information').offset().top);
    $(this).css('color', '#ffd800');
    $('#dpMenu').css('color', "#373737");
    $('#pMenu').css('color', "#373737");
    $('#mmMenu').css('color', "#373737");
    $('#ccMenu').css('color', "#373737");
  });

  $('#ccMenu').on('click', function() {
    $(window).scrollTop($('.dash.current.classes').offset().top);
    $(this).css('color', '#ffd800');
    $('#dpMenu').css('color', "#373737");
    $('#pMenu').css('color', "#373737");
    $('#mmMenu').css('color', "#373737");
    $('#siMenu').css('color', "#373737");
  });

  $('#mmMenu').on('click', function() {
    $(window).scrollTop($('.dash.three.and.boxes').offset().top);
    $(this).css('color', '#ffd800');
    $('#dpMenu').css('color', "#373737");
    $('#pMenu').css('color', "#373737");
    $('#ccMenu').css('color', "#373737");
    $('#siMenu').css('color', "#373737");
    allHide();
    $('#majorDiv').show();
  });

  $('#pMenu').on('click', function() {
    $(window).scrollTop($('.dash.three.and.boxes').offset().top);
    $(this).css('color', '#ffd800');
    $('#dpMenu').css('color', "#373737");
    $('#mmMenu').css('color', "#373737");
    $('#ccMenu').css('color', "#373737");
    $('#siMenu').css('color', "#373737");
    allHide();
    $('#pathwayDiv').show();
  });

  $(".cont-btn").click(function(){
    $(".main-inside").hide();
    $(".log-seg").show();
  });
$("#creds input").keypress(function(e){
  if (e.which == 13) {
        e.preventDefault();
        $("#creds").submit();

    }
})
  $("#creds").submit(function(e){
    e.preventDefault();
      logIn();
  });
  $(".print-btn").click(function(){
    window.print();
  });


  /************* END SINGLE PAGE MARKUP **************/

});
