
// from: https://developers.google.com/maps/documentation/javascript/examples/map-geolocation
function findMe() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var lat = position.coords.latitude
      var lng = position.coords.longitude
      $("#hideLat").val(lat);
      console.log(lat);
      $("#hideLng").val(lng);
      console.log(lng)
    });
  } else {
    // Browser doesn't support Geolocation
	$('#noLocation').html("Unable to retrieve your location");
  }
}

// $('#geoCheckbox').on('check', googleGeoFindMe)

$("#geoCheckbox").click(function () {
	var thisCheck = $(this);
    if(thisCheck.is (':checked')) {
    	findMe();
    }
});
