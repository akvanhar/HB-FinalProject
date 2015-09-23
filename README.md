Make Less Mush
===========

*A Hackbright Final Project*

created by: [Alyson van Hardenberg](https://www.linkedin.com/in/akvanhar)

Contact: avanhardenberg@gmail.com

Having a baby is a full time job, and making them a wide variety of healthy, nutritious food is a lot of work! *Make Less Mush* is a full-stack web application that endeavors to make this job easier by providing a social-media based food sharing/messaging service. Using the Facebook Graph API, Twilio API and Google Maps API, users can choose their food-sharing experience. They can personalize it by logging in with Facebook and viewing their friends postings, they can view a map of posts to see what's in their local vicinity, and they can choose to receive text messages when someone sends them a message about their mush.

###Table of Contents
* [Home Page](#homepage)
* [All Listings](#listings)
* [User Listings](#userlistings)
* [Messages](#messages)


## <a name="homepage"></a>Home Page

On the home page, a user can fill out the form to post a listing for mush.  They can opt-in to receive text messages by entering a phone number into the appropriate field. When another user sends them a message about their post, the server calls the Twilio API and sends them a message.

The user can also opt in to share their location. This uses HTML 5 Geolocate to get their current location. As this can take a few seconds, until the location loads, a loading message is displayed and the submit button is disabled using jQuery, Ajax and JavaScript.

Also on the home page, a user can view 5 listings. These listings are obtained by querying the Sqlite database with filters to select first one listing from each of the user's Facebook friends, and then the rest of the listings in descending posting-date order. The list is then limited to only 5 listings.

On the bottom right hand side of the home page, a user can see thumbnails of their Facebook friends who are Make Less Mush users. If the user does not currently have anybody in this list, a message is displayed instead.

![Home screen image](https://raw.githubusercontent.com/akvanhar/MakeLessMush/master/static/images/home.jpg)


## <a name="listings"></a>All Listings

On the listings page, a user can toggle between the map view and a table view.  

The map is created by passing locations from the database to the Google Maps API using JSON.  JavaScript is used to create markers and Info Windows for each active listing.

![Map of Mush](https://raw.githubusercontent.com/akvanhar/HB-FinalProject/master/static/images/map.jpg)

The listings table view is created by passing information to the html directly using Jinja templating. The listings are filtered so that most recent listings come first, with the user's Facebook friends' listings at the top of the page. Allergen icons are shown if the posting user selected specific allergen checkboxes.  A tool tip appears if the user hovers the icon with their mouse.  The posting user's Facebook profile picture is displayed if they signed into Make Less Mush with Facebook.

![Table of Listings](https://raw.githubusercontent.com/akvanhar/HB-FinalProject/master/static/images/table.jpg)

If a user is interested in a particular listing, they can click on the title to reach a page where they can send that user a message. The form is pre-filled for the user, using Jinja to personalize it. The user can edit it as they wish.

![I'm interested](https://raw.githubusercontent.com/akvanhar/HB-FinalProject/master/static/images/iminterested.jpg)

If a user wants to view another specific user's listings, there are many ways they can access their page. They can click on their name or their Facebook profile picture from any of the pages where those are present.

![A particular user's listings](https://raw.githubusercontent.com/akvanhar/HB-FinalProject/master/static/images/userlistings.jpg)


## <a name="userlistings"></a>User Listings

A user can view their mush listings by click the My Listings link in the header. Here, they can update their listings, specify who they shared the mush with and deactivate a listing. When the listing is deactivated, the row in the database is updated, and that listing will now only be showed in that particular user's deactivated listings table.

![My listings](https://raw.githubusercontent.com/akvanhar/HB-FinalProject/master/static/images/mylistings.jpg)

![Update listing](https://raw.githubusercontent.com/akvanhar/HB-FinalProject/master/static/images/updatelisting.jpg)


## <a name="messages"></a>Messages

In the header on all pages, the user can see a count of their messages waiting to be read.

On the messages page, they can see their messages, and take actions by clicking buttons that alter that message row in the database.  This uses Ajax/jQuery to connect to the server and update the page without refreshing.

The reply button opens a modal window where the user can type in a new message. When this is sent it sends a text to the user with the message using the Twilio API.

The mark message as read/unread buttons update the database, and also visually change the DOM when the user clicks them. Unread messages are bolded.

The delete message button deletes that message from the database permanently. 

Both the delete button and the read/unread buttons update the badge in the header of the page when they are clicked.

![Messaging](https://raw.githubusercontent.com/akvanhar/HB-FinalProject/master/static/images/messages.jpg)

*Make Less Mush* was built by Alyson van Hardenberg over the course of 3 and half weeks as part of the Hackbright Academy Summer 2015 fellowship.

##### Technology:
- Python (passes pep8)
- Flask
- Javascript / jQuery
- AJAX
- Postgresql
- SQLAlchemy
- Google Maps API
- Facebook Graph API
- Twilio API
- HTML / CSS
- Twitter Bootstrap
- Python unittest
- Deployed on Heroku

(Dependencies are listed in requirements.txt)

##### Database
*Make Less Mush* users post listings and messages to a sqlite database.During this encapsulated process, the server handles the form inputs, allocating the appropriate data-fields to the correct table so that subsequent users can see the posted mush and messages.
The database tables utilize foreign keys in order to establish relationships between tables.
The server passes the queried database information to the browser using Jinja templating. This allows the user to have a dynamic experience while interacting with the site.

##### Frontend

The front-end is composed of Twitter Bootstrap, html forms, JavaScript, Facebook Graph API, custom CSS, jQuery UI elements and Google Maps API. 
Messaging interactivity is created with a combination of JavaScript, jQuery and AJAX.
Location is shared via HTML5 Geolocation. These locations are stored in the database and later are passed to the Google Maps API to load markers with InfoWindows on the listings map.

##### Plans for Make Less Mush 2.0

* Ability to search listings
* Allow a user to view their sent messages
