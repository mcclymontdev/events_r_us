(function() {
    var placesAutocomplete = places({
      appId: 'plFDOT075MSR',
      apiKey: '9ae347daeb22af17669388f186c51ee9',
      container: document.getElementById('id_Address'),
      templates: {
        value: function(suggestion) {
          return suggestion.name;
        }
      }
    }).configure({
      type: 'address'
    });
    placesAutocomplete.on('change', function resultSelected(e) {
      document.getElementById('id_Latitude').value = e.suggestion.latlng.lat;
      document.getElementById('id_Longitude').value = e.suggestion.latlng.lng;
    });
  })();