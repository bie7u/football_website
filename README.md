# Sports web application
> The main content of this project is show a leagues, timetables and live matches. Of course there have more features.
> 
> Look at project (hosted on heroku) [_first-bl-app.herokuapp.com_](https://first-bl-app.herokuapp.com/). <!-- If you have the project hosted somewhere, include the link here. -->

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Deploy](#deploy)
* [Room for Improvement](#room-for-improvement)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
- This project show the big part of my skills. There have some interested features, which I display below.
- This website is create for people which interested about regional football leagues. This web page display important date from this kind of users.
- I decided to do this app because I'm interesting about football and I want to give people opportunity to check a result of match their favourite amator team.
<!-- You don't have to answer all the questions - just the ones relevant to your project. -->


## Technologies Used
- Python - 3.9.6
- Django - 3.2.12
- Celery - 5.2.6
- BeautifulSoup - 4.10.0
- PostgreSQL
- HTMX
- CSS
- HTML

- Heroku (to host website)
- Amazon AWS (to host a static files - images)

## Features
- ### Scrap a website to get a sports data:
&emsp; First features which I created on this website is the most of important. I use a Beautifulsoup and request to get data from [90minut.pl](http://www.90minut.pl/)  website. I use a celery to add background task (this task is responsible for take data from 90minut.pl), because scrapping need time and server without this task initiate a timeout error. I have two files which are related with this feature. This is 'user_panel/scrape.py' (get data from website in JSON format and add to 'import_data' folder) and 'user_panel/script.py' (load data to the database).



https://user-images.githubusercontent.com/83407728/169259016-11578a50-b65d-490d-ac39-d9c0f9141cb5.mp4


 - ### Set today and live matches:
&emsp; This feature use a django_celery_beat, htmx, and pymessenger2 (to connect with messenger and set bot). The page have a special subpage "NA ŻYWO" in which automatically add a today matches. If the match start, there set to 'live' using celery beat. Any users can send a actual result of match using messenger. Enough write any message and messenger bot automatically send a link with edit result request. When user send a 'live' result of match. Admin or Editor must accept a request in special menu. Subpage 'NA ŻYWO' use a htmx to auto refresh result and minute of match. 


https://user-images.githubusercontent.com/83407728/169329407-4ea502c2-11d5-4105-b5db-31173ef60bc3.mp4


 - ### Editor Panel:
&emsp; This website have three groups of users ('user' - normal user which is login in, 'editor' - user which have a special permission, 'admin'). Editor panel is available from user which have a 'editor' or 'admin' group. You can be a 'editor' only if admin give you this permission. If you be in one of this group you can add a article to blog, accept a requests about result 'live' matches, edit league (set results, change dates, hours of starts, actual round etc.), accept a request from normal user to update a info about team.

 - ### Authentication system:
 &emsp; I choosen a 'django allauth' package to create a authentication system. Apart from basic registration using email you can login with google account. If you using email to registration you must confirm your email (click a link in message which website send to you after registration). If you forget your password you can recover them. Enough click in a special link below the login panel. This is standard from all websites. If you are login you can change a username or password of your account. 
 
 - ### Blog system:
 &emsp; Everyone can add a article to blog, but users with group 'user' after added must wait for accept from editor or admin. In every article all login in users can add a comment. If you add a option 'artykuł sponsorowany' your entry show on home page (can show only 5 latest entries). If you click 'CZYTAJ WIĘCEJ' you see all articles. You can sorted in by league. In rights side of article details you can see a last 5 'sponsor entries'. 
 
 #### Watch presentation on youtube (in polish language) [https://www.youtube.com/watch?v=tN_QU9bzfv8&ab_channel=KrystianBiel](https://www.youtube.com/watch?v=tN_QU9bzfv8&ab_channel=KrystianBiel)

## Deploy
I'm using heroku to host website. Heroku redis is need to django celery. I'm connect my project with AMAZON AWS S3 to host static files. 


## Room for Improvement

Room for improvement:
- Buy a better server on heroku, because now django celery beat not working all time.
- Add more features for basic users
- Add Facebook social login

To do:
- Option for editors to delete comments


## Contact
Created by [devcode.biel@gmail.com](devcode.biel@gmail.com) - feel free to contact me!


<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
