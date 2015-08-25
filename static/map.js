
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
      $("#geoMessage").html("");
      $('#submitButton').removeAttr('disabled');
    });
  } else {
    // Browser doesn't support Geolocation
	$('#geoMessage').html("Unable to retrieve your location");
  }
}

$("#geoCheckbox").click(function () {
	var thisCheck = $(this);
    if(thisCheck.is (':checked')) {
    	$('#submitButton').attr('disabled', 'disabled');
    	$("#geoMessage").html("...Waiting for location...");
    	findMe();
    }
});