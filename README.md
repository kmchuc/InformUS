![](/readme-imgs/logo.png)
# InformUS
InformUS is a full-stack web application created to inform users of voter suppression occuring at nearby polling centers. Users can locate nearby polling centers displayed on the map using markers and view comments for each location. Unregistered users are not allowed to leave comments but do have access to view comments for any polling location.

**Contents**
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Installation](#installation)
- [About Me](#about-me)

To watch a screencast of the application go to:

[![Alt text](https://img.youtube.com/vi/AwLZJL1cUz8/0.jpg)](https://www.youtube.com/watch?v=AwLZJL1cUz8)


## Overview
![](/readme-imgs/homepage.png)
<br>

**The Map:**
* Shows markers representing nearby polling centers.
* Info box includes location's name, hours, and coordinates

**Users can:**
* Login/logout/register (creating an account)
* Find nearest polling centers using any address
* Add a review for a polling center
* View all reviews left by other users for a polling center

## Tech Stack
**Backend:**
Python, Flask, Flask-SQLAlchemy, Flask-Login, Jinja2

**Frontend:**
JavaScript, jQuery, AJAX, Jijna, HTML5, CSS3, Boostrap

**APIs:**
Google Maps JavaScript, Google Civic Information, Geocode

## Features
**Map:**
<br>
Google maps methods to initliaze a visual map containing markers for each polling location.
Store comments in a database with associated tables for users, comments, and polling centers
Flask app routes AJAX requests to the database and Flask sessions
<br>
![](/readme-imgs/map.gif)

**Markers**
<br>
Query database to construct a JSON file which supplied my javascript function to populate the map. 
Used Google Maps event listeners to create interactive markers
Click on map marker once to view information about polling center such as name, hours, and location
Click on map marker twice to view comments at the bottom of the page
When logged in, user can leave comment for polling center in the info box. 
<br>
![](/readme-imgs/interactivemap.gif)

**Comments**
<br>
A logged in user can leave comments for polling centers, when submitted the comment is saved into the database in relation to the user's ID
<br>
![](readme-imgs/commentmap.gif)

## About Me

Kimberly Chuc is a software engineer located in the San Francisco Bay Area. She previously worked as an EMT striving towards becoming a Physician Assistant. Her passion for politics and love for problem solving led her to creating her capstone package. She hopes this project provides people with the proper resources to practice their right to vote! 
