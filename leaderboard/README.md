# Warbadge scoreboard
This is the scoreboard app for [warbadge.ninja](https://warbadge.ninja).
This code was in a hurry late at night to quickly setup a contest at Shmoocon 2018. It not optimized, probably does not sanitize input properly and may have SQL injection issues. Be warned. It is posted here for Shmoocon attendees that may want to play with the badges and do a contest of their own.

# Stack
The stack is flask, gunicorn, bootstrap and mysql. No ORM, just SQL queries.

# Setup
Create a mysql database.
Use the schema files to create tables.
Setup a mysql user.
Configure the mysql creds in app.py
pip install -r requirements.txt
python ./app.py

# TODO:
Probably some sql injection issues in the checkin code. Need to input validation.
Unit tests
Add some automation to setup a dev instance
