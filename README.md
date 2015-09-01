Make Less Mush
===========

*A Hackbright Final Project*

created by: [Alyson van Hardenberg](https://www.linkedin.com/in/akvanhar)
Contact: avanhardenberg@gmail.com

Having a baby is a full time job, and making them a wide variety of healthy, nutritious food is a lot of work! *Make Less Mush* is a full-stack web application that endeavors to make this job easier by providing a social-media based food sharing/messaging service. Using the Facebook Graph API, Twilio API and Google Maps API, users can choose their food-sharing experience. They can personalize it by logging in with Facebook and viewing their friends postings, they can view a map of posts to see what's in their local viscinity, and they can choose to receive text messages when someone sends them a message about their mush.

![Home screen image](link to image here)
![Map of Mush](link to map image)
![Messaging](link to messaging)

<b>Author:</b><br>
Alyson graduated from an accelerated nursing program with a Bachelor of Science in Nursing. While pursuing this career, Alyson was drawn to the rapidly changing, creative aspect of the technical industry. Alyson spent time talking to software engineers, who pointed her towards Hackbright Academy. Alyson is excited to bring the skill of fast-paced problem-solving that she developed as a nurse to her software development. Developing software has given Alyson another medium in which to express her creativity. Alyson also expresses this passion for creativity in her hobbies as a potter, a knitter and a baker.

##### Technology:
- Python
- Flask
- Javascript / jQuery
- AJAX
- SQLite / SQLAlchemy
- Google Maps API
- Facebook Graph API
- Twilio API
- HTML / CSS
- Bootstrap
- Python unittest

(Dependencies are listed in requirements.txt)

##### Database
*Make Less Mush* users post listings and messages to a sqlite database.During this encapsulated process, the server handles the form inputs, allocating the appropriate datafields to the correct datatable so that subsequent users can see the posted mush and messages.
The database tables utilize foreign keys in order to establish relationships between tables.
The server passes the queried database information to the browser using Jinja templating. This allows the user to have a dynamic experience while interacting with the site.

##### Frontend

The front-end is composed of Twitter Bootstrap, html forms, JavaScript, Facebook Graph API, custom CSS, jQuery UI elements and Google Maps API. 
Messaging interactivity is created with a compination of JavaScript, jQuery and AJAX.
Location is shared via HTML5 Geolocation. These locations are stored in the database and later are passed to the Google Maps API to load markers with InfoWindows on the listings map.

![picture of map]

###### Plans For Version 2.0
