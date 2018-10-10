

$(function() {
    $('#submitBtn').click(function() {
      var submissionData = $('#creds').serialize()
        $.ajax({
            url: '/webScraperTool',
            data: submissionData,
            type: 'POST',
            success: function(body){
              var test = `{"Student": "Coltrane, Gary", "ID": "20066526", "Classification": "Senior", "Advisors": "Coleman, Ronald G Rice, Mary C", "Overall GPA": "3.359", "Student Type": "Traditional Continuing", "Term Location": "HEOP", "Level": "Undergraduate", "Degree": "B.S.", "College": "Computer Science & Mathematics", "Major": "Computer Science", "Minor": "CompSci: Software Development"}`
              var parse = JSON.parse(body);
              console.log(parse);
              var {College, Major, Level, Student,ID,Classification} = parse
                $(".main-content").empty();
                $(".main-content").append("<h1> Success </h1>")
                $(".main-content").append(`<p> ${Student}: ${ID}</p>`)
                $(".main-content").append(`${College} ${Major}: ${Level}`)



            }
        });
    });
});
