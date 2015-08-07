//Facebook initialize.

function getUserDetails() {
	console.log("We're in getUserDetails")
	debugger;
 	FB.api('/me', {fields: ['last_name', 'first_name', 'email', 'id']}, function(response) {
 		console.log(response);
 		var fname = response.first_name;
 		console.log(fname);
 		var lname = response.last_name;
 		console.log(lname);
 		var email = response.email;
 		console.log(email);
 		var fbUserId = response.id;
 		console.log(fbUserId);

 		return [fbUserId, fname, lname, email];
 	})
 }

function submit_info_to_server(accessToken, userDetails) {
      //takes the access token, and a userdetails list as input, submits a form to the server.
      //userDetails in the following list: [fbUserId, fname, lname, email]
      var form = document.createElement('form');
      var user_id_element = document.createElement('input');
      var user_fname_element = document.createElement('input');
      var user_lname_element = document.createElement('input');
      var user_email_element = document.createElement('input');

      //get details from fb api in the form of a list
      //

      var fbUserId = userDetails[0];
      var fname = userDetails[1];
      var lname = userDetails[2];
      var email = userDetails[3];
      
      form.method = "POST";
      form.action = "/facebook_login_portal";

      
      //set element values
      user_id_element.value = fbUserId;
      user_fname_element.value = fname;
      user_lname_element.value = lname;
      user_email_element.value = email;

      //set element names
      user_id_element.name = 'fbUserId';
      user_fname_element.name = 'fbfname';
      user_lname_element.name = 'fblname';
      user_email_element.name = 'fbemail';

      form.appendChild(user_id_element);

      document.body.appendChild(form);

      
      alert('About to submit!')
      debugger;
      form.submit();
  }

function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    if (response.status === 'connected') {
    	//User is connected to both MLM and FB. 
    	//Collect the access token.
    	var accessToken = response.authResponse.accessToken;
    	var userDetails = getUserDetails;
    	submit_info_to_server(accessToken, userDetails);

    } else if (response.status === 'not_authorized') {
      // User is connected to FB, but not MLM
      document.getElementById('status').innerHTML = 'Please log into Make Less Mush.';
    } else {
      // The person is not logged into Facebook, so we're not sure if
      // they are logged into MLM or not.
      document.getElementById('status').innerHTML = 'Please log into Facebook.';
    }
  }

function checkLoginState() {
	FB.getLoginStatus(function(response) {
	  statusChangeCallback(response);
	});
}


window.fbAsyncInit = function() {
  FB.init({
    appId      : '478449745662319', //Make Less Mush appId
    cookie     : true,  // enable cookies to allow the server to access the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.2' // use version 2.2
  });

  // 	//Now check to see which of the three login statuses is present for the user
  //   FB.getLoginStatus(function(response) {
  //   statusChangeCallback(response);
  // });
};

// Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));


