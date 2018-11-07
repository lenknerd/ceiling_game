// Javascript for Ceiling Game - button clicks and regular updates
// Copyright 2018, David Lenkner

$(document).ready(function() {

  // Commit turn score
  $("#commit_score").click(function(e) {
    e.preventDefault();
    $.ajax({
      type: "GET",
      url: "/commit_score",
      success: function(result) {
        console.log('Committed score');
      },
      error: function(result) {
        console.log('Error committing score!');
      }
    });
  });

  // Void turn score
  $("#void_turn").click(function(e) {
    e.preventDefault();
    $.ajax({
      type: "GET",
      url: "/void_turn",
      success: function(result) {
        console.log('Voided turn');
      },
      error: function(result) {
        console.log('Error voiding turn!');
      }
    });
  });

  // Every so often, update score display
  window.setInterval(function(){
    $.ajax({
      type: "GET",
      url: "/status_update",
      success: function(result) {
        console.log('Got update, putting in div with id sumlines_and_table');
        $("#status_table").html(result);
      },
      error: function(result) {
        alert('Error getting status update!');
      }
    }); 
  }, 1500);

});
