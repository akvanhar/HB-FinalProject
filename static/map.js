var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 37.773561, lng: -122.444323},
    zoom: 13
  });

  $.get('/listings.json', function(data) {
    var image = 'static/images/mlmlogo.jpg';
    for (var key in data) {
        var location = data[key];
            // Define content of infoWindow per marker
            var contentString = (
              '<div id="content">' + '<div id="siteNotice">'+'</div>'+
              '<h3>Mush:' + location['title'] + '</h3>' +
              '<p>Posting User: ' + location['posting_user'] + '</p>' +
              '<p>Date Posted: ' + location['date_posted'] + '</p>'+
              '</div>'
            );
            console.log(contentString);

            // Create info window 
            var infoWindow = new google.maps.InfoWindow({
              content: contentString
            });

            // Create marker per location object
            marker = new google.maps.Marker({
              position: {lat: location['latitude'], lng: location['longitude']},
              map: map,
              animation: google.maps.Animation.DROP,
              title: location['title'],
            });

            // Add event listeners per marker
            bindinfoWindow(marker, map, infoWindow, contentString);

    }  // END for loop
  });//end $get
}

function bindinfoWindow(marker, map, infoWindow, html) {
  google.maps.event.addListener(marker, 'click', function() {
    // Set infoWindow content and open it when user clicks.
    infoWindow.setContent(html);
    infoWindow.open(map, marker);
  });
}