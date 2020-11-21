$(document).ready(function(){
   
  // Toggle tab menu in minute-details
    $('#minute-container .tab-menu').click(function(){
      var tab_id = $(this).attr('data-tab');
   
      $('#minute-container .tab-menu').removeClass('current');
      $('.tab-content').removeClass('current');
   
      $(this).addClass('current');
      $("#"+tab_id).addClass('current');
    })
  })