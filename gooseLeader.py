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
            influUsers.append(user['user'])
            #sort
            influUsers = sorted(influUsers, key = lambda user: user['followers_count'], reverse = True)
            #get top userCount
            influUsers = influUsers[0:userCount]
        return influUsers             

    def userHTMLReport(self, users, title = None):
        """Creates an Html file with details on users"""
        filename = (title + "report.html")
        with codecs.open(filename,'w+','utf-8') as file:
            file.write("<!DOCTYPE html><html><head>")
            if title != None: file.write("<title>"+title+"</title>")
            file.write("</head><body>")
            for user in users:
                file.write("<div><p><a href='https://twitter.com/"+user['screen_name']+"'>")
                file.write("<img src='"+user['profile_image_url_https']+"'></a></p>")
                file.write("<p>Name: "+ str(user['name']).replace('\\','\\\\')+"</p>")
                file.write("<p>Username: "+ str(user['screen_name']).replace('\\','\\\\')+"</p>")
                file.write("<p>Verified: "+ str(user['verified']).replace('\\','\\\\')+"</p>")
                file.write("<p>Contributors: "+ str(user['contributors_enabled']).replace('\\','\\\\')+"</p>")
                file.write("<p>Location: "+ user['location']+"</p>")
                file.write("<p>Followers: "+ str(user['followers_count']).replace('\\','\\\\')+"</p>")          
                file.write("<p>Description: "+ str(user['description']).replace('\\','\\\\')+"</p>")
                if user['url'] != 'null':
                    file.write("<p>Url: <a href='"+ str(user['url'])+"'>"+str(user['url'])+"</a></p>")          
                file.write("</div>")
            file.write("</body></html>")
