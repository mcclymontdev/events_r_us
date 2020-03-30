$(function() {
    get_location_button = document.getElementById("get_location_button");
    search_form = document.getElementById("search_form");
});

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(submitPosition);
    } else {
        get_location_button.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function submitPosition(position) {
    search_form.id_Latitude.value = position.coords.latitude;
    search_form.id_Longitude.value = position.coords.longitude;
    search_form.submit();
}
