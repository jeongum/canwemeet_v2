$(document).ready(function(){
  // Emotion Filter
  $('input:checkbox[id=with-emotion]').click(function() {
    let check = $(this).is(":checked");
    $('.content.anger').css(
      "background-color", check ? "#ffb2b2" : "transparent");

    $('.content.happiness').css(
      "background-color", check ? "#ffedae" : "transparent");

    $('.content.neutral').css(
      "background-color", check ? "#d9ead3" : "transparent");

    $('.content.sadness').css(
      "background-color", check ? "#9fc5e8" : "transparent");

    $('.emotion-icon').css("display", check ? "block" : "none");
  });


  // Highlight Filter
  $('input:checkbox[id=with-highlight]').click(function() {
    //Write Functions here
  });

  // Toggle tab menu in minute-details
  $('#minute-container .tab-menu').click(function(){
    let tab_id = $(this).attr('data-tab');
   
    $('#minute-container .tab-menu').removeClass('current');
    $('.tab-content').removeClass('current');
   
    $(this).addClass('current');
    $("#"+tab_id).addClass('current');
  })

  // Draw Emotion Graph Pie Chart
  // 나중에 DB에서 감정 % 받아와서 변수에 저장해야 함. 지금은 임시로 지정해 두겠습니다.
  let entire_emotion = [25, 55, 10, 10];  //anger, happiness, neutral, sadness
  let my_emotion = [30, 25, 15, 30];      //anger, happiness, neutral, sadness

  let entire_gradient_points = [entire_emotion[0],
                                entire_emotion[0] + entire_emotion[1],
                                entire_emotion[0] + entire_emotion[1] + entire_emotion[2]]
    
  let my_gradient_points = [my_emotion[0],
                            my_emotion[0] + my_emotion[1],
                            my_emotion[0] + my_emotion[1] + my_emotion[2]]

  let entire_gradient = "conic-gradient(#ffb2b2 0%" + entire_gradient_points[0] + "%, #ffedae "
                        + entire_gradient_points[0] + "% " + entire_gradient_points[1] + "%, #d9ead3 "
                        + entire_gradient_points[1] + "% " + entire_gradient_points[2] + "%, #9fc5e8 "
                        + entire_gradient_points[2] + "% 100%)";

  let my_gradient = "conic-gradient(#ffb2b2 0%" + my_gradient_points[0] + "%, #ffedae "
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