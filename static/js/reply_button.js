$(document).ready(function(event){
  $(".reply-btn").click(function(){
    $(this).parent().next(".replied-comments").fadeToggle();
  });
});
