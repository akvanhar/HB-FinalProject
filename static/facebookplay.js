
window.fbAsyncInit = function() {
    FB.init({
        appId      : '478449745662319',
        xfbml      : true,
        cookie     : true,
        version    : 'v2.4'
    });
    // place code here that I want to run as soon as the page is loaded

    //share something on facebook
    // FB.ui(
    //    {
    //     method: 'share_open_graph',
    //     action_type: 'og.likes',
    //     action_properties: JSON.stringify({
    //       object:'https://developers.facebook.com/docs/',
    //     })
    //   }, function(response){
    //     console.log(response);
    //   });

};  //close the fbAsyncInit function

(function(d, s, id){
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

function myFacebookLogin() {
      FB.login(function(){}, {scope: 'publish_actions'});
    }

function myFacebookLogout() {
  FB.logout(function(response) {
  // user is now logged out
});
}