
var class_prefix = "#id_Crush_email_";
var num_fields = 3;

//Make default text fields empty
$('#vent-form').submit(function() {
  for (var num = 1; num <= num_fields; ++num) {
    if ($(class_prefix + num).val() == "Start by typing a name or email"){
      $(class_prefix + num).val("");
    }    
  }
});

$(document).ready(function()
{
  for (var num = 1; num <= num_fields; ++num) {
    $(class_prefix + num).addClass("defaultTextActive");
    $(class_prefix + num).focus(function(srcc)
    {
        if ($(this).val() == $(this)[0].value)
        {
            $(this).removeClass("defaultTextActive");
            $(this).val("");
        }
    });
    
    $(class_prefix + num).blur(function()
    {
        if ($(this).val() == "")
        {
            $(this).addClass("defaultTextActive");
            $(this).val($(this)[0].value);
        }
    });
    
    $(class_prefix + num).blur();
  }

  //do manual searches before all the usernames are loaded
  for (var num = 1; num <= num_fields; ++num) {
    $(class_prefix + num).autocomplete({autoFocus: true, delay: 1, source: function(request, response){
      $.getJSON("/getlabels/",
        request,
        function(data) {
          response(data.slice(0, 10));
        }
      );
    }});
  }
  //load all the usernames
  $.get("/names/", function(data){
    data = JSON.parse(data);
    for (var num = 1; num <= num_fields; ++num) {
      $(class_prefix + num).autocomplete({autoFocus: true, delay: 1, source: function(request, response){
        var results = $.ui.autocomplete.filter(data, request.term);
        response(results.slice(0, 10));
      }});
    }
  });
});
