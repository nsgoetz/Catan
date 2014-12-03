$(document).ready(function() {

  $(".color-selector").change(function(){
    color = $(".color-selector").val()
    $(".title").css("background-color", color)
  })

  function start_game(){
  }
})