
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

$("#geoCheckbox").click(function () {
	var thisCheck = $(this);
    if(thisCheck.is (':checked')) {
    	findMe();
    }
});

function waitForLocationAndSubmit(evt) {
	evt.preventDefault();
	var checkbox = $("#geoCheckbox")
	if(checkbox.is (':checked')) {
		var lngInput = $("#hideLng");
		console.log(lngInput)
		var lngVal = lngInput.val();
		var i = 0;
		while (lngVal === "" && i<100000000){
		// 	lngVal = lngInput.val();
		// 	i++;
			// dont submit
		// }
	}
	// this.submit()
}

$("#postForm").on('submit', waitForLocationAndSubmit);

// In findMe... before fxn callback, disable submit button, and display "waiting for location"
// incallback enable submit