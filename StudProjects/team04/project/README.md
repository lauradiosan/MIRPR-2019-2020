# midrapr

Installing and launching the application:
 * Install npm
 * Install python 3.7
 * Run pip install -r requirements.txt
 * Create a .sqlite3 file and put it's name in the properties.yaml file from the backend folder (in this file all the
 session information will be stored)
 * Run app.py from the backend folder using python
 * Go in the folder admin_frontend and run npm start command
 * The script start_client should be installed on all the machines you want to monitor
 * You simply run start_client script on every machine and then press "Start session" button from the GUI (frontend) 
 and the script starts sending data to the backend. When you press "Stop session" you can see the report for the data
 collected. 

Requirements:
 * As a user I want to be able to start a session so I can record data from the children.
 * As a user I want to be able to stop a session so I can see a report of the collected data from the current session.
 * As a user I want to be able to select a previous session so I can see the report for that session.
 * As a user I want to be able to see the report as a pie chart containing the percentage of each detected emotion 
 during the selected session.
 * As a user I want to be able to filter the details of a session by emotion so I can see each screen shot when the 
 user's emotion is the one selected by me.