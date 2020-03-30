$(function() {
    rating_form = document.getElementById("rating_form");
    $('.rating input').change(function() {
        rating_form.submit();
     });
});