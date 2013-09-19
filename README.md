Follow @UWParkingBot to get up-to-the-(5)-minute information about 
UW parking lots and how full they are. 

This account is student-run and is not affiliated with the University of Waterloo. 

parkingBot
==========

A Twitter Bot that tweets University of Waterloo parking information

A Tokens.py file is needed to run this code. It must define the following constants:

Twitter API
- CONSUMER_KEY
- CONSUMER_SECRET
- ACCESS_KEY	
- ACCESS_SECRET

uWateloo API
- UW_KEY (html address)

Path to some file for storing information
- DATA_FILE 


This script is meant to run periodically. 
It currently runs every 5 minutes Mon-Fri, 8am-6pm. 
This is because there is a limit to the number of requests
one can make to api.uwaterloo.ca. 
