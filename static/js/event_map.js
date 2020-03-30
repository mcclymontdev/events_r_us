$(document).ready(function() {
    // Setup map.
    var map = L.map('map-container', {
        zoomControl: false
    });

    // Get lat and long from event.
    var Latitude = document.getElementById("Latitude").value;
    var Longitude = document.getElementById("Longitude").value;

    // Setup our map layer.
    var osm_bright = new L.TileLayer(
        'https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png', {
            minZoom: 10,
            maxZoom: 15,
            attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
        }
    );

    var markerList = [];

    // Initialise map.
    map.setView([0, 0], 1);
    map.addLayer(osm_bright);

    // Create event marker, add it to the map and push it to our markers array.
    var marker = L.marker([Latitude,Longitude]);
    marker.addTo(map);
    markerList.push(marker);

    // Center marker on map.
    map.fitBounds(L.featureGroup(markerList).getBounds().pad(0.75), {animate: false});
})