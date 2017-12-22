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

class Scope:
    """Allows for searches of tweets and specific manipulations search results"""
    def __init__(self, 
                 accessToken = None,
                 accessSecret = None,
                 consumerKey = None,
                 consumerSecret = None):
        #get tokens, keys, secrets from init.txt file
        file = open('init.txt', 'r')
        if accessToken is None:
            for line in file:
                spot = line.find('=') + 1
                if 'accessToken= ' in line:
                    accessToken = line[spot:]
        if accessSecret is None:
            for line in file:
                spot = line.find('=') + 1
                if 'accessSecret= ' in line:
                    accessSecret = line[spot:]
        if consumerKey is None:
            for line in file:
                spot = line.find('=') + 1
                if 'consumerKey= ' in line:
                    consumerKey = line[spot:]
        if consumerSecret is None:
            for line in file:
                spot = line.find('=') + 1
                if 'consumerSecret= ' in line:
                    consumerSecret = line[spot:]
        oauth = OAuth(accessToken, accessSecret, consumerKey, consumerSecret)

        #twitter search
        self.twitter = Twitter(auth=oauth)

    def __search(self, query, tweetCount, langauge = None, resultType = None):
        """searches using twitter REST API"""
        #optional argument check
        if language == None: langauge = ''
        if resultType == None: resultType = ''
        
        tweets = twitter.search.tweets(q = query, result_type = resultType,
                                            lang=language, count=tweetCount)
        return tweets

    def getInfluUsers(self, userCount, tweets):
        """Returns info on most influential users in a given search"""
        influUsers = []
        for user in tweets['user']:
            influUsers.append(user)
            #sort
            influUsers = sorted(influUsers, key = lambda user: user['followers_count'], reverse = True)
            #get top userCount
            influUsers = influUsers[0:userCount]
        return influUsers

    def userHTMLReport(self, users, title = None):
        """Creates an Html file with details on users"""
        filename = (title, "report.html")
        with open(filename,'w+') as file:
            file.write("<!DOCTYPE html><html><head>")
            if title != None: file.write("<title>",title,"</title>")
            file.write("</head><body>")
            for user in users:
                file.write("<div><p><a href='https://twitter.com/",user['screen_name'],"'>")
                file.write("<img src='",user['profile_image_url_https'],"'></a></p>")
                file.write("<p>Name: ", user['name'],"</p>")
                file.write("<p>Username: ", user['screen_name'],"</p>")
                file.write("<p>Verified: ", user['verified'],"</p>")
                file.write("<p>Contributors: ", user['contributors_enabled'],"</p>")
                file.write("<p>Location: ", user['location'],"</p>")
                file.write("<p>Followers: ", user['followers_count'],"</p>")          
                file.write("<p>Description: ", user['description'],"</p>")
                if user['url'] != null: file.write("<p>Url: ", user['url'],"</p>")          
                file.write("</div>")
            file.write("</body></html>")
