function foreachMap(index){
    var map = new google.maps.Map(document.getElementsByClassName('map')[index], {
      'zoom': 14, 'center': new google.maps.LatLng(25.03518, 121.54388)   // CLBC.
    });

    var updateMap = function (map, center) {
      map.setCenter(center);
      var marker = new google.maps.Marker({'map': map, 'position': center});
    };


    var address = $('.addressMap').eq(index).html();
  //  console.log(address);
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK && results.length) {
        updateMap(map, results[0].geometry.location);
      } else if (google.maps.places) {
        var service = new google.maps.places.PlacesService(map);
        var request = {'location': map.getCenter(), 'radius': 50000, 'query': address};
        service.textSearch(request, function (results, status) {
          if (status == google.maps.GeocoderStatus.OK && results.length)
            updateMap(map, results[0].geometry.location);
        });
      }
    });
}


function initMap() {
  for(i = 0;i< $('.addressMap').length;i++)
    foreachMap(i);
}

