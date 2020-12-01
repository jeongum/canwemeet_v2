$(document).ready(function(){
    // Toggle tab menu in minute-details
    $('#minute-container .tab-menu').click(function(){
      var tab_id = $(this).attr('data-tab');
   
      $('#minute-container .tab-menu').removeClass('current');
      $('.tab-content').removeClass('current');
   
      $(this).addClass('current');
      $("#"+tab_id).addClass('current');
    })

    // Draw Emotion Graph Pie Chart
    // 나중에 DB에서 감정 % 받아와서 변수에 저장해야 함. 지금은 임시로 지정해 두겠습니다.
    var entire_emotion = [19.4, 16.1, 51.6, 12.9];  //anger, happiness, neutral, sadness
    var my_emotion = [25, 12.5, 50, 12.5];      //anger, happiness, neutral, sadness

    var entire_gradient_points = [entire_emotion[0],
                                  entire_emotion[0] + entire_emotion[1],
                                  entire_emotion[0] + entire_emotion[1] + entire_emotion[2]]
    
    var my_gradient_points = [my_emotion[0],
                              my_emotion[0] + my_emotion[1],
                              my_emotion[0] + my_emotion[1] + my_emotion[2]]

    var entire_gradient = "conic-gradient(#ffb2b2 0%" + entire_gradient_points[0] + "%, #ffedae "
                          + entire_gradient_points[0] + "% " + entire_gradient_points[1] + "%, #d9ead3 "
                          + entire_gradient_points[1] + "% " + entire_gradient_points[2] + "%, #9fc5e8 "
                          + entire_gradient_points[2] + "% 100%)";

    var my_gradient = "conic-gradient(#ffb2b2 0%" + my_gradient_points[0] + "%, #ffedae "
                          + my_gradient_points[0] + "% " + my_gradient_points[1] + "%, #d9ead3 "
                          + my_gradient_points[1] + "% " + my_gradient_points[2] + "%, #9fc5e8 "
                          + my_gradient_points[2] + "% 100%)";

    $('#entire-emotion-graph').css({
      "margin-bottom": "15px",
      width: "150px",
      height: "150px",
      background: String(entire_gradient),
      "border-radius": "50%"
    });

    
    $('#my-emotion-graph').css({
      "margin-bottom": "15px",
      width: "150px",
      height: "150px",
      background: String(my_gradient),
      "border-radius": "50%"
    });
  })