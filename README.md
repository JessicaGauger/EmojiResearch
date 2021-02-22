# EmojiResearch

This project consists of communicating with Twitters API to obtain tweets that can later be analyzed to see how the Covid-19 Pandemic has affected Emoji Use.
This project can be used for all kinds of research involving keywords and emoji during a specific time frame. 

Here is how you get started:

First you will need to create a database, create tables inside the database and finally populate the database. All of this can be done using my Import Emoji Tool.

Next you will need to create a Twitter Developer Portal. You will then have to create a project. Once you navigate to the project you will be able to find your bearier token,
access tokens and secret. You will need these for later.

How to run the code:

First you will open your command prompt and you will have to cd into the EmojiResearchProject folder. 
Next you will cd into the emoji-reseasrch-website folder. 
Once you are in the emoji-research-website folder you will then type 'code .' which will open the project in Visual Studio Code.
Once the emoji-research-website project opens you will relocate to the terminal (ctrl-j for a shortcut).
Then you will type in 'npm start' to run the project.
This will oben the Emoji Reaseach Tool website in your browser. 
Leave this open and go on to the next step below.

Next you will open your command promp agaian and cd into the EMojiReasearchProject folder.
Then you will cd into the EmojiAnalysis folder.
Once in the EmojiAnalysis fodler cd into the Server folder.
Once you are in the Server folder type in 'nodemon app.js' to run the project.
When the message "Starting the api. Listening on port: 4000. db connected." is shown you can go back to the Emoji Research Tool website in your browser.

You will then be able to regsiter and login. Once you are logged in you are then able to search for tweets by a specific keyword, phrase and/or emoji 
from a specific start date until a specific end date. Note: the start date and end date have to be two different days otherwise you will get an error.
For example:
  start date: 01/01/2021
  end date:   01/02/2021

