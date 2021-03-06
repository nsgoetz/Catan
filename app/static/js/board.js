side_len = 70;
edge_width = "5px";
vertex_size = 20;
var current_player;

function vertex_coordinates(c, r){
  var x = Math.floor((c*Math.sqrt(3)*side_len)/2);
  var y = ((Math.floor(r/2)) * side_len) + ((Math.floor((r+1)/2))*(side_len/2) - 2*r)
  return {x: x, y: y}
}

function vertex_coordinates_2(c, r){
  var x = Math.floor((c*Math.sqrt(3)*side_len)/2) - 5
  var y = (((Math.floor(r/2)) * side_len) + ((Math.floor((r+1)/2))*(side_len/2)) - 10*r -((r%2)*20))/4 - vertex_size
  return {x: x, y: y}
}

$(document).ready(function() {
  var pathArray = window.location.pathname.split( '/' );
  var game_id = pathArray[pathArray.length-1]
  $.ajax({
    type: "POST",
    url:'/games/'+game_id+"/get_game_data",
    data:{game_id: game_id}
  }).success(function(data){
    current_player = data.current_player;
    color = data.color;
  });

  $.each($(".edge"), function(i, e){
    var vertexArr = e.id.split(":");
    var v1 = vertexArr[0].split(",");
    var v2 = vertexArr[1].split(",");
    var starts = vertex_coordinates(Math.min(v1[0], v2[0]), Math.min(v1[1], v2[1]));
    var x0 = starts.x;
    var y0 = starts.y;
    $(e).css({
      width: String(side_len)+"px",
      height: edge_width
    });
    if($(e).hasClass("side-edge")){
      $(e).css({
        top: String(y0+(side_len/(2.5*Math.sqrt(3))))+"px",
        left: String(x0-(side_len/2)+3)+"px"
      });
    } else {
      $(e).css({
        top: String(y0)+"px",
        left: String(x0)+"px"
      });
    }
    $(e).click(function(){
      console.log("clicled",[v1, v2])
    })
  })

  $.each($(".vertex"), function(i, e){
    var cArr = e.id.split(",");
    var c = cArr[0]
    var r = cArr[1]
    var CDict = vertex_coordinates_2(c, r)
    $(e).css({
      width: String(vertex_size) + "px",
      height: String(vertex_size) + "px",
      top: String(CDict.y)+"px",
      left: String(CDict.x )+"px"
    });
  })


  $.each($(".hex"), function(i, e){
    var cArr = e.id.split(",");
    var c = cArr[0]
    var r = cArr[1]
    var CDict = vertex_coordinates_2(c, r)
    $(e).css({
      width: String(vertex_size) + "px",
      height: String(vertex_size) + "px",
      top: String(CDict.y-15)+"px",
      left: String(CDict.x-side_len/2-50)+"px"
    });
    $.each($(e).children(".probability"), function(i, el){
      $(el).css({
        top: String(side_len*5/6)+"px",
        left: String(side_len)+"px"
    })})

  })

})

$(".vertex").click(function(e){
  e.css({"background-color": color})
})