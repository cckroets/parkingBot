import urllib2
import xml.etree.ElementTree as ET
import sys
import datetime
import Tokens
from twython import Twython


### Tokens.py must define the following: ####
# CONSUMER_KEY
# CONSUMER_SECRET
# ACCESS_KEY	
# ACCESS_SECRET	
# UW_KEY (html address)
# DATA_FILE 
#############################################

# Create an instance of the Twitter API
twitter	 =	Twython(Tokens.CONSUMER_KEY,
			Tokens.CONSUMER_SECRET,
			Tokens.ACCESS_KEY,
			Tokens.ACCESS_SECRET)

# Tweet a message and return its ID
def send_tweet(msg):
	tweet = twitter.update_status(status=msg)
	tweetID = tweet['id_str']
	return tweetID

# Delete a tweet using its ID
def delete_tweet(tweetID):
	twitter.destroy_status(id=tweetID)


### Program Details ####
# Read in old parking info (from 5 minutes ago)
# Make request for parking new info
# Compare new info vs. old info
# Find differences
# 	For each difference
#		delete the old tweet
#		tweet the new info
#		replace the tweet ID in the file

PARKING_FILE = Tokens.DATA_FILE

# The minimum number of spaces a lot can have to be
# considered open. Otherwise it is limited or full
LIMIT_THRESHOLD = 5

# Aux. File looks like:
# Lot	Avail.	Tweet ID
##############################
# C 	0	 	312032...83091 
# N 	3 		312032...84920
# W 	40		312032...24344
# X 	67		312032...39434
 

# A parking lot class 
class ParkingLot:
	# Create an instance of a parking lot
	def __init__(self, name, empties, tweetID):
		self.LotName = name
		self.EmptySpaces = empties
		self.TweetID	= tweetID

	# Update the Tweet ID
	def update_id(self,newID):
		self.TweetID = newID

	# Return a string of info about the lot
	def to_string(self):
		return self.LotName + "\t" + str(self.EmptySpaces) + "\t" + self.TweetID + "\n"

	# Return the lot name as a hashtag 
	def hashtag(self):
		return "#Lot_" + self.LotName 

	# Return an appropriate tweet if the info has changed significantly
	def message(self,newEmpties):
		# If the lot has just became empty:
		if (newEmpties <= 0 and newEmpties < self.EmptySpaces):
			msg = self.hashtag() + " is full!"
		# If the lot has just became limited (< 5 available spaces):
		elif (newEmpties != self.EmptySpaces and newEmpties < LIMIT_THRESHOLD):
			# There is one spot left 
			if (newEmpties == 1):
				msg = self.hashtag() + " has 1 spot left!"
			# There are N in (1,LIMIT_THRESHOLD) spots left
			else:
				msg = self.hashtag() + " has " + str(newEmpties) + " spaces available."
		# If the lot has just became open (5 or more spaces available)
		elif (newEmpties >= LIMIT_THRESHOLD > self.EmptySpaces):
			msg = self.hashtag() + " is open with at least " + str(LIMIT_THRESHOLD) + " spots available."
		# Otherwise, do not send a tweet
		else: 
			msg = None
		# Update the count
		self.EmptySpaces = newEmpties
		return msg
#/ ParkingLot


# Returns an array of ints (each representing number of empties)
def get_latest_empty_count():
    # Request parking data from api.uwaterloo.ca
    response = urllib2.urlopen(Tokens.UW_KEY)

    # Make XML Tree from result
    root = ET.fromstring(response.read())
    root = root.find('data')

    LotEmpties = []

    # Parse results
    for result in root:
        count = result.find('LatestCount').text
        cap   = result.find('Capacity').text
        empties = int(cap) - int(count)
        LotEmpties.append(empties)
    return LotEmpties



# Create array of lots from old info
def get_old_info():
	f = open(PARKING_FILE,'r')
	Lots = []
	for line in f:
		words = line.split()
		name = words[0]
		empties = int(words[1])
		tweetID = words[2]
		Lots.append(ParkingLot(name,empties,tweetID))
	return Lots

# Update and Tweet information
def update_info(Lots):
	Empties = get_latest_empty_count()		# Latest info on emptiness in each lot
	f = open(PARKING_FILE, 'w')				# Open parking file for writing updates
	# For each Parking Lot
	for l in range(len(Lots)):
		msg = Lots[l].message(Empties[l])
		if (msg is not None):
			delete_tweet(Lots[l].TweetID)	# Delete the old tweet
			newID = send_tweet(msg)				# Tweet info
			Lots[l].update_id(newID) 		# Update Tweet ID
		# Write parking info to file
		f.write(Lots[l].to_string())
	f.close()


# Run entire script
def run():
	Lots = get_old_info()
	update_info(Lots)


# Run script
run()

