#Identifies influential users based on twitter trends
#Simon Rosner
#12/21/2017

#JSON stuff
try:
    import json
except ImportError:
    import simplejson as json

#twitter stuff
from twitter import Twitter, OAuth, TwitterHTTPError

#file stuff
import os
import os.path
import codecs

#time stuff
import time
import datetime

class gooseLeader:
    """Allows for searches of tweets and specific manipulations search results"""
    def __init__(self, 
                 accessToken = None,
                 accessSecret = None,
                 consumerKey = None,
                 consumerSecret = None):
        #get tokens, keys, secrets from init.txt file where applicable
        file = open('init.txt', 'r')
        for line in file:
            spot = line.find('=') + 1
            if 'accessToken=' in line and accessToken is None:
                    accessToken = line[spot:].strip()
            elif 'accessSecret=' in line and accessSecret is None:
                    accessSecret = line[spot:].strip()
            elif 'consumerKey=' in line and consumerKey is None:
                    consumerKey = line[spot:].strip()
            elif 'consumerSecret=' in line and consumerSecret is None:
                    consumerSecret = line[spot:].strip()

        oauth = OAuth(accessToken, accessSecret, consumerKey, consumerSecret)

        #twitter search
        self.twitter = Twitter(auth=oauth)

    def search(self, query, tweetCount, language = None, resultType = None):
        """searches using twitter REST API"""
        #optional argument check
        if language == None: language = ''
        if resultType == None: resultType = ''
        
        tweets = self.twitter.search.tweets(q = query, result_type = resultType,
                                            lang=language, count=tweetCount)
        tweets = tweets
        return tweets

    def getInfluUsers(self, userCount, tweets):
        """Returns info on most influential users in a given search"""
        influUsers = []
        for user in tweets['statuses']:
            #handles dupes but raises complexity. Seek better solution to dupes
            if user['user'] not in influUsers:
                influUsers.append(user['user'])
                #sort
                influUsers = sorted(influUsers, key = lambda user: user['followers_count'], reverse = True)
                #get top userCount
                influUsers = influUsers[0:userCount]
        return influUsers             

    def userHTMLReport(self, users, title = None, prefix = "", postfix = ""):
        """Creates an Html file with details on users"""
        filename = (prefix + title + postfix + '.html')
        with codecs.open(filename,'w+','utf-8') as file:
            file.write("<!DOCTYPE html>\n<html>\n<head>\n")
            if title != None:
                file.write("<title>"+title+"</title>\n")
            file.write("</head>\n<body>\n")
            file.write("<div>\n<span>Search: "+title+"</span><br/>\n")
            file.write("<span>Time: "+datetime.datetime.now().strftime("%d %B %Y %H:%M")+"</span>\n<div>")
            for user in users:
                file.write("<div>\n")
                file.write("<p style='border: 2px solid #"+str(user['profile_link_color'])+"'>\n")
                file.write("<a href='https://twitter.com/"+user['screen_name']+"'>")
                file.write("<img src='"+user['profile_image_url_https']+"'>\n</a>")
                file.write("<br/>Name: "+ str(user['name']))
                file.write("<br/>Username: "+ str(user['screen_name']))
                file.write("<br/>Verified: "+ str(user['verified']))
                file.write("<br/>Contributors: "+ str(user['contributors_enabled']))
                file.write("<br/>Location: "+ user['location'])
                file.write("<br/>Followers: "+ str(user['followers_count']))          
                file.write("<br/>Description: "+ str(user['description']))
                if user['url'] != 'null':
                    file.write("<br/>Url: <a href='"+ str(user['url'])+"'>"+str(user['url'])+"</a>\n")          
                file.write("</p>\n</div>\n")
            file.write("</body>\n</html>")
