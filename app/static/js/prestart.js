$(document).ready(function() {

  $(".color-selector").change(function(){
    color = $(".color-selector").val()
    $(".title").css("background-color", color)
  })

})
function start_game(game_id){
  $.ajax({
    type: "POST",
    url: "/games/"+game_id+"/start",
    success: function(data){location.reload();}
  })
}
