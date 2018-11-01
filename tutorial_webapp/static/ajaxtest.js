// Test ajax request
$(document).ready(function() {
  $("#upd").click(function(e) {
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: "/ajaxtest_query",
      data: {
        nplayas: 4,
        nturns: 3
      },
      success: function(result) {
        alert('hey got result back, puttin it in');
        $("#ajax_result_here").html(result);
      },
      error: function(result) {
        alert('uh oh getting result back');
      }
    });
  });
});
