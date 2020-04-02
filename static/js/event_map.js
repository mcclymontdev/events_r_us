$(document).ready(function() {
    // Setup map.
    var map = L.map('map-container', {
        zoomControl: false
    });

    // Get lat and long from event.
    var Latitude = document.getElementById("Latitude").value;
    var Longitude = document.getElementById("Longitude").value;

    // Setup our map layer.
    var OSMDefault = new L.TileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            minZoom: 10,
            maxZoom: 15,
            attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
        }
    );

    var markerList = [];

    // Initialise map.
    map.setView([0, 0], 1);
    map.addLayer(OSMDefault);

    // Create event marker, add it to the map and push it to our markers array.
    var marker = L.marker([Latitude,Longitude]);
    marker.addTo(map);
    markerList.push(marker);

    // Center marker on map.
    map.fitBounds(L.featureGroup(markerList).getBounds().pad(0.75), {animate: false});
})