var popup
var img
var popupImage
var closeButton

$(document).ready(function() {
    popup = document.getElementById("event-image-popup");
    img = document.getElementById("event-image");
    popupImage = document.getElementById("popup-image");
    closeButton = document.getElementsByClassName("close-popup")[0];

    img.onclick = function(){
      popupImage.src = img.src;
      popup.style.display = "block";
    }

    closeButton.onclick = function() {
      popup.style.display = "none";
    }
});
